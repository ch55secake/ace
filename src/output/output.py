from rich.live import Live
from rich.markdown import Markdown


def display_stream_as_markdown(response_stream: str) -> None:
    """
    Outputs the stream as markdown.
    """
    full_response = ""
    with Live(auto_refresh=True) as live:
        for chunk in response_stream:
            full_response += chunk
            live.update(Markdown(full_response))

    return full_response

def display_stream_as_raw_text(response_stream: dict) -> None:
    """
    Outputs the stream as raw text. Will still have some Markdown syntax.
    """
    full_response = ""
    with Live(auto_refresh=True) as live:
        for chunk in response_stream:
            full_response += chunk
            live.update(Markdown(full_response))

    return full_response
