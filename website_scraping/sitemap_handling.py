# from website_scraping.scrape_n_store import website_to_text

import json
import os

# filename = website_to_text("https://apple.com/", "uuid1234", 10, 5)

def read_json_from_file(filename):
    with open(filename, 'r') as json_file:
        json_data = json.load(json_file)
    return json_data

# fetched_entire_website = read_json_from_file(filename)

def return_sitemap(data):

    # Extract only "sl_number" and "url" from each entry
    slno_and_url = [{"sl_number": entry["sl_number"], "url": entry["url"]} for entry in data]

    # Create a JSON with the extracted information
    result_json = json.dumps(slno_and_url, indent=4)

    return result_json

def filter_json_by_sl_number(sl_numbers, filename):
    try: 

        # Parse the JSON data
        data = read_json_from_file(filename)

        # Initialize a list to store the filtered objects
        filtered_objects = []

        # Iterate through the data and filter by sl_number
        for entry in data:
            if "sl_number" in entry and entry["sl_number"] in sl_numbers:
                filtered_objects.append(entry)

        return filtered_objects
    except Exception as e:
        return f"Error: {str(e)}"

# # List of sl_numbers to filter
# sl_numbers_to_filter = [1, 3]



def create_filtered_json_for_vectorise(filename, filtered_json):

    # Split the filename into base and extension
    base, extension = os.path.splitext(filename)

    # Add ".filtered" before the extension
    filename_filtered = base + ".filtered" + extension

    # Open the file for writing and save the JSON variable to it
    with open(filename_filtered, "w") as json_file:
        json.dump(filtered_json, json_file, indent=4)

    return filename_filtered

# # filename_filtered = create_filtered_json_for_vectorise(filename, filter_json_by_sl_number(sl_numbers_to_filter))