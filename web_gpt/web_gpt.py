# -*- coding: utf-8 -*-
import asyncio
import json
import re

from web_gpt.open_ai_helper import OpenAiHelper
from web_gpt.langchain_helper import LangChainHelper


class WebGPT(OpenAiHelper, LangChainHelper):
    def __init__(
            self,
            model: str = "gpt-3.5-turbo",
            vector_store_model: str = "gpt-3.5-turbo-16k",
            prompt: str = """
                Используйте следующие фрагменты контекста, чтобы ответить на вопрос в конце. 
                Инструкции:
                 - Внимательно вчитайся в документ и проанализируй его полностью вникнув в его смысл.
                 - Проведи герменевтический анализ, исследуя в глубину текстовые и контекстуальные слои документа.
                 - Отвечай на вопрос максимально подробно на вопрос пользователя, настолько насколько позволяет контекст.
                 - Если вы не знаете ответа, просто скажите, что вы не знаете, не пытайтесь придумать ответ. 
                 - Приводи фрагменты контекста откуда ты взял информацию.
                 - Отвечай всегда в виде маркировочного списка.
                 - Изучи документ, проникнись его сущностью, выяви скрытые смыслы и подтекст. 
                 - Отвечай только на Русском языке, даже если контекст на английском. 
                {context}
            """,
            urls_count: int = 1,
            search_region: str = "ru-ru"
    ):
        """
        Класс основанный на OpenAi API и LangChain, без шовно подключающий ChatGPT к интернету
        :param model: модель чата
        :param vector_store_model: модель которая будет производить поиск по сайту, рекомендуется "gpt-3.5-turbo-16k"
        :param prompt: инструкция для нейросети о том как работать с документом, рекомендуется оставить дефолтный
        :param urls_count: количество ссылок с которых нейросеть возьмет информацию, рекомендуется не более 3
        :param search_region: регион для поиска в интернете, например "ru-ru"
        """
        self.urls_count = urls_count
        self.messages = None
        self.open_ai_key = self.get_open_ai_key()
        self.loop = asyncio.get_event_loop()
        self.prompt = prompt
        OpenAiHelper.__init__(self, model)
        LangChainHelper.__init__(self, vector_store_model, search_region)
        self.open_ai_key = self.get_open_ai_key()

    async def ask(self, messages: list):
        """
        Метод Класса основанный для запроса к WebGPT, если для ответа пользователя потребуется информация из интернета, то запустит методы LangChain, иначе
        WebGPT выдаст обычный ответ

        Ответ возвращается в виде dict:
        Если для ответа не потребовался интернет: {"type": "def", "content": "Ответ"}
        Если для ответа потребовался интернет: {"type": "web", "content": "Ответ", "vectorstore": "форматированный источник информации"}

        :param messages: список сообщений, подробнее https://platform.openai.com/docs/api-reference/chat
        """
        self.messages = messages
        chat_completion = await self.chat_completion(messages=self.messages)
        try:
            if chat_completion["choices"][0]["message"]["content"] is not None:
                return {"type": "def", "content": chat_completion["choices"][0]["message"]["content"]}
            llm_answer = await self.vector_store_asq(json.loads(chat_completion["choices"][0]["message"]["function_call"]["arguments"])["query"])
            return {"type": "web", "content": llm_answer["content"], "vectorstore": llm_answer["vectorstore"]}
        except Exception as e:
            raise Exception(e)

    async def vector_store_asq(self, query=None, old_vectorstore=None, messages: list = None):
        """
        Метод Класса основанный для запроса к уже существующему vectorstore
        WebGPT выдаст обычный ответ

        Ответ возвращается в виде dict:
        {"content": "Ответ", "vectorstore": vectorstore}

        :param old_vectorstore: форматированный источник информации, который возвращается в методе ask
        :param messages: список сообщений, подробнее https://platform.openai.com/docs/api-reference/chat
        """
        template = self.prompt
        if old_vectorstore is None:
            query = await self.find_links(query)
            if len(query["text"]) < 2:
                query["text"] = "Очень подробно суммаризируй эту статью"
            vector_data = await self.create_index(query)
            vectorstore = vector_data[0]
            old_vectorstore = vector_data[1]
            last_query = query["text"]
            template += "\n\nВопрос пользователя: {question}\nОтвет полезного помощника, который следует инструкциям:"
        else:
            vectorstore = (await self.create_index(all_splits=old_vectorstore))[0]
            self.messages = messages
            if len(self.messages) > 1:
                for message in self.messages[:-1]:
                    if message["role"] == "user":
                        template += f"Вопрос пользователя: {message['content']}"
                    else:
                        template += f"Ответ полезного помощника, который следует инструкциям: {message['content']}"
            template += "Вопрос пользователя: {question}\nОтвет полезного помощника, который следует инструкциям:"
            last_query = self.messages[-1]["content"]

        result = await self.llm_asq(template=template, vectorstore=vectorstore, last_query=last_query)

        return {"content": result["result"], "vectorstore": old_vectorstore}

    @staticmethod
    async def find_links(text):
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        matches = re.findall(pattern, text)
        if len(matches) != 0:
            return {"text": text.replace(matches[0], ""), "url": matches[0]}
        return {"text": text, "url": None}
