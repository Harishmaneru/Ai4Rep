import requests
import json
from ..config import LINKEDIN_SCRAPING_API, USER_ID

def scrape_linkedin(post_url, session_cookie):
    headers = {
        # "user-id": USER_ID,
        "Content-Type": "application/json"
    }
    
    # Print the URL and session cookie for debugging purposes
    print("Post URL:", post_url)
    print("Session Cookie:", session_cookie)
    
    payload = {
        "postUrl": post_url,
        "sessionCookie": session_cookie
    }
    
    # Make the request to the Phantombuster API
    response = requests.post(LINKEDIN_SCRAPING_API, json=payload, headers=headers)
    
    # Print the full response for debugging
    print("Full Response:")
    print(f"Status Code: {response.status_code}")
    print("Headers:", response.headers)
    print("Text:", response.text)
    
    if response.status_code == 200:
        response_json = response.json()
        # Print the JSON response for debugging
        print("JSON Response:", json.dumps(response_json, indent=2))
        return response_json
    else:
        raise Exception(f"Failed to scrape LinkedIn post: {response.text}")
