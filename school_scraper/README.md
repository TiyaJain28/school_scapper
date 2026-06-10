# School Data Collection Pipeline

Automated pipeline to collect comprehensive school information and generate
Kidrovia-format content pages with full Excel output.

## Project Structure

```
school_scraper/
├── main.py                  # Entry point — run this
├── src/
│   ├── scraper.py           # Web scraping (Wikipedia, official sites)
│   ├── generator.py         # HTML content page generator (Kidrovia format)
│   └── exporter.py          # Excel/CSV export
├── data/
│   └── schools_input.csv    # Input: list of schools to process
├── output/
│   ├── schools_data.xlsx    # Output: populated spreadsheet
│   ├── schools_data.csv     # Output: CSV version
│   ├── missing_report.xlsx  # Output: missing data report
│   └── pages/               # Output: one HTML page per school
├── logs/
│   └── pipeline.log         # Execution log
└── requirements.txt
```

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/school-data-pipeline.git
cd school-data-pipeline
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Run full pipeline (scrape + generate + export)
```bash
python main.py
```

### Run with custom input file
```bash
python main.py --input data/my_schools.csv
```

### Run without web scraping (use input data only — fast, for testing)
```bash
python main.py --skip-scrape
```

## Input Format

The input CSV (`data/schools_input.csv`) must have these columns:

| Column | Description |
|---|---|
| School | Full school name |
| city | City name |
| category | e.g. "Private Schools" |
| website | School website (with or without https://) |
| description | Short description |
| verification_status | e.g. "Verified" |
| address | Full street address |
| phone | Phone number |

## Output

| File | Description |
|---|---|
| `output/schools_data.xlsx` | Main spreadsheet with all collected data |
| `output/schools_data.csv` | CSV version of the same data |
| `output/pages/*.html` | Kidrovia-format HTML content per school |
| `output/missing_report.xlsx` | Schools/fields that could not be collected |

## Data Sources (in priority order)
1. Input CSV (verified data provided)
2. Wikipedia (founding year, student count, type)
3. Official school website (about text, tagline, images)
4. Regex extraction from description field (fallback)

## Adding More Schools

Simply add rows to `data/schools_input.csv` and re-run `python main.py`.
The pipeline will only process schools not already in the output.

## Requirements

See `requirements.txt`:
```
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
openpyxl>=3.1.0
pandas>=2.0.0
```

## Logs

All activity is logged to `logs/pipeline.log` including:
- Successful scrapes
- HTTP errors and retries
- Missing data warnings
- Processing errors

## Notes

- The scraper uses polite delays (1–2s between requests)
- Retry logic: 3 attempts per URL with exponential backoff
- Bot detection: if a school's site blocks scraping, data falls back to Wikipedia or input CSV
- All generated content matches the Kidrovia template structure exactly
