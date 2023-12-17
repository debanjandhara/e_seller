from urllib.parse import urlparse
import os
import requests
import json

def save_filename(website, user_id):
    output_folder = f"data/{user_id}/"
    base_url = urlparse(website)
    if base_url:
        filename = output_folder + base_url.netloc + ".json"
    else:
        filename = output_folder + "unknown_domain.json"

    return filename

def save_filename_filtered(website, user_id):
    output_folder = f"data/{user_id}/"
    base_url = urlparse(website)
    if base_url:
        filename = output_folder + base_url.netloc
    else:
        filename = output_folder + "unknown_domain"

    return filename

def save_only_filename_filtered(website):
    base_url = urlparse(website)
    if base_url:
        filename = base_url.netloc
    else:
        filename = "unknown_domain"

    return filename

def vector_name_find(website, user_id):
    output_folder = f"data/{user_id}/vectors/"
    base_url = urlparse(website)
    if base_url:
        filename = output_folder + base_url.netloc
    else:
        filename = output_folder + "unknown_domain"

    return filename

def upload_document(link, user_id):
    folder_path = f"data/{user_id}/uploads/"
    # Check if the folder exists, create if not
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Extract the file name from the download link
    file_name = os.path.join(folder_path, link.split("/")[-1])

    # Download the file
    response = requests.get(link)
    if response.status_code == 200:
        
        if os.path.exists(file_name):
            # If the file exists, delete it
            os.remove(file_name)
            print(f"Deleted existing file: {file_name}")
        
        # Save the file
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded and saved to {file_name}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

def extract_filename_from_link(link):
    # Parse the download link
    parsed_url = urlparse(link)
    
    # Extract the filename from the path
    filename = os.path.basename(parsed_url.path)

    return filename

def list_folders(directory):
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return json.dumps({"error": "Invalid directory path"})

    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

    result = {"count": len(folders), "folders": {}}

    for index, folder in enumerate(folders, start=1):
        result["folders"][index] = folder

    return json.dumps(result, indent=2)


# download_link = "https://getsamplefiles.com/download/png/sample-1.png"
# filename = extract_filename_from_link(download_link)
# print(f"Extracted filename: {filename}")

