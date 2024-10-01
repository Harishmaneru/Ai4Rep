import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.agents.find_people_agent import FindPeopleAgent
from src.agents.enrich_people_agent import EnrichPeopleAgent
from src.agents.linkedin_scraping_agent import LinkedInScrapingAgent
import re
from fuzzywuzzy import fuzz
import ssl


app = Flask(__name__)

allowed_origins = [
    "http://localhost:3000",
    "https://sales.onepgr.com",
    "https://auto-sdr.com",
    "http://127.0.0.1:3000",
    # Add more domains as needed
]

# CORS(app, supports_credentials=True)
CORS(app, resources={r"/api/*": {"origins": allowed_origins}}, supports_credentials=True)
#CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
#CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "https://sales.onepgr.com","https://auto-sdr.com"]}}, supports_credentials=True)
logging.basicConfig(level=logging.DEBUG)

# Initialize agents
app.find_people_agent = FindPeopleAgent()
app.enrich_people_agent = EnrichPeopleAgent()
app.linkedin_scraping_agent = LinkedInScrapingAgent()


# Define intents and keywords
intents_and_keywords = [
    {
        "intent": "find_people",
        "keywords": ["find", "search", "look for", "discover", "locate", "give details of"],
        "patterns": [
            r"find .+ (working|in|at) .+",
            r"search .+ (working|in|at) .+",
            r"give .+ details of .+ (working|in|at) .+",
        ],
    },
    {
        "intent": "enrich_people",
        "keywords": ["enrich", "find email", "find phone", "get contact", "additional info"],
        "patterns": [
            r"enrich .+ with .+",
            r"find (email|phone|contact) for .+",
            r"get (email|phone|contact) of .+",
        ],
    },

# -------------intents_and_keywords for LinkedIn Tasks ------------------------------------------------------------------ 
 {
        "intent": "linkedin_scrape_comments_likes",
        "keywords": ["scrape LinkedIn comments", "get LinkedIn likes", "LinkedIn comments", "LinkedIn likes"],
        "patterns": [
            r"scrape LinkedIn comments from https:\/\/www\.linkedin\.com\/in\/\w+\/?",
            r"get LinkedIn likes for https:\/\/www\.linkedin\.com\/posts\/\w+",
            r"scrape LinkedIn post https:\/\/www\.linkedin\.com\/posts\/\w+",
        ],
    },
    {
        "intent": "linkedin_scrape_profile",
        "keywords": ["scrape LinkedIn profile", "get LinkedIn profile data"],
        "patterns": [
            r"scrape LinkedIn profile of https:\/\/www\.linkedin\.com\/in\/\w+\/?",
            r"get LinkedIn profile for https:\/\/www\.linkedin\.com\/in\/\w+\/?",
        ],
    },
    {
        "intent": "sales_navigator_profile",
        "keywords": ["scrape Sales Navigator profile", "get Sales Navigator profile"],
        "patterns": [
            r"scrape Sales Navigator profile for https:\/\/www\.linkedin\.com\/sales\/people\/\w+",
            r"get Sales Navigator profile of https:\/\/www\.linkedin\.com\/sales\/people\/\w+",
        ],
    },
    {
        "intent": "sales_navigator_emails",
        "keywords": ["scrape emails from Sales Navigator", "get Sales Navigator emails"],
        "patterns": [
            r"scrape emails from Sales Navigator https:\/\/www\.linkedin\.com\/sales\/search\/people\?query=.+",
            r"get emails from Sales Navigator search https:\/\/www\.linkedin\.com\/sales\/search\/people\?query=.+",
        ],
    },
]

def match_intent_pattern(input_text):
    input_lower = input_text.lower()
    for intent in intents_and_keywords:
        for pattern in intent["patterns"]:
            if re.search(pattern, input_lower):
                return intent["intent"]
    return None

def find_most_similar_intent(input_text):
    input_lower = input_text.lower()
    max_score = 0
    best_intent = None
    for intent in intents_and_keywords:
        for keyword in intent["keywords"]:
            score = fuzz.partial_ratio(keyword, input_lower)
            if score > max_score:
                max_score = score
                best_intent = intent["intent"]
    return best_intent if max_score > 70 else None

# def determine_agent_type(prompt):
#     # Try to match intent based on patterns
#     intent = match_intent_pattern(prompt)
    
#     # If no pattern match, use fuzzy matching
#     if not intent:
#         intent = find_most_similar_intent(prompt)
    
#     if intent == "find_people":
#         return "find"
#     elif intent == "enrich_people":
#         return "enrich"
#     elif intent == "linkedin_scrape":
#         return "linkedin_scrape"
#     else:
#         return "unknown"

