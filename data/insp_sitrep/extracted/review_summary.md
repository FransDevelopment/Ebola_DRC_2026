# INSP SitRep Ingest Review

This packet is generated from official INSP source sync plus advisory public-PDF extraction.

## First Checks
- Source review queue: `data/insp_sitrep/extracted/source_review_queue.csv`
- Processed draft review: `data/insp_sitrep/extracted/processed_draft_review.csv`
- Processed draft CSVs: `data/insp_sitrep/extracted/processed_drafts`
- Processed candidate CSVs: `data/insp_sitrep/processed`

## Run Summary
- Reports discovered: 2
- Table II values extracted: 61
- Processed draft files written: 4
- Processed candidate files written: 2
- Source manifest statuses: official_verified: 2
- Source gate statuses: passed: 2
- Layout statuses: known_text_layout: 1, partial_extract: 1
- Source review queue: manual_review_required: 1
- Processed draft review: candidate_added: 4, manual_review_required: 1, match: 57

## INSP Source Timing
| Report | Report Date | INSP Post Published | INSP Post Modified | PDF Last-Modified | Layout | Blocker |
|---|---|---|---|---|---|---|
| 013 | 2026-05-27 | 2026-05-28T17:25:51Z | 2026-05-28T18:17:12Z | Thu, 28 May 2026 18:16:59 GMT | known_text_layout |  |
| 014 | 2026-05-28 | 2026-05-30T14:03:52Z | 2026-05-30T14:03:57Z | Sat, 30 May 2026 14:03:03 GMT | partial_extract | table_ii_missing |

## Reviewer Actions
- Source rows are report-level gates. Processed candidate rows are Table II field-level drafts with accepted evidence methods.
- A report can need manual review for one field while still producing candidate rows for other fields with stronger evidence.
- National headline values are recorded once in `source_reports.csv`; this helper does not expand new national totals across every zone.
- Review manual rows by opening `source_raw_path` and comparing only the listed ambiguous field(s).
- Review `candidate_added` rows as new processed CSV rows proposed by this run.
- Review changed `processed/*.csv` rows in the draft PR against the official PDFs.
- Treat `processed_draft_review.csv` as the pre-candidate comparison against prior processed files.

## Reports Needing Review
| Report | Date | Status | Reason | Local PDF |
|---|---|---|---|---|
| 014 | 2026-05-28 | manual_review_required | table_ii_missing | `data/insp_sitrep/raw/SitRep_MVE_014-2026.pdf` |

## High-Confidence Draft Reports
013
