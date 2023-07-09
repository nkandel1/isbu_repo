import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def limit_description(description):
    if len(description) > 250:
        description = description[:250] + "..."  # Truncate and add ellipsis
    return description


# Create empty lists to store the scraped data
phone_list = []
company_name_list = []
description_list = []
website_list = []

# Function to scrape data from a company page and append it to the lists
def scrape_company_page(driver):
    try:
        website_element = driver.find_element(By.XPATH, '//*[@id="main"]/main/div/div/div/div[2]/div[2]/div[3]/div[2]/div/div/a')
        website = website_element.get_attribute("href")
    except NoSuchElementException:
        website = "N/A"

    try:
        company_name_element = driver.find_element(By.XPATH, '//*[@id="main"]/main/div/div/div/div[2]/div[1]/div[2]/h1')
        company_name_text = company_name_element.text.strip()
    except NoSuchElementException:
        company_name_text = "N/A"

    try:
        phone_element = driver.find_element(By.XPATH, '//*[@id="main"]/main/div/div/div/div[2]/div[2]/div[2]/div/div')
        phone = phone_element.text.strip()
    except NoSuchElementException:
        phone = "N/A"

    try:
        description_element = driver.find_element(By.XPATH, '//*[@id="main"]/main/div/div/div/div[2]/div[2]/div[1]')
        description = description_element.text.strip()
        description = limit_description(description)
    except NoSuchElementException:
        description = "N/A"

    # Append the scraped data to the respective lists
    phone_list.append(phone)
    company_name_list.append(company_name_text)
    description_list.append(description)
    website_list.append(website)


# URL of the RSS feed
rss_feed_url = "https://www.thesecurityevent.co.uk/exhibitor-list?&sortby=Community_Featured%20desc%2Ctitle%20asc&searchgroup=44F675C2-exhibitors"

# Configure Selenium WebDriver
driver = webdriver.Chrome()  # Replace with the appropriate WebDriver for your browser
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

# Open the RSS feed
driver.get(rss_feed_url)

# Find and click on each company link containing "2023"
company_links = driver.find_elements(By.XPATH, '//a[contains(@class, "m-exhibitors-list__items__item__header__title__link") and contains(@href, "exhibitors/")]')
for index, company_link in enumerate(company_links):
    company_url = company_link.get_attribute("href")

    # Open the company page in a new tab
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(company_url)

    # Scrape data from the company page and append it to the lists
    scrape_company_page(driver)

    # Close the company tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# Close the browser
driver.quit()

# Create a dataframe from the scraped data
data = {
    "Phone": phone_list,
    "Company Name": company_name_list,
    "Description": description_list,
    "Website": website_list
}
df = pd.DataFrame(data)

print(df)

# Convert the dataframe to a CSV file
df.to_csv("scraped_data.csv", index=False)

