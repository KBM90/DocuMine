# DocuMine ⛏️
**The Intelligent PDF Harvester**

A Python script that extracts all PDF file links from a given URL and optionally downloads them to your local machine.

## Features

- 🔍 **Extract PDF Links**: Automatically finds all PDF links on a webpage
- 💾 **Save Links**: Export the list of PDF links to a text file
- ⬇️ **Download PDFs**: Bulk download all PDF files to a specified directory
- 📊 **Progress Tracking**: Real-time download progress with success/failure indicators
- 🔄 **Duplicate Handling**: Automatically handles duplicate filenames
- ⚡ **Error Handling**: Robust error handling for network issues and invalid URLs

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Method 1: Web Application (Recommended)
This launches a user-friendly interface in your browser.
```bash
streamlit run app.py
```

### Method 2: Command Line Interface
```bash
# Interactive mode
python pdf_extractor.py

# Direct URL mode
python pdf_extractor.py https://www.justice.gov/epstein/court-records
```

## Workflow

1. **Enter URL**: Provide the webpage URL containing PDF files
2. **View Results**: The script displays all found PDF files with their URLs
3. **Save Links** (Optional): Choose to save the list of links to a text file
4. **Download PDFs** (Optional): Choose to download all PDF files to a directory

## Example Output

```
Fetching content from: https://www.justice.gov/epstein/court-records

================================================================================
Found 1234 PDF file(s):
================================================================================

1. 001.pdf
   Filename: 001.pdf
   URL: https://www.justice.gov/multimedia/Court%20Records/...

...

Do you want to save these links to a file? (y/n): y
Enter output filename (default: pdf_links.txt): my_pdfs.txt

PDF links saved to: my_pdfs.txt

Do you want to download all PDF files? (y/n): y
Enter download directory (default: downloaded_pdfs): my_downloads

================================================================================
Downloading 1234 PDF file(s) to 'my_downloads'...
================================================================================

[1/1234] Downloading: 001.pdf... ✓ Success (245,678 bytes)
[2/1234] Downloading: 002.pdf... ✓ Success (189,432 bytes)
...

================================================================================
Download Summary:
  Successful: 1230
  Failed: 4
  Total: 1234
================================================================================
```

## Requirements

- Python 3.6+
- requests
- beautifulsoup4

## Error Handling

The script handles various error scenarios:
- Invalid URLs
- Network connection issues
- Missing or inaccessible PDF files
- File system errors
- Duplicate filenames (automatically renamed)

## Notes

- Downloaded files are saved with their original filenames
- If a file with the same name exists, it will be renamed with a counter (e.g., `file_1.pdf`, `file_2.pdf`)
- The script uses streaming downloads for efficient memory usage with large files
- A user-agent header is included to ensure compatibility with most websites
