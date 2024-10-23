import requests
from bs4 import BeautifulSoup

# Base URL for OpenHoldem documentation
base_url = "https://documentation.help/OpenHoldem/"

# Open a text file to write the content
with open('OpenHoldem_Documentation.txt', 'w', encoding='utf-8') as file:

    # Send a request to the introduction page
    response = requests.get(base_url + "introduction.html")
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links to other sections in the documentation
    links = soup.find_all('a')

    # Extract the hrefs (links) of all the sections
    for link in links:
        href = link.get('href')
        if href:  # Ensure href exists
            section_url = base_url + href
            print(f"Scraping: {section_url}")
            section_response = requests.get(section_url)
            section_soup = BeautifulSoup(section_response.text, 'html.parser')
            # Extract the content from each section and write to file
            file.write(section_soup.get_text())
            file.write("\n\n---\n\n")  # Add separator between sections