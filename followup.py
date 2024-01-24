import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException

def read_csv(file_name):
    try:
        contacts = []  # List of tuples (phone_number, name)
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[4] == 'Sent':  # Checking if the message status is 'Sent'
                    contacts.append((row[3], row[1]))  # WhatsApp number and Name
        return contacts
    except FileNotFoundError:
        print(f"File not found: {file_name}")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def send_followup_message(driver, phone_number, name, message_template):
    try:
        personalized_message = message_template.format(name=name)
        encoded_message = personalized_message.replace("\n", "%0A")
        url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"        
        driver.get(url)
        time.sleep(12)
        send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "_3XKXx"))
        )
        send_button.click()
        time.sleep(5)  # Wait for message to be sent
    except TimeoutException:
        print(f"Timeout occurred while trying to send a message to {phone_number}.")
    except WebDriverException as e:
        print(f"Web driver exception occurred: {e}")
    except Exception as e:
        print(f"Error sending follow-up message to {phone_number}: {e}")

def main():
    try:
        config = json.load(open("followup_config.json"))
        followup_message_template = config["followup_message"]
        csv_file = config["csv_file_name"]
    except FileNotFoundError:
        print("Configuration file not found.")
        return
    except KeyError:
        print("Missing required configuration data.")
        return
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        return

    try:
        driver = webdriver.Chrome()  # Setup your WebDriver as per your requirements
        driver.get("https://web.whatsapp.com")
        input("Press ENTER after scanning the QR code and your chats are visible.")
    except WebDriverException as e:
        print(f"Error initializing web driver: {e}")
        return

    contacts = read_csv(csv_file)
    for phone_number, name in contacts:
        send_followup_message(driver, phone_number, name, followup_message_template)

    driver.quit()

if __name__ == "__main__":
    main()
