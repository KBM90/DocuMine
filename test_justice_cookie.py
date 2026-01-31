
import requests

TARGET_PDF = "https://www.justice.gov/epstein/files/DataSet%2010/EFTA01381975.pdf"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

CANDIDATE_VALUES = ["true", "1", "yes", "verified"]

def test_cookie(name, value):
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        cookies = {name: value}
        print(f"Testing {name}={value}...", end="")
        
        response = session.get(TARGET_PDF, cookies=cookies, timeout=10, allow_redirects=False)
        
        if response.status_code == 200:
             content_type = response.headers.get('Content-Type', '').lower()
             if 'application/pdf' in content_type:
                 print(" SUCCESS! (PDF Content)")
                 return True
             else:
                 print(f" Failed (200 OK but type is {content_type})")
        elif response.status_code in [301, 302]:
            print(f" Redirected to {response.headers.get('Location')}")
        else:
            print(f" Status {response.status_code}")
            
    except Exception as e:
        print(f" Error: {e}")
    return False

if __name__ == "__main__":
    print(f"Target: {TARGET_PDF}")
    
    # Test justiceGovAgeVerified
    found = False
    for val in CANDIDATE_VALUES:
        if test_cookie("justiceGovAgeVerified", val):
             found = True
             break
    
    if not found:
        print("\njusticeGovAgeVerified alone did not work. Likely need the Queue-IT cookie too.")
