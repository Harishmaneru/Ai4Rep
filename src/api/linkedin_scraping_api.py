import requests
import json
from ..config import (
    PHANTOMBUSTER_LINKEDIN_COMMENTS_LIKES_API,
    PHANTOMBUSTER_LINKEDIN_PROFILE_API,
    PHANTOMBUSTER_SALES_NAVIGATOR_PROFILE_API,
    PHANTOMBUSTER_SALES_NAVIGATOR_EMAILS_API
)

# Scrape LinkedIn comments and likes
def scrape_linkedin_comments_likes(post_url, session_cookie):
    headers = {"Content-Type": "application/json"}
    payload = {"postUrl": post_url, "sessionCookie": session_cookie}

    # Make request to the Phantombuster API
    response = requests.post(PHANTOMBUSTER_LINKEDIN_COMMENTS_LIKES_API, json=payload, headers=headers)

    # Log the response for debugging
    print("Response status code:", response.status_code)
    print("Response content:", response.text)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to scrape LinkedIn comments/likes: {response.text}")


# Scrape LinkedIn profile
def scrape_linkedin_profile(profile_url, session_cookie):
    headers = {"Content-Type": "application/json"}
    payload = {"profileUrl": profile_url, "sessionCookie": session_cookie}

    response = requests.post(PHANTOMBUSTER_LINKEDIN_PROFILE_API, json=payload, headers=headers)

    # Log the response for debugging
    print("Response status code:", response.status_code)
    print("Response content:", response.text)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to scrape LinkedIn profile: {response.text}")


# Scrape Sales Navigator profile
def scrape_sales_navigator_profile(profile_url, session_cookie):
    headers = {"Content-Type": "application/json"}
    payload = {"profileUrl": profile_url, "sessionCookie": session_cookie}

    response = requests.post(PHANTOMBUSTER_SALES_NAVIGATOR_PROFILE_API, json=payload, headers=headers)

    # Log the response for debugging
    print("Response status code:", response.status_code)
    print("Response content:", response.text)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to scrape Sales Navigator profile: {response.text}")


# Scrape emails from Sales Navigator search results
def scrape_sales_navigator_emails(querieURL, session_cookie):
    headers = {"Content-Type": "application/json"}
    payload = {"querieURL": querieURL, "sessionCookie": session_cookie}

    response = requests.post(PHANTOMBUSTER_SALES_NAVIGATOR_EMAILS_API, json=payload, headers=headers)

    # Log the response for debugging
    print("Response status code:", response.status_code)
    print("Response content:", response.text)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to scrape emails from Sales Navigator: {response.text}")
