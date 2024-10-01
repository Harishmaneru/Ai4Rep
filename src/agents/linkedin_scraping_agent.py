import requests
import time
from ..config import PHANTOMBUSTER_LINKEDIN_API  

class LinkedInScrapingAgent:
    def __init__(self, post_url, session_cookie):
        self.post_url = post_url
        self.session_cookie = session_cookie
        self.phantombuster_api_url = PHANTOMBUSTER_LINKEDIN_API   

    def scrape_linkedin_data(self):
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "postUrl": self.post_url,
            "sessionCookie": self.session_cookie
        }


        response = requests.post(self.phantombuster_api_url, json=payload, headers=headers)

        if response.status_code == 200:
            # Wait for the agent to finish scraping
            time.sleep(50)  # Wait for Phantombuster to scrape the data
            
            return response.json()
        else:
            return {"error": f"Failed to scrape data. Status code: {response.status_code}"}
