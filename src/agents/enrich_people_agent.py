from src.api.enrich_people_api import enrich_people

class EnrichPeopleAgent:
    def __init__(self):
        pass

    def enrich_people(self, params):
        # Determine enrich type based on params or prompt
        if 'email' in params and 'phone' in params:
            enrich_type = 'both'
        elif 'email' in params:
            enrich_type = 'email'
        elif 'phone' in params:
            enrich_type = 'phone'
        else:
            enrich_type = 'both'  # Default to both if not specified

        # Prepare people data
        people_data = params.get('people', [])
        
        # Call the API
        result = enrich_people(people_data, enrich_type)
        return result