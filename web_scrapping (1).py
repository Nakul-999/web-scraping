import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to fetch and parse the HTML page
def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: Unable to fetch page {url}")
            return None
    except Exception as e:
        print(f"Error occurred while fetching {url}: {e}")
        return None

# Function to parse the HTML and extract company details
def parse_company_data(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    companies = []

    company_cards = soup.find_all('div', class_='company-card')  
    
    for card in company_cards:
        name = card.find('h2', class_='company-name')
        website = card.find('a', class_='website-link')
        phone = card.find('span', class_='contact-number')
        address = card.find('span', class_='company-address')
        category = card.find('span', class_='industry-category')
        description = card.find('p', class_='company-description')

        company_data = {
            'Company Name': name.text.strip() if name else 'N/A',
            'Website URL': website['href'].strip() if website else 'N/A',
            'Contact Number': phone.text.strip() if phone else 'N/A',
            'Location/Address': address.text.strip() if address else 'N/A',
            'Industry/Category': category.text.strip() if category else 'N/A',
            'Company Description': description.text.strip() if description else 'N/A'
        }
        companies.append(company_data)

    return companies

# Function to scrape multiple pages
def scrape_directory(base_url, pages_to_scrape=3):
    all_companies = []

    for page_number in range(1, pages_to_scrape + 1):
        print(f"Scraping page {page_number}...")
        url = f"{base_url}?page={page_number}"
        page_content = fetch_page(url)
        if page_content:
            companies = parse_company_data(page_content)
            all_companies.extend(companies)
        time.sleep(2) 

    return all_companies

# Main function to run the script
def main():
    base_url = 'https://' 
    companies = scrape_directory(base_url)

    # Save data to CSV file
    if companies:
        df = pd.DataFrame(companies)
        df.to_csv('b2b_companies.csv', index=False)
        print("Data saved to b2b_companies.csv")
    else:
        print("No data found.")

# Run the main function
if __name__ == "__main__":
    main()
