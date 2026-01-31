
import requests

TARGET_PDF = "https://www.justice.gov/epstein/files/DataSet%2010/EFTA01381975.pdf"
HEADERS = {
    'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'
}

try:
    print(f"Testing access to: {TARGET_PDF} as Googlebot...")
    response = requests.get(TARGET_PDF, headers=HEADERS, timeout=10, allow_redirects=False)
    
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type', '').lower()
        if 'application/pdf' in content_type:
            print("SUCCESS! Googlebot bypass works.")
        else:
            print(f"Failed. Content-Type is {content_type}")
    elif response.status_code in [301, 302]:
        print(f"Redirected to: {response.headers.get('Location')}")
    else:
        print("Failed.")

except Exception as e:
    print(f"Error: {e}")
