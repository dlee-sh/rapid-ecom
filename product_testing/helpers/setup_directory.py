import shutil


def setup_directory(working_directory):
    """
    When initiating product-testing script, user creates a working directory
    Where the product-description.txt (input for copy-gen) is stored
    Where the copywriting.json output is stored
    Where the logo is stored
    Where the theme files are replicated to and zipped
    """
    print(f"Cloning templates into working directory (path={working_directory})")
    shutil.copytree("../templates/theme", f"{working_directory}/theme")
    shutil.copytree("../templates/pages", f"{working_directory}/pages")
    print("Templates cloned.")
    return


if __name__ == "__main__":
    working_directory = "/Volumes/dlee-projects/ecom/ecom-media/0024 - Le-Tours"
    setup_directory(working_directory)
