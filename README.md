# SMARD Data Extractor

A Python tool for extracting and processing energy market data from the German SMARD (Strommarktdaten) platform.

## Overview

The SMARD Data Extractor allows you to programmatically download and consolidate energy market data from Germany's official electricity market data platform. The tool fetches multiple data streams including renewable energy generation, consumption, and pricing data, then merges them into a unified dataset.

## Features

- **Multi-source Data Extraction**: Downloads data from multiple SMARD modules simultaneously
- **Automatic Data Merging**: Combines different energy data streams into a single CSV file
- **Flexible Time Ranges**: Configurable date ranges for data extraction
- **Clean Data Output**: Properly formatted CSV files with German localization support
- **Error Handling**: Robust error handling for API requests and data processing

## Supported Data Types

The extractor currently supports the following SMARD data modules:

| Data Type | Module ID | Description |
|-----------|-----------|-------------|
| Wind Onshore | 1004067 | Onshore wind power generation [MW] |
| Photovoltaik | 1004068 | Solar photovoltaic generation [MW] |
| Erdgas | 1004071 | Natural gas power generation [MW] |
| Verbrauch | 5000410 | Total electricity consumption [MW] |
| Pricing | 8004169 | Germany/Luxembourg electricity prices [€/MWh] |

## Installation

### Prerequisites

- Python 3.7 or higher
- Required Python packages:

```bash
pip install requests pandas
```

### Clone the Repository

```bash
git clone https://github.com/hakimdalim/smard-data-extractor.git
cd smard-data-extractor
```

## Usage

### Basic Usage

Run the script to extract data for the predefined time period (July 2024 - July 2025):

```bash
python smard_data_extractor.py
```

### Customizing Time Range

Modify the time range variables in the script:

```python
# Set your desired time range
dt_from = datetime(2024, 7, 1, 0, 0)  # Start date
dt_to = datetime(2025, 7, 1)          # End date
```

### Adding New Data Modules

To include additional SMARD data modules, add them to the `module_map` dictionary:

```python
module_map = {
    1004067: "Wind Onshore [MW]",
    1004068: "Photovoltaik [MW]",
    # Add new modules here
    NEW_MODULE_ID: "Description [Unit]"
}
```

## Output

The script generates a CSV file named `juli24-25_energie_zusammengefasst_mit_aufloesung.csv` containing:

- **Datum von** / **Datum bis**: Time period columns
- **Data columns**: One column for each requested data type with values in MW or €/MWh
- **Hourly resolution**: Data points for each hour in the specified time range

### Sample Output Structure

```csv
Datum von;Datum bis;Wind Onshore [MW];Photovoltaik [MW];Erdgas [MW];Verbrauch [MW];Deutschland/Luxemburg [€/MWh]
01.07.2024 00:00;01.07.2024 01:00;12450.5;0;8920.3;45234.1;89.42
01.07.2024 01:00;01.07.2024 02:00;11890.2;0;9150.7;42891.5;78.31
...
```

## API Information

This tool uses the official SMARD API endpoint:
- **Base URL**: `https://www.smard.de/nip-download-manager/nip/download/market-data`
- **Parameter Dictionaries**: `https://www.smard.de/en/user-guide`
- **Parameter IDs**: `https://smard.api.bund.dev/`
- **Data Format**: CSV with semicolon separation
- **Resolution**: Hourly data
- **Region**: Germany (DE)

## Error Handling

The script includes error handling for:
- Network connection issues
- Invalid API responses
- Missing or malformed data
- File writing permissions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Data provided by [SMARD.de](https://www.smard.de/) - the official German electricity market data platform
- Built for researchers, analysts, and developers working with German energy market data

## Disclaimer

This tool is not officially affiliated with SMARD or the German Federal Network Agency. Please ensure compliance with SMARD's terms of service when using their API.

## Contact

Project Link: [https://github.com/hakimdalim/smard-data-extractor](https://github.com/hakimdalim/smard-data-extractor)

---

**Note**: Make sure to respect the SMARD API rate limits and terms of service when using this tool for automated data extraction.