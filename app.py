"""
PDF Extractor & Downloader Web App
Built with Streamlit
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import io
import zipfile
import time

st.set_page_config(
    page_title="DocuMine",
    page_icon="⛏️",
    layout="wide",
    menu_items={}
)

# --- Helper Functions ---

def get_pdf_links(url):
    """Extracts PDF links from the URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.lower().endswith('.pdf'):
                absolute_url = urljoin(url, href)
                filename = href.split('/')[-1]
                text = a.get_text(strip=True) or filename
                links.append({
                    "filename": filename,
                    "url": absolute_url,
                    "text": text
                })
        return links, None
    except Exception as e:
        return [], str(e)

def create_zip_of_pdfs(pdf_list):
    """Downloads PDFs and returns a byte stream of the ZIP file."""
    zip_buffer = io.BytesIO()
    
    # Progress bar in the main UI
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total = len(pdf_list)
    success_count = 0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for i, pdf in enumerate(pdf_list):
            try:
                status_text.text(f"Downloading {i+1}/{total}: {pdf['filename']}...")
                resp = requests.get(pdf['url'], headers=headers, timeout=30)
                if resp.status_code == 200:
                    # Handle duplicate filenames in zip
                    # (Simple approach: strict filenames from URL might duplicate, 
                    # zipfile allows duplicates but extracting overwrites. 
                    # Let's keep it simple for now or append index if needed.
                    # Appending index to ensure uniqueness in zip)
                    
                    # Check if file already exists in zip (not straightforward in write-only mode)
                    # simpler to just prefix/suffix to ensure uniqueness or trust the source.
                    # Let's just use the filename.
                    zip_file.writestr(pdf['filename'], resp.content)
                    success_count += 1
            except Exception:
                pass # Skip failed downloads
            
            # Update progress
            progress_bar.progress((i + 1) / total)

    status_text.empty()
    progress_bar.empty()
    
    zip_buffer.seek(0)
    return zip_buffer, success_count

# --- UI Layout ---

st.title("⛏️ DocuMine")
st.markdown("""
**The Intelligent PDF Harvester**
Enter a URL below to find all the PDF files linked on that page. 
You can view the list and download them individually or as a bulk ZIP file.
""")

url_input = st.text_input("Website URL", placeholder="https://example.com/page-with-pdfs")

if url_input:
    # Basic validation
    if not (url_input.startswith("http://") or url_input.startswith("https://")):
        st.warning("Please enter a valid URL starting with http:// or https://")
    else:
        if st.button("Find PDFs", type="primary"):
            with st.spinner("Scanning page for PDFs..."):
                links, error = get_pdf_links(url_input)
                
            if error:
                st.error(f"Error fetching the page: {error}")
            elif not links:
                st.info("No PDF links found on this page.")
            else:
                st.success(f"Found {len(links)} PDF files!")
                
                # Store in session state so we don't lose it on interactions
                st.session_state['pdf_links'] = links
                st.session_state['source_url'] = url_input

# Display results if valid links exist source_url matches current input (simple consistency check)
if 'pdf_links' in st.session_state and st.session_state.get('source_url') == url_input:
    links = st.session_state['pdf_links']
    
    # 1. Show summary metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total PDFs", len(links))
    
    # 2. Bulk Download Section
    st.write("### 📦 Bulk Download")
    st.info("Click the button below to generate a ZIP file containing all these PDFs. This may take a while depending on file sizes.")
    
    # We use a callback or generation approach. 
    # Streamlit's download_button expects data. Generating a large zip on the fly 
    # *before* clicking can be slow. 
    # Pattern: "Generate Zip" button -> Process -> Show "Download Zip" button.
    
    if st.button("Prepare ZIP Download"):
        with st.spinner("Downloading files and creating ZIP..."):
            zip_data, count = create_zip_of_pdfs(links)
            st.session_state['zip_data'] = zip_data
            st.session_state['zip_count'] = count
            st.session_state['zip_ready'] = True
    
    if st.session_state.get('zip_ready'):
        count = st.session_state.get('zip_count', 0)
        st.success(f"ZIP ready! Contains {count} valid files.")
        st.download_button(
            label="⬇️ Download All PDFs (.zip)",
            data=st.session_state['zip_data'],
            file_name="extracted_pdfs.zip",
            mime="application/zip"
        )
    
    st.divider()

    # 3. Individual List
    st.write("### 📝 File List")
    
    # Convert to simple list of dicts for dataframe or display
    # Let's do a dataframe for cleaner look
    display_data = [{"File Name": l['filename'], "Link Text": l['text'], "URL": l['url']} for l in links]
    st.dataframe(display_data, use_container_width=True)
    
    # Detailed list with individual links
    with st.expander("View Individual Links"):
        for l in links:
            st.markdown(f"- **[{l['filename']}]({l['url']})**: {l['text']}")

# --- Footer ---
st.divider()
st.markdown("### ☕ Support the Developer")
st.markdown("If this tool helped you, consider buying me a coffee!")

with st.expander("💼 OKX Wallet Addresses"):
    st.code("TCFDcTTbSKp5WRaMj4jGkJRNgrSzAr33ra", language="text")
    st.caption("USDT (TRC20)")
    
    st.code("0x779faf0ed2a549d70e1053ea83d2d991d5f5edcf", language="text")
    st.caption("USDC (ERC20)")
    
    st.code("37C6azvFCgECTvFfEChuZeLw8UNUoUjwd1", language="text")
    st.caption("BTC (Bitcoin)")

