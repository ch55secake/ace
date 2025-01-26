import json

import httpx
from requests import Response


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
        return response_data["choices"][0]["message"]["content"]


    def send_query(self, query: str) -> dict:
        """
        Send a query to the openai chat completions api, the query should be treated as the message content that will
        be part of the request
        :param query:
        :return:
        """
        http_client: httpx.Client = httpx.Client()
        with http_client.stream(method='POST', url=self.base_url, data=self.build_req(query), headers=self.build_headers(), timeout=None) as response:
            for chunk in response.iter_text():
                print(chunk)
                return json.loads(chunk)


    def get_available_list_of_model(self) -> list[str]:
        """

        """
        http_client: httpx.Client = httpx.Client()
        response: Response = http_client.get(url="https://api.openai.com/v1/models", headers=self.build_headers())
        available_list_of_models: list[str] = []
        if response.status_code == 200:
            resp_dict = response.json()["data"]
            available_list_of_models.extend(key["id"] for key in resp_dict if key["owned_by"] in ["openai", "system"])
        return available_list_of_models
