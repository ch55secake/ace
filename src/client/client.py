from dataclasses import dataclass
import requests as req


# @dataclass
# class OpenAIResponse:
#
#     model: str
#     choices: dict
#
#     @property
#     def model(self) -> :

@dataclass
class Request:

    model: str
    messages: list[dict]

    @property
    def model(self) -> str:
        return self.model

    @property
    def get_content(self) -> str:
        """
        Get the content of the message that you are about to send.
        :return: a string of the message content that you have sent
        """
        return self.messages[1]["content"]

    @classmethod
    def build_req(cls, query: str) -> dict[str, list[dict]]:
        """
        Build a request that specifies specific context for the chatbot.
        :param query: query passed in by the user.
        :return: return dict to be passed in to post request
        """
        return {
            "model": cls.model,
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
        }

class Client:

    def __init__(self, api_key: str):
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.api_key = api_key


    def send_query(self, query: str) -> dict:
        """
        Send a query to the openai chat completions api, the query should be treated as the message content that will
        be part of the request
        :param query:
        :return:
        """
        req.post(self.base_url, data={"query": query})
