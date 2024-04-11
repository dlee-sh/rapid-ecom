from rich.console import Console
import os
import glob


def create_pages(working_directory, store_name, domain):
    """
    Receives template:page inputs, replaces all the {storename} {domain} {email} placeholders
    Saves for posting to shopify
    """
    console = Console()
    # for file in working directory,
    # regex match all the {storename} {domain} {email placeholders}
    # and replace them with the variables defined
    # then save (within the for loop)

    page_directory = f"{working_directory}/pages"

    for page_path in glob.glob(os.path.join(page_directory, "*.html")):
        with open(page_path, "r", encoding="utf-8") as file:
            page = file.read()

        page = page.replace("${storename}", store_name)
        page = page.replace("${domain}", domain)
        page = page.replace("${email}", f"support@{domain}")

        with open(page_path, "w", encoding="utf-8") as file:
            file.write(page)
        console.print(
            f"Successfully written page: {os.path.basename(page_path)}",
            style="bold cyan",
        )

    return


if __name__ == "__main__":
    create_pages(
        working_directory="/Volumes/dlee-projects/ecom/ecom-media/0022 - test",
        store_name="GlowupBrush",
        domain="glowupbrush.com",
    )
