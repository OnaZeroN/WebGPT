# WebGPT

WebGPT является библиотекой, основанной на OpenAI API и LangChain. Она позволяет без шва подключать ChatGPT к интернету для выполнения запросов и получения актуальной информации.

## Основной класс - `WebGPT`

```python
from web_gpt import WebGPT
```

### Описание

Класс основанный на OpenAi API и LangChain, без шовно подключающий ChatGPT к интернету.

#### Параметры

* `model`: модель чата
* `vector_store_model`: модель, которая будет производить поиск по сайту, рекомендуется "gpt-3.5-turbo-16k"
* `prompt`: инструкция для нейросети о том, как работать с документом, рекомендуется оставить дефолтный
* `urls_count`: количество ссылок, с которых нейросеть возьмет информацию, рекомендуется не более 3
* `search_region`: регион для поиска в интернете, например "ru-ru"

### Методы

#### `ask`

```python
result = await web_gpt.ask([{"role": "user", "content": "Расскажи последние новости в мире"}])
```

##### Описание

Метод класса основанный для запроса к WebGPT. Если для ответа пользователя потребуется информация из интернета, то запустит методы LangChain, иначе WebGPT выдаст обычный ответ.

##### Тип возвращаемого значения

`Dict`

###### Параметры результата

* Если для ответа не потребовался интернет: `{"type": "def", "content": "Ответ"}`
* Если для ответа потребовался интернет: `{"type": "web", "content": "Ответ", "vectorstore": "форматированный источник информации"}`

##### Параметры

* `messages`: список сообщений, подробнее https://platform.openai.com/docs/api-reference/chat


#### `vector_store_asq`

```python
vectorstore_result = await web_gpt.vector_store_asq(old_vectorstore=result["vectorstore"], messages=[{"role": "user", "content": "Расскажи подробнее про <что-то>"}])
```

##### Описание

Метод класса основанный для запроса к уже существующему vectorstore. WebGPT выдаст обычный ответ.

##### Тип возвращаемого значения

`Dict`

###### Параметры результата

* `{"content": "Ответ", "vectorstore": vectorstore}`

##### Параметры

* `old_vectorstore`: форматированный источник информации, который возвращается в методе `ask`
* `messages`: список сообщений, подробнее https://platform.openai.com/docs/api-reference/chat

## Пример использования

```python
from web_gpt import WebGPT

web_gpt = WebGPT(
    model="gpt-3.5-turbo",
    vector_store_model="gpt-3.5-turbo-16k",
    prompt="",
    urls_count=3,
    search_region="ru-ru"
)

result = await web_gpt.ask([{"role": "user", "content": "Расскажи последние новости в мире"}])

if result["type"] == "web":
    vectorstore_result = await web_gpt.vector_store_asq(old_vectorstore=result["vectorstore"], messages=[{"role": "user", "content": "Расскажи подробнее про <что-то>"}])
    print(vectorstore_result["content"])
else:
    print(result["content"])
