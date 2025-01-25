import json

import httpx
from rich.console import Console
from rich.markdown import Markdown

class Client:

    def __init__(self, api_key: str):
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4o-mini"
        self.api_key = api_key


    def build_req(self, query: str) -> str:
        """
        Build a request that specifies specific context for the chatbot.
        :param query: query passed in by the user.
        :return: return dict to be passed in to post request
        """
        return json.dumps({
            "model": self.model,
            "messages": [
                {
                 "role": "developer",
                 "content": "You are a helpful assistant. Be concise always. Avoid providing similar answers."
                },
                {
                 "role": "user",
                 "content": query
                }
            ]
        })

    def build_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def get_content_from_response(response_data: dict) -> str:
        """

        :param response_data:
        :return:
        """
        return json.loads(response_data["choices"][0]["message"]["content"])


    def send_query(self, query: str) -> dict:
        """
        Send a query to the openai chat completions api, the query should be treated as the message content that will
        be part of the request
        :param query:
        :return:
        """
        http_client: httpx.Client = httpx.Client()
        console = Console()
        with http_client.stream(method='POST', url=self.base_url, data=self.build_req(query), headers=self.build_headers()) as response:
            for chunk in response.iter_text():
                console.print(Markdown(json.loads(chunk)["choices"][0]["message"]["content"]))
                return json.loads(chunk)
