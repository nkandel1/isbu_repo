import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

def limit_description(description):
    if len(description) > 250:
        description = description[:250] + "..."  # Truncate and add ellipsis
    return description


phone_list = []
company_name_list = []
description_list = []
website_list = []


# Function to scrape data from a company page
def scrape_company_page(driver):
    try:
        # Extract website
        website_element = driver.find_element(By.XPATH, '/html/body/div[2]/section[4]/div/div[1]/div/section[3]/div/div[2]/div/div/div/p/a')
        website = website_element.text.strip()
    except NoSuchElementException:
        website = "N/A"

    try:
        # Extract company name
        company_name_element = driver.find_element(By.XPATH, '/html/body/div[2]/section[1]/div/div/div/div/div/h1')
        company_name_text = company_name_element.text.strip()
    except NoSuchElementException:
        company_name_text = "N/A"
    
    try:
        # Extract phone number
        phone_element = driver.find_element(By.XPATH, '/html/body/div[2]/section[4]/div/div[1]/div/section[4]/div/div[2]/div/div/div/p')
        phone = phone_element.text.strip()
        
        #phone_element_match = re.search(r'\b(?:\+?1[-.]?)?(?:\(\d{3}\)|\d{3})[-.]?\d{3}[-.]?\d{4}\b', phone)
        #phone_number = phone_element_match.group(0) if phone_element_match else ""

    except NoSuchElementException:
        phone = "N/A"
    
    try:
        # Extract description
        description_element = driver.find_element(By.XPATH, '/html/body/div[2]/section[2]/div/div[1]/div/div[4]/div/p[2]')
        description = description_element.text.strip()
        description = limit_description(description)
    except NoSuchElementException:
        description = "N/A"

    # Print extracted information
    # print("Phone:", phone)
    # print("Company Name:", company_name_text)
    # print("Description:", description)
    # print("Website:", website)
    # print()
    phone_list.append(phone)
    company_name_list.append(company_name_text)
    description_list.append(description)
    website_list.append(website)


# URL of the RSS feed
rss_feed_url = "https://securex.co.za/exhibitors/"

# Configure Selenium WebDriver
driver = webdriver.Chrome()  # Replace with the appropriate WebDriver for your browser
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

# Open the RSS feed
driver.get(rss_feed_url)

# Find and click on each company link containing "2023"
company_links = driver.find_elements(By.XPATH, '//a[contains(text(), "Read More")]')
for index, company_link in enumerate(company_links):
    company_url = company_link.get_attribute("href")

    # Open the company page in a new tab
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(company_url)

    # Scrape data from the company page
    scrape_company_page(driver)

    # Close the company tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# Close the browser
driver.quit()

data = {
    "Phone": phone_list,
    "Company Name": company_name_list,
    "Description": description_list,
    "Website": website_list
}
df = pd.DataFrame(data)

print(df)

# Convert the dataframe to a CSV file
df.to_csv("Securex_data.csv", index=False)