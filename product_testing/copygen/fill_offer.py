from rich.console import Console
import json


def select_offer(working_directory, project_code):
    """
    After copywriting.json is generated, user is prompted to select an offer out of five offers.
    The selected offer is then replaced in theme file: settings_data.json
    """
    console = Console()
    copywriting_file_path = f"{working_directory}/{project_code}-copywriting.json"
    settings_json_file_path = f"{working_directory}/theme/config/settings_data.json"

    console.print(
        f"Loading {project_code} copywriting and settings_data files...",
        style="bold cyan",
    )

    with open(copywriting_file_path, "r") as file:
        copywriting = json.load(file)
    offers = copywriting[2]

    for key, value in offers.items():
        console.print(f"{key}:", style="bold red")
        console.print(f"{value}", style="yellow")

    console.print("Please make a selection [1] [2] [3] [4] [5]:", style="bold red")
    selection = input("(Alternatively, enter your own) -->   ")

    with open(settings_json_file_path, "r") as file:
        settings_json_file = json.load(file)

    if len(selection) == 1:
        settings_json_file["current"]["sections"]["header"]["settings"][
            "announcement_text"
        ] = offers[f"offer{selection}"]
        with open(settings_json_file_path, "w") as file:
            json.dump(settings_json_file, file, indent=2, ensure_ascii=False)
        console.print(
            f"Successfully written settings_data.json with offer: [{selection}]",
            style="bold cyan",
        )

    else:
        settings_json_file["current"]["sections"]["header"]["settings"][
            "announcement_text"
        ] = f"{selection}"
        with open(settings_json_file_path, "w") as file:
            json.dump(settings_json_file, file, indent=2, ensure_ascii=False)
        console.print(
            f"Successfully written settings_data.json with offer: {selection}",
            style="bold cyan",
        )
    return
