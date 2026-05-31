# INSP situation reports (SitRep MVE) — health-zone outbreak indicators

Daily **case, death, contact-tracing, hospitalisation, point-of-entry (PoE), and national cumulative** indicators, extracted from Institut National de Santé Publique (INSP) **Situation Reports** on the 2026 Bundibugyo Ebolavirus (BDBV) outbreak (`SitRep_MVE_*` PDFs in `raw/`).

These data complement WHO weekly external sitreps in `data/epi/` with **INSP-internal reporting** at sitrep date resolution and additional operational fields.

------------------------------------------------------------------------

## Source documents

**Publisher:** [Institut National de Santé Publique (INSP)]([https://insp.cd/](https://insp.cd/category/actualites/)), Democratic Republic of the Congo.

**Series:** SitRep **MVE** (maladie à virus Ebola), 2026.

**Committed PDFs (`raw/`):**

| File                      | Report |
|---------------------------|--------|
| `SitRep_MVE_001-2026.pdf` | 001    |
| `SitRep_MVE_002-2026.pdf` | 002    |
| `SitRep_MVE_004-2026.pdf` | 004    |
| `SitRep_MVE_005-2026.pdf` | 005    |
| `SitRep_MVE_006-2026.pdf` | 006    |
| `SitRep_MVE_007-2026.pdf` | 007    |
| `SitRep_MVE_008-2026.pdf` | 008    |
| `SitRep_MVE_009-2026.pdf` | 009    |
| `SitRep_MVE_010-2026.pdf` | 010    |
| `SitRep_MVE_011-2026.pdf` | 011    |
| `SitRep_MVE_012-2026.pdf` | 012    |
| `SitRep_MVE_012-2026_v2.pdf` | 012 v2 |
| `SitRep_MVE_013-2026.pdf` | 013    |
| `SitRep_MVE_014-2026.pdf` | 014    |

**Not in repo:** `SitRep_MVE_003-2026.pdf` (gap between 002 and 004).

**Source intake:** PDFs from SitRep 013 onward are synced from the official INSP post/PDF URLs with `tools/insp_sitrep_sources.py`; `source_reports.csv` records URL, INSP post timing, PDF `Last-Modified`, hash, source-gate status, PDF/report identity status, layout status, extractability, evidence confidence, draft status, and blocking reason.

**Extraction:** Processed values remain editorial outputs. `tools/insp_sitrep_sources.py` provides custody and advisory checks against public PDF text, but does not silently overwrite existing `processed/*.csv` values.

| Folder | Source | Grain | Role |
|----|----|----|----|
| `data/epi/` | WHO Weekly External Situation Report | Weekly | Official external case/death tables |
| `data/insp_sitrep/` | INSP SitRep MVE PDFs | Daily (per report date) | INSP operational and national summary metrics |

------------------------------------------------------------------------

## Repository layout

| Path | Description |
|----|----|
| `raw/SitRep_MVE_*.pdf` | Source sitreps (Git LFS) |
| `processed/insp_sitrep__*__daily.csv` | **28** contract tables (listed below) |
| `process.R` | Map `nom` to canonical shapefile names |
| `provenance.csv` | Lightweight sidecar for source report / table / row / column review |
| `source_reports.csv` | Official INSP URL, WordPress post timing, PDF `Last-Modified`, raw/official hash, source-gate status, PDF/report identity status, text extractability, layout status, confidence, headline/table extraction status, draft status, and blocking reason |
| `extracted/table_ii_values.csv` | Advisory public-PDF Table II extraction used for review against processed CSVs |
| `extracted/source_review_queue.csv` | Small report-level queue for blocked or partial extraction, with local raw PDF path and review action |
| `extracted/review_summary.md` | Short reviewer entry point with run counts, blockers, high-confidence reports, and next actions |
| `metadata.yaml` | Provenance, licence, and pipeline notes |

**Data Process and Decision Workflow:**

All files labeled "\_national" should match exactly to the top banner of each SitRep (on page 1), which is always publicly available

Health zone level information should match exactly to the latest version of each SitRep (ex. v2 of Report 012). If there is an updated version of a SitRep released, we will update out .csv reports accordingly.

If a new SitRep disagrees with the previously reported values (i.e. reported cases decrease from report to report), we will report values exactly as is, with matching dates to track changes. While health zone level metrics may disagree with national values, we will report the tabular data verbatim.

Occasionally, health zone level data may be sent directly from INSP to INRB. This data may not feature in the SitRep PDFs but will be included in the csv files on this repo.

| Layer | Zones | Date range in CSVs |
|----|----|----|
| Outbreak-zone metrics | **21** canonical `nom` values (see list below) | Mostly **2026-05-14** – **2026-05-24** (ISO); hospitalisation and PoE from **2026-05-20**; PoE through **2026-05-23** |
| National `national_*` metrics | **519** rows per date (same total on every row) | **2026-05-28** (ISO) |

PDFs **013** and **014** are in `raw/`; 014 headline values are recorded once in `source_reports.csv`, while its Table II rows remain manual-review because the public PDF layout does not expose that table cleanly.

**Outbreak-affected zones in processed data:** Adi, Aru, Bambu, Bunia, Butembo, Goma, Kalunguta, Karisimbi, Katwa, Kilo, Komanda, Kyondo, Mahagi, Mangala, Miti-Murhesa, Mongbalu, Nizi, Nyakunde, Oicha, Rwampara, Tchomia.

------------------------------------------------------------------------

## Filename contract

``` text
insp_sitrep__<metric>__daily.csv
```

Grammar: `tools/lib/schema.py`. Each file is a long-format vector: **`nom`**, **`date`**, plus one metric column.

------------------------------------------------------------------------

## Processed outputs (28 files)

### Case, death, and contact tracing

| File | Value column | Notes |
|----|----|----|
| `insp_sitrep__new_suspected_cases__daily.csv` | `new_suspected_cases` |  |
| `insp_sitrep__cumulative_suspected_cases__daily.csv` | `cumulative_suspected_cases` |  |
| `insp_sitrep__new_confirmed_cases__daily.csv` | `new_confirmed_cases` |  |
| `insp_sitrep__cumulative_confirmed_cases__daily.csv` | `cumulative_confirmed_cases` |  |
| `insp_sitrep__new_suspected_deaths__daily.csv` | `new_suspected_deaths` |  |
| `insp_sitrep__cumulative_suspected_deaths__daily.csv` | `cumulative_suspected_deaths` |  |
| `insp_sitrep__cumulative_confirmed_deaths__daily.csv` | `cumulative_confirmed_deaths` | No separate `new_confirmed_deaths` file |
| `insp_sitrep__new_contacts_listed__daily.csv` | `new_contacts_listed` |  |
| `insp_sitrep__cumulative_contacts_traced__daily.csv` | `cumulative_contacts_traced` |  |
| `insp_sitrep__new_contacts_isolated__daily.csv` | `new_contacts_isolated` |  |
| `insp_sitrep__cumulative_contacts_isolated__daily.csv` | `cumulative_contacts_isolated` |  |
| `insp_sitrep__contacts_seen__daily.csv` | `contacts_seen` |  |

### National cumulative totals (519 zones per date)

Republic-wide figures from sitrep summary tables, **copied to every `nom`** on that `date`. **Do not sum across zones.**

| File | Value column | Notes |
|----|----|----|
| `insp_sitrep__national_cumulative_suspected_cases__daily.csv` | `national_cumulative_suspected_cases` |  |
| `insp_sitrep__national_cumulative_confirmed_cases__daily.csv` | `national_cumulative_confirmed_cases` |  |
| `insp_sitrep__national_cumulative_suspected_deaths__daily.csv` | `national_cumulative_suspected_deaths` |  |
| `insp_sitrep__national_cumulative_confirmed_deaths__daily.csv` | `national_cumulative_confirmed_deaths` |  |

### Hospitalisation (from 2026-05-20 in current data)

| File | Value column | Notes |
|----|----|----|
| `insp_sitrep__hospitalised__daily.csv` | `hospitalised` |  |
| `insp_sitrep__in_bed_previous_day__daily.csv` | `in_bed_previous_day` |  |
| `insp_sitrep__new_hosp_admissions__daily.csv` | `new_all_admissions` | Metric token in filename is `new_hosp_admissions` |
| `insp_sitrep__new_hosp_detainees__daily.csv` | `new_hosp_detainees` |  |
| `insp_sitrep__new_hosp_other__daily.csv` | `new_other` |  |
| `insp_sitrep__hosp_escaped__daily.csv` | `escaped` |  |

### Points of entry (zone totals; 2026-05-20 – 2026-05-23)

| File | Value column |
|----|----|
| `insp_sitrep__total_poe_screened__daily.csv` | `total_poe_screened` |
| `insp_sitrep__total_poe_passed__daily.csv` | `total_poe_passed` |
| `insp_sitrep__total_poe_sanitised__daily.csv` | `total_poe_sanitised` |
| `insp_sitrep__total_poe_hand_washing__daily.csv` | `total_poe_hand_washing` |
| `insp_sitrep__total_poe_refused_screening__daily.csv` | `total_poe_refused_screening` |
| `insp_sitrep__total_poe_refused_hand_washing__daily.csv` | `total_poe_refused_hand_washing` |

Per-site PoE breakdown in the PDFs is not exported.

------------------------------------------------------------------------

## CSV contract

| Column | Description |
|----|----|
| `nom` | Canonical health-zone name after `process.R` (see `data/shapefiles/`, `data/aliases.csv`) |
| `date` | Sitrep **report date** (ISO `YYYY-MM-DD`) |
| `<metric>` | Count, or **`ND`** if not reported in that sitrep |

**Uniqueness:** one row per (`nom`, `date`) per file.

**Missing values:** treat `ND` as missing in analysis (`na.strings = "ND"` in R).

**Source clocks:** `date` is the SitRep report date for the extracted table row, using the date representation already present in the referenced processed CSV. It is not onset date, specimen date, publication timestamp, retrieval date, or build timestamp. `metadata.yaml` records repository retrieval and folder-level period metadata.

**Example (R):**

``` r
library(here)

cases <- read.csv(
  here("data/insp_sitrep/processed/insp_sitrep__cumulative_confirmed_cases__daily.csv"),
  na.strings = "ND"
)
cases[cases$date == "24/05/2026", c("nom", "cumulative_confirmed_cases")]
```

------------------------------------------------------------------------

## Workflow

### 1. Official PDF source sync

From repo root:

``` bash
python -m tools.insp_sitrep_sources \
  --sync-official-pdfs \
  --parse-pdfs \
  --extract-table-ii \
  --write-processed-drafts \
  --write-processed-candidates \
  --compare-processed \
  --min-report-number 13
```

This discovers INSP SitRep posts, syncs the official PDF bytes into `raw/`, writes `source_reports.csv`, writes advisory extracted Table II values when the public PDF exposes a parseable table, writes processed-contract draft CSVs under `extracted/processed_drafts/`, and can merge those same source-gated Table II values into `processed/` as draft PR candidate changes. The workflow starts at SitRep 013 so it does not rewrite earlier manually uploaded PDFs; earlier source differences can still be reviewed separately with `--verify-official-pdfs` if needed. Processed candidates require the source gate to pass (`raw_matches_official`) and an accepted value evidence method; if a future PDF has an unsupported layout, the tool still records the official PDF and review blocker but does not create processed-value candidates for unsupported claims. National headline values are recorded once per report in `source_reports.csv` rather than expanded across every health zone as new candidate rows.

The source release detector is polling-based: each run queries the INSP WordPress API for `SitRep MVE` posts, records the post `date_gmt` / `modified_gmt`, resolves the PDF linked from each official post, records the PDF `Last-Modified` / `ETag`, and writes any newly discovered report number to the local raw/source manifest outputs. It does not require INSP to change its workflow. To ingest new public releases, run the command above manually or use the maintainer workflow; new source PDFs are detected when INSP publishes a matching post/PDF.

Repeated runs are delta-aware. If an existing `source_reports.csv` row proves the local raw PDF already matched the official PDF and INSP's current `ETag` or `Last-Modified`/size headers are unchanged, the tool reuses the local raw file and does not download the PDF again. If INSP changes the post/PDF, the manifest is missing, or the remote headers are insufficient to prove sameness, the tool downloads the official PDF to verify the hash. The committed manifest and review summary use stable source status such as `official_verified`, so freshly synced versus reused local bytes do not create review noise.

For emergency pre-release review, a manually supplied PDF can be placed in `raw/` using the normal filename. Treat that as advisory only: processed candidates remain blocked unless the official INSP post/PDF can be discovered and the local bytes match the official source.

For nontechnical maintainers after this workflow is merged, use **Actions → INSP SitRep ingest → Run workflow**. The same workflow also runs once per day on a schedule. Each run syncs official PDFs from SitRep 013 onward, writes advisory Table II processed drafts, writes draft PR candidate rows into `processed/`, runs focused tests and INSP QA, uploads the review packet, and opens or updates a draft PR only when durable source/processed data changed. Review-packet-only churn is uploaded as an artifact without opening a PR.

### 2. Editorial extraction

1. Review `extracted/review_summary.md` first. It gives the short action list, source timing, source-gate counts, layout counts, high-confidence reports, and reports needing review.
2. Review `extracted/source_review_queue.csv`. Each row has `source_raw_path`, INSP timing fields, and `review_action`, so blocked/partial extraction can be compared directly against the ingested PDF.
3. Review `source_reports.csv` for `post_published_at`, `post_modified_at`, `last_modified`, `source_gate_status`, `source_relation`, `source_identity_status`, `layout_status`, `text_extractable`, `headline_status`, `table_ii_status`, `draft_status`, and `blocking_reason`.
4. Review `extracted/processed_draft_review.csv` for `candidate_added`, `value_mismatch`, `missing_processed`, `manual_review_required`, and `blocked` rows; value rows also carry `source_raw_path`.
5. Review the changed `processed/*.csv` rows in the draft PR against the official PDF and the generated draft/review files. Revise or remove any candidate row that does not survive editorial review.
6. Add or update `provenance.csv` with the source report number, PDF filename, table/row/column reference when available, processed output file, metric, extracted value, and review status.
7. Use **spellings as they appear in the PDF** in `nom` (e.g. `Mongbwalu`, `Nyankunde`). Excel exports may include a UTF-8 BOM; that is fine before running `process.R`.
8. Use the same `date` value as the processed row when adding provenance entries, including the row's existing date format. Current processed SitRep CSVs contain mixed date formats; a full date-format normalisation should be handled as a separate data-cleanup change.

### 3. Name normalisation (`process.R`)

From repo root:

``` bash
Rscript data/insp_sitrep/process.R
```

Maps PDF spellings via `data/aliases.csv` (e.g. `Mongbwalu` → `Mongbalu`, `Nyankunde` → `Nyakunde`, `Karissibi` → `Karisimbi`). Stops on unresolved names or duplicate (`nom`, `date`) keys.

### 4. QA and GeoJSON build

``` bash
python -m tools.qa insp_sitrep
python -m tools.build_geojson   # if vectors pass QA
```

------------------------------------------------------------------------

## Data quality and limitations

| Issue | Detail |
|----|----|
| Manual transcription | Verify against source PDFs before release. |
| Partial zone coverage | Only reported outbreak zones appear in zone-level files; missing zone ≠ zero. |
| `ND` cells | Metric not published for that zone/date. |
| Missing sitrep 003 | Gap between reports 002 and 004. |
| PDF vs processed lag | `raw/` includes 013–014; 014 Table II rows are not drafted because the public PDF layout does not expose that table cleanly. |
| National files | Existing files repeat one national total across 519 zones per date; do not sum across zones. New source sync records national headline values once in `source_reports.csv` instead of adding more repeated national candidate rows. |
| Hospitalisation column names | e.g. `new_all_admissions`, `new_other`, `escaped` differ from filename tokens. |
| Advisory PDF automation | `tools.insp_sitrep_sources` syncs official PDFs and extracts machine-readable public values when available; processed CSV changes still require editorial review. |

### Structural data follow-up

This source-sync workflow reduces manual PDF intake and review work, but the root data-quality issue is still the public PDF shape. A structurally stable INSP companion CSV would let the repository ingest high-confidence values without depending on PDF layout. That CSV handoff is separate from this workflow change.

------------------------------------------------------------------------

## Provenance

- **Reports:** `raw/SitRep_MVE_*.pdf`; SitRep 013 onward is synced from official INSP PDF URLs recorded in `source_reports.csv`
- **Geometry:** `data/shapefiles/DRC_Health_zones.shp`
- **Aliases:** `data/aliases.csv`
- **Metadata:** `metadata.yaml`
- **INSP contact:** [pierre.akilimali@insp.cd](mailto:pierre.akilimali@insp.cd)
- **Extraction sidecar:** `provenance.csv` records source report references for selected transcribed rows and defines the schema for full backfill.

See `data/README.md` for project-wide conventions.
