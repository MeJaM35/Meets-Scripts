import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the website
driver.get("https://www.vocabulary.com/lists/1465120")

# Wait for the page to load
time.sleep(5)

# Find the wordlist section
wordlist_section = driver.find_element(By.CLASS_NAME, "wordlist")

# Find all word elements within the wordlist section
words = wordlist_section.find_elements(By.CLASS_NAME, "word")
definitions = wordlist_section.find_elements(By.CLASS_NAME, "definition")

# Extract text from elements
word_list = [word.text for word in words]
definition_list = [definition.text for definition in definitions]

# Debug: Print lengths of the lists
print(f"Number of words: {len(word_list)}")
print(f"Number of definitions: {len(definition_list)}")

# Ensure both lists are of the same length
if len(word_list) == len(definition_list):
    # Create a DataFrame
    data = {'Word': word_list, 'Definition': definition_list}
    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv('vocabulary_words.csv', index=False)
else:
    print("The number of words and definitions do not match.")

# Close the driver
driver.quit()
