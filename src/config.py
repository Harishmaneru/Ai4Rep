import os
from dotenv import load_dotenv

load_dotenv()

USER_ID = os.getenv('USER_ID')


# Phantombuster API base URL
PHANTOMBUSTER_API_BASE_URL = "https://videoresponse.onepgr.com:3001"

# LinkedIn Comments and Likes Scraping Endpoint
PHANTOMBUSTER_LINKEDIN_COMMENTS_LIKES_API = f"{PHANTOMBUSTER_API_BASE_URL}/LinkedInlikescomments"

# LinkedIn Profile Scraping Endpoint
PHANTOMBUSTER_LINKEDIN_PROFILE_API = f"{PHANTOMBUSTER_API_BASE_URL}//LinkedIncompanyurl"

# Sales Navigator Profile Scraping Endpoint
PHANTOMBUSTER_SALES_NAVIGATOR_PROFILE_API = f"{PHANTOMBUSTER_API_BASE_URL}/LinkedInprofileurl"

# Sales Navigator Emails Scraping Endpoint
PHANTOMBUSTER_SALES_NAVIGATOR_EMAILS_API = f"{PHANTOMBUSTER_API_BASE_URL}/LinkedInquerieURL"


FIND_PEOPLE_API = "https://crawl.onepgr.com:3002/search-people"
ENRICH_PEOPLE_API = "https://crawl.onepgr.com:3002/enrich-people"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
APOLLO_API_KEY = os.getenv('APOLLO_API_KEY')
LEADMAGIC_API_KEY = os.getenv('LEADMAGIC_API_KEY')
SKRAPP_API_KEY = os.getenv('SKRAPP_API_KEY')
SITE_API_KEYS = {
    'apollo': APOLLO_API_KEY,
    'leadmagic': LEADMAGIC_API_KEY,
    'skrapp': SKRAPP_API_KEY
}