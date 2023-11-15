from urllib.parse import urlparse

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
        filename = output_folder + base_url.netloc + ".filtered.json"
    else:
        filename = output_folder + "unknown_domain.filtered.json"

    return filename

def vector_name_find(website, user_id):
    output_folder = f"data/{user_id}/vectors/"
    base_url = urlparse(website)
    if base_url:
        filename = output_folder + base_url.netloc + ".filtered.json"
    else:
        filename = output_folder + "unknown_domain.filtered.json"

    return filename
