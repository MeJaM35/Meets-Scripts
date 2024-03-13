import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

SCROLL_PAUSE_TIME = 10

class LinkedIn:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_argument('--incognito')
        self.browser = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.browser, 10)

    def login(self, username, password):
        self.browser.get('https://linkedin.com')
        self.wait.until(EC.presence_of_element_located((By.ID, "session_key")))
        username_element = self.browser.find_element(By.ID, "session_key")
        username_element.send_keys(username)
        password_element = self.browser.find_element(By.ID, "session_password")
        password_element.send_keys(password)
        login_button = self.browser.find_element(By.CLASS_NAME, "sign-in-form__submit-btn--full-width")
        login_button.click()

    def get_recent_activity(self, profile_url):
        self.browser.get(profile_url)
        try:
            last_height = self.browser.execute_script("return document.body.scrollHeight")
            while True:
                # Scroll down to bottom
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

                elements = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'feed-shared-update-v2__description-wrapper')))
                return [element.text for element in elements]
        except Exception as e:
            print(f"An error occurred while retrieving recent activity for {profile_url}: {e}")
            return []

        finally:
            self.browser.get("https://www.linkedin.com/feed/")  # Navigate back to the feed to avoid potential issues with LinkedIn

    def close(self):
        self.browser.close()

if __name__ == "__main__":
    linkedin = LinkedIn()

    # Replace 'urls.csv' with the name of your CSV file containing URLs
    with open('users.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            url = row[0]
            linkedin.login("add_ur_email", "add_ur_pwd")
            activity = linkedin.get_recent_activity(url)
            linkedin.close()

            # Check if the file exists and open it in append mode if it does, or write mode if it doesn't
            file_exists = open('BB.csv', 'a').close()

            with open('BB.csv', 'a', newline='', encoding='utf-8') as output_file:
                writer = csv.writer(output_file)
                if not file_exists:
                     writer.writerow(["Recent Activity"])
        for row in activity:
            writer.writerow([row])

    print("Recent activity data has been written to BB.csv")