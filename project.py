import requests
from bs4 import BeautifulSoup
import json

# URL of the website
url = 'https://www.mukeshassociates.com/division_3.php'

# Fetch the webpage content
response = requests.get(url)
if response.status_code == 200:
    html_content = response.content
else:
    print(f"Failed to retrieve webpage. Status code: {response.status_code}")
    exit()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Function to extract job details
def extract_job_details(job_section):
    job_title_tag = job_section.find('h4')
    job_title = job_title_tag.text.strip() if job_title_tag else 'Not available'
    
    def find_next_text(tag, label):
        element = job_section.find('th', string=label)
        if element and element.find_next('td'):
            return element.find_next('td').text.strip()
        return 'Not available'
    
    qualification = find_next_text(job_section, 'Qualification')
    professional_experience = find_next_text(job_section, 'Overall Professional Experience')
    relevant_experience = find_next_text(job_section, 'Relevant Experience')
    
    return {
        "company": "Mukesh & Associates",
        "job_title": job_title,
        "eligibility_criteria": qualification,
        "job_description": professional_experience,
        "location": "Assam"
    }

# Find all job sections (using <td colspan="5"> as the container)
job_sections = soup.find_all('td', colspan="5")

# Extract details for each job
jobs_data = []
for job_section in job_sections:
    job_data = extract_job_details(job_section)
    jobs_data.append(job_data)

# Write the JSON data to a file
output_file = 'merged_jobs_data.json'
with open(output_file, 'w') as json_file:
    json.dump(jobs_data, json_file, indent=4)

print(f"Job data has been saved to {output_file}")
