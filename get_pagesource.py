import requests
from bs4 import BeautifulSoup

def save_page_source(url, output_file):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request fails
        soup = BeautifulSoup(response.content, 'html.parser')
        page_source = soup.prettify()  # Get the prettified HTML content

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(page_source)
        print(f"Page source saved to {output_file}")
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")

# Example usage:
url_to_crawl = "https://example.com"
output_filename = "example_page_source.txt"
save_page_source(url_to_crawl, output_filename)
