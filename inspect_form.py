import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.justice.gov/multimedia/Court%20Records/Bryant%20v.%20Indyke,%20No.%20119-cv-10479%20(S.D.N.Y.%202019)/001.pdf"

try:
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print("--- Forms found on page ---")
    for form in soup.find_all('form'):
        print(f"Action: {form.get('action')}")
        print(f"Method: {form.get('method')}")
        print("Inputs:")
        for inp in form.find_all('input'):
            print(f"  - Name: {inp.get('name')}, Value: {inp.get('value')}, Type: {inp.get('type')}")
        print("Buttons:")
        for btn in form.find_all('button'):
             print(f"  - Name: {btn.get('name')}, Text: {btn.get_text(strip=True)}")
    
    print("\n--- Page Text Snippet ---")
    print(soup.get_text()[:500])

except Exception as e:
    print(e)
