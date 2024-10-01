import requests
import json
from ..config import ENRICH_PEOPLE_API, SITE_API_KEYS, USER_ID

def enrich_people(people_data, enrich_type, site_ids=['apollo', 'leadmagic', 'skrapp']):
    print("Received people_data:")
    print(json.dumps(people_data, indent=2))
    
    print(f"Enrich type: {enrich_type}")
    
    enriched_data = []
    
    for person in people_data:
        for site_id in site_ids:
            # Extract common data
            first_name = person.get('first_name', '')
            last_name = person.get('last_name', '')
            domain = person.get('organization', {}).get('primary_domain', '')
            company_name = person.get('organization', {}).get('name', '')
            
            print(f"\nProcessing person: {first_name} {last_name}")
            print(f"Domain: {domain}")
            print(f"Company: {company_name}")
            print(f"Enriching with {site_id}")
            
            if site_id == 'apollo':
                data = {
                    "people": [{
                        "first_name": first_name,
                        "last_name": last_name,
                        "domain": domain,
                        "organization_name": company_name,
                    }],
                    "enrichType": enrich_type,
                    "siteId": site_id,
                    "userId": USER_ID
                }
            elif site_id == 'leadmagic':
                data = {
                    "people": [{
                        "first_name": first_name,
                        "last_name": last_name,
                        "domain": domain,
                        "company_name": company_name
                    }],
                    "enrichType": enrich_type,
                    "siteId": site_id,
                    "userId": USER_ID
                }
            elif site_id == 'skrapp':
                data = {
                    "people": [{
                        "firstName": first_name,
                        "lastName": last_name,
                        "domain": domain
                    }],
                    "enrichType": enrich_type,
                    "siteId": site_id,
                    "userId": USER_ID
                }

            response = requests.post(ENRICH_PEOPLE_API, json=data)
            if response.status_code == 200:
                new_data = response.json()[0]  # Assuming the API returns a list with one person
                if not enriched_data or new_data != enriched_data[-1]:
                    enriched_data.append(new_data)
                    break  # Move to the next person if we got new data
            else:
                print(f"Failed to enrich with {site_id}: {response.text}")
    
    return enriched_data