from src.api.linkedin_scraping_api import (
    scrape_linkedin_comments_likes,
    scrape_linkedin_profile,
    scrape_sales_navigator_profile,
    scrape_sales_navigator_emails
)

class LinkedInScrapingAgent:
    def __init__(self):
        pass

    def scrape_linkedin_comments_likes(self, post_url, session_cookie):
        """Scrape LinkedIn post for comments and likes."""
        return scrape_linkedin_comments_likes(post_url, session_cookie)

    def scrape_linkedin_profile(self, profile_url, session_cookie):
        """Scrape LinkedIn profile data."""
        return scrape_linkedin_profile(profile_url, session_cookie)

    def scrape_sales_navigator_profile(self, profile_url, session_cookie):
        """Scrape Sales Navigator profile."""
        return scrape_sales_navigator_profile(profile_url, session_cookie)

    def scrape_sales_navigator_emails(self, querieURL, session_cookie):
        """Scrape Sales Navigator search results for emails."""
        print(f"Attempting to scrape emails with URL: {querieURL}")

        return scrape_sales_navigator_emails(querieURL, session_cookie)
