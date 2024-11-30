import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Get the current directory of the Python script
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, 'form.html')

# Load JSON data from file
with open(os.path.join(current_dir, 'form_data.json'), 'r', encoding='utf-8') as file:
    form_data = json.load(file)

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "./",  # Set download directory
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
chrome_options.add_argument("--allow-file-access-from-files")

# Initialize the Chrome driver with the options
driver = webdriver.Chrome(options=chrome_options)

# Open the HTML form page using the dynamically generated file path
driver.get(f"file:///{html_file_path}")

# Wait for the page to load
time.sleep(2)

# Fill in the number of fields
num_fields_input = driver.find_element(By.ID, "numFields")
num_fields_input.clear()
num_fields_input.send_keys(str(form_data['numFields']))

# Click the "Generate Options" button to create input rows
generate_options_button = driver.find_element(By.XPATH, "//button[text()='অপশন তৈরি করুন']")
generate_options_button.click()

time.sleep(1)  # Let the options render

# Fill in the generated options and input values in Bangla
for i, field in enumerate(form_data['fields']):
    # Check if the row is multi-column
    is_multi_column_checkbox = driver.find_element(By.ID, f'isMultiColumn{i}')
    if field['isMultiColumn']:
        if not is_multi_column_checkbox.is_selected():
            is_multi_column_checkbox.click()
    else:
        if is_multi_column_checkbox.is_selected():
            is_multi_column_checkbox.click()

    # Select input style
    input_style_select = driver.find_element(By.ID, f'inputStyle{i}')
    input_style_select.click()
    input_style_option = driver.find_element(By.CSS_SELECTOR, f"option[value='{field['inputStyle']}']")
    input_style_option.click()

    # Set the character count
    char_count_input = driver.find_element(By.ID, f'charCount{i}')
    char_count_input.clear()
    char_count_input.send_keys(str(field['charCount']))

# Generate the form by clicking the "Generate Form" button
generate_form_button = driver.find_element(By.XPATH, "//button[text()='ফর্ম তৈরি করুন']")
generate_form_button.click()

time.sleep(2)  # Wait for the form to generate

# Automatically fill the form with Bangla values
for i, field in enumerate(form_data['fields']):
    if field['isMultiColumn']:
        for j, value in enumerate(field['values']):
            field_input = driver.find_element(By.CSS_SELECTOR,
                                              f'.form-row:nth-of-type({i + 1}) .form-field:nth-of-type({j + 1}) input')
            field_input.clear()
            field_input.send_keys(value)
    else:
        field_input = driver.find_element(By.CSS_SELECTOR, f'.form-row:nth-of-type({i + 1}) .form-field input')
        field_input.clear()
        field_input.send_keys(field['values'][0])

# Take a screenshot of the entire page
screenshot_path = os.path.join(current_dir, 'form_screenshot.png')
driver.save_screenshot(screenshot_path)

print(f"Screenshot saved as: {screenshot_path}")

# Close the browser
driver.quit()