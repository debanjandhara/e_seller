from pyngrok import ngrok
from flask import Flask, request

from website_scraping.scrape_n_store import website_to_text, read_file_to_string
from website_scraping.sitemap_handling import return_sitemap, read_json_from_file, filter_json_by_sl_number, create_filtered_json_for_vectorise
from website_scraping.utils import *
from website_scraping.token_counter import num_tokens_from_string

from db_store_n_query.vector_create_n_query import *


app = Flask(__name__)

# # Define your function
# def add_numbers(a, b):
#     result = a + b
#     return f"The sum of {a} and {b} is {result}"

# Define an API endpoint for your function
@app.route('/scrape_website', methods=['POST'])
def scrape_and_return_sitemap():
    website = request.args.get('website')
    user_id = request.args.get('user_id')
    max_depth = int(request.args.get('max_depth'))
    total_number_of_links = int(request.args.get('total_number_of_links'))
    # filename = website_to_text(website, user_id, max_depth, total_number_of_links)
    # fetched_entire_website = read_json_from_file(filename)
    # response = return_sitemap(fetched_entire_website)
    response = return_sitemap(read_json_from_file(website_to_text(website, user_id, max_depth, total_number_of_links)))
    return response

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
    response2 = str(num_tokens_from_string(read_file_to_string(create_filtered_json_for_vectorise(filename, filter_json_by_sl_number(sl_numbers, filename)))))
    return response2

@app.route('/create_vector_from_website', methods=['POST'])
def create_vector_from_website():
    website = request.args.get('website')
    user_id = request.args.get('user_id')
    vector_name = vector_name_find(website, user_id)
    content = read_file_to_string(vector_name)
    create_vector(content, vector_name)
    response3 = "created vector"
    return response3


@app.route('/query_vectors', methods=['POST'])
def merge_vectors():
    website = request.args.get('website')
    user_id = request.args.get('user_id')
    query = request.args.get('query')
    response4 = query_from_vector(query, vector_name)
    return response4


# left this one 👇

@app.route('/create_vector_from_document', methods=['POST'])
def create_vector_from_document():
    website = request.args.get('website')
    user_id = request.args.get('user_id')
    sl_numbers = eval(request.args.get('sl_numbers'))
    filename = save_filename(website, user_id)
    response2 = str(num_tokens_from_string(read_file_to_string(create_filtered_json_for_vectorise(filename, filter_json_by_sl_number(sl_numbers, filename)))))
    return response2

@app.route('/merge_vectors', methods=['POST'])
def merge_vectors():
    website = request.args.get('website')
    user_id = request.args.get('user_id')
    sl_numbers = eval(request.args.get('sl_numbers'))
    filename = save_filename(website, user_id)
    response2 = str(num_tokens_from_string(read_file_to_string(create_filtered_json_for_vectorise(filename, filter_json_by_sl_number(sl_numbers, filename)))))
    return response2


# Opening tunnel
public_url = ngrok.connect("5000", "http")

# # Print the public URL
print(f' * ngrok tunnel "{public_url}"')

# Run the Flask app
if __name__ == '__main__':
    app.run()

# import sys

# # print the original sys.path
# print('Original sys.path:', sys.path)

# # append a new directory to sys.path
# sys.path.append('C:\D-Drive\Debanjan\Projects\e_seller\website_scraping')
# sys.path.append('C:\D-Drive\Debanjan\Projects\e_seller\db_store_n_query')

# # print the updated sys.path
# print('Updated sys.path:', sys.path)
