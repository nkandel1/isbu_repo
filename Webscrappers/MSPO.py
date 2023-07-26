import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd

# Function to scrape data from a company page
def scrape_company_page(driver):
    try:
        # Extract website
        website_element = driver.find_element(By.XPATH, '//strong[contains(text(), "www.")]')
        website = website_element.text.strip()
    except NoSuchElementException:
        website = "N/A"

    try:
        # Extract email
        email_element = driver.find_element(By.XPATH, '//*[contains(text(), "@")]')
        email = email_element.text.strip()
    except NoSuchElementException:
        email = "N/A"

    try:
        # Extract company name
        company_name_element = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div[3]/div/div[2]/div[1]/div/div/div/div/div/h1')
        company_name = company_name_element.text.strip()
    except NoSuchElementException:
        company_name = "N/A"

    try:
        strong_element = driver.find_element(By.XPATH, '//strong[not(contains(text(), "@"))]')
        address = strong_element.text.strip()
    except NoSuchElementException:
        address = "N/A"

    # Return the extracted information as a dictionary
    return {
        "Email": email,
        "Company Name": company_name,
        "Address": address,
        "Website": website
    }

# URL of the RSS feed
url = "https://www.targikielce.pl/en/mspo/list-of-exhibitors"

# Configure Selenium WebDriver
driver = webdriver.Chrome()  # Replace with the appropriate WebDriver for your browser
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 5)

# Open the RSS feed
driver.get(url)

# Find and click on each company info button
company_links = driver.find_elements(By.XPATH, '//*[@id="main-content"]//following-sibling::tr//a[starts-with(@href, "http") and contains(@class, "button")]')

# Initialize a list to store the data for all companies
companies_data = []

for index, company_link in enumerate(company_links):
    if index >= 477:
        break

    company_url = company_link.get_attribute("href")

    # Open the company page in a new tab
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(company_url)

    try:
        # Wait for the company page to load
        company_name_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main-content"]/div/div[3]/div/div[2]/div[1]/div/div/div/div/div/h1')))
        company_data = scrape_company_page(driver)
        companies_data.append(company_data)
    except TimeoutException:
        print("Error: Timed out waiting for the company page to load")

    # Close the company tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# Close the browser
driver.quit()

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(companies_data)

# Print the DataFrame
print(df)

# Convert the DataFrame to a CSV file
df.to_csv("MSPO_data.csv", index=False)
