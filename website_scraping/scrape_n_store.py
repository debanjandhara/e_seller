import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag

import os
import json

def save_filename(website, user_id):
    output_folder = f"content/{user_id}/"
    base_url = urlparse(website)
    if base_url:
        filename = output_folder + base_url.netloc + ".json"
    else:
        filename = output_folder + "unknown_domain.json"

    return filename

# Function to remove empty lines from a file
def remove_empty_lines_from_string(text):
    # Split the text into lines
    lines = text.splitlines()

    # Filter out empty lines
    non_empty_lines = [line for line in lines if line.strip()]

    # Rejoin the non-empty lines with newline characters
    cleaned_text = '\n'.join(non_empty_lines)

    return cleaned_text


# Function to scrape a website and save its text to a file
def scrape_and_save(url: str, output_folder: str, max_depth: int, sl_number_list: list, total_number_of_links: int, scraped_websites: set, depth: int = 0, base_url: str = None):

    sl_number = sl_number_list[0]


    if (sl_number>=total_number_of_links):
        return

    if not isinstance(depth, int):
        depth = 0

    if depth > max_depth or url in scraped_websites:
        return

    try:
        # Send an HTTP request and get the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Check for any request errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the text from the webpage
        extracted_text = soup.get_text()

        text = remove_empty_lines_from_string(extracted_text)
        sl_number += 1
        sl_number_list[0] = sl_number


        # Use the base URL or domain name as the file name
        if base_url:
            filename = output_folder + base_url.netloc + ".json"
        else:
            filename = output_folder + "unknown_domain.json"

        # # Save the URL and content to the file
        # with open(filename, 'a', encoding='utf-8') as file:
        #     file.write("\n\nURL: " + url + "\n")
        #     file.write("\nContent: " + text + "\n\n")

        # Create a dictionary to store the data
        data_entry = {
            "sl_number": sl_number,
            "url": url,
            "content": text
        }

        # Create a dictionary with the timestamp and data
        json_data = data_entry

        # Check if the file exists
        if not os.path.exists(filename):
            # File doesn't exist, so write the entire JSON structure
            with open(filename, 'w') as json_file:
                json.dump([json_data], json_file, indent=4)  # Wrap json_data in a list
        else:
            # File exists, so load the existing data and append the new data
            try:
                with open(filename, 'r') as json_file:
                    existing_data = json.load(json_file)
            except FileNotFoundError:
                existing_data = []

            # Append the new data to the existing data
            if isinstance(existing_data, list):
                existing_data.append(json_data)
            else:
                existing_data = [existing_data, json_data]  # Create a list with existing data and new data

            # Save the combined data to the JSON file
            with open(filename, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)


        print(f"Scraped and saved {url}, Count : {sl_number}")

        # Mark the website as scraped
        scraped_websites.add(url)

        depth = depth + 1  # Increment depth here, but after type checking

        # Find and follow hyperlinks from the same domain
        if depth < max_depth:
            for link in soup.find_all('a'):
                if (sl_number>=total_number_of_links):
                    break
                href = link.get('href')
                if href:
                    new_url = urljoin(url, href)

                    # Check if the link doesn't just redirect within the same page
                    if not urldefrag(new_url).fragment:
                        # Check if the link is from the same domain
                        if base_url and urlparse(new_url).netloc == base_url.netloc:
                            scrape_and_save(new_url, output_folder, max_depth, sl_number_list, total_number_of_links, scraped_websites, depth, base_url)

    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")

    return filename

def read_file_to_string(file_path):
    try:
        # Initialize an empty string to store the file contents
        file_contents = ""

        # Open the file and read its contents
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()

        return file_contents
    except FileNotFoundError:
        return "File not found."

def website_to_text(website, user_id, max_depth, total_number_of_links):

    # Folder where you want to store the json files
    # global output_folder
    output_folder = f"data/{user_id}/"

    # Maximum depth for recursion
    # global max_depth
    # max_depth = tree_depth

    # Set to keep track of scraped websites
    # global scraped_websites
    scraped_websites = set()

    # Initializing the Main Counter
    # global sl_number
    sl_number = 0

    sl_number_list = [sl_number]

    # Selecting the Total Number of Lists

    # global total_number_of_links
    # total_number_of_links = max_links
    
    filename = save_filename(website, user_id)
    if os.path.exists(filename):
        os.remove(filename)    

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    base_url = urlparse(website)
    filename = scrape_and_save(website, output_folder=output_folder, max_depth=max_depth, sl_number_list=sl_number_list, total_number_of_links=total_number_of_links, scraped_websites=scraped_websites, depth=0, base_url=base_url)
    return filename

# filename = website_to_text("https://apple.com/", "uuid1234", 100, 10)
# print(filename)