import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Chrome WebDriver using WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Implicit wait
driver.implicitly_wait(10)  # Set an implicit wait of 10 seconds

# Navigate to the target URL
driver.get("https://ttdevasthanams.ap.gov.in/home/dashboard")

try:
    # Wait for the "Log In" button to be clickable
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Log In']"))
    )
    
    # Click the "Log In" button
    login_button.click()

    # Wait for the mobile input field to be present
    mobile_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @maxlength='10']"))
    )

    # Clear any pre-filled values
    mobile_input.clear()

    # Enter the mobile number
    mobile_number = "9985809986"
    mobile_input.send_keys(mobile_number)

    # Trigger input event using JavaScript to ensure the button is enabled
    driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", mobile_input)

    # Debugging: Print the value of the input field
    print(f"Entered mobile number: {mobile_input.get_attribute('value')}")

    # Wait for the submit button to be clickable
    submit_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Get OTP')]"))
    )
    
    # Click the submit button
    submit_button.click()
    print("Get OTP button clicked. Please check your mobile for the OTP.")

    # Wait for the OTP input fields to be present
    otp_inputs = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.XPATH, "//input[@type='tel' and @maxlength='1']"))
    )

    # Prompt the user to enter the OTP manually
    otp_value = input("Please enter the OTP received on your mobile: ")

    # Enter the OTP into the input fields
    for i in range(len(otp_inputs)):
        otp_inputs[i].clear()
        otp_inputs[i].send_keys(otp_value[i])

    # Wait for the submit OTP button to be clickable
    submit_otp_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
    )
    
    # Scroll to the submit OTP button before clicking
    driver.execute_script("arguments[0].scrollIntoView();", submit_otp_button)

    # Click the submit button using standard click or JavaScript click as a fallback
    try:
        submit_otp_button.click()
    except Exception as e:
        print("Standard click failed, trying JavaScript click:", e)
        driver.execute_script("arguments[0].click();", submit_otp_button)

    print("OTP submitted.")

    # Wait for the page to load after OTP submission
    time.sleep(5)  # You can adjust this duration as needed

    # Now look for the "Special Entry Darshan" option
    try:
        # Wait for the "Special Entry Darshan" option to be clickable
        special_entry_option = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'services_label__T0cqk') and contains(text(), 'Special Entry Darshan')]"))
        )
        
        # Scroll to the "Special Entry Darshan" option before clicking
        driver.execute_script("arguments[0].scrollIntoView();", special_entry_option)

        # Click on the "Special Entry Darshan" option
        special_entry_option.click()
        print("Navigated to Special Entry Darshan.")
    except Exception as e:
        print("Failed to locate Special Entry Darshan option.")
        print("Current page source:", driver.page_source)  # Print the page source for debugging
        raise e  # Re-raise the exception after printing the page source

finally:
    # Close the browser
    driver.quit()
