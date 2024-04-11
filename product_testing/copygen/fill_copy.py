import json
from rich.console import Console


def fill_product_page(copywriting_json, working_directory, store_name):
    console = Console()

    # Load the prefill copywriting json file
    with open(copywriting_json, "r") as file:
        copywriting = json.load(file)
    console.print("... Copywriting JSON imported successfully", style="bold cyan")

    # Load the product page json file:
    product_template = f"{working_directory}/theme/templates/product.json"
    with open(product_template, "r") as file:
        product_page = json.load(file)
    console.print("... Product Page JSON imported successfully", style="bold cyan")

    sections = product_page["sections"]

    ### BENEFITS ###
    beneft_section_titles = [
        "text-and-image",
        "06a32a55-d23d-4eca-9650-049df523b259",
        "a6255fd5-01ed-420d-92a8-4737ac12c024",
        "3cd1f24c-46cf-499c-9264-85ba49111504",
        "3eb54d88-3a1e-4806-b0b4-c9ed077bbcff",
    ]

    for i, section_title in enumerate(beneft_section_titles):
        sections[section_title]["settings"]["title"] = copywriting[0][f"headline{i+1}"]
        sections[section_title]["settings"][
            "text"
        ] = f"<p>{copywriting[0][f'description{i+1}']}</p>"

    console.print("... Benefits written.", style="bold cyan")

    ### TESTIMONIALS ###
    testimonial_location = sections["d8146d07-df59-4515-8844-7480369d0fd3"]["blocks"]
    testimonial_section_title_base = "template--18925686063390__d8146d07-df59-4515-8844-7480369d0fd3-1684129146a6d0f84c-"

    i = 0
    while i < 5:
        testimonial_location[f"{testimonial_section_title_base}{i}"]["settings"][
            "testimonial"
        ] = f"<p>{copywriting[6][f'testimonial{i+1}']}</p>"
        testimonial_location[f"{testimonial_section_title_base}{i}"]["settings"][
            "author"
        ] = copywriting[6][f"author{i+1}"]
        i += 1

    console.print("... Testimonials written.", style="bold cyan")

    ### FAQS ###
    faq_location = sections["c41ec2e9-1e31-446e-8d7e-f7616265fdb6"]
    faq_section_titles = [
        "747bf1df-f3fd-4fb0-a589-8bf23261ea69",
        "7218453b-9f84-486b-a4b9-c38f3264d433",
        "678bc910-cc96-466e-b21c-a696b0b14275",
        "f5e94919-1bb6-4bc7-96c9-cbd22ce80016",
        "5e2d5e86-4a4c-44a8-98bf-751f655f6271",
        "c1219372-6907-40c4-b5ec-be1f7f407394",
        "6712ad4a-cb9b-4b34-b0ff-35a2aaa5c6cc",
        "79e912e1-f412-4a4b-9bf1-e66a797f177b",
        "eb93fcdf-e9e7-48e8-9288-d30bf778fda1",
    ]

    for i, section_title in enumerate(faq_section_titles):
        faq_location["blocks"][section_title]["settings"]["title"] = copywriting[5][
            f"question{i+1}"
        ]
        faq_location["blocks"][section_title]["settings"][
            "text"
        ] = f"<p>{copywriting[5][f'answer{i+1}']}</p>"

    # Change the FAQ heading
    faq_location["settings"]["title"] = f"{store_name} FAQs"

    console.print("... FAQs written.", style="bold cyan")

    # Write the file
    with open(product_template, "w") as file:
        json.dump(product_page, file, indent=2, ensure_ascii=False)
    console.print("... Product JSON updating complete.", style="bold cyan")

    return
