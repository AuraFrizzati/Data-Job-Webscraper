# from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_nhs_jobs():
    URL = r"https://www.jobs.nhs.uk/candidate/search/results?keyword=data&location=Cardiff%20(Caerdydd)&distance=20&language=en"
    
    # Keywords to filter job titles
    target_keywords = [
        "data", 
        "analyst", 
        "digital", 
        "information", 
        "informatics",
        "cloud"]
    
    # Add headers to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Find all job listings
    job_listings = soup.find_all("li", {"class": "nhsuk-list-panel search-result nhsuk-u-padding-3"})
    
    jobs_data = []
    
    for job in job_listings:
        try:
            # Extract job title and link
            job_title_element = job.find("a", {"data-test": "search-result-job-title"})
            job_title = job_title_element.text.strip() if job_title_element else "N/A"
            
            # Filter by keywords in job title (case-insensitive)
            if not any(keyword.lower() in job_title.lower() for keyword in target_keywords):
                continue  # Skip this job if it doesn't contain any target keywords
            
            job_link = "https://www.jobs.nhs.uk" + job_title_element.get('href') if job_title_element else "N/A"
            
            # Extract location
            location_element = job.find("div", {"data-test": "search-result-location"})
            if location_element:
                location_div = location_element.find("div", {"class": "location-font-size"})
                location = location_div.text.strip() if location_div else "N/A"
            else:
                location = "N/A"
            
            # Extract salary
            salary_element = job.find("li", {"data-test": "search-result-salary"})
            if salary_element:
                salary_strong = salary_element.find("strong")
                salary = salary_strong.text.strip() if salary_strong else "N/A"
            else:
                salary = "N/A"
            
            # Extract date posted
            date_element = job.find("li", {"data-test": "search-result-publicationDate"})
            if date_element:
                date_strong = date_element.find("strong")
                date_posted = date_strong.text.strip() if date_strong else "N/A"
            else:
                date_posted = "N/A"
            
            # Extract working pattern
            working_pattern_element = job.find("li", {"data-test": "search-result-workingPattern"})
            if working_pattern_element:
                working_pattern_strong = working_pattern_element.find("strong")
                working_pattern = working_pattern_strong.text.strip() if working_pattern_strong else "N/A"
            else:
                working_pattern = "N/A"
            
            # Extract closing date
            closing_date_element = job.find("li", {"data-test": "search-result-closingDate"})
            if closing_date_element:
                closing_date_strong = closing_date_element.find("strong")
                closing_date = closing_date_strong.text.strip() if closing_date_strong else "N/A"
            else:
                closing_date = "N/A"
            
            jobs_data.append({
                'Job Title': job_title,
                'Job Link': job_link,
                'Location': location,
                'Salary': salary,
                'Date Posted': date_posted,
                'Working Pattern': working_pattern,
                'Closing Date': closing_date
            })
            
        except Exception as e:
            print(f"Error processing job listing: {e}")
            continue
    
    return jobs_data

# Run the scraper
if __name__ == "__main__":
    jobs = scrape_nhs_jobs()
    
    if jobs:
        # Create DataFrame and save to CSV
        df = pd.DataFrame(jobs)
        df.to_csv('nhs_jobs_data.csv', index=False)
        
        print(f"Successfully scraped {len(jobs)} jobs containing target keywords:")
    else:
        print("No jobs found with the specified keywords.")