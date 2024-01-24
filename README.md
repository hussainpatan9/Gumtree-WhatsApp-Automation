
# Gumtree Automation for WhatsApp Messaging

This Python automation script empowers users to interact seamlessly with Gumtree ads by automating the process of scraping advertisements, extracting relevant information, and sending personalized WhatsApp messages. Whether for business or personal use, this tool enhances outreach efforts on Gumtree efficiently, making it an invaluable asset for connecting with ad posters.

## Features

- **Automated Login**: Effortlessly logs into WhatsApp Web and Gumtree.
- **Ad Scraping**: Extracts essential information from Gumtree ads, including ad name, WhatsApp number, and poster name.
- **Automated Messaging**: Sends personalized messages to extracted WhatsApp numbers.
- **Record Keeping**: Maintains records of processed ads to prevent duplicate messaging.
- **Run-specific Data Logging**: Generates a new file for each script run to log processed ads.

## Prerequisites

- Python 3
- Selenium WebDriver
- Chrome Browser
- Appropriate ChromeDriver installed

## Setup and Configuration

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configuration File (`config.json`)

Store your Gumtree login credentials and other configurations in this file.

```json
{
    "email": "your_email@example.com",
    "password": "your_password",
    "base_url": "https://www.gumtree.com/your-category",
    "message_template": "Hello {name}, I'm interested in your ad titled '{ad_title}'."
}
```

### 3. ChromeDriver

Download and install ChromeDriver compatible with your Chrome version from [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).

## Usage

### Main Script (`main_script.py`)

#### 1. Run the Script:

Navigate to the script directory and execute:

```bash
python main_script.py
```

#### 2. Manual Interaction:

Manually scan the WhatsApp QR code for login when prompted.

#### 3. Automated Processes:

The script will automatically navigate Gumtree pages, extract ad information, and send messages.

### Follow-up Script (`followup.py`)

#### 1. Run the Script:

Navigate to the script directory and execute:

```bash
python followup.py
```

#### 2. Manual Interaction:

Manually scan the WhatsApp QR code for login when prompted.

#### 3. Automated Processes:

The script will send follow-up messages to contacts with a "Sent" message status in the CSV file.

## Data Logging

- **`processed_ads.csv`**: Contains records of all processed ads.
- **Run-specific files**: Named with a timestamp, containing data from that specific run.

## Best Practices

- Ensure compliance with the terms of service of WhatsApp and Gumtree.
- Respect privacy laws and regulations when handling personal information.
- Use responsibly to avoid spamming and potential account bans.

## File Structure

- **`main_script.py`**: The main script for Gumtree automation.
- **`followup.py`**: Script for sending follow-up messages.
- **`config.json`**: Configuration file for Gumtree login, URL, and message template.
- **`processed_ads.csv`**: Record of processed ads, including WhatsApp message status.
- **`run_data_<timestamp>.csv`**: Run-specific record file for each execution.
- **`utils/`**: Directory containing utility functions and modules.
- **`README.md`**: Project documentation.


## License

This project is licensed under the [MIT License](LICENSE).

Explore the documentation to make the most of this Gumtree automation tool for WhatsApp messaging. Use it responsibly and enjoy enhanced efficiency in your Gumtree outreach efforts.
```
