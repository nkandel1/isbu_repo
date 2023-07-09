import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
#NEED BOBBY HELP
# Function to scrape data from a company page
def scrape_company_page(driver):
    try:
        # Extract website
        website_element = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div[3]/div/div[2]/div[1]/div/div/div/div/div/ul/li[4]/a/strong')
        website = website_element.text.strip()
    except NoSuchElementException:
        website = "N/A"

    try:
        # Extract email
        email_element = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div[3]/div/div[2]/div[1]/div/div/div/div/div/ul/li[3]/a/strong')
        #email = re.search(r'[\w\.-]+@[\w\.-]+', email_element.get_attribute("href")).group()
        email = email_element.text.strip()
    except NoSuchElementException:
        email = "N/A"

    try:
        # Extract company name
        company_name_element = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div[3]/div/div[2]/div[1]/div/div/div/div/div/h1')
        company_name = company_name_element.text.strip()
        # Extract the company name using a regular expression
    except NoSuchElementException:
        company_name = "N/A"
    
    

    try:
        # Extract description
        phone_element = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div[3]/div/div[2]/div[1]/div/div/div/div/div/ul/li[2]/a/strong')
        #phone_element_match = re.search(r'\b(?:\+?1[-.]?)?(?:\(\d{3}\)|\d{3})[-.]?\d{3}[-.]?\d{4}\b', phone_number)
        #phone_number = phone_element_match.group(0) if phone_element_match else ""
        phone_number = phone_element.text.strip()
    except NoSuchElementException:
        phone_number = "N/A"

    # Print extracted information
    print("Email:", email)
    print("Company Name:", company_name)
    print("Phone:", phone_number)
    print("Website:", website)
    print()


# URL of the RSS feed
url = "https://www.targikielce.pl/en/mspo/list-of-exhibitors"

# Configure Selenium WebDriver
driver = webdriver.Chrome()  # Replace with the appropriate WebDriver for your browser
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

# Open the RSS feed
driver.get(url)

# Find and click on each company info button
company_links = driver.find_elements(By.XPATH, '//*[@id="main-content"]//following-sibling::tr//a[starts-with(@href, "http") and contains(@class, "button")]')
for index, company_link in enumerate(company_links):
    
    company_url = company_link.get_attribute("href")

    # Open the company page in a new tab
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(company_url)

    try:
        # Wait for the company page to load
        company_name_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main-content"]/div/div[3]/div/div[2]/div[1]/div/div/div/div/div/h1')))
        scrape_company_page(driver)
    except TimeoutException:
        print("Error: Timed out waiting for the company page to load")

    # Close the company tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# Close the browser
driver.quit()
