# smard-data-extractor

A Python-based data extraction tool for German electricity market data from [SMARD.de](https://www.smard.de) (Strommarktdaten).

## Overview

This project automates the extraction of German electricity market data including consumption patterns, generation sources, CO₂ intensity metrics, and market pricing information. The tool leverages SMARD's backend API endpoints to efficiently gather comprehensive energy market data.

## Features

- **Net Electricity Consumption** - Extract Germany-wide consumption data (Netzlast)
- **Actual Generation Data** - Retrieve generation data by energy source (Tatsächliche Erzeugung)
- **CO₂ Intensity Tracking** - Monitor carbon intensity of electricity generation
- **Market Price Data** - Access electricity market pricing information
- **Automated Data Processing** - Batch download with configurable time ranges
- **Multiple Export Formats** - CSV output with structured data organization

## Data Sources

All data is sourced from **SMARD.de** - the official German electricity market data portal operated by the Federal Network Agency (Bundesnetzagentur).

### Available Data Categories
- Electricity consumption (Netzlast)
- Actual generation by source (Tatsächliche Erzeugung)
- CO₂ intensity (CO₂-Intensität) 
- Market prices (Marktpreise)
- Cross-border electricity trading
- Grid frequency and stability metrics

## Project Structure

```
smard-data-extractor/
├── README.md
├── requirements.txt
├── setup.py
├── src/
│   ├── __init__.py
│   ├── smard_client.py      # Main API client
│   ├── data_processor.py    # Data cleaning and transformation
│   ├── validators.py        # Data validation utilities
│   └── visualizations.py    # Plotting and analysis tools
├── data/
│   ├── raw/                 # Raw downloaded data
│   ├── processed/           # Cleaned and processed datasets
│   └── exports/             # Final CSV exports
├── config/
│   └── settings.yaml        # Configuration parameters
├── scripts/
│   ├── extract_generation.py   # Task 1: Generation data extraction
│   ├── api_discovery.py        # Task 2: API endpoint mapping
│   └── validate_data.py        # Data validation routines
├── tests/
│   ├── test_client.py
│   ├── test_processor.py
│   └── test_validators.py
└── docs/
    ├── api_endpoints.md     # Documented API patterns
    └── data_dictionary.md   # Field definitions and units
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/smard-data-extractor.git
cd smard-data-extractor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies
```
requests>=2.28.0
pandas>=1.5.0
numpy>=1.24.0
matplotlib>=3.6.0
seaborn>=0.12.0
pyyaml>=6.0
selenium>=4.0.0  # Optional: for complex scraping
beautifulsoup4>=4.11.0
pytest>=7.0.0  # For testing
```

## Usage

### Quick Start
```python
from src.smard_client import SMARDClient

# Initialize client
client = SMARDClient()

# Extract 2024 generation data
generation_data = client.get_generation_data(
    start_date="2024-01-01",
    end_date="2024-12-31",
    resolution="hourly",
    region="germany"
)

# Export to CSV
generation_data.to_csv("data/exports/actual_generation_2024.csv")
```

### Command Line Interface
```bash
# Extract generation data for 2024
python scripts/extract_generation.py --year 2024 --output data/exports/

# Discover and document API endpoints
python scripts/api_discovery.py --output docs/api_endpoints.md

# Validate downloaded data
python scripts/validate_data.py --input data/raw/ --reference entso-e
```

## Tasks & Implementation

### Task 1: Generation Data Extraction ✅
Extract hourly electricity generation data for all of 2024, organized by energy source.

**Implementation**: `scripts/extract_generation.py`
- Automated retrieval of Germany-wide hourly data
- Energy source classification (wind, solar, coal, nuclear, etc.)
- CSV export with standardized formatting
- Progress tracking and error handling

**Output**: `data/exports/actual_generation_2024.csv`

### Task 2: API Endpoint Discovery 🔧
Reverse-engineer SMARD's backend API through network analysis.

**Implementation**: `scripts/api_discovery.py`
- Browser automation for endpoint discovery
- XHR/JSON request pattern analysis  
- Payload structure documentation
- Authentication and rate limiting assessment

**Output**: `docs/api_endpoints.md`

### Task 3: Data Validation & Quality Assurance ⚡
Cross-reference extracted data with authoritative sources.

**Validation Sources**:
- ENTSO-E Transparency Platform
- Fraunhofer ISE Energy Charts
- Agora Energiewende data

**Metrics**:
- Unit consistency (MW, €/MWh, gCO₂/kWh)
- Temporal continuity checks
- Range validation and outlier detection
- Missing data identification and handling

## Data Output

### CSV Structure
All exported data follows a standardized format:
```csv
timestamp,energy_source,value_mw,data_type,region,quality_flag
2024-01-01T00:00:00Z,wind_onshore,15420.5,actual_generation,DE,validated
2024-01-01T00:00:00Z,solar,0.0,actual_generation,DE,validated
```

### Generated Visualizations
- Hourly generation mix stacked area charts
- CO₂ intensity heatmaps over time  
- Price volatility and correlation analysis
- Renewable energy penetration trends
- Seasonal consumption patterns

## Configuration

Edit `config/settings.yaml` to customize extraction parameters:

```yaml
extraction:
  default_resolution: "hourly"
  max_concurrent_requests: 10
  retry_attempts: 3
  timeout_seconds: 30

data_sources:
  smard_base_url: "https://www.smard.de"
  api_version: "v1"
  
validation:
  enable_cross_validation: true
  reference_sources: ["entso-e", "fraunhofer"]
  tolerance_percentage: 5.0

export:
  csv_encoding: "utf-8"
  date_format: "ISO8601"
  include_metadata: true
```

## API Documentation

### Discovered Endpoints

| Endpoint | Purpose | Parameters |
|----------|---------|------------|
| `/chart_data/{category}/{subcategory}` | Time series data | timestamp, resolution |
| `/download/{format}` | Bulk data export | date_range, filters |
| `/metadata/regions` | Available regions | - |
| `/metadata/categories` | Data categories | - |

For detailed API documentation, see `docs/api_endpoints.md`.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-extraction-method`)
3. Commit your changes (`git commit -am 'Add new extraction method'`)
4. Push to the branch (`git push origin feature/new-extraction-method`)
5. Create a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add unit tests for new functionality
- Update documentation for API changes
- Validate data quality before committing exports

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/test_client.py -v
pytest tests/test_validators.py -v

# Generate coverage report
pytest --cov=src tests/
```

## Data Quality & Reliability

### Known Limitations
- SMARD data may include preliminary values subject to revision
- Some historical data gaps exist, particularly for newer metrics
- API rate limiting may affect large bulk downloads
- CO₂ intensity calculations use grid-average methodologies

### Quality Assurance
- Automated data validation against multiple reference sources
- Statistical outlier detection and flagging
- Temporal continuity verification
- Unit conversion accuracy checks

## License

MIT License - see `LICENSE` file for details.

## Acknowledgments

- **Bundesnetzagentur** for providing SMARD.de data portal
- **ENTSO-E** for transparency platform reference data
- **Fraunhofer ISE** for Energy Charts validation data

## Support

For questions, issues, or contributions:
- Create an issue in the GitHub repository
- Email: [your-email@domain.com]
- Documentation: See `docs/` directory

---

**Note**: This project is for educational and research purposes. Please respect SMARD.de's terms of service and implement appropriate rate limiting when accessing their services.
