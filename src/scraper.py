"""
School Data Scraper
Collects school information and generates Kidrovia-format content pages.
"""

import csv
import time
import logging
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/scraper.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

RETRY_LIMIT = 3
RETRY_DELAY = 2  # seconds between retries


@dataclass
class SchoolRecord:
    name: str
    city: str
    category: str
    website: str
    description: str
    verification_status: str
    address: str
    phone: str
    # Enriched fields (scraped)
    founded: str = ""
    ages: str = ""
    students: str = ""
    ratio: str = ""
    school_type: str = ""
    annual_fee: str = ""
    tagline: str = ""
    about_long: str = ""
    philosophy: str = ""
    outcomes: str = ""
    faculty: str = ""
    wellbeing: str = ""
    curriculum: str = ""
    achievements: str = ""
    facilities: str = ""
    admissions_info: str = ""
    application_deadline: str = ""
    image_url: str = ""
    errors: list = field(default_factory=list)


def fetch_url(url: str, retries: int = RETRY_LIMIT) -> Optional[BeautifulSoup]:
    """Fetch a URL with retry logic. Returns BeautifulSoup or None."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml")
        except requests.exceptions.HTTPError as e:
            log.warning(f"HTTP error ({e}) for {url}, attempt {attempt}/{retries}")
        except requests.exceptions.ConnectionError as e:
            log.warning(f"Connection error for {url}, attempt {attempt}/{retries}: {e}")
        except requests.exceptions.Timeout:
            log.warning(f"Timeout for {url}, attempt {attempt}/{retries}")
        except Exception as e:
            log.error(f"Unexpected error for {url}: {e}")
            break

        if attempt < retries:
            time.sleep(RETRY_DELAY * attempt)

    return None


def scrape_wikipedia(school_name: str) -> dict:
    """Try to get data from Wikipedia."""
    search_name = school_name.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{search_name}"
    soup = fetch_url(url)
    result = {}

    if not soup:
        # Try with "_New_York_City" suffix for NYC schools
        url2 = f"https://en.wikipedia.org/wiki/{search_name}_(New_York_City)"
        soup = fetch_url(url2)

    if not soup:
        log.info(f"Wikipedia: no page found for {school_name}")
        return result

    log.info(f"Wikipedia: found page for {school_name}")

    # Extract infobox
    infobox = soup.find("table", {"class": "infobox"})
    if infobox:
        for row in infobox.find_all("tr"):
            cells = row.find_all(["th", "td"])
            if len(cells) == 2:
                key = cells[0].get_text(strip=True).lower()
                val = cells[1].get_text(strip=True)
                if "founded" in key or "established" in key:
                    result["founded"] = val
                elif "type" in key:
                    result["school_type"] = val
                elif "enrollment" in key or "students" in key:
                    result["students"] = val
                elif "ratio" in key:
                    result["ratio"] = val
                elif "age" in key or "grade" in key:
                    result["ages"] = val

    # First paragraphs for about text
    content_div = soup.find("div", {"class": "mw-parser-output"})
    if content_div:
        paras = []
        for p in content_div.find_all("p", recursive=False):
            text = p.get_text(strip=True)
            if len(text) > 80:
                paras.append(text)
            if len(paras) >= 2:
                break
        if paras:
            result["about_long"] = " ".join(paras)

    return result


def scrape_official_site(school: SchoolRecord) -> dict:
    """Try to scrape data from the school's official website."""
    result = {}
    website = school.website
    if not website.startswith("http"):
        website = "https://" + website

    # Try /about page first, then homepage
    for path in ["/about", "/about-us", "/history", "/"]:
        url = website.rstrip("/") + path
        soup = fetch_url(url)
        if not soup:
            continue

        log.info(f"Official site: scraped {url}")

        # Try to find founding year
        text = soup.get_text()
        import re
        year_match = re.search(r"[Ff]ounded\s+(?:in\s+)?(\d{4})", text)
        if year_match and not result.get("founded"):
            result["founded"] = year_match.group(1)

        # Try to find student count
        students_match = re.search(r"(\d[\d,]+)\s+students", text)
        if students_match and not result.get("students"):
            result["students"] = students_match.group(1)

        # Try to find a tagline or motto
        for tag in soup.find_all(["h1", "h2", "blockquote"])[:5]:
            t = tag.get_text(strip=True)
            if 20 < len(t) < 200 and not result.get("tagline"):
                result["tagline"] = t
                break

        # Find a meaningful paragraph for about
        for p in soup.find_all("p"):
            t = p.get_text(strip=True)
            if len(t) > 150 and not result.get("about_long"):
                result["about_long"] = t
                break

        # Find an image
        for img in soup.find_all("img", src=True):
            src = img["src"]
            if any(k in src.lower() for k in ["campus", "school", "building", "hero", "banner"]):
                if src.startswith("http"):
                    result["image_url"] = src
                    break

        if result:
            break

    return result


def enrich_school(school: SchoolRecord) -> SchoolRecord:
    """Enrich a school record with scraped data."""
    log.info(f"Enriching: {school.name}")

    # 1. Try Wikipedia
    wiki_data = scrape_wikipedia(school.name)
    for k, v in wiki_data.items():
        if v and not getattr(school, k, ""):
            setattr(school, k, v)

    time.sleep(1)  # polite delay

    # 2. Try official site
    site_data = scrape_official_site(school)
    for k, v in site_data.items():
        if v and not getattr(school, k, ""):
            setattr(school, k, v)

    # 3. Fall back to data already in input
    if not school.founded:
        import re
        year = re.search(r"\b(1[6-9]\d{2}|20[0-2]\d)\b", school.description)
        if year:
            school.founded = year.group(1)

    log.info(
        f"Done: {school.name} — founded={school.founded}, "
        f"students={school.students}, about={len(school.about_long)} chars"
    )
    return school


def load_schools(csv_path: str) -> list[SchoolRecord]:
    """Load school records from CSV."""
    schools = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            schools.append(SchoolRecord(
                name=row.get("School", "").strip(),
                city=row.get("city", "").strip(),
                category=row.get("category", "").strip(),
                website=row.get("website", "").strip(),
                description=row.get("description", "").strip(),
                verification_status=row.get("verification_status", "").strip(),
                address=row.get("address", "").strip(),
                phone=row.get("phone", "").strip(),
            ))
    log.info(f"Loaded {len(schools)} schools from {csv_path}")
    return schools


def run(csv_path: str = "data/schools_input.csv"):
    """Main entry point."""
    Path("logs").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)

    schools = load_schools(csv_path)
    enriched = []
    missing_report = []

    for school in schools:
        try:
            school = enrich_school(school)
            enriched.append(school)
        except Exception as e:
            log.error(f"Failed to process {school.name}: {e}")
            missing_report.append({
                "School Name": school.name,
                "Missing Field(s)": "All enriched fields",
                "Reason": str(e),
            })

    return enriched, missing_report


if __name__ == "__main__":
    enriched, missing = run()
    print(f"\nProcessed {len(enriched)} schools")
    print(f"Missing report: {len(missing)} entries")