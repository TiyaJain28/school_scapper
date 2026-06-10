"""
main.py — Entry point for School Data Collection Pipeline
Usage: python main.py [--input data/schools_input.csv] [--skip-scrape]
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.scraper import load_schools, enrich_school, SchoolRecord
from src.generator import generate_all
from src.exporter import export_to_excel, export_to_csv, export_missing_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def run_pipeline(csv_path: str, skip_scrape: bool = False):
    """Run the full data collection and content generation pipeline."""
    print("\n" + "=" * 60)
    print("  SCHOOL DATA COLLECTION PIPELINE")
    print("=" * 60)

    # Step 1: Load schools from CSV
    print("\n[1/5] Loading schools from input CSV...")
    schools = load_schools(csv_path)
    print(f"  Loaded {len(schools)} schools")

    # Step 2: Enrich with scraped data
    enriched = []
    missing_report = []

    if skip_scrape:
        print("\n[2/5] Skipping web scraping (--skip-scrape flag set)")
        enriched = schools
    else:
        print(f"\n[2/5] Enriching {len(schools)} schools via web scraping...")
        for i, school in enumerate(schools, 1):
            print(f"  [{i}/{len(schools)}] {school.name}")
            try:
                school = enrich_school(school)
                enriched.append(school)
                print(f"  ✓ Done: found={school.founded or 'N/A'}, students={school.students or 'N/A'}")
            except Exception as e:
                log.error(f"Failed: {school.name} — {e}")
                missing_report.append({
                    "School Name": school.name,
                    "Missing Field(s)": "enriched data",
                    "Reason": str(e),
                    "Location": school.city,
                })
                enriched.append(school)  # still include with original data

    # Step 3: Export Excel + CSV
    print("\n[3/5] Exporting spreadsheet...")
    excel_path = export_to_excel(enriched)
    csv_out_path = export_to_csv(enriched)

    # Step 4: Generate HTML content pages
    print("\n[4/5] Generating Kidrovia content pages...")
    pages = generate_all(enriched)
    print(f"  Generated {len(pages)} content pages in output/pages/")

    # Step 5: Missing data report
    print("\n[5/5] Writing missing data report...")
    # Check for missing mandatory fields
    for school in enriched:
        missing_fields = []
        for field in ["name", "city", "address", "phone", "website", "description"]:
            val = getattr(school, field, "")
            if not val or val.strip() == "":
                missing_fields.append(field)
        if missing_fields:
            missing_report.append({
                "School Name": school.name or "UNKNOWN",
                "Missing Field(s)": ", ".join(missing_fields),
                "Reason": "Field not found in input data or scraped sources",
                "Location": school.city,
            })

    if missing_report:
        export_missing_report(missing_report, "output/missing_report.xlsx")
    else:
        print("  No missing data — all fields populated!")

    # Summary
    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60)
    print(f"  Schools processed : {len(enriched)}")
    print(f"  Pages generated   : {len(pages)}")
    print(f"  Missing records   : {len(missing_report)}")
    print(f"\n  Outputs:")
    print(f"    {excel_path}")
    print(f"    {csv_out_path}")
    print(f"    output/pages/   ({len(pages)} HTML files)")
    if missing_report:
        print(f"    output/missing_report.xlsx")
    print()

    return enriched, missing_report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="School Data Collection Pipeline")
    parser.add_argument(
        "--input",
        default="data/schools_input.csv",
        help="Path to input CSV file (default: data/schools_input.csv)",
    )
    parser.add_argument(
        "--skip-scrape",
        action="store_true",
        help="Skip web scraping and use input data only (useful for testing)",
    )
    args = parser.parse_args()

    Path("logs").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)

    run_pipeline(args.input, skip_scrape=args.skip_scrape)
