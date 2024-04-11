from rich.console import Console


def add_pixel_theme_liquid(working_directory, pixel_code):
    """
    Receives a working directory where the theme.liquid file is contained
    Replaces the placeholder hash with the provided pixel code
    """
    console = Console()
    console.print("Opening theme.liquid...", style="bold cyan")
    theme_liquid_path = f"{working_directory}/theme/layout/theme.liquid"
    # Read the content of the theme.liquid file
    with open(theme_liquid_path, "r") as file:
        theme_liquid = file.read()

    # Replace the placeholder hash with the new code snippet
    placeholder = "03dc8cb268d33b11f8f5f4d879b65434c0ae2840"

    if theme_liquid.find(placeholder) == -1:
        console.print(
            "Hash not identified. Please double check theme.liquid. Exiting process...",
            style="bold cyan",
        )
        exit(0)
    else:
        console.print("Hash identified. Proceeding to fill...", style="bold cyan")

    updated_theme_liquid = theme_liquid.replace(placeholder, pixel_code)
    console.print("Updating hash with pixel now", style="bold cyan")

    # Write the updated content back to the file
    with open(theme_liquid_path, "w") as file:
        file.write(updated_theme_liquid)
    console.print(
        "Theme.liquid successfully updated with pixel code", style="bold cyan"
    )
    return
