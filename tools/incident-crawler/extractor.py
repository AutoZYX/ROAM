#!/usr/bin/env python3
"""
ROAM LLM-based Incident Extractor
Takes raw crawled articles and generates ROAM-format YAML files.

Usage:
    python extractor.py --input raw_incidents/2026-04-05/techcrunch/incident_abc123.json
    python extractor.py --batch raw_incidents/2026-04-05/
"""
import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import requests
import yaml


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('roam-extractor')


class LLMExtractor:
    """Use LLM to extract ROAM-format structured data from raw articles."""

    def __init__(self, api_key: Optional[str] = None, provider: str = 'anthropic'):
        self.provider = provider
        self.api_key = api_key or os.environ.get(
            'ANTHROPIC_API_KEY' if provider == 'anthropic' else 'OPENAI_API_KEY'
        )
        if not self.api_key:
            raise ValueError(f"No API key for {provider}. Set environment variable.")

        # Load extraction prompt
        prompt_path = Path(__file__).parent / 'prompts' / 'extraction-prompt.md'
        with open(prompt_path, 'r', encoding='utf-8') as f:
            self.system_prompt = f.read()

    def extract(self, article_text: str, article_url: str,
                source_name: str) -> Dict:
        """Extract structured ROAM schema from article text."""
        user_message = f"""Article URL: {article_url}
Source: {source_name}
Article Content:
---
{article_text[:8000]}
---

Extract a ROAM incident record in strict YAML format, following the schema and taxonomy provided."""

        if self.provider == 'anthropic':
            return self._call_anthropic(user_message)
        elif self.provider == 'openai':
            return self._call_openai(user_message)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _call_anthropic(self, user_message: str) -> Dict:
        """Call Anthropic Claude API."""
        headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json',
        }
        payload = {
            'model': 'claude-3-5-sonnet-20241022',
            'max_tokens': 4096,
            'system': self.system_prompt,
            'messages': [{'role': 'user', 'content': user_message}]
        }
        try:
            r = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers, json=payload, timeout=60
            )
            r.raise_for_status()
            data = r.json()
            content = data['content'][0]['text']
            return self._parse_yaml_response(content)
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return {}

    def _call_openai(self, user_message: str) -> Dict:
        """Call OpenAI API (fallback)."""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        payload = {
            'model': 'gpt-4-turbo-preview',
            'messages': [
                {'role': 'system', 'content': self.system_prompt},
                {'role': 'user', 'content': user_message},
            ],
            'temperature': 0.2,
        }
        try:
            r = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers, json=payload, timeout=60
            )
            r.raise_for_status()
            data = r.json()
            content = data['choices'][0]['message']['content']
            return self._parse_yaml_response(content)
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {}

    def _parse_yaml_response(self, content: str) -> Dict:
        """Extract YAML from LLM response (may contain markdown code blocks)."""
        # Strip markdown code blocks
        yaml_match = re.search(r'```ya?ml\s*\n(.*?)\n```', content, re.DOTALL)
        if yaml_match:
            yaml_str = yaml_match.group(1)
        else:
            yaml_str = content

        try:
            return yaml.safe_load(yaml_str) or {}
        except yaml.YAMLError as e:
            logger.error(f"YAML parse error: {e}")
            return {}


def extract_from_raw_item(raw_file: Path, extractor: LLMExtractor,
                           output_dir: Path) -> Optional[Path]:
    """Extract single raw item to ROAM YAML."""
    with open(raw_file, 'r', encoding='utf-8') as f:
        raw_item = json.load(f)

    logger.info(f"Extracting: {raw_file.name}")

    # Combine title + summary as article text
    article_text = f"{raw_item.get('title', '')}\n\n{raw_item.get('summary', '')}"
    if len(article_text.strip()) < 100:
        logger.warning(f"Article too short, skipping: {raw_file.name}")
        return None

    # Call LLM
    result = extractor.extract(
        article_text=article_text,
        article_url=raw_item.get('url', ''),
        source_name=raw_item.get('source_name', '')
    )

    if not result or 'id' not in result:
        logger.warning(f"Extraction failed or empty: {raw_file.name}")
        return None

    # Add metadata
    result['sources'] = result.get('sources', [])
    if not any(s.get('url') == raw_item.get('url') for s in result['sources']):
        result['sources'].append({
            'url': raw_item.get('url'),
            'title': raw_item.get('title', '')
        })

    result['contributor'] = 'ROAM Crawler (auto-extracted, needs review)'
    result['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    result['_extraction_metadata'] = {
        'source_id': raw_item.get('source_id'),
        'raw_file': str(raw_file),
        'review_status': 'REVIEW_NEEDED',
        'extractor_version': '1.0',
    }

    # Save YAML
    year = result.get('date', datetime.now().strftime('%Y-%m-%d'))[:4]
    out_dir = output_dir / year
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{result['id']}-auto.yaml"

    with open(out_file, 'w', encoding='utf-8') as f:
        yaml.dump(result, f, allow_unicode=True, sort_keys=False,
                  default_flow_style=False)

    logger.info(f"Extracted → {out_file}")
    return out_file


def main():
    parser = argparse.ArgumentParser(description='ROAM Incident LLM Extractor')
    parser.add_argument('--input', help='Single raw JSON file to extract')
    parser.add_argument('--batch', help='Directory of raw items to batch extract')
    parser.add_argument('--output', default='extracted_yaml',
                        help='Output directory for YAML files')
    parser.add_argument('--provider', default='anthropic',
                        choices=['anthropic', 'openai'])
    args = parser.parse_args()

    output_dir = Path(__file__).parent / args.output
    extractor = LLMExtractor(provider=args.provider)

    if args.input:
        extract_from_raw_item(Path(args.input), extractor, output_dir)
    elif args.batch:
        batch_dir = Path(args.batch)
        for raw_file in batch_dir.rglob('incident_*.json'):
            try:
                extract_from_raw_item(raw_file, extractor, output_dir)
            except Exception as e:
                logger.error(f"Error extracting {raw_file}: {e}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
