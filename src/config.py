import os
from dotenv import load_dotenv

load_dotenv()

USER_ID = os.getenv('USER_ID')

LINKEDIN_SCRAPING_API = "https://videoresponse.onepgr.com:3001/LinkedInlikescomments"


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