import requests

url = "https://www.justice.gov/multimedia/Court%20Records/Bryant%20v.%20Indyke,%20No.%20119-cv-10479%20(S.D.N.Y.%202019)/001.pdf"

print(f"Testing URL: {url}")

try:
    response = requests.get(url, timeout=15, verify=False)
    print(f"Status Code: {response.status_code}")
    print(f"Content Type: {response.headers.get('Content-Type')}")
    print(f"Redirect History: {response.history}")
    
    if 'text/html' in response.headers.get('Content-Type', ''):
        print("\n--- Response Content Preview (First 500 chars) ---")
        print(response.text[:500])
        print("--------------------------------------------------")
        
        # Check for keywords
        if "robot" in response.text.lower():
            print("FOUND: 'robot' keyword in response")
        if "age" in response.text.lower():
            print("FOUND: 'age' keyword in response")
        if "challenge" in response.text.lower():
            print("FOUND: 'challenge' keyword in response")

except Exception as e:
    print(f"Error: {e}")
