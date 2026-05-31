"""Tests for INSP SitRep source discovery and extraction helpers."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from tools import insp_sitrep_sources as sources


VERIFIED_SHA = "a" * 64


SITREP13_TEXT = """
                    Rapport de Situation de la 17ème Epidémie de la Maladie à Virus EBOLA /RDC
                                                            SitRep N°013/MVB_27/2026

Date de rapportage               27 mai 2026
Date de publication              28 mai 2026

    125                   17                   906*                   223                  70,1%                 8,7%                       1        ND

Cumul cas             Cumul décès           Cumul cas         Cumul Décès Taux d’occupation                Taux d’occupation                      Cumul cas
confirmés              parmi les             suspects          suspects   chez les suspects                chez les confirmés          Guéris
                                    * Le nombre de cas suspects a été revu à la baisse suite au retrait des non-cas et des cas confirmés.

 Tableau II. Répartition des cas, décès suspects et confirmés de maladie à virus Ebola dans les zones
                      de santé de la DPS Ituri, Nord-Kivu et Sud Kivu au 27 mai 2026
                                                                                 Nbre de
                                                               Nbre de cas                       Nbre de cas          Nbre de
                   Provinces           Zones de santé                             décès
                                                                suspects*                        Confirmés*          contacts*
                                                                                suspects*
                                   Aru                                4             1                  1                 0
                                   Bambu                              6             2                  0                244
                                   Bunia                            249            48                 37                404
                                   Kilo                               8             2                  1                 41
                       Ituri       Mongbwalu                        339            88                 20                222
                                   Nizi                               6             2                  2                220
                                   Nyankunde                         45            11                 10                397
                                   Rwampara                         228            69                 33                697
                                   Echantillons sans
                                                                     0              0                  6                  0
                                   fiche
                                Sous total                          885            223               110                2225
                 Nord-Kivu         Butembo                            7             0                 5                   28
                                   Goma                               0             0                 1                   74
                                   Kalunguta                         13             0                 2                  ND
                                   Karisimbi                                                                             181
                                   Katwa                             0              0                  4                 111
                                   Kyondo                            0              0                  0                  16
                                   Oicha                             0              0                  2                 ND
                                Sous total                          20              0                 14                 410
                 Sud-Kivu          Miti Murhesa                      1              0                  1                 ND
                                Sous total                           1              0                  1                  0
                                   Total                            906            223               125               2635**
 *Ces données sont susceptibles de changer après harmonisation des données à différents niveaux de la pyramide sanitaire avec le système de

Surveillance aux Points d’entrées et Points de contrôle (PoE/PoC) :
"""


SITREP14_TEXT = """
                                                       Rapport de Situation de la 17 ème Epidémie de la Maladie à Virus EBOLA /RDC
                                                                              SitRep N°014/MVB_28/2026

Provinces touchées (3)                        ITURI, NORD-KIVU & SUD-KIVU
                                              ITURI : Aru, Damas, Bunia, Kilo, Mongbwalu, Nizi, Nyankunde et Rwampara
Zones de Santé touchées
                                              NORD-KIVU : Butembo, Goma, Oicha, Kalunguta et Katwa
(13)
                                              SUD-KIVU : Miti-Murhesa
Date de rapportage                            28 mai 2026
Date de publication                           29 mai 2026




                                                                                            ND                              ND                                    1
    210                          17                         349*                                                                                                                                    ND
Cumul cas                 Cumul décès                    Cumul Cas                 Taux d’occupation                 Taux d’occupation
                           parmi les                      Suspects                                                                                             Guéris
confirmés                                                                          chez les suspects                 chez les confirmés                                                          Cumul cas
                           confirmés                                                                                                                                                           confirmés CTE
         Le nombre de cas suspects a été revu à la baisse, ces derniers ayant fait l'objet d'investigations et de prélèvements dont les résultats ont confirmé certains cas et infirmé d'autres.
         Les décès suspects ont été temporairement exclus du comptage dans l'attente des résultats des investigations en cours, qui permettront de les confirmer et de les classer comme cas
          probables, ou de les écarter définitivement.


                       0. FAITS SAILLANTS
"""


SITREP12_TEXT = """
            Rapport de Situation de la 17ème Epidémie de la Maladie à Virus EBOLA /RDC
                                                   SitRep N°012/MVB_26/2026
Date de rapportage               26 mai 2026
Date de publication              26 mai 2026


    121                17*               1077               246               ND                ND              0             ND
Cumul cas          Cumul décès         Cumul cas Cumul Décès Taux d’occupation            Taux d’occupation
                                                                                                               Guéris   Nbre des cas
confirmés            parmi les          suspects       suspects     chez les suspects     chez les confirmés            actifs
                     confirmés
            *Ces décès sont sous-estimés car la confirmation de diagnostics est tardive
"""


UNKNOWN_FUTURE_TEXT = """
            Rapport de Situation de la 17ème Epidémie de la Maladie à Virus EBOLA /RDC
                                                   SitRep N°015/MVB_29/2026
