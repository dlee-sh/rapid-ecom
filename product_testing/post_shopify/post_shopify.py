from rich.console import Console
from rich.progress import Progress
from dotenv import load_dotenv
import shopify
import dropbox
import os
import shutil
import base64
import traceback

load_dotenv()


def upload_theme_to_dropbox(local_file_path, project_id):
    """
    Receives a local path to a compressed theme file,
    uploads it to dropbox and returns a raw URL
    """

    # Initialize helpers
    console = Console()

    # Initialize dropbox key and client
    console.print("Initializing Dropbox client...", style="bold cyan")
    DBX_TOKEN = os.getenv("DROPBOX_TOKEN")
    dbx = dropbox.Dropbox(DBX_TOKEN)
    dropbox_path = f"/{project_id}-theme.zip"

    # Read the local file
    with open(local_file_path, "rb") as f:
        file_data = f.read()
    console.print("File read. Uploading to Dropbox...", style="bold cyan")

    # Upload to Dropbox
    response = dbx.files_upload(file_data, dropbox_path)

    # Define the settings for a public link
    link_settings = dropbox.sharing.SharedLinkSettings(
        requested_visibility=dropbox.sharing.RequestedVisibility.public
    )

    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(
        dropbox_path, settings=link_settings
    )
    shareable_link = shared_link_metadata.url.replace("&dl=0", "&dl=1")
    console.print("File successfully uploaded. Resource location:", style="bold cyan")
    console.print(shareable_link, style="blue")

    return shareable_link


def post_shopify(working_directory, store_id, access_token, project_id):
    """
    Requires shop ID and Password
    Takes inputs (theme), (pages)
    Posts Store Pages
    Posts a logo file to pre-emptively link settings_data.json file
    Posts and publishes theme
    Generates a discount code
    """

    console = Console()

    # Initialize the Shopify API
    shop_url = f"{store_id}.myshopify.com"
    api_version = "2023-04"
    console.print(
        f"Connecting to {shop_url} with ShopifyAPI version {api_version}...",
        style="bold cyan",
    )
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)
    console.print(f"Shopify API connection successful.", style="bold cyan")

    # Compressing theme
    console.print(f"Compressing theme directory...", style="bold cyan")
    shutil.make_archive(
        f"{working_directory}/theme", "zip", f"{working_directory}/theme"
    )
    console.print(f"Theme compressed at: {working_directory}")

    # Upload theme to Dropbox
    raw_url = upload_theme_to_dropbox(f"{working_directory}/theme.zip", project_id)
    raw_url = raw_url.replace("https://www", "https://dl")

    # Uploading theme to Shopify
    try:
        console.print(
            f"Attempting to upload theme from {raw_url}...", style="bold cyan"
        )
        new_theme = shopify.Theme()
        new_theme.name = "store-creation-theme"
        new_theme.src = raw_url
        new_theme.role = "main"
        new_theme.save()

        # Check if the theme was uploaded successfully
        if new_theme.errors:
            console.print(
                f"Theme upload failed with errors: {new_theme.errors.full_messages()}",
                style="bold red",
            )
        else:
            console.print(f"Theme uploaded successfully.", style="bold green")

    except Exception as e:
        console.print(f"An error occurred during theme upload: {e}", style="bold red")
        traceback.print_exc()

    with Progress() as progress:
        task = progress.add_task("[cyan] Uploading Pages...", total=7)
        for filename in os.listdir(f"{working_directory}/pages"):
            if filename.endswith(".html"):
                file_path = os.path.join(f"{working_directory}/pages", filename)
                with open(file_path, "r") as file:
                    html_content = file.read()
                    page = shopify.Page()
                    page.title = filename.replace(".html", "")
                    page.body_html = html_content
                    page.save()
                    # trying to test whether NOT printing will fix the status bar.
                    # console.print(f" ✅ Uploaded {filename}", style="bold cyan")
                    progress.update(task, advance=1)

    shopify.ShopifyResource.clear_session()
    return


if __name__ == "__main__":
    working_directory = "/Volumes/dlee-projects/ecom/ecom-media/0024 - Le-Tours"
    store_id = "3d3933-4"
    access_token = "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"
    project_id = "0024"

    post_shopify(working_directory, store_id, access_token, project_id)
