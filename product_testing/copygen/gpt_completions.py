from openai import OpenAI
from rich.progress import Progress
from rich.console import Console
import json


def gpt_completions(OPENAI_API_KEY, product_description):
    """
    Returns an array "Responses" containing key-value pairs for GPT-4 copywriting completions
    """
    console = Console()

    # prompts
    prompt_path = "../templates/llm-prompts.json"
    with open(prompt_path, "r") as file:
        prompts = json.load(file)

    # initialize
    client = OpenAI(api_key=OPENAI_API_KEY)
    console.print("OpenAI API Client Successfully Intialized...", style="bold cyan")

    responses = []

    with Progress() as progress:
        task = progress.add_task("[cyan]Writing Copy...", total=len(prompts))

        for key, prompt in prompts.items():
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                response_format={"type": "json_object"},
                temperature=0.0,
                messages=[
                    {
                        "role": "system",
                        "content": f"{prompt['system']}",
                    },
                    {
                        "role": "user",
                        "content": f"{product_description}\n{prompt['task']}\nReturn a JSON without a parent array: {prompt['validation']}",
                    },
                ],
            )

            console.print(f" ✅ {key}s written", style="bold cyan")
            output = response.choices[0].message.content
            responses.append(output)
            progress.update(task, advance=1)

    return responses
