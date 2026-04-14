# ROAM Human Review Workflow

All auto-extracted incidents require human review before merging to the main database. This document defines the reviewer responsibilities and quality assurance procedures.

## Reviewer Responsibilities

1. **Verify factual accuracy** of every extracted field
2. **Validate source URL** accessibility and relevance
3. **Confirm scenario classification** per ROAM taxonomy
4. **Assign final severity/urgency** ratings
5. **Deduplicate** against existing incidents
6. **Assign final ROAM-YYYY-NNN ID** to replace auto-generated ID

## Review Checklist

### Field-by-Field Verification

**Required fields (MUST verify):**
- [ ] `id`: Replaced auto-ID with proper ROAM-YYYY-NNN (next available number)
- [ ] `date`: Matches source article's reported event date
- [ ] `operator`: Matches official company name
- [ ] `location.city`, `location.country`: Correct, verified
- [ ] `location.road_type`: Matches one of allowed enum values
- [ ] `scenario.primary`: Correct taxonomy code (not REVIEW_NEEDED)
- [ ] `severity`: Matches ROAM severity scale (S0-S4)
- [ ] `description`: Factually accurate, 2-3 sentences

**Quality fields (SHOULD verify):**
- [ ] `urgency`: Matches ROAM urgency scale (U0-U3)
- [ ] `impact.*`: Reasonable estimates or confirmed numbers
- [ ] `emergency_response.*`: Matches article reporting
- [ ] `systemic_issues`: List is factual, not speculative

### URL Validation

**Every URL in `sources` must be:**
- [ ] Accessible (HTTP 200 response)
- [ ] Still live (not 404 after time)
- [ ] Relevant to the incident (not tangentially related)
- [ ] From a credible source (A-tier media, S-tier official)

**Test command:**
```bash
curl -I -L "https://..."
```

If URL returns 403/paywall, note this but keep URL. If 404 or completely broken, find alternative source.

### Scenario Classification Verification

Review the assigned `scenario.primary` code:

1. Read the 27-sub-scenario definitions in `taxonomy/scenario-taxonomy-v1.0.md`
2. Confirm the chosen code best matches the incident narrative
3. If multiple scenarios apply, use `scenario.secondary` array
4. If ambiguous between two codes, choose the more specific one

**Common misclassifications to watch for:**
- C1 (mid-road freeze) vs B1 (intersection hesitation): duration matters
- A1 (cloud failure) vs A3 (infrastructure): cause of connectivity loss
- E3 (emergency vehicle) vs F1 (passenger trapped): who is affected

### Severity/Urgency Assignment Guidelines

**Severity criteria (objective, outcome-based):**

| Level | Definition |
|-------|-----------|
| S0 | Near-miss, no impact |
| S1 | Minor disruption <5min, no injuries |
| S2 | Significant disruption OR minor injury, 5-30min |
| S3 | Major paralysis OR serious injury, >30min OR multiple vehicles |
| S4 | Fatality OR >50 vehicles affected OR mass system failure |

**Urgency criteria (time-sensitivity):**

| Level | Definition |
|-------|-----------|
| U0 | Can wait (days/weeks) |
| U1 | Within 30 minutes |
| U2 | Within 10 minutes |
| U3 | Immediate - passenger safety / emergency services blocked |

**Common errors:**
- Confusing severity (outcome) with urgency (time-pressure)
- Overestimating severity from dramatic language in articles
- Underestimating urgency when passengers are trapped

## Deduplication Procedure

Before merging a new incident:

1. Search existing incidents by:
   - Date (±2 days)
   - Operator
   - City

```bash
grep -l "operator: \"Waymo\"" incidents/2026/*.yaml | xargs grep -l "San Francisco"
```

2. Read descriptions of candidate matches
3. If same underlying event, merge sources (don't create duplicate)
4. If different events same day, keep separate but cross-reference in descriptions

## PR Approval Process

### Auto-Crawl PRs (from GitHub Actions)

1. **Reviewer assigned** automatically via CODEOWNERS
2. **Initial review** within 48 hours
3. **Verify checklist** items above
4. **Make corrections** directly in PR (commit to PR branch)
5. **Request changes** if quality insufficient
6. **Approve and merge** only when all checklist items complete

### Manual Contributions

External contributors submit PRs with manually created incident YAMLs:

1. Same checklist applies
2. Additional verification: contributor identity known/verified
3. Extra scrutiny on sources (check for astroturfing)

## Quality Metrics Tracking

Maintainer should track monthly:

- **Review backlog**: Auto-crawl PRs awaiting review
- **Rejection rate**: % of auto-extracted items failing review
- **False positive rate**: Non-incident articles wrongly crawled
- **Source coverage**: # incidents per source, to rebalance priorities
- **Time-to-merge**: From auto-crawl to main database

Report metrics quarterly to inform crawler/extractor improvements.

## Escalation

For disputed classifications (ambiguous scenario, disputed severity):

1. Open GitHub Discussion
2. Tag 2+ reviewers
3. Reference ROAM taxonomy documentation
4. Document decision rationale in incident file

## Training New Reviewers

New reviewers should:

1. Read ROAM taxonomy, severity scale, urgency scale documents
2. Shadow-review 5 existing incidents alongside experienced reviewer
3. Submit first 3 reviews for senior reviewer verification
4. Graduate to independent review after consistency check

## Contact

Maintainer: Yuxin Zhang (https://www.linkedin.com/in/zhangyuxin/)
Project: https://github.com/AutoZYX/ROAM
