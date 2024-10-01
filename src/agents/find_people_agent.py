# import os
# from dotenv import load_dotenv
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# from src.api.find_people_api import find_people
# from ..config import OPENAI_API_KEY

# # Load environment variables
# load_dotenv()

# class FindPeopleAgent:
#     def __init__(self):
#         self.llm = OpenAI(temperature=0, api_key=OPENAI_API_KEY)
#         self.domain_chain = self._setup_domain_chain()

#     def _setup_domain_chain(self):
#         prompt_template = """Given the company name: {company_name}
#         What is the most likely domain (website URL) for this company?
#         Provide only the domain name, without 'http://' or 'www.'.
#         If unsure, respond with 'unknown'.
#         Domain:"""
        
#         prompt = PromptTemplate(
#             input_variables=["company_name"],
#             template=prompt_template
#         )
#         return LLMChain(llm=self.llm, prompt=prompt)

#     def _get_domain(self, company_name):
#         response = self.domain_chain.run(company_name=company_name)
#         return response.strip().lower()

#     def find_people(self, params):
#         # Extract company names and find their domains
#         companies = params.get("company", "").split(',')
#         domains = []
#         for company in companies:
#             company = company.strip()
#             if company:
#                 domain = self._get_domain(company)
#                 if domain != "unknown":
#                     domains.append(domain)

#         # Prepare criteria with found domains
#         criteria = {
#             "domains": domains,
#             "page": params.get("page", 1),
#             "perPage": params.get("perPage", 10),
#             "locations": [params.get("location", "")] if params.get("location") else [],
#             "seniorities": [params.get("seniority", "")] if params.get("seniority") else [],
#             "employeeRanges": [params.get("companySize", "1,1000000")],
#             "titles": [params.get("title", "")] if params.get("title") else []
#         }

#         # Remove empty lists from criteria
#         criteria = {k: v for k, v in criteria.items() if v}

#         # Call the API
#         result = find_people(criteria)
#         return result



import os
from dotenv import load_dotenv
from langchain_community.llms import OpenAI

# from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from src.api.find_people_api import find_people
from ..config import OPENAI_API_KEY

# Load environment variables
load_dotenv()

class FindPeopleAgent:
    def __init__(self):
        self.llm = OpenAI(temperature=0, api_key=OPENAI_API_KEY)
        self.domain_chain = self._setup_domain_chain()
        self.company_search_chain = self._setup_company_search_chain()

    def _setup_domain_chain(self):
        prompt_template = """Given the company name: {company_name}
        What is the most likely domain (website URL) for this company?
        Provide only the domain name, without 'http://' or 'www.'.
        If unsure, respond with 'unknown'.
        Domain:"""
        
        prompt = PromptTemplate(
            input_variables=["company_name"],
            template=prompt_template
        )
        return LLMChain(llm=self.llm, prompt=prompt)

    def _setup_company_search_chain(self):
        prompt_template = """Given the following description or category: {description}
        And the location (if provided): {location}
        Provide a list of 10 real, well-known companies that fit this description.
        Format the response as a comma-separated list of company names only.
        Companies:"""
        
        prompt = PromptTemplate(
            input_variables=["description", "location"],
            template=prompt_template
        )
        return LLMChain(llm=self.llm, prompt=prompt)

    def _get_domain(self, company_name):
        response = self.domain_chain.run(company_name=company_name)
        return response.strip().lower()

    def _search_companies(self, description, location):
        response = self.company_search_chain.run(description=description, location=location)
        return [company.strip() for company in response.split(',') if company.strip()]
    

    def find_people(self, params):
        companies = params.get("company", "").split(',')
        domains = []
        locations = [loc.strip() for loc in params.get("location", "").split(',') if loc.strip()]

        for company in companies:
            company = company.strip()
            if company:
                # Check if it's a specific company name or a general description
                if any(keyword in company.lower() for keyword in ["startup", "sector", "industry", "companies","SaaS companies"]):
                    # It's a description, so search for companies
                    for location in locations:
                        searched_companies = self._search_companies(company, location)
                        for searched_company in searched_companies:
                            domain = self._get_domain(searched_company)
                            if domain != "unknown":
                                domains.append(domain)
                else:
                    # It's a specific company name
                    domain = self._get_domain(company)
                    if domain != "unknown":
                        domains.append(domain)
        titles = params.get("title", "")
        if titles:
    # Split titles by comma and strip whitespace
         titles = [title.strip() for title in titles.split(',') if title.strip()]
        else:
         titles = [""] 

        employee_range = params.get("companySize", "")
        if not employee_range:  # This will catch empty strings, None, or any falsy value
         employee_range = "1,1000000"
         
        # Prepare criteria with found domains
         criteria = {
           "domains": domains, 
    "page": params.get("page", 1),
    "perPage": params.get("perPage", 10),
    "locations": locations if locations else [""],  
    "seniorities": [params.get("seniority", "")],
    "employeeRanges": [employee_range],
    "titles": titles
        }

        # Remove empty lists from criteria
        criteria = {k: v for k, v in criteria.items() if v}

        # Call the API
        result = find_people(criteria)
        return result
    

    