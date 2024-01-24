import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException  # Import TimeoutException
import csv
import time
import random
import json
import os
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_run_specific_file():
    """
    Create a new CSV file for the current run with a timestamp.
    Returns the filename.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"run_data_{timestamp}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Advertisement Name", "Name", "Link", "WhatsApp Number", "Message Status"])
    return filename

def update_run_specific_record(ad_name, name, ad_link, whatsapp_number, status, filename):
    """
    Update the run-specific record file with the new entry.
    """
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([ad_name, name, ad_link, whatsapp_number, status])

def human_like_delay(minimum=2, maximum=5):
    time.sleep(random.uniform(minimum, maximum))

def random_mouse_movement(driver):
    try:
        # Find all interactable elements on the page
        elements = driver.find_elements(By.XPATH, "//*[not(self::option)]")
        interactable_elements = [elem for elem in elements if elem.is_displayed() and elem.is_enabled()]

        if interactable_elements:
            # Choose a random element and move to it
            target_element = random.choice(interactable_elements)
            action = ActionChains(driver)
            action.move_to_element(target_element).perform()
            human_like_delay(0.5, 1.5)
    except Exception as e:
        logging.warning(f"Error during random mouse movement: {e}")


def simulate_human_scrolling(driver):
    try:
        total_height = driver.execute_script("return document.body.scrollHeight")
        scrolled_height = 0
        while scrolled_height < total_height:
            scroll_amount = random.randint(100, 300)  # Random scroll step between 100 and 300 pixels
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            scrolled_height += scroll_amount
            human_like_delay(1, 3)  # Random delay between each scroll step

            # Randomly decide whether to scroll up a little
            if random.choice([True, False]):
                scroll_up_amount = random.randint(50, 150)
                driver.execute_script(f"window.scrollBy(0, -{scroll_up_amount});")
                scrolled_height -= scroll_up_amount
                human_like_delay(0.5, 2)

    except Exception as e:
        logging.warning(f"Error during human-like scrolling: {e}")


def human_like_typing(element, text):
    for character in text:
        element.send_keys(character)
        human_like_delay(0.1, 0.3)


def perform_whatsapp_login(driver):
    driver.get("https://web.whatsapp.com")
    input("Press ENTER after logging into WhatsApp Web, and your chats are visible.")

    time.sleep(10)


def perform_login(driver, username, password):
    driver.get("https://my.gumtree.com/login")

    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "(//input[@id='email'])[1]"))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='fld-password']"))
    )
    submit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[normalize-space()='Login']")
        )
    )
    simulate_human_scrolling(driver)
    # username_field.send_keys(username)
    human_like_typing(username_field, username)
    time.sleep(2)
    # password_field.send_keys(password)
    human_like_typing(password_field, password)
    time.sleep(2)
    driver.execute_script("arguments[0].click();", submit_button)
    time.sleep(5)
    random_mouse_movement(driver)
    simulate_human_scrolling(driver)


def extract_info(driver, ad_url):
    try:
        driver.get(ad_url)
        # time.sleep(random.uniform(8, 10))

        reveal_btn_xpath = "(//button[contains(@class,'reveal-button')])[2]"
        try:
            reveal_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, reveal_btn_xpath))
            )
            time.sleep(random.uniform(5, 7))
            random_mouse_movement(driver)
            simulate_human_scrolling(driver)
            reveal_btn.click()
            time.sleep(3)
        except Exception:
            logging.warning(
                "Reveal button not found, WhatsApp number might not be present."
            )
            return None, None, None  # Returning None if reveal button is not found

        whatsapp_number_xpath = "//h2[@data-q='seller-phone-number']"
        ad_name_xpath = "//h1[@data-q='vip-title']"
        ad_poster_name_xpath = "//h2[@class='truncate-line seller-rating-block-name']"

        whatsapp_number = (
            WebDriverWait(driver, 10)
            .until(EC.presence_of_element_located((By.XPATH, whatsapp_number_xpath)))
            .text
        )
        ad_name = (
            WebDriverWait(driver, 10)
            .until(EC.presence_of_element_located((By.XPATH, ad_name_xpath)))
            .text
        )
        name = (
            WebDriverWait(driver, 10)
            .until(EC.presence_of_element_located((By.XPATH, ad_poster_name_xpath)))
            .text.strip()
            .title()
        )

        return ad_name, whatsapp_number, name
    except Exception as e:
        logging.error(f"Error extracting information: {e}")
        return None, None, None
    

def send_whatsapp_message(driver, whatsapp_number, message_template):
    try:
        encoded_message = message_template.replace("\n", "%0A")
        url = f"https://web.whatsapp.com/send?phone={whatsapp_number}&text={encoded_message}"        
        driver.get(url)
        time.sleep(random.uniform(12, 15))
        # Wait for either the send button to be clickable or the error message to appear
        WebDriverWait(driver, 35).until(
            EC.any_of(
                EC.element_to_be_clickable((By.CLASS_NAME, "_3XKXx")),
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(text(),'Phone number shared via url is invalid.')]",
                    )
                ),
            )
        )

        invalid_number_msg = driver.find_elements(
            By.XPATH,
            "//div[contains(text(),'Phone number shared via url is invalid.')]",
        )

        if invalid_number_msg:
            logging.error(f"Invalid WhatsApp number: {whatsapp_number}")
            return "Invalid Number"
        else:
            click_btn = driver.find_element(By.CLASS_NAME, "_3XKXx")
            click_btn.click()
            time.sleep(5)
            return "Sent"
    except Exception as e:
        logging.error(f"Error sending message to {whatsapp_number}: {e}")
        return "Failed"


def navigate_pages(driver, base_url):
    ad_links = []
    page = 1
    while True:
        driver.get(f"{base_url}/page{page}")
        links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//a[@data-q='search-result-anchor']")
            )
        )
        ad_links.extend([link.get_attribute("href") for link in links])
        time.sleep(random.uniform(8, 10))
        random_mouse_movement(driver)
        simulate_human_scrolling(driver)
        # Check if 'Next' button is present
        next_buttons = driver.find_elements(
            By.XPATH, "//a[contains(@class, 'pagination-link--next')]"
        )
        if not next_buttons:
            logging.info("No 'Next' button found. Assuming only one page is available.")
            break

        # Check if 'Next' button is disabled
        try:
            next_button_disabled = driver.find_element(
                By.XPATH, "//a[contains(@class, 'pagination-link--next')][@disabled]"
            )
            logging.info(f"'Next' button disabled on page {page}. Stopping pagination.")
            break
        except Exception:
            logging.info(f"Collected links from page {page}")
            page += 1

    return ad_links


def check_record(ad_link, whatsapp_number, record_file="processed_ads.csv"):
    """
    Check if the ad link and WhatsApp number are already in the record.
    Returns True if the record exists, False otherwise.
    """
    if not os.path.exists(record_file):
        return False

    with open(record_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if ad_link in row and whatsapp_number in row:
                return True
    return False


def update_record(
    ad_name, name, ad_link, whatsapp_number, status, record_file="processed_ads.csv"
):
    """
    Update the record file with the new entry.
    """
    with open(record_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([ad_name, name, ad_link, whatsapp_number, status])


def main():
    with open("config.json", "r") as file:
        config = json.load(file)

    # Extract configuration values
    username = config["email"]
    password = config["password"]
    base_url = config["base_url"]
    message_template = config["message_template"]

    chrome_options = webdriver.ChromeOptions()
    # ... your existing Chrome options ...
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--disable-extensions-http-throttling")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    perform_whatsapp_login(driver)
    perform_login(driver, username, password)

    ad_links = navigate_pages(driver, base_url)

    # Initialize the record file if it doesn't exist
    if not os.path.exists("processed_ads.csv"):
        with open("processed_ads.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Advertisement Name", "Name", "Link", "WhatsApp Number", "Message Status"]
            )

    run_specific_filename = create_run_specific_file()

    try:
        for ad_link in ad_links:
            ad_name, whatsapp_number, name = extract_info(driver, ad_link)
            if ad_name and whatsapp_number:
                whatsapp_number = f"+44{whatsapp_number}"

                # Check if the ad has already been processed
                if check_record(ad_link, whatsapp_number):
                    logging.info(f"Ad already processed: {ad_link}")
                    continue

                personalized_message = message_template.format(name=name)
                status = send_whatsapp_message(driver, whatsapp_number, personalized_message)

                # Update the overall and run-specific records
                update_record(ad_name, name, ad_link, whatsapp_number, status)
                update_run_specific_record(ad_name, name, ad_link, whatsapp_number, status, run_specific_filename)

                # Introduce delay
                time.sleep(random.uniform(2, 5))
            else:
                logging.info("No WhatsApp number found for ad.")
                update_record(ad_name,name, ad_link, "N/A", "N/A")
                update_run_specific_record(ad_name,name, ad_link, "N/A", "N/A", run_specific_filename)

    except Exception as e:
        logging.error(f"Error during processing: {e}")

    driver.quit()

if __name__ == "__main__":
    main()