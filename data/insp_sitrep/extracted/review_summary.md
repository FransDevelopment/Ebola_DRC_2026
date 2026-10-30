# INSP SitRep Ingest Review

This packet is generated from official INSP source sync plus advisory public-PDF extraction.

## First Checks
- Source review queue: `data/insp_sitrep/extracted/source_review_queue.csv`
- Processed draft review: `data/insp_sitrep/extracted/processed_draft_review.csv`
- Processed draft CSVs: `data/insp_sitrep/extracted/processed_drafts`

## Run Summary
- Reports discovered: 2
- Table II values extracted: 0
- Processed draft files written: 0
- Processed candidate files written: 0
- Source manifest statuses: missing_pdf_url: 2
- Source gate statuses: blocked_missing_official_pdf_url: 2
- Layout statuses: known_text_layout: 1, partial_extract: 1
- Source review queue: blocked: 2
- Processed draft review: blocked: 2

## INSP Source Timing
| Report | Report Date | INSP Post Published | INSP Post Modified | PDF Last-Modified | Layout | Blocker |
|---|---|---|---|---|---|---|
| 013 | 2026-05-27 | 2026-05-28T17:25:51Z | 2026-05-28T18:17:12Z |  | known_text_layout | blocked_missing_official_pdf_url |
| 014 | 2026-05-28 | 2026-05-30T14:03:52Z | 2026-05-30T14:03:57Z |  | partial_extract | table_ii_missing;blocked_missing_official_pdf_url |

## Reviewer Actions
- Source rows are report-level gates. Processed candidate rows are Table II field-level drafts with accepted evidence methods.
- A report can need manual review for one field while still producing candidate rows for other fields with stronger evidence.
- National headline values are recorded once in `source_reports.csv`; this helper does not expand new national totals across every zone.
- Resolve blocked source/layout rows before trusting automated drafts for those reports.

## Reports Needing Review
| Report | Date | Status | Reason | Local PDF |
|---|---|---|---|---|
| 013 | 2026-05-27 | blocked | blocked_missing_official_pdf_url | `data/insp_sitrep/raw/SitRep_MVE_013-2026.pdf` |
| 014 | 2026-05-28 | blocked | table_ii_missing;blocked_missing_official_pdf_url | `data/insp_sitrep/raw/SitRep_MVE_014-2026.pdf` |

## High-Confidence Draft Reports
None.
