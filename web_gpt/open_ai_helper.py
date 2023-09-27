import os
import openai


class OpenAiHelper:
    def __init__(self, model: str):
        self.model = model
        self.functions = [
                {
                    "name": "internet_search",
                    "description": "Функция для нахождения информации в интернете, ее надо вызывать когда для ответа юзера требуется актуальная информация из интернета",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Запрос в интернет, если в запросе есть ссылка, то передавай сообщение юзера БЕЗ изменений"
                            }
                        },
                        "required": ["properties"],
                    },
                }
            ]

    async def chat_completion(self, messages):
        openai.api_key = self.get_open_ai_key()
        return await openai.ChatCompletion.acreate(
            model=self.model,
            messages=messages,
            functions=self.functions
        )

    @staticmethod
    def get_open_ai_key():
        open_ai_key = os.getenv("OPENAI_API_KEY")
        if open_ai_key is not None:
            return open_ai_key
        else:
            raise Exception("""
    The environment variable Open AI API key is not set
    Information on how to get the API key can be found here
    https://platform.openai.com/docs/api-reference/
    For easy installation of the Open AI API key in environment variable:
    os.environ['OPENAI_API_KEY'] = "api_key"
                """)
