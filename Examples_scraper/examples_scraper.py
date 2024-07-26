# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import time

# # from selenium.common.exceptions import WebDriverException

# # try:
# #     # Attempt to initialize the WebDriver
# #     driver = webdriver.Chrome()
# #     print("ChromeDriver is installed and accessible.")
# #     driver.quit()
# # except WebDriverException as e:
# #     print("ChromeDriver is not installed or not in your PATH.")
# #     print(e)

# # Specify the path to the correct ChromeDriver executable
# driver_path = "/opt/homebrew/bin/chromedriver"

# try:
#     # Initialize the WebDriver
#     driver = webdriver.Chrome(executable_path=driver_path)

#     # Navigate to the website
#     driver.get("https://www.theidioms.com")

#     # Locate the search bar element
#     search_bar = driver.find_element(By.NAME, "q")

#     # Enter text into the search bar
#     search_text = "OpenAI GPT-4"
#     search_bar.send_keys(search_text)

#     # Submit the search
#     search_bar.send_keys(Keys.RETURN)

#     # Wait for the results to load
#     time.sleep(2)

#     # Locate the first 'a' element with the class 'gs-title'
#     first_result = driver.find_element(By.CSS_SELECTOR, "a.gs-title")
#     first_result.click()

#     # Wait for a few seconds to see the result
#     time.sleep(5)

# finally:
#     # Close the WebDriver
#     driver.quit()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def capitalize_first_letter(text):
    # Check if the text is not empty
    if text:
        # Lowercase the entire string, then capitalize the first letter
        lowercased_text = text.lower()
        return lowercased_text[0].upper() + lowercased_text[1:]
    return text


# Path to the ChromeDriver installed via Homebrew
driver_path = "/opt/homebrew/bin/chromedriver"

# Initialize the WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

search_title = "when one kills two birds with stone"


try:
    # Navigate to the website
    driver.get("https://www.theidioms.com")

    # Locate the search bar element
    search_bar = driver.find_element(By.ID, "q")

    # Enter text into the search bar
    search_bar.send_keys(search_title)

    # Submit the search (press Enter)
    search_bar.send_keys(Keys.RETURN)

    # Wait for the results to load (you might want to use WebDriverWait for better practice)
    time.sleep(2)

    # Locate the first 'a' element with the class 'gs-title'
    first_result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.gs-title"))
    )
    first_result.click()

    # Wait for the new page to load and locate the h1 element with id 'title'
    h1_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "title"))
    )

    # Get the text inside the h1 element
    h1_text = capitalize_first_letter(h1_element.text)

    print()
    print("Search title: ", search_title)
    print("Found title: ", h1_text)
    print()

    # Wait for a few seconds to see the result (optional)
    time.sleep(5)

finally:
    # Close the WebDriver
    driver.quit()
