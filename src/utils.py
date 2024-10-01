def format_people_for_enrichment(people_data):
    formatted_people = []
    for person in people_data:
        formatted_person = {
            "id": person.get("id", ""),
            "first_name": person.get("first_name", ""),
            "last_name": person.get("last_name", ""),
            "name": person.get("name", ""),
            "title": person.get("jobTitle", ""),
            "company": person.get("company", ""),
            "domain": person.get("domain", ""),
            "email": person.get("email", ""),
            "phone": person.get("phone", ""),
            "linkedin_url": person.get("linkedin_url", ""),
            "location": person.get("location", "")
        }
        formatted_people.append(formatted_person)
    return formatted_people