
import requests
import time

TARGET_PDF = "https://www.justice.gov/epstein/files/DataSet%2010/EFTA01381975.pdf"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

CANDIDATE_COOKIES = [
    {"age_verified": "1"},
    {"age_verified": "true"},
    {"age_gate": "1"},
    {"age_gate": "true"},
    {"doj_age_verified": "1"},
    {"doj-age-verified": "1"},
    {"agreed": "1"},
    {"agreed": "true"},
    {"legal_age": "yes"},
    {"is_adult": "1"},
    {"confirm_age": "1"},
    {"site_disclaimer": "1"},
    # Generic Drupal/PHP ones
    {"has_js": "1"},
]

def check_cookie(cookie_dict):
    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        # First visit the age verify page to get any session cookies
        session.get("https://www.justice.gov/age-verify", timeout=10)
        
        # Now add our candidate cookie
        session.cookies.update(cookie_dict)
        
        print(f"Testing cookie: {cookie_dict}...", end="", flush=True)
        response = session.get(TARGET_PDF, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '').lower()
            if 'application/pdf' in content_type or response.content.startswith(b'%PDF'):
                print(" SUCCESS!")
                return True
            else:
                print(f" Failed (Content-Type: {content_type})")
        else:
            print(f" Failed (Status: {response.status_code})")
            
    except Exception as e:
        print(f" Error: {e}")
    return False

if __name__ == "__main__":
    print(f"Testing access to: {TARGET_PDF}")
    found = False
    
    # Test without cookies first
    print("Testing NO cookies...", end="")
    if check_cookie({}):
        print("Wait, no cookies needed? Weird.")
        found = True
    
    if not found:
        for cookie in CANDIDATE_COOKIES:
            if check_cookie(cookie):
                print(f"\nFOUND WORKING COOKIE: {cookie}")
                found = True
                break
    
    if not found:
        print("\nCould not find a working cookie from the candidate list.")
