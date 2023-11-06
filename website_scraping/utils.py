from urllib.parse import urlparse

def save_filename(website, user_id):
    output_folder = f"content/{user_id}/"
    base_url = urlparse(website)
    if base_url:
        filename = output_folder + base_url.netloc + ".json"
    else:
        filename = output_folder + "unknown_domain.json"

    return filename
