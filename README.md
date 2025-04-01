# Param Extractor

## Overview
Param Extractor is a Burp Suite extension that extracts URLs with parameters from Burp history, making it easier to identify endpoints for fuzzing and security testing. It automatically collects GET, POST, and JSON parameters and formats them for use in security assessments.

## Features
- Extracts parameters from Burp history (GET, POST, JSON).
- Provides a dedicated Burp Suite tab.
- Supports exporting extracted URLs to a text file.
- Includes a right-click context menu for quick saving.
- Simple and user-friendly interface.

## Installation
1. Open **Burp Suite** and navigate to the **Extender** tab.
2. Click **Add** and select the `ParamExtractor.py` file.
3. Ensure **Python** is enabled in the **Burp Extender Options** (Jython required for Python extensions).
4. The extension will appear under the **Param Extractor** tab.

## Usage
1. Open the **Param Extractor** tab.
2. Click **Scan** to extract URLs with parameters from Burp's history.
3. Review the extracted data in the text area.
4. Use **Export to File** to save the results.
5. Click **Clear** to reset the output.

### Context Menu Option
- Right-click within Burp Suite and select **Copy to file** to quickly export results.

## Example Output
```
https://example.com/api/v1/resource?id=FUZZ&token=FUZZ
https://example.com/login?username=FUZZ&password=FUZZ
https://api.example.com/data?query=FUZZ
```

## License
This project is licensed under the MIT License.


 
