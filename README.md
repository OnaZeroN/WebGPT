# WebGPT

WebGPT is a library based on the Openal API and Long Chain. It allows you to connect ChatGPT to the Internet without a seam to make requests and receive responses with up-to-date information.

If the user's response requires information from the Internet, it will launch Long Chain methods, otherwise WebGPT will give a normal response from ChatGPT

You can also throw off the link (you can do it together with the signature of what to do) and it will work on this link.

A repository is attached to the response, which can be inserted into the parameters and continue the dialogue on this site

## Usage
Simple Usage

```python
import os
import asyncio

from web_gpt import WebGPT

os.environ['OPENAI_API_KEY'] = "openai_api_key"


async def exaple():
    web_gpt = WebGPT()
    result = await web_gpt.ask([{"role": "user", "content": "Расскажи последние новости в тюмени"}])
    print(result["content"])

asyncio.run(exaple())
```

Requests to the processed site

```python
import os
import asyncio

from web_gpt import WebGPT

os.environ['OPENAI_API_KEY'] = "openai_api_key"


async def exaple():
    web_gpt = WebGPT()
    result = await web_gpt.ask([{"role": "user", "content": "Tell us the latest news in the world of neural networks"}])
    print(result["content"])
    if result["type"] == "web":
        vectorstore_result = await web_gpt.vector_store_asq(old_vectorstore=result["vectorstore"], messages=[{"role": "user", "content": "Tell me more about <something>"}])
        print(vectorstore_result["content"])

asyncio.run(exaple())
```

# Detailed description

## Class WebGPT 

### Params

* `model`: chat model
* `vector_store_model`: the model that will search the site is recommended "gpt-3.5-turbo-16k"
* `prompt`: instructions for the neural network on how to work with the document, you must add {context} to the end, it is recommended to leave the default
* `urls_count`: the number of links from which the neural network will take information, it is recommended no more than 3
* `search_region`: the region to search on the Internet, for example "ru-ru"

### Methods

### ask

```python
result = await web_gpt.ask([{"role": "user", "content": "https://openai.com/gpt-4 summarize this article"}])
```

##### Description

A class method based on a request to Web GT. If the user's response requires information from the Internet, it will launch Long Chain methods, otherwise WebGPT will give a normal response.

##### Return `Dict`

###### Result Parameters

* If the Internet was not required for the response: `{"type": "def", "content": "Response"}`
* If the response required the Internet: `{"type": "web", "content": "Response", "vectorstore": "formatted information source"}`

##### Parameters

* `messages`: list of messages, more details https://platform.openai.com/docs/api-reference/chat





### vector_store_asq

```python
vectorstore_result = await web_gpt.vector_store_asq(old_vectorstore=result["vectorstore"], messages=[{"role": "user", "content": "Tell me more about <something>"}])
```

##### Description

A method of the class based on a request to an already existing vectorstore. WebGPT will give a normal response.

##### Return `Dict`

###### Result Parameters

* `{"content": "answer", "vectorstore": vectorstore}`

##### Parameters

* `old_vectorstore`: the formatted source of information that is returned in the method `ask`
* `messages`: list of messages, more details https://platform.openai.com/docs/api-reference/chat

# Issues

In this version of the project, token counting does not work yet, this will definitely be added in future versions.

# Contacts

- Telegram https://t.me/onazeron
