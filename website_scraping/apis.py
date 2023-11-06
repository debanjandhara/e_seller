from pyngrok import ngrok
from flask import Flask, request

from scrape_n_store import website_to_text, read_file_to_string
from sitemap_handling import return_sitemap, read_json_from_file, filter_json_by_sl_number, create_filtered_json_for_vectorise
from utils import save_filename
from token_counter import num_tokens_from_string

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

# Opening tunnel
public_url = ngrok.connect("5000", "http")

# # Print the public URL
print(f' * ngrok tunnel "{public_url}"')

# Run the Flask app
if __name__ == '__main__':
    app.run()