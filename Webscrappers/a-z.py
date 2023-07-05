import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# Function to scrape data from a company page
def scrape_company_page(driver):
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//h2[contains(text(),"Contact Details")]')))
        name_element = driver.find_element(By.XPATH, '//h2[contains(text(),"Contact Details")]//following-sibling::strong')
        name = name_element.text.strip()
        print("Name:", name)
    except NoSuchElementException:
        print("Name: N/A")
    except TimeoutException:
        print("Contact Details section not found")
        
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//h2[contains(text(),"Contact Details")]')))
        email_element = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div[1]/div[3]/div[2]/a[2]')
        email = email_element.text.strip()
        print("Email:", email)
    except NoSuchElementException:
        print("Email: N/A")
    except TimeoutException:
        print("Contact Details section not found")    
    
    
    

    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//h2[contains(text(),"Products and Services")]')))
        company_description_element = driver.find_element(By.XPATH,'//h2[contains(text(),"Products and Services")]//following-sibling::ul')
        company_des_text = company_description_element.text.strip()
        print("Description:", company_des_text)
    except NoSuchElementException:
        print("Description: N/A")
    except TimeoutException:
        print("Products and Services section not found")

    print()

# URL of the website
ds_url = "https://www.defence-and-security.com/contractors/indexAtoZ.html"

# Configure Selenium WebDriver
driver = webdriver.Chrome()  # Replace with the appropriate WebDriver for your browser
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)  # Increased timeout to 20 seconds

# Open the website
driver.get(ds_url)

# Find and click on each company link
company_links = driver.find_elements(By.XPATH, '//a[contains(@href, "http")]')
for index, company_link in enumerate(company_links):
    if index < 12:
        continue

    company_url = company_link.get_attribute("href")

    # Open the company page in a new tab
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(company_url)

    # Scrape the information from the company page
    scrape_company_page(driver)

    # Close the company tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# Close the browser
driver.quit()
