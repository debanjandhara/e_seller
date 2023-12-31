from pyngrok import ngrok
from flask import Flask, request
import json

from website_scraping.scrape_n_store import website_to_text, read_file_to_string
from website_scraping.sitemap_handling import return_sitemap, read_json_from_file, filter_json_by_sl_number, create_filtered_json_for_vectorise
from website_scraping.utils import *
from website_scraping.token_counter import num_tokens_from_string

from db_store_n_query.vector_create_n_query import *

# ngrok.set_auth_token("2ZUwGNURTLVLJ75FsAXvZ9KiSqV_6AmeZ1JrwQTk3jmAkFAuP")

app = Flask(__name__)

# # Define your function
# def add_numbers(a, b):
#     result = a + b
#     return f"The sum of {a} and {b} is {result}"

@app.route('/')
def hello_world():
    return 'Hello, World!'


# Define an API endpoint for your function
@app.route('/scrape_website', methods=['POST'])
def scrape_and_return_sitemap():
    website = request.args.get('website')
    user_id = request.args.get('user_id')
    # max_depth = int(request.args.get('max_depth'))
    max_depth = 1000
    total_number_of_links = int(request.args.get('total_number_of_links'))
    filename = website_to_text(website, user_id, max_depth, total_number_of_links)
    print(filename)
    fetched_entire_website = read_json_from_file(filename)
    response = return_sitemap(fetched_entire_website)
    # response = return_sitemap(read_json_from_file(website_to_text(website, user_id, max_depth, total_number_of_links)))
    return json.loads(response)

# From a selected list of sitemaps, tells the number of token used
@app.route('/get_tokens', methods=['POST'])
def return_no_of_tokens_from_selection():
    website = request.args.get('website')
    user_id = request.args.get('user_id')
    sl_numbers = eval(request.args.get('sl_numbers'))
    filename = save_filename(website, user_id)
    # filtered_json = filter_json_by_sl_number(sl_numbers, filename)
    # filename_filtered = create_filtered_json_for_vectorise(filename, filtered_json)
    # string_for_token_count = read_file_to_string(filename_filtered)
    # response2 = str(num_tokens_from_string(string_for_token_count))
    response2 = int(num_tokens_from_string(read_file_to_string(create_filtered_json_for_vectorise(filename, filter_json_by_sl_number(sl_numbers, filename)))))
    json_response = json.dumps({"result": response2})
    print(type(json_response))
    return json.loads(json_response)

@app.route('/get_tokens_docs', methods=['POST'])
def return_no_of_tokens_from_docs():
    filename = request.args.get('filename')
    user_id = request.args.get('user_id')
    link = request.args.get('link')
    if link is not None:
        filename = extract_filename_from_link(link)
    print(filename)
    file_with_path = f"data/{user_id}/uploads/{filename}"
    print(file_with_path)
    content = read_document(file_with_path)
    response2 = int(num_tokens_from_string(content))
    json_response = json.dumps({"result": response2})
    return json.loads(json_response)


@app.route('/create_vector_from_website', methods=['POST'])
def create_vector_from_website():
    website = request.args.get('website')
    user_id = request.args.get('user_id')
    filename_filtered = save_filename_filtered(website, user_id)
    print("file to be vectorised --> ",filename_filtered)
    content = read_file_to_string(filename_filtered)
    vector_folder_name = vector_name_find(website, user_id)
    create_vector(content, vector_folder_name)
    # response3 = vector_folder_name
    response = "success"
    json_response = json.dumps({"result": response})
    return json.loads(json_response)

@app.route('/upload_documents', methods=['POST'])
def upload_documents():
    link = request.args.get('link')
    user_id = request.args.get('user_id')
    upload_document(link, user_id)
    response = "success"
    json_response = json.dumps({"result": response})
    return json.loads(json_response)

@app.route('/create_vector_from_document', methods=['POST'])
def create_vector_from_document():
    filename = request.args.get('filename')
    user_id = request.args.get('user_id')
    link = request.args.get('link')
    if link is not None:
        filename = extract_filename_from_link(link)
    file_with_path = f"data/{user_id}/uploads/{filename}"
    content = read_document(file_with_path)
    create_vector(content, f"data/{user_id}/vectors/{filename}")
    # response = f"data/{user_id}/vectors/{filename}"
    response = "success"
    json_response = json.dumps({"result": response})
    return json.loads(json_response)


@app.route('/merge_vectors', methods=['POST'])
def merge_vectors():
    user_id = request.args.get('user_id')
    response2 = merge_db(user_id)
    json_response = json.dumps({"result": response2})
    return json.loads(json_response)

@app.route('/list_all_vector', methods=['POST'])
def list_all_vector():
    user_id = request.args.get('user_id')
    folder_path = f"data/{user_id}/vectors/"
    json_response = list_folders(folder_path)
    return json.loads(json_response)

@app.route('/delete_specific_vector', methods=['POST'])
def delete_specific_vector():
    user_id = request.args.get('user_id')
    link = request.args.get('link')
    filename = request.args.get('filename')
    website = request.args.get('website')
    if link is not None:
        filename = extract_filename_from_link(link)
    if website is not None:
        filename = save_only_filename_filtered(website)
    folder_path = f"data/{user_id}/vectors/{filename}"
    response2 = delete_folder(folder_path)
    json_response = json.dumps({"result": response2})
    return json.loads(json_response)


@app.route('/query_vectors', methods=['POST'])
def query_vector():
    user_id = request.args.get('user_id')
    query = request.args.get('query')
    response4 = query_from_vector(query, user_id)
    json_response = json.dumps({"result": response4})
    return json.loads(json_response)


# # # Opening tunnel
# public_url = ngrok.connect("5000", "http")

# # # Print the public URL
# print(f' * ngrok tunnel "{public_url}"')

# Run the Flask app
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080)
    app.run()
