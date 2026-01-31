"""
DocuMine - PDF Link Extractor and Downloader
This script extracts all PDF file links from a given URL and optionally downloads them.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys
import os
from pathlib import Path


def extract_pdf_links(url):
    """
    Extract all PDF links from a given URL.
    
    Args:
        url (str): The URL to scrape for PDF links
        
    Returns:
        list: A list of dictionaries containing PDF information (filename and URL)
    """
    try:
        # Send GET request to the URL
        print(f"Fetching content from: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all anchor tags
        all_links = soup.find_all('a', href=True)
        
        # Filter PDF links
        pdf_links = []
        for link in all_links:
            href = link['href']
            
            # Check if the link ends with .pdf (case-insensitive)
            if href.lower().endswith('.pdf'):
                # Convert relative URLs to absolute URLs
                absolute_url = urljoin(url, href)
                
                # Extract filename from URL
                filename = href.split('/')[-1]
                
                # Get link text if available
                link_text = link.get_text(strip=True)
                
                pdf_links.append({
                    'filename': filename,
                    'url': absolute_url,
                    'text': link_text if link_text else filename
                })
        
        return pdf_links
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def display_pdf_links(pdf_links):
    """
    Display the extracted PDF links in a formatted way.
    
    Args:
        pdf_links (list): List of dictionaries containing PDF information
    """
    if not pdf_links:
        print("\nNo PDF files found on this page.")
        return
    
    print(f"\n{'='*80}")
    print(f"Found {len(pdf_links)} PDF file(s):")
    print(f"{'='*80}\n")
    
    for idx, pdf in enumerate(pdf_links, 1):
        print(f"{idx}. {pdf['text']}")
        print(f"   Filename: {pdf['filename']}")
        print(f"   URL: {pdf['url']}")
        print()


def save_to_file(pdf_links, output_file='pdf_links.txt'):
    """
    Save the PDF links to a text file.
    
    Args:
        pdf_links (list): List of dictionaries containing PDF information
        output_file (str): Output filename
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Total PDF files found: {len(pdf_links)}\n")
            f.write("="*80 + "\n\n")
            
            for idx, pdf in enumerate(pdf_links, 1):
                f.write(f"{idx}. {pdf['text']}\n")
                f.write(f"   Filename: {pdf['filename']}\n")
                f.write(f"   URL: {pdf['url']}\n\n")
        
        print(f"\nPDF links saved to: {output_file}")
        
    except Exception as e:
        print(f"Error saving to file: {e}")


def download_pdfs(pdf_links, download_dir='downloaded_pdfs'):
    """
    Download all PDF files to a specified directory.
    
    Args:
        pdf_links (list): List of dictionaries containing PDF information
        download_dir (str): Directory to save downloaded PDFs
    """
    if not pdf_links:
        print("No PDFs to download.")
        return
    
    # Create download directory if it doesn't exist
    Path(download_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*80}")
    print(f"Downloading {len(pdf_links)} PDF file(s) to '{download_dir}'...")
    print(f"{'='*80}\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    successful_downloads = 0
    failed_downloads = 0
    
    for idx, pdf in enumerate(pdf_links, 1):
        try:
            print(f"[{idx}/{len(pdf_links)}] Downloading: {pdf['filename']}...", end=' ')
            
            # Download the PDF
            response = requests.get(pdf['url'], headers=headers, timeout=60, stream=True)
            response.raise_for_status()
            
            # Save to file
            file_path = os.path.join(download_dir, pdf['filename'])
            
            # Handle duplicate filenames
            counter = 1
            original_path = file_path
            while os.path.exists(file_path):
                name, ext = os.path.splitext(original_path)
                file_path = f"{name}_{counter}{ext}"
                counter += 1
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = os.path.getsize(file_path)
            print(f"✓ Success ({file_size:,} bytes)")
            successful_downloads += 1
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed - {str(e)}")
            failed_downloads += 1
        except Exception as e:
            print(f"✗ Failed - {str(e)}")
            failed_downloads += 1
    
    print(f"\n{'='*80}")
    print(f"Download Summary:")
    print(f"  Successful: {successful_downloads}")
    print(f"  Failed: {failed_downloads}")
    print(f"  Total: {len(pdf_links)}")
    print(f"{'='*80}\n")


def main():
    """Main function to run the PDF extractor."""
    
    # Check if URL is provided as command line argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # Prompt user for URL
        url = input("Enter the URL to extract PDF links from: ").strip()
    
    if not url:
        print("Error: No URL provided.")
        return
    
    # Validate URL format
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print("Error: Invalid URL format. Please include http:// or https://")
        return
    
    # Extract PDF links
    pdf_links = extract_pdf_links(url)
    
    # Display results
    display_pdf_links(pdf_links)
    
    if not pdf_links:
        return
    
    # Ask if user wants to save links to file
    save_choice = input("\nDo you want to save these links to a file? (y/n): ").strip().lower()
    if save_choice == 'y':
        filename = input("Enter output filename (default: pdf_links.txt): ").strip()
        if not filename:
            filename = 'pdf_links.txt'
        save_to_file(pdf_links, filename)
    
    # Ask if user wants to download the PDFs
    download_choice = input("\nDo you want to download all PDF files? (y/n): ").strip().lower()
    if download_choice == 'y':
        download_dir = input("Enter download directory (default: downloaded_pdfs): ").strip()
        if not download_dir:
            download_dir = 'downloaded_pdfs'
        download_pdfs(pdf_links, download_dir)


if __name__ == "__main__":
    main()
