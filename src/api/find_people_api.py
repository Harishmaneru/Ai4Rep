
import requests
from ..config import FIND_PEOPLE_API, USER_ID

def find_people(criteria):
    headers = {
        "user-id": USER_ID,
        "Content-Type": "application/json"
    }
    
    # Print the criteria
    print("Criteria:", criteria)
    
    response = requests.post(FIND_PEOPLE_API, json=criteria, headers=headers)
    
    # Print the full response
    print("Full Response:")
    print(f"Status Code: {response.status_code}")
    print("Headers:", response.headers)
    print("Text:", response.text)
    
    if response.status_code == 200:
        response_json = response.json()
        # Print the JSON response
        print("JSON Response:", response_json)
        return response_json
    else:
        raise Exception(f"Failed to find people: {response.text}")
    