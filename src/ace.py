from typing import Annotated

import rich
import typer as t

from src.client.client import Client
from src.config.config import does_config_file_exist, get_config
from src.config.config import initialize_config
from src.output.output import display_stream_as_markdown

app: t.Typer = t.Typer()

@app.command(help="Write a new configuration path to the path provided. If a path is not provided it will default to $HOME/.config/."
                  "It will create a new yaml file which stores your api key.",
             short_help="Create a new configuration file at $HOME/.config/")
def init(api_key: Annotated[str, t.Argument()], filepath: Annotated[str, t.Option()] = f".config/ace/config.yaml"):
    if not does_config_file_exist(filepath):
        initialize_config(api_key=api_key)


@app.command(help="Send a request to the OpenAI api and ask a model a question. Will return the answer formatted as markdown",
             short_help="Ask the model a question")
def ask(query: Annotated[str, t.Argument()], model: Annotated[str, t.Option()] = "gpt-4o"):
    api_key: str = get_config().api_key
    open_api_client: Client = Client(api_key=api_key, model=model)
    query_response: str = open_api_client.send_query(query=query)
    display_stream_as_markdown(query_response)


@app.command(help="Get the available list of models that you can use from the OpenAI API.",
             short_help="Fetch a list of available models.")
def models() -> None:
    api_key: str = get_config().api_key
    open_api_client: Client = Client(api_key=api_key)
    available_models: list[str] = open_api_client.get_available_list_of_models()
    rich.print("[bold]Here is the list of models currently supported by open ai:[/bold]")
    for model in available_models:
        rich.print(f" - [bold green]{model}[/]")

@app.callback()
def callback() -> None:
    """

    Query various OpenAI models from the command line.

    Formats answers in markdown to the terminal.

    Use any model of your choice from the API.

    """

def main():
   app()

if __name__ == "__main__":
    main()