Date de rapportage               29 mai 2026
Date de publication              30 mai 2026

Cette édition présente les indicateurs dans un format narratif et graphique.
Les valeurs cumulatives nationales et les tableaux par zone de santé ne sont pas exposés
dans les libellés publics utilisés par les versions précédentes.
""" * 3


def test_extract_pdf_url_from_post_content():
    post = {
        "link": "https://insp.cd/sitrep-mve-n-013-2026/",
        "content": {
            "rendered": (
                '<a href="https://insp.cd/wp-content/uploads/2026/05/'
                'SitRep_MVE_RDC_NA°013_27_05_2026_ES-IM4.pdf">PDF</a>'
            )
        },
    }

    assert sources._extract_pdf_url(post).endswith("SitRep_MVE_RDC_NA°013_27_05_2026_ES-IM4.pdf")


def test_parse_report_text_extracts_dates_totals_and_revision_note():
    parsed = sources.parse_report_text(SITREP13_TEXT)

    assert parsed["report_number"] == "013"
    assert parsed["report_date"] == "2026-05-27"
    assert parsed["publication_date"] == "2026-05-28"
    assert parsed["national_confirmed_cases"] == "125"
    assert parsed["national_confirmed_deaths"] == "17"
    assert parsed["national_suspected_cases"] == "906"
    assert parsed["national_suspected_deaths"] == "223"
    assert "revu à la baisse" in parsed["revision_notes"]


def test_parse_report_text_extracts_sitrep14_split_banner_and_withheld_deaths():
    parsed = sources.parse_report_text(SITREP14_TEXT)

    assert parsed["report_number"] == "014"
    assert parsed["report_date"] == "2026-05-28"
    assert parsed["publication_date"] == "2026-05-29"
    assert parsed["national_confirmed_cases"] == "210"
    assert parsed["national_confirmed_deaths"] == "17"
    assert parsed["national_suspected_cases"] == "349"
    assert parsed["national_suspected_deaths"] == "ND"
    assert parsed["headline_status"] == "headline_extracted"
    assert "décès suspects" in parsed["revision_notes"]


def test_parse_report_text_extracts_adjacent_sitrep12_death_columns():
    parsed = sources.parse_report_text(SITREP12_TEXT)

    assert parsed["report_number"] == "012"
    assert parsed["report_date"] == "2026-05-26"
    assert parsed["national_confirmed_cases"] == "121"
    assert parsed["national_confirmed_deaths"] == "17"
    assert parsed["national_suspected_cases"] == "1077"
    assert parsed["national_suspected_deaths"] == "246"


def test_parse_pdf_text_marks_page_break_only_text_as_not_extractable():
    parsed = sources.parse_pdf_text("\f\f\f\n")

    assert parsed["text_extractable"] == "false"
    assert parsed["text_chars"] == "0"
    assert parsed["layout_status"] == "image_only_pdf"
    assert parsed["extraction_confidence"] == "blocked"
    assert parsed["draft_status"] == "blocked"
    assert parsed["blocking_reason"] == "not_publicly_extractable"
    assert parsed["headline_status"] == "text_not_extractable"
    assert parsed["table_ii_status"] == "text_not_extractable"
    assert "national_confirmed_cases" not in parsed


def test_parse_pdf_path_records_pdftotext_failures_without_crashing(tmp_path: Path, monkeypatch):
    path = tmp_path / "broken.pdf"
    path.write_bytes(b"not a real pdf")

    def fail_pdf_text(pdf_path: Path) -> str:
        raise RuntimeError("pdftotext failed")

    monkeypatch.setattr(sources, "_pdf_text", fail_pdf_text)

    parsed = sources.parse_pdf_path(path)

    assert parsed["text_extractable"] == "false"
    assert parsed["layout_status"] == "image_only_pdf"
    assert parsed["draft_status"] == "blocked"
    assert parsed["headline_status"] == "pdf_text_failed:RuntimeError"
    assert "pdf_text_failed:RuntimeError" in parsed["blocking_reason"]


def test_table_ii_status_reports_missing_table_for_sitrep14_shape():
    parsed = sources.parse_report_text(SITREP14_TEXT)

    assert sources.table_ii_status(SITREP14_TEXT, parsed) == "table_ii_missing"


def test_extract_table_ii_assigns_values_by_layout_columns():
    source = sources.ReportSource(
        report_number=13,
        title="SitRep MVE N° 013/2026",
        post_url="https://insp.cd/sitrep-mve-n-013-2026/",
        post_id=24889,
        pdf_url="https://insp.cd/wp-content/uploads/2026/05/example.pdf",
        parsed={"report_date": "2026-05-27"},
    )

    rows = sources.extract_table_ii(SITREP13_TEXT, source)
    by_key = {(r.nom_raw, r.metric): r.value for r in rows}

    assert by_key[("Bunia", "cumulative_suspected_cases")] == "249"
    assert by_key[("Bunia", "cumulative_suspected_deaths")] == "48"
    assert by_key[("Bunia", "cumulative_confirmed_cases")] == "37"
    assert by_key[("Bunia", "cumulative_contacts_traced")] == "404"
    assert by_key[("Karisimbi", "cumulative_contacts_traced")] == "181"
    assert by_key[("Miti Murhesa", "cumulative_confirmed_cases")] == "1"
    assert ("Karisimbi", "cumulative_suspected_cases") not in by_key
    assert not any(r.nom_raw == "Echantillons sans" for r in rows)
    assert not any(r.nom_raw == "Total" for r in rows)
    assert not any(r.nom_raw == "s total" for r in rows)


def test_write_source_reports_includes_resilience_status_columns(tmp_path: Path):
    path = tmp_path / "source_reports.csv"
    source = sources.ReportSource(
        report_number=14,
        title="SitRep MVE N° 014/2026",
        post_url="https://insp.cd/sitrep-mve-n-014-2026/",
        post_id=24894,
        post_published_at="2026-05-30T14:03:52Z",
        post_modified_at="2026-05-30T14:03:57Z",
        pdf_url="https://insp.cd/wp-content/uploads/2026/05/example.pdf",
        source_relation="raw_matches_official",
        last_modified="Sat, 30 May 2026 14:03:03 GMT",
        pdf_sha256=VERIFIED_SHA,
        official_pdf_sha256=VERIFIED_SHA,
        parsed=sources.parse_pdf_text(SITREP14_TEXT),
    )

    sources.write_source_reports(path, [source])

    with path.open(newline="", encoding="utf-8") as f:
        row = next(csv.DictReader(f))

    assert row["text_extractable"] == "true"
    assert int(row["text_chars"]) > sources.TEXT_EXTRACTABLE_MIN_CHARS
    assert row["post_published_at"] == "2026-05-30T14:03:52Z"
    assert row["post_modified_at"] == "2026-05-30T14:03:57Z"
    assert row["last_modified"] == "Sat, 30 May 2026 14:03:03 GMT"
    assert row["source_gate_status"] == "passed"
    assert row["layout_status"] == "partial_extract"
    assert row["extraction_confidence"] == "partial"
    assert row["headline_status"] == "headline_extracted"
    assert row["table_ii_status"] == "table_ii_missing"
    assert row["national_values_status"] == "found_withheld_by_sitrep"
    assert row["national_suspected_deaths"] == "ND"
    assert row["draft_status"] == "ready_for_review"
    assert row["blocking_reason"] == "table_ii_missing"
    assert row["status"] == "official_verified"


def test_filter_sources_by_report_number_keeps_requested_window():
    rows = [
        sources.ReportSource(report_number=12, title="", post_url="", post_id=12),
        sources.ReportSource(report_number=13, title="", post_url="", post_id=13),
        sources.ReportSource(report_number=14, title="", post_url="", post_id=14),
        sources.ReportSource(report_number=15, title="", post_url="", post_id=15),
    ]

    filtered = sources.filter_sources_by_report_number(
        rows,
        min_report_number=13,
        max_report_number=14,
    )

    assert [row.report_number for row in filtered] == [13, 14]


def test_sync_official_pdfs_replaces_stale_raw_bytes(tmp_path: Path, monkeypatch):
    raw_path = tmp_path / "data" / "insp_sitrep" / "raw" / "SitRep_MVE_007-2026.pdf"
    raw_path.parent.mkdir(parents=True)
    raw_path.write_bytes(b"derived image-only copy")
    official_bytes = b"official source pdf bytes"

    monkeypatch.setattr(sources, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        sources,
        "_head_url",
        lambda url, *, allow_insecure_tls=False: {"content-length": str(len(official_bytes))},
    )
    monkeypatch.setattr(
        sources,
        "_download_url",
        lambda url, path, *, allow_insecure_tls=False: path.write_bytes(official_bytes),
    )
    source = sources.ReportSource(
        report_number=7,
        title="SitRep MVE N° 007/2026",
        post_url="https://insp.cd/sitrep-mve-n-007-2026/",
        post_id=1,
        pdf_url="https://insp.cd/wp-content/uploads/2026/05/example.pdf",
        raw_path="data/insp_sitrep/raw/SitRep_MVE_007-2026.pdf",
    )

    [enriched] = sources.enrich_pdf_metadata([source], sync_official_pdfs=True)

    expected_sha = hashlib.sha256(official_bytes).hexdigest()
    assert raw_path.read_bytes() == official_bytes
    assert enriched.pdf_sha256 == expected_sha
    assert enriched.official_pdf_sha256 == expected_sha
    assert enriched.pdf_bytes == len(official_bytes)
    assert enriched.official_pdf_bytes == len(official_bytes)
    assert enriched.source_relation == "raw_matches_official"
    assert enriched.status == "official_synced"


def test_sync_official_pdfs_skips_download_when_manifest_proves_unchanged(
    tmp_path: Path,
    monkeypatch,
):
    raw_path = tmp_path / "data" / "insp_sitrep" / "raw" / "SitRep_MVE_007-2026.pdf"
    raw_path.parent.mkdir(parents=True)
    official_bytes = b"official source pdf bytes"
    raw_path.write_bytes(official_bytes)
    official_sha = hashlib.sha256(official_bytes).hexdigest()
    pdf_url = "https://insp.cd/wp-content/uploads/2026/05/example.pdf"

    monkeypatch.setattr(sources, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        sources,
        "_head_url",
        lambda url, *, allow_insecure_tls=False: {
            "content-length": str(len(official_bytes)),
            "etag": '"abc123"',
            "last-modified": "Sat, 30 May 2026 12:00:00 GMT",
        },
    )

    def fail_download(url: str, path: Path, *, allow_insecure_tls: bool = False) -> None:
        raise AssertionError("unchanged source should not be downloaded")

    monkeypatch.setattr(sources, "_download_url", fail_download)
    source = sources.ReportSource(
        report_number=7,
        title="SitRep MVE N° 007/2026",
        post_url="https://insp.cd/sitrep-mve-n-007-2026/",
        post_id=1,
        pdf_url=pdf_url,
        raw_path="data/insp_sitrep/raw/SitRep_MVE_007-2026.pdf",
    )
    cache = {
        7: {
            "pdf_url": pdf_url,
            "pdf_sha256": official_sha,
            "official_pdf_sha256": official_sha,
            "official_pdf_bytes": str(len(official_bytes)),
            "source_gate_status": "passed",
            "etag": '"abc123"',
            "last_modified": "Sat, 30 May 2026 12:00:00 GMT",
        }
    }

    [enriched] = sources.enrich_pdf_metadata(
        [source],
        sync_official_pdfs=True,
        source_report_cache=cache,
    )

    assert enriched.status == "official_unchanged"
    assert enriched.source_relation == "raw_matches_official"
    assert enriched.parsed["source_gate_status"] == "passed"


def test_sync_official_pdfs_blocks_instead_of_crashing_on_download_timeout(tmp_path: Path, monkeypatch):
    raw_path = tmp_path / "data" / "insp_sitrep" / "raw" / "SitRep_MVE_007-2026.pdf"
    raw_path.parent.mkdir(parents=True)
    raw_path.write_bytes(b"previous local pdf")

    monkeypatch.setattr(sources, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        sources,
        "_head_url",
        lambda url, *, allow_insecure_tls=False: {"content-length": "1234"},
    )

    def timeout(url: str, path: Path, *, allow_insecure_tls: bool = False) -> None:
        raise TimeoutError("read timed out")

    monkeypatch.setattr(sources, "_download_url", timeout)
    source = sources.ReportSource(
        report_number=7,
        title="SitRep MVE N° 007/2026",
        post_url="https://insp.cd/sitrep-mve-n-007-2026/",
        post_id=1,
        pdf_url="https://insp.cd/wp-content/uploads/2026/05/example.pdf",
        raw_path="data/insp_sitrep/raw/SitRep_MVE_007-2026.pdf",
    )

    [enriched] = sources.enrich_pdf_metadata([source], sync_official_pdfs=True)

    assert enriched.status == "pdf_download_failed:TimeoutError"
    assert enriched.source_relation == "official_unchecked"
    assert enriched.parsed["source_gate_status"] == "blocked_official_unchecked"
    assert enriched.parsed["draft_status"] == "blocked"
    assert "blocked_official_unchecked" in enriched.parsed["blocking_reason"]


def test_source_identity_mismatch_blocks_drafts(tmp_path: Path, monkeypatch):
    raw_path = tmp_path / "data" / "insp_sitrep" / "raw" / "SitRep_MVE_013-2026.pdf"
    raw_path.parent.mkdir(parents=True)
    raw_path.write_bytes(b"official source pdf bytes")
    official_sha = hashlib.sha256(raw_path.read_bytes()).hexdigest()

    monkeypatch.setattr(sources, "REPO_ROOT", tmp_path)
    source = sources.ReportSource(
        report_number=13,
        title="SitRep MVE N° 013/2026",
        post_url="https://insp.cd/sitrep-mve-n-013-2026/",
        post_id=13,
        pdf_url="https://insp.cd/wp-content/uploads/2026/05/example.pdf",
        raw_path="data/insp_sitrep/raw/SitRep_MVE_013-2026.pdf",
        official_pdf_sha256=official_sha,
        parsed={
            "report_number": "014",
            "pdf_text_status": "text_extracted",
            "draft_status": "ready_for_review",
        },
    )

    [enriched] = sources.enrich_pdf_metadata([source])

    assert enriched.parsed["source_gate_status"] == "passed"
    assert enriched.parsed["source_identity_status"] == "blocked_report_number_mismatch"
    assert enriched.parsed["draft_status"] == "blocked"
    assert "blocked_report_number_mismatch" in enriched.parsed["blocking_reason"]
    assert sources.build_processed_draft_values([], [enriched]) == []


def test_processed_drafts_write_review_shaped_csvs(tmp_path: Path):
    table_row = sources.ExtractedValue(
        report_number=13,
        report_date="2026-05-27",
        nom_raw="Bunia",
        metric="cumulative_suspected_cases",
        value="249",
        source_pdf="https://insp.cd/example.pdf",
        source_post="https://insp.cd/sitrep-mve-n-013-2026/",
    )
    source = sources.ReportSource(
        report_number=13,
        title="SitRep MVE N° 013/2026",
        post_url="https://insp.cd/sitrep-mve-n-013-2026/",
        post_id=24889,
        pdf_url="https://insp.cd/example.pdf",
        source_relation="raw_matches_official",
        pdf_sha256=VERIFIED_SHA,
        official_pdf_sha256=VERIFIED_SHA,
        parsed={
            "report_date": "2026-05-27",
            "national_confirmed_cases": "125",
            "draft_status": "ready_for_review",
        },
    )

    drafts = sources.build_processed_draft_values([table_row], [source])
    written = sources.write_processed_drafts(tmp_path / "drafts", drafts)

    assert {
        path.name for path in written
    } == {
        "insp_sitrep__cumulative_suspected_cases__daily.csv",
    }
    with (tmp_path / "drafts" / "insp_sitrep__cumulative_suspected_cases__daily.csv").open(
        newline="",
        encoding="utf-8",
    ) as f:
        assert list(csv.DictReader(f)) == [
            {"nom": "Bunia", "date": "2026-05-27", "cumulative_suspected_cases": "249"}
        ]
    assert not (
        tmp_path / "drafts" / "insp_sitrep__national_cumulative_confirmed_cases__daily.csv"
    ).exists()

    processed = tmp_path / "processed"
    processed.mkdir()
    processed_path = processed / "insp_sitrep__cumulative_suspected_cases__daily.csv"
    with processed_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nom", "date", "cumulative_suspected_cases"])
        writer.writerow(["Bunia", "2026-05-27", "250"])

    counts = sources.write_processed_review(tmp_path / "review.csv", drafts, processed_dir=processed)

    assert counts["value_mismatch"] == 1
    assert "missing_processed" not in counts

    with processed_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Mongbalu", "2026-05-14", "246"])

    candidates = sources.write_processed_candidates(processed, drafts)

    assert candidates == []
    assert processed_path not in candidates
    with processed_path.open(newline="", encoding="utf-8") as f:
        candidate_rows = list(csv.DictReader(f))
    assert {"nom": "Mongbalu", "date": "2026-05-14", "cumulative_suspected_cases": "246"} in candidate_rows
    assert {"nom": "Bunia", "date": "2026-05-27", "cumulative_suspected_cases": "250"} in candidate_rows


def test_processed_review_marks_missing_rows_as_candidate_added_in_candidate_mode(tmp_path: Path):
    draft = sources.ProcessedDraftValue(
        metric="cumulative_contacts_traced",
        nom="Oicha",
        date="2026-05-27",
        value="ND",
        source_report_number=13,
        source_pdf="https://insp.cd/example.pdf",
        source_post="https://insp.cd/sitrep-mve-n-013-2026/",
        method="pdftotext_layout_table_ii",
    )

    counts = sources.write_processed_review(
        tmp_path / "review.csv",
        [draft],
        processed_dir=tmp_path / "processed",
        candidate_mode=True,
    )

    assert counts == {"candidate_added": 1}
    with (tmp_path / "review.csv").open(newline="", encoding="utf-8") as f:
        row = next(csv.DictReader(f))
    assert row["status"] == "candidate_added"
    assert row["nom"] == "Oicha"


def test_processed_candidates_preserve_existing_rows_and_append_only(
    tmp_path: Path,
    monkeypatch,
):
    processed = tmp_path / "processed"
    processed.mkdir()
    processed_path = processed / "insp_sitrep__cumulative_suspected_deaths__daily.csv"
    processed_path.write_bytes(
        b"nom,date,cumulative_suspected_deaths\r\nNyankunde,2026-05-27,15\r\n"
    )

    def canonical(name: str) -> str | None:
        return "Nyakunde" if name in {"Nyankunde", "Nyakunde"} else None

    monkeypatch.setattr(sources, "to_canonical", canonical)
    drafts = [
        sources.ProcessedDraftValue(
            metric="cumulative_suspected_deaths",
            nom="Nyakunde",
            date="2026-05-27",
            value="11",
            source_report_number=13,
            source_pdf="https://insp.cd/example.pdf",
            source_post="https://insp.cd/sitrep-mve-n-013-2026/",
            method="pdftotext_layout_table_ii",
        ),
        sources.ProcessedDraftValue(
            metric="cumulative_suspected_deaths",
            nom="Nyakunde",
            date="2026-05-28",
            value="16",
            source_report_number=14,
            source_pdf="https://insp.cd/example.pdf",
            source_post="https://insp.cd/sitrep-mve-n-014-2026/",
            method="pdftotext_layout_table_ii",
        ),
    ]

    candidates = sources.write_processed_candidates(processed, drafts)

    assert candidates == [processed_path]
    with processed_path.open(newline="", encoding="utf-8") as f:
        assert list(csv.DictReader(f)) == [
            {"nom": "Nyankunde", "date": "2026-05-27", "cumulative_suspected_deaths": "15"},
            {"nom": "Nyakunde", "date": "2026-05-28", "cumulative_suspected_deaths": "16"},
        ]
    assert b"\r\n" in processed_path.read_bytes()


def test_processed_candidates_skip_existing_row_with_equivalent_date_format(
    tmp_path: Path,
    monkeypatch,
):
    processed = tmp_path / "processed"
    processed.mkdir()
    processed_path = processed / "insp_sitrep__cumulative_confirmed_cases__daily.csv"
    processed_path.write_text(
        "nom,date,cumulative_confirmed_cases\n"
        "Mongbalu,27/05/2026,20\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(sources, "to_canonical", lambda name: "Mongbalu")
    drafts = [
        sources.ProcessedDraftValue(
            metric="cumulative_confirmed_cases",
            nom="Mongbalu",
            date="2026-05-27",
            value="20",
            source_report_number=13,
            source_pdf="https://insp.cd/example.pdf",
            source_post="https://insp.cd/sitrep-mve-n-013-2026/",
            method="pdftotext_layout_table_ii",
        )
    ]

    candidates = sources.write_processed_candidates(processed, drafts)

    assert candidates == []
    assert processed_path.read_text(encoding="utf-8").splitlines() == [
        "nom,date,cumulative_confirmed_cases",
        "Mongbalu,27/05/2026,20",
    ]


def test_processed_candidates_reuse_existing_display_date_for_same_day(
    tmp_path: Path,
    monkeypatch,
):
    processed = tmp_path / "processed"
    processed.mkdir()
    processed_path = processed / "insp_sitrep__cumulative_contacts_traced__daily.csv"
    processed_path.write_text(
        "nom,date,cumulative_contacts_traced\n"
        "Kyondo,27/05/2026,16\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(sources, "to_canonical", lambda name: name)
    drafts = [
        sources.ProcessedDraftValue(
            metric="cumulative_contacts_traced",
            nom="Oicha",
            date="2026-05-27",
            value="ND",
            source_report_number=13,
            source_pdf="https://insp.cd/example.pdf",
            source_post="https://insp.cd/sitrep-mve-n-013-2026/",
            method="pdftotext_layout_table_ii",
        )
    ]

    candidates = sources.write_processed_candidates(processed, drafts)

    assert candidates == [processed_path]
    assert processed_path.read_text(encoding="utf-8").splitlines() == [
        "nom,date,cumulative_contacts_traced",
        "Kyondo,27/05/2026,16",
        "Oicha,27/05/2026,ND",
    ]


def test_processed_drafts_remove_stale_generated_metric_files(tmp_path: Path):
    output_dir = tmp_path / "drafts"
    output_dir.mkdir()
    stale = output_dir / sources.PROCESSED_DRAFT_BY_METRIC["national_cumulative_confirmed_cases"]
    stale.write_text("nom,date,national_cumulative_confirmed_cases\nBunia,2026-05-01,1\n")
    value = sources.ProcessedDraftValue(
        metric="cumulative_suspected_cases",
        nom="Bunia",
        date="2026-05-27",
        value="249",
        source_report_number=13,
        source_pdf="https://insp.cd/example.pdf",
        source_post="https://insp.cd/sitrep-mve-n-013-2026/",
        method="pdftotext_layout_table_ii",
    )

    written = sources.write_processed_drafts(output_dir, [value])

    assert written == [output_dir / sources.PROCESSED_DRAFT_BY_METRIC["cumulative_suspected_cases"]]
    assert not stale.exists()


def test_processed_drafts_require_verified_source_gate():
    source = sources.ReportSource(
        report_number=13,
        title="SitRep MVE N° 013/2026",
        post_url="https://insp.cd/sitrep-mve-n-013-2026/",
        post_id=24889,
        pdf_url="https://insp.cd/example.pdf",
        source_relation="raw_matches_official",
        parsed={
            "report_date": "2026-05-27",
            "national_confirmed_cases": "125",
            "draft_status": "ready_for_review",
        },
    )

    row = sources.ExtractedValue(
        report_number=13,
        report_date="2026-05-27",
        nom_raw="Bunia",
        metric="cumulative_suspected_cases",
        value="249",
        source_pdf=source.pdf_url,
        source_post=source.post_url,
    )

    assert sources.build_processed_draft_values([row], [source]) == []


def test_unsupported_future_layout_blocks_drafts_and_writes_review_row(tmp_path: Path):
    parsed = sources.parse_pdf_text(UNKNOWN_FUTURE_TEXT)
    source = sources.ReportSource(
        report_number=15,
        title="SitRep MVE N° 015/2026",
        post_url="https://insp.cd/sitrep-mve-n-015-2026/",
        post_id=24895,
        pdf_url="https://insp.cd/example.pdf",
        source_relation="raw_matches_official",
        pdf_sha256=VERIFIED_SHA,
        official_pdf_sha256=VERIFIED_SHA,
        parsed=parsed,
    )

    assert parsed["layout_status"] == "unsupported_text_layout"
    assert parsed["draft_status"] == "blocked"
    assert sources.build_processed_draft_values([], [source]) == []

    counts = sources.write_processed_review(tmp_path / "review.csv", [], sources=[source])

    assert counts["blocked"] == 1
    with (tmp_path / "review.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows == [
        {
            "status": "blocked",
            "processed_file": "",
            "metric": "",
            "nom": "",
            "date": "2026-05-29",
            "processed_value": "",
            "extracted_value": "",
            "source_report_number": "015",
            "source_pdf": "https://insp.cd/example.pdf",
            "source_post": "https://insp.cd/sitrep-mve-n-015-2026/",
            "source_raw_path": "",
            "method": "manual_review_required",
            "draft_status": "blocked",
            "blocking_reason": "headline_not_found;table_ii_missing;national_values_not_found",
        }
    ]


def test_partial_layout_writes_manual_review_row(tmp_path: Path):
    source = sources.ReportSource(
        report_number=14,
        title="SitRep MVE N° 014/2026",
        post_url="https://insp.cd/sitrep-mve-n-014-2026/",
        post_id=24894,
        pdf_url="https://insp.cd/example.pdf",
        source_relation="raw_matches_official",
        pdf_sha256=VERIFIED_SHA,
        official_pdf_sha256=VERIFIED_SHA,
        parsed=sources.parse_pdf_text(SITREP14_TEXT),
    )

    drafts = sources.build_processed_draft_values([], [source])
    counts = sources.write_processed_review(tmp_path / "review.csv", drafts, sources=[source])

    assert drafts == []
    assert counts["manual_review_required"] == 1
    with (tmp_path / "review.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    manual_rows = [row for row in rows if row["status"] == "manual_review_required"]
    assert manual_rows[0]["source_report_number"] == "014"
    assert manual_rows[0]["blocking_reason"] == "table_ii_missing"


def test_source_review_queue_is_small_and_points_to_local_pdf(tmp_path: Path):
    source = sources.ReportSource(
        report_number=14,
        title="SitRep MVE N° 014/2026",
        post_url="https://insp.cd/sitrep-mve-n-014-2026/",
        post_id=24894,
        post_published_at="2026-05-30T14:03:52Z",
        post_modified_at="2026-05-30T14:03:57Z",
        pdf_url="https://insp.cd/example.pdf",
        raw_path="data/insp_sitrep/raw/SitRep_MVE_014-2026.pdf",
        source_relation="raw_matches_official",
        last_modified="Sat, 30 May 2026 14:03:03 GMT",
        pdf_sha256=VERIFIED_SHA,
        official_pdf_sha256=VERIFIED_SHA,
        parsed=sources.parse_pdf_text(SITREP14_TEXT),
    )

    counts = sources.write_source_review_queue(tmp_path / "source_review_queue.csv", [source])

    assert counts == {"manual_review_required": 1}
    with (tmp_path / "source_review_queue.csv").open(newline="", encoding="utf-8") as f:
        row = next(csv.DictReader(f))
    assert row["review_status"] == "manual_review_required"
    assert row["post_published_at"] == "2026-05-30T14:03:52Z"
    assert row["pdf_last_modified"] == "Sat, 30 May 2026 14:03:03 GMT"
    assert row["source_raw_path"] == "data/insp_sitrep/raw/SitRep_MVE_014-2026.pdf"
    assert row["blocking_reason"] == "table_ii_missing"
    assert "Open data/insp_sitrep/raw/SitRep_MVE_014-2026.pdf" in row["review_action"]


def test_review_summary_points_reviewer_to_small_queue_and_pdf(tmp_path: Path):
    source = sources.ReportSource(
        report_number=14,
        title="SitRep MVE N° 014/2026",
        post_url="https://insp.cd/sitrep-mve-n-014-2026/",
        post_id=24894,
        post_published_at="2026-05-30T14:03:52Z",
        post_modified_at="2026-05-30T14:03:57Z",
        pdf_url="https://insp.cd/example.pdf",
        raw_path="data/insp_sitrep/raw/SitRep_MVE_014-2026.pdf",
        source_relation="raw_matches_official",
        last_modified="Sat, 30 May 2026 14:03:03 GMT",
        pdf_sha256=VERIFIED_SHA,
        official_pdf_sha256=VERIFIED_SHA,
        status="official_unchanged",
        parsed=sources.parse_pdf_text(SITREP14_TEXT),
    )

    sources.write_review_summary(
        tmp_path / "review_summary.md",
        [source],
        source_review_counts={"manual_review_required": 1},
        processed_review_counts={"missing_processed": 519, "value_mismatch": 2},
        extracted_count=4,
        draft_file_count=4,
        source_review_queue=tmp_path / "source_review_queue.csv",
        processed_review=tmp_path / "processed_draft_review.csv",
        processed_draft_dir=tmp_path / "processed_drafts",
    )

    summary = (tmp_path / "review_summary.md").read_text(encoding="utf-8")
    assert "Source review queue" in summary
    assert "INSP Source Timing" in summary
    assert "2026-05-30T14:03:52Z" in summary
    assert "Sat, 30 May 2026 14:03:03 GMT" in summary
    assert "field-level drafts" in summary
    assert "manual_review_required" in summary
    assert "value_mismatch: 2" in summary
    assert "data/insp_sitrep/raw/SitRep_MVE_014-2026.pdf" in summary
    assert "table_ii_missing" in summary


def test_compare_processed_reports_value_mismatches(tmp_path: Path, monkeypatch):
    processed = tmp_path / "processed"
    processed.mkdir()
    path = processed / "insp_sitrep__cumulative_suspected_deaths__daily.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nom", "date", "cumulative_suspected_deaths"])
        writer.writerow(["Bunia", "2026-05-27", "55"])

    monkeypatch.setitem(
        sources.PROCESSED_BY_METRIC,
        "cumulative_suspected_deaths",
        path.name,
    )
    row = sources.ExtractedValue(
        report_number=13,
        report_date="2026-05-27",
        nom_raw="Bunia",
        metric="cumulative_suspected_deaths",
        value="48",
        source_pdf="",
        source_post="",
    )

    diffs = sources.compare_processed([row], processed_dir=processed)

    assert len(diffs) == 1
    assert "processed=55 extracted=48" in diffs[0]


def test_compare_processed_treats_equivalent_date_formats_as_same_row(
    tmp_path: Path,
    monkeypatch,
):
    processed = tmp_path / "processed"
    processed.mkdir()
    path = processed / "insp_sitrep__cumulative_confirmed_cases__daily.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nom", "date", "cumulative_confirmed_cases"])
        writer.writerow(["Mongbalu", "27/05/2026", "20"])

    monkeypatch.setitem(
        sources.PROCESSED_BY_METRIC,
        "cumulative_confirmed_cases",
        path.name,
    )
    monkeypatch.setattr(sources, "to_canonical", lambda name: "Mongbalu")
    row = sources.ExtractedValue(
        report_number=13,
        report_date="2026-05-27",
        nom_raw="Mongbalu",
        metric="cumulative_confirmed_cases",
        value="20",
        source_pdf="",
        source_post="",
    )

    assert sources.compare_processed([row], processed_dir=processed) == []


def test_main_compares_processed_before_writing_candidates(tmp_path: Path, monkeypatch):
    raw_path = tmp_path / "data" / "insp_sitrep" / "raw" / "SitRep_MVE_013-2026.pdf"
    raw_path.parent.mkdir(parents=True)
    raw_path.write_bytes(b"pdf")
    source = sources.ReportSource(
        report_number=13,
        title="SitRep MVE N° 013/2026",
        post_url="https://insp.cd/sitrep-mve-n-013-2026/",
        post_id=13,
        pdf_url="https://insp.cd/example.pdf",
        raw_path="data/insp_sitrep/raw/SitRep_MVE_013-2026.pdf",
        pdf_sha256=VERIFIED_SHA,
        official_pdf_sha256=VERIFIED_SHA,
        source_relation="raw_matches_official",
        parsed={
            "report_date": "2026-05-27",
            "draft_status": "ready_for_review",
            "source_gate_status": "passed",
        },
    )
    extracted = sources.ExtractedValue(
        report_number=13,
        report_date="2026-05-27",
        nom_raw="Bunia",
        metric="cumulative_suspected_deaths",
        value="48",
        source_pdf=source.pdf_url,
        source_post=source.post_url,
    )
    order: list[str] = []

    monkeypatch.setattr(sources, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sources, "PROCESSED_DIR", tmp_path / "processed")
    monkeypatch.setattr(sources, "discover_sources", lambda **kwargs: [source])
    monkeypatch.setattr(sources, "enrich_pdf_metadata", lambda rows, **kwargs: list(rows))

    def extract(path: Path, row_source: sources.ReportSource) -> list[sources.ExtractedValue]:
        order.append("extract")
        return [extracted]

    def compare(rows, processed_dir=sources.PROCESSED_DIR):
        order.append("compare")
        return ["value mismatch"]

    def write_candidates(processed_dir: Path, draft_values):
        order.append("candidate")
        return []

    monkeypatch.setattr(sources, "extract_table_ii_from_pdf", extract)
    monkeypatch.setattr(sources, "compare_processed", compare)
    monkeypatch.setattr(sources, "write_processed_candidates", write_candidates)

    exit_code = sources.main([
        "--compare-processed",
        "--write-processed-drafts",
        "--write-processed-candidates",
        "--write-source-reports",
        str(tmp_path / "source_reports.csv"),
        "--write-extracted-dir",
        str(tmp_path / "extracted"),
        "--write-processed-draft-dir",
        str(tmp_path / "drafts"),
        "--write-review-diffs",
        str(tmp_path / "review.csv"),
        "--write-source-review-queue",
        str(tmp_path / "source_review_queue.csv"),
        "--write-review-summary",
        str(tmp_path / "review_summary.md"),
    ])

    assert exit_code == 0
    assert order == ["extract", "compare", "candidate"]
