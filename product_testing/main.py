from dotenv import load_dotenv
from rich.console import Console
from helpers.setup_directory import setup_directory
from backend.write_dns import write_dns
from backend.generate_pixel import generate_pixel
from copygen.gpt_completions import gpt_completions
from copygen.fill_copy import fill_product_page
from copygen.fill_pixel import add_pixel_theme_liquid
from copygen.fill_offer import select_offer
from post_shopify.post_shopify import post_shopify
from post_shopify.create_pages import create_pages
import os
import json

load_dotenv()
console = Console()

# CONFIG
base_directory = "/Volumes/dlee-projects/ecom/ecom-media"

# INPUTS
store_name = input("Store Name: ")
domain = input("Store Domain: ")
project_code = input("Store Code: ")

working_directory = f"{base_directory}/{project_code} - {store_name}"
os.makedirs(working_directory)
print(f"Instantiated working directory at: {working_directory}")

product_description = input("Describe the product in detail: ")
with open(f"{working_directory}/product_description.txt", "w") as file:
    file.write(product_description)
print("Saved product description as text file.")

# 0. SETUP
setup_directory(working_directory)

if input("Waiting on user to purchase domain, (y/n) to proceed: ") == "y":
    write_dns(os.getenv("CLOUDFLARE_EMAIL"), os.getenv("CLOUDFLARE_API_KEY"), domain)

# 2. PIXEL
pixel_name, pixel_code = generate_pixel(
    app_id=os.getenv("META_APP_ID"),
    app_secret=os.getenv("META_APP_SECRET"),
    access_token=os.getenv("META_LONG_TOKEN"),
    business_id="redacted",
    ad_account_ids=["redacted", "redacted", "redacted"],
    pid=project_code,
    store_name=store_name,
)

# 3. THEME: COPY
copywriting_master = gpt_completions(
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"), product_description=product_description
)
copywriting = [json.loads(obj) for obj in copywriting_master]
# Save copywriting outputs to outputs folder
copywriting_file_path = f"{working_directory}/{project_code}-copywriting.json"
with open(copywriting_file_path, "w") as file:
    json.dump(copywriting, file, indent=2, ensure_ascii=False)
# Replace product.json with copywriting
fill_product_page(copywriting_file_path, working_directory, store_name)

# 4. THEME: PIXEL
# Replace hash with pixel code
add_pixel_theme_liquid(working_directory, pixel_code)

# 5. THEME: OFFER
select_offer(working_directory, project_code)

# 6. PAGES
create_pages(working_directory, store_name, domain)

# 7. POST TO SHOPIFY
console.print("Waiting on user to create a Shopify store...", style="bold light_coral")
console.print(
    "Be sure to enable read/write theme & pages access scopes", style="light_coral"
)
store_id = input("Store ID: ")
access_token = input("Access Token: ")

post_shopify(
    working_directory, store_id, access_token, domain, store_name, project_code
)

console.print("💗💗💗 Store creation complete 💗💗💗", style="bold sea_green2")
