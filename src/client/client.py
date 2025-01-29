import json

import httpx
import rich
from httpx import Response


class Client:

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.model = model
        self.api_key = api_key


    def build_req(self, query: str) -> str:
        """
        Build a request that specifies specific context for the chatbot.
        :param query: query passed in by the user.
        :return: return dict to be passed in to post request
        """
        if "o1" in self.model:
            return json.dumps({
                "model": self.model,
                "messages": [{
                    "role": "user",
                    "content": query,
                }]
            })
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
            ],
            "stream": True
        })

    def build_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }


    def send_query(self, query: str) -> str:
        """
        Send a query to the openai chat completions api, the query should be treated as the message content that will
        be part of the request
        :param query: the query passed in by the user.
        :return: the response content as a stream to be handled by the output methods.
        """
        http_client: httpx.Client = httpx.Client()
        with http_client.stream(method='POST', url=self.base_url, data=self.build_req(query), headers=self.build_headers(), timeout=None) as response:
            for chunk in response.iter_text():
                if chunk.strip():
                    for line in chunk.splitlines():
                        if line.strip() == "data: [DONE]":
                            break

                        if line.startswith("data: "):
                            try:
                                yield from self.parse_and_get_data(json_data=line[6:])
                            except json.JSONDecodeError as e:
                                rich.print(f"[bold red]Failed to parse json:[/bold red] {e}")

    @staticmethod
    def parse_and_get_data(json_data) -> str:
        """
        Parse the json data into a stream to be handled by the output methods.
        :param json_data: the json data to be parsed.
        """
        parsed_data: dict = json.loads(json_data)
        content: str = parsed_data.get("choices", [{}])[0].get("delta", {}).get("content", "")
        if content:
            yield content

    def get_available_list_of_models(self) -> list[str]:
        """
        Fetch available list of models for usage
        """
        http_client: httpx.Client = httpx.Client()
        response: Response = http_client.get(url="https://api.openai.com/v1/models", headers=self.build_headers())
        available_list_of_models: list[str] = []
        if response.status_code == 200:
            resp_dict = response.json()["data"]
            available_list_of_models.extend(key["id"] for key in resp_dict if key["owned_by"] in ["openai", "system"])
        return available_list_of_models