def determine_agent_type(prompt):
    # Attempt to find a direct match with the defined patterns
    intent = match_intent_pattern(prompt)
    
    # If no direct match, attempt fuzzy matching
    if not intent:
        intent = find_most_similar_intent(prompt)
    
    # Return the detected intent directly or 'unknown' if no intent is matched
    return intent if intent else "unknown"


@app.route('/api/process', methods=['POST', 'OPTIONS'])
def process_request():
    if request.method == 'OPTIONS':
        return '', 204

    data = request.json
    app.logger.debug(f"Received data: {data}")
    
    prompt = data.get('prompt')
    params = data.get('params')
    
    app.logger.debug(f"Extracted prompt: {prompt}")
    app.logger.debug(f"Extracted params: {params}")
    
    if not prompt:
        app.logger.error(f"Missing prompt. Received data: {data}")
        return jsonify({"success": False, "error": "Missing prompt"}), 400
    
    if not params:
        app.logger.error(f"Missing params. Received data: {data}")
        return jsonify({"success": False, "error": "Missing params"}), 400
    
        # Initialize variables to avoid UnboundLocalError
    post_url = params.get('postUrl', '')  # Initialize to empty string if not present
    profile_url = params.get('profileUrl', '')  # Initialize to empty string if not present
    session_cookie = params.get('sessionCookie', '')  # Initialize to empty string if not present
    querieURL = params.get('querieUrl', '')  # Initialize to empty string if not present

    agent_type = determine_agent_type(prompt)

    try:
        agent_type = determine_agent_type(prompt)
        app.logger.debug(f"Determined agent type: {agent_type}")

        if agent_type == "find":
            # Find people
            found_people = app.find_people_agent.find_people(params)
            app.logger.debug(f"Found people: {found_people}")
            result = {'found_people': found_people}
        
        elif agent_type == "enrich":
            # Enrich people
            enrich_type = params.get('enrich_type', 'both')
            people_to_enrich = params.get('people', [])
            
            if not people_to_enrich:
                raise ValueError("No people data provided for enrichment")
            
            enriched_people = app.enrich_people_agent.enrich_people({
                'people': people_to_enrich,
                'enrich_type': enrich_type
            })
            app.logger.debug(f"Enriched people: {enriched_people}")
            result = {'enriched_people': enriched_people}
# -------------LinkedIn Scraping ------------------------------------------------------------------  
        elif agent_type in ["linkedin_scrape_comments_likes", "linkedin_scrape_profile", "sales_navigator_profile", "sales_navigator_emails"]:
            if 'postUrl' in params:
                post_url = params['postUrl']
            if 'profileUrl' in params:
                profile_url = params['profileUrl']
            session_cookie = params.get('sessionCookie', '')
            if agent_type == "linkedin_scrape_comments_likes":
                result = app.linkedin_scraping_agent.scrape_linkedin_comments_likes(post_url, session_cookie)
            elif agent_type == "linkedin_scrape_profile":
                result = app.linkedin_scraping_agent.scrape_linkedin_profile(profile_url, session_cookie)
            elif agent_type == "sales_navigator_profile":
                result = app.linkedin_scraping_agent.scrape_sales_navigator_profile(profile_url, session_cookie)
            elif agent_type == "sales_navigator_emails":
                querieUrl = params.get('querieUrl')  # Use querieUrl consistently
            if querieUrl is None:
              app.logger.error("Missing querieUrl in params")
              return jsonify({"success": False, "error": "Missing querieUrl parameter"}), 400
            app.logger.debug(f"Scraping Sales Navigator emails with querieUrl: {querieUrl}")
            result = app.linkedin_scraping_agent.scrape_sales_navigator_emails(querieUrl, session_cookie)
        else:
            return jsonify({"success": False, "error": "Invalid or unrecognized intent"}), 400

        return jsonify({"success": True, "data": result})

    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 400
@app.route('/api/sample', methods=['POST'])
def sample_connection():
    return jsonify({"message": "Sample backend connection successful"})

@app.route('/api/test', methods=['POST'])
def test_connection():
    return jsonify({"message": "Backend connection successful"})

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Origin'] = 'https://sales.onepgr.com'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# if __name__ == "__main__":
#     ssl_context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
#     ssl_context.load_cert_chain(
#         certfile='/home/ubuntu/ssl_certs/fullchain.pem', 
#         keyfile='/home/ubuntu/ssl_certs/onepgr.com.key'
#     )
    
    # app.run(host='0.0.0.0', port=443, ssl_context=ssl_context, debug=True)
    # app.run(host='127.0.0.1', port=5001, debug=True)
app.run(host='127.0.0.1', port=5001, debug=False)
