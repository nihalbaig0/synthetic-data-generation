import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

# Get the current directory of the Python script
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, 'bank_form.html')

# Load JSON data from file
with open(os.path.join(current_dir, 'bank.json'), 'r', encoding='utf-8') as file:
    form_data = json.load(file)

chrome_options = Options()
chrome_options.add_argument("--allow-file-access-from-files")

# Initialize the Chrome driver with the options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the HTML form page using the dynamically generated file path
driver.get(f"file:///{html_file_path}")

# Wait for the page to load
time.sleep(2)

def fill_input_field(field_id, value):
    try:
        field = driver.find_element(By.ID, field_id)
        field.clear()
        field.send_keys(value)
    except Exception as e:
        print(f"Error filling field {field_id}: {e}")

def fill_checkbox(field_id):
    try:
        checkbox = driver.find_element(By.ID, field_id)
        if not checkbox.is_selected():
            checkbox.click()
    except Exception as e:
        print(f"Error checking checkbox {field_id}: {e}")

# Fill Permanent Address fields
for key, value in form_data['permanent_address'].items():
    fill_input_field(f"permanent_{key}", value)

# Fill Work/Business/Office Address fields
for key, value in form_data['work_address'].items():
    fill_input_field(f"work_{key}", value)

# Fill Educational Qualification fields
for degree in form_data['educational_qualification']['degree']:
    fill_checkbox(degree)
fill_input_field("last_institution", form_data['educational_qualification']['last_institution'])

# Fill Details of Profession fields
for category in form_data['profession_details']['category']:
    fill_checkbox(category)
fill_input_field("organization_name", form_data['profession_details']['organization_name'])
fill_input_field("department", form_data['profession_details']['department'])
fill_input_field("designation", form_data['profession_details']['designation'])
fill_input_field("employed_since", form_data['profession_details']['employed_since'])
fill_input_field("prev_employer", form_data['profession_details']['previous_employment']['employer'])
fill_input_field("prev_designation", form_data['profession_details']['previous_employment']['designation'])
fill_input_field("service_length", form_data['profession_details']['previous_employment']['service_length'])
fill_input_field("total_service_length", form_data['profession_details']['total_service_length'])
fill_checkbox(form_data['profession_details']['primary_contact'])

# Fill Monthly Income Details fields
fill_checkbox("salaried")
fill_input_field("gross_salary", form_data['monthly_income']['salaried']['gross_salary'])
fill_input_field("total_deductions", form_data['monthly_income']['salaried']['total_deductions'])
fill_input_field("net_salary", form_data['monthly_income']['salaried']['net_salary'])
fill_input_field("additional_income", form_data['monthly_income']['additional_income'])
fill_input_field("spouse_income", form_data['monthly_income']['spouse_income'])
fill_input_field("other_income", form_data['monthly_income']['other_income'])

# Resize the window to full page height
total_height = driver.execute_script("return document.body.scrollHeight")
driver.set_window_size(1920, total_height)

# Wait a moment for resizing
time.sleep(2)

# Take a screenshot of the full page
screenshot_path = os.path.join(current_dir, 'filled_form_screenshot.png')
driver.save_screenshot(screenshot_path)

# Confirm screenshot saved
print(f"Screenshot saved as: {screenshot_path}")

# Optional: open and view the screenshot (uses Pillow)
screenshot = Image.open(screenshot_path)
screenshot.show()

# Close the browser
driver.quit()
