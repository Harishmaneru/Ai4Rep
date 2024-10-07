from langchain.tools import Tool
from ..api.find_people_api import find_people
from ..api.enrich_people_api import enrich_people
from ..api.linkedin_scraping_api import scrape_linkedin   
import json

def find_people_api(criteria_json: str) -> str:
    """Use this tool to find people based on given criteria."""
    criteria_dict = json.loads(criteria_json)
    result = find_people(criteria_dict)
    return json.dumps(result)

find_people_tool = Tool(
    name="Find People",
    func=find_people_api,
    description="Use this to find people based on given criteria. Input should be a JSON string with the following keys: domains, page, perPage, locations, seniorities, employeeRanges, titles."
)

def enrich_people_api(input_str: str) -> str:
    """Use this tool to enrich people data"""
    try:
        print(f"Received input: {input_str}")  # Debug print
        
        input_dict = json.loads(input_str)
        action_input = json.loads(input_dict['action_input'])
        
        print(f"Parsed action_input: {action_input}") # Debug print
        
        result = enrich_people(
            people_data=action_input['people'],
            enrich_type=action_input['enrich_type']
        )
        return json.dumps(result)
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON input. Details: {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error occurred. Details: {str(e)}"

enrich_people_tool = Tool(
    name="Enrich People",
    func=enrich_people_api,
    description="Use this to enrich people data with email and phone information. Input should be a JSON string with 'action_input' containing another JSON string with 'people' (list of people data) and 'enrich_type'."
)


# Adding the LinkedIn scraper function
def scrape_linkedin_api(input_str: str) -> str:
    """Use this tool to scrape LinkedIn post data (comments and likes)"""
    try:
        print(f"Received input: {input_str}")  # Debug print

        input_dict = json.loads(input_str)
        post_url = input_dict.get('postUrl')
        session_cookie = input_dict.get('sessionCookie')

        if not post_url or not session_cookie:
            return "Error: Missing 'postUrl' or 'sessionCookie'."

        # Call the LinkedIn scraping API function
        result = scrape_linkedin(post_url, session_cookie)

        print(f"Scraping result: {result}")  # Debug print
        return json.dumps(result)
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON input. Details: {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error occurred. Details: {str(e)}"

# Tool for LinkedIn Scraping
linkedin_scraper_tool = Tool(
    name="LinkedIn Scraper",
    func=scrape_linkedin_api,
    description="Use this tool to scrape LinkedIn post data (comments and likes). Input should be a JSON string with 'postUrl' and 'sessionCookie'."
)