#!/usr/bin/env python3
"""
ROAM Incident Crawler
Automated collection of L4+ robotaxi incidents from public sources.

Usage:
    python crawler.py --source nhtsa --days 7
    python crawler.py --all
    python crawler.py --list-sources
"""
import argparse
import hashlib
import json
import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

import feedparser
import requests
import yaml
from bs4 import BeautifulSoup


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('roam-crawler')


class BaseCrawler(ABC):
    """Abstract base class for all source crawlers."""

    def __init__(self, source_config: Dict, output_dir: Path):
        self.config = source_config
        self.source_id = source_config['source_id']
        self.name = source_config['name']
        self.keywords = source_config.get('keywords_filter', [])
        self.output_dir = output_dir
        self.session = self._create_session()
        self.retry_count = 3
        self.retry_backoff = 2  # seconds, exponential

    def _create_session(self) -> requests.Session:
        """Create requests session with polite headers."""
        s = requests.Session()
        s.headers.update({
            'User-Agent': 'ROAM-Incident-Crawler/1.0 (+https://github.com/AutoZYX/ROAM)',
            'Accept': 'text/html,application/xml,application/json',
        })
        return s

    def _check_robots_txt(self, url: str) -> bool:
        """Check robots.txt compliance."""
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        try:
            r = self.session.get(robots_url, timeout=10)
            # Simplified: if disallowed-for-all, return False
            if r.status_code == 200 and 'User-agent: *\nDisallow: /' in r.text:
                logger.warning(f"{self.name}: robots.txt disallows crawling")
                return False
        except Exception as e:
            logger.debug(f"robots.txt check failed for {self.name}: {e}")
        return True

    def _fetch_with_retry(self, url: str) -> Optional[requests.Response]:
        """Fetch URL with exponential backoff retry."""
        for attempt in range(self.retry_count):
            try:
                r = self.session.get(url, timeout=30)
                if r.status_code == 200:
                    return r
                elif r.status_code == 429:  # Rate limited
                    wait = (self.retry_backoff ** attempt) * 5
                    logger.warning(f"{self.name}: rate limited, waiting {wait}s")
                    time.sleep(wait)
                else:
                    logger.warning(f"{self.name}: HTTP {r.status_code} for {url}")
                    return None
            except Exception as e:
                wait = self.retry_backoff ** attempt
                logger.warning(f"{self.name}: attempt {attempt+1} failed: {e}, waiting {wait}s")
                time.sleep(wait)
        return None

    def _matches_keywords(self, text: str) -> bool:
        """Check if text matches any keyword filter."""
        if not self.keywords:
            return True
        text_lower = text.lower()
        return any(kw.lower() in text_lower for kw in self.keywords)

    def _hash_url(self, url: str) -> str:
        """Generate MD5 hash of URL for deduplication."""
        return hashlib.md5(url.encode('utf-8')).hexdigest()[:12]

    def _save_item(self, item: Dict) -> Path:
        """Save item to output directory."""
        date_str = datetime.now().strftime('%Y-%m-%d')
        out_dir = self.output_dir / date_str / self.source_id
        out_dir.mkdir(parents=True, exist_ok=True)

        url_hash = self._hash_url(item['url'])
        out_file = out_dir / f"incident_{url_hash}.json"

        # Skip if already crawled (deduplication)
        if out_file.exists():
            logger.debug(f"Skipping duplicate: {item['url']}")
            return out_file

        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(item, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved: {out_file.name}")
        return out_file

    @abstractmethod
    def crawl(self, since_days: int = 7) -> List[Dict]:
        """Crawl source and return list of candidate incidents."""
        pass


class RSSCrawler(BaseCrawler):
    """Crawl RSS/Atom feeds."""

    def crawl(self, since_days: int = 7) -> List[Dict]:
        rss_url = self.config.get('rss_url', self.config.get('url'))
        logger.info(f"Crawling RSS: {self.name}")

        feed = feedparser.parse(rss_url)
        if feed.bozo:
            logger.warning(f"{self.name}: RSS parse warnings")

        cutoff_date = datetime.now() - timedelta(days=since_days)
        candidates = []

        for entry in feed.entries:
            # Parse publish date
            pub_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
            if pub_date and pub_date < cutoff_date:
                continue

            title = entry.get('title', '')
            summary = entry.get('summary', '')
            link = entry.get('link', '')

            # Keyword filter
            combined_text = f"{title} {summary}"
            if not self._matches_keywords(combined_text):
                continue

            candidates.append({
                'source_id': self.source_id,
                'source_name': self.name,
                'url': link,
                'title': title,
                'summary': summary,
                'published_at': pub_date.isoformat() if pub_date else None,
                'crawled_at': datetime.now().isoformat(),
                'raw_language': self.config.get('language', 'en'),
            })

            time.sleep(0.5)  # Polite rate limiting

        logger.info(f"{self.name}: {len(candidates)} candidates found")

        # Save each candidate
        for item in candidates:
            self._save_item(item)

        return candidates


class APICrawler(BaseCrawler):
    """Crawl JSON APIs (Reddit, Twitter, etc.)."""

    def crawl(self, since_days: int = 7) -> List[Dict]:
        api_url = self.config.get('api_url', self.config.get('url'))
        logger.info(f"Crawling API: {self.name}")

        response = self._fetch_with_retry(api_url)
        if not response:
            return []

        try:
            data = response.json()
        except Exception as e:
            logger.error(f"{self.name}: JSON parse error: {e}")
            return []

        candidates = []
        # Reddit JSON structure
        if 'data' in data and 'children' in data.get('data', {}):
            for post in data['data']['children']:
                pd = post.get('data', {})
                title = pd.get('title', '')
                selftext = pd.get('selftext', '')
                url = pd.get('url', '')

                if not self._matches_keywords(f"{title} {selftext}"):
                    continue

                candidates.append({
                    'source_id': self.source_id,
                    'source_name': self.name,
                    'url': url,
                    'title': title,
                    'summary': selftext[:500],
                    'published_at': datetime.fromtimestamp(
                        pd.get('created_utc', 0)).isoformat(),
                    'crawled_at': datetime.now().isoformat(),
                    'raw_language': self.config.get('language', 'en'),
                    'metadata': {
                        'score': pd.get('score'),
                        'num_comments': pd.get('num_comments'),
                    }
                })
                time.sleep(0.3)

        logger.info(f"{self.name}: {len(candidates)} candidates found")
        for item in candidates:
            self._save_item(item)
        return candidates


class HTMLCrawler(BaseCrawler):
    """Crawl HTML pages (fallback when no RSS available)."""

    def crawl(self, since_days: int = 7) -> List[Dict]:
        url = self.config['url']
        logger.info(f"Crawling HTML: {self.name}")

        if not self._check_robots_txt(url):
            logger.warning(f"{self.name}: skipped due to robots.txt")
            return []

        response = self._fetch_with_retry(url)
        if not response:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        candidates = []

        # Generic article link extraction (each site may need custom logic)
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text(strip=True)

            if not text or len(text) < 20:
                continue
            if not self._matches_keywords(text):
                continue

            # Normalize URL
            if href.startswith('/'):
                from urllib.parse import urljoin
                href = urljoin(url, href)
            elif not href.startswith('http'):
                continue

            candidates.append({
                'source_id': self.source_id,
                'source_name': self.name,
                'url': href,
                'title': text,
                'summary': '',  # HTML crawler doesn't have summary without fetching
                'published_at': None,
                'crawled_at': datetime.now().isoformat(),
                'raw_language': self.config.get('language', 'en'),
            })

            if len(candidates) >= 20:  # Limit per page
                break
            time.sleep(0.5)

        logger.info(f"{self.name}: {len(candidates)} candidates found")
        for item in candidates:
            self._save_item(item)
        return candidates


def load_sources_config(config_path: Path) -> List[Dict]:
    """Load sources configuration."""
    with open(config_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('sources', [])


def create_crawler(source_config: Dict, output_dir: Path) -> BaseCrawler:
    """Factory method to create appropriate crawler."""
    source_type = source_config.get('type', 'HTML').upper()
    if source_type == 'RSS':
        return RSSCrawler(source_config, output_dir)
    elif source_type == 'API':
        return APICrawler(source_config, output_dir)
    else:
        return HTMLCrawler(source_config, output_dir)


def main():
    parser = argparse.ArgumentParser(description='ROAM Incident Crawler')
    parser.add_argument('--source', help='Source ID to crawl')
    parser.add_argument('--all', action='store_true', help='Crawl all sources')
    parser.add_argument('--days', type=int, default=7, help='Days to look back')
    parser.add_argument('--list-sources', action='store_true',
                        help='List available sources')
    parser.add_argument('--config', default='config/sources.yaml',
                        help='Sources config file')
    parser.add_argument('--output', default='raw_incidents',
                        help='Output directory')
    args = parser.parse_args()

    config_path = Path(__file__).parent / args.config
    output_dir = Path(__file__).parent / args.output

    sources = load_sources_config(config_path)

    if args.list_sources:
        print(f"Available sources ({len(sources)}):")
        for s in sources:
            print(f"  [{s['priority']}] {s['source_id']}: {s['name']} ({s['language']})")
        return

    # Filter sources
    if args.source:
        sources = [s for s in sources if s['source_id'] == args.source]
        if not sources:
            logger.error(f"Source '{args.source}' not found")
            return
    elif not args.all:
        parser.print_help()
        return

    # Crawl each source
    total_candidates = 0
    for source_config in sources:
        try:
            crawler = create_crawler(source_config, output_dir)
            candidates = crawler.crawl(since_days=args.days)
            total_candidates += len(candidates)
            time.sleep(2)  # Polite delay between sources
        except Exception as e:
            logger.error(f"Error crawling {source_config['source_id']}: {e}")

    logger.info(f"Total candidates collected: {total_candidates}")


if __name__ == '__main__':
    main()
