# Django LLM API Server

An API server for LLM services.

Marc Schwarzschild<br>
The Brookhaven Group, LLC<br>
2024

[Github Repo](https://github.com/TheBrookhavenGroup/djangollmapi.git)

## Objective

Provide a RESTful API with an access control for an LLM service.  These 
services typically require a large data set to be loaded into memory.  
That data would be cached once for all subsequent API calls.

Consider also that memory and GPU resources are expensive and may only 
handle a single task at a time.  In this configuration we have a single 
Linux server with two GPUs.  A separate LLM could be loaded and remain
resident for each GPU.  This could easily be expanded to `n` models on `n` 
GPUs.

The API is secured with a key, optional usage parameters limiting the 
number of API calls made, and an expiration date.

## Features

1. Access Key assigned by site Admin.
2. Possible usage restriction on number of requests.
3. Possible usage restriction within date window.
4. Single threading of LLM calls enables data caching in GPUs for 
   subsequent calls.

## Example Python Client

The following code demonstrates how to use the API.  The server checks if 
the call is made within valid dates assigned to the key and the number of 
times the API is called.  The key can also be restricted to a number of 
calls, a usage limitation.

```python
"""
curl --request POST --url http://localhost:8000/api/ \
     --header "Authorization: Bearer <put your key here>" \
     --header 'Content-Type: application/json' \
     --data '{"text": "Is this real?"}'

"""

import requests

key = "<put your key here>"
header = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
data = {'text': 'This could be any payload data the api expects.'}

response = requests.post('http://localhost:8000/api/',
                         headers=header,
                         json=data)
print(response.content)
```

## Architecture

The Django web framework is obviously at the heart of our system.  We chose 
it because it is a complete framework, we did not have to look further 
for components like the ORM, templating, security middleware, RESTful view 
base classes, and so on.

An example stack running on Ubuntu would include:

1. Nginx
2. Gunicorn
3. Postgres 
4. Celery 
5. Redis

A serial celery server limited to a single worker with a concurrency set to 
1 was configured so that anything cached by celery will be loaded once for 
the first call and memoized for all subsequent calls.

### Algorithm

The Algorithm used by the API is defined in an external pip installable
package.  It needs to have a class named `Algorithm` with a `run(input_text)`
method. An instance of `Algorithm` would be memoized so its constructor 
would load model data.  The `run(input_text)` method implements the 
algorithm using one or more LLMs and maybe GPUs.

An example is [tbg_llm_example](https://github.com/TheBrookhavenGroup/tbg_llm_example.git).

The `tbg_llm_example` package is also used in the unit tests.

### Config File

A config file must be set in the `DJANGO_LLM_API_CONFIG` environment 
variable and typically has the value "~/.djangollmapi".  The config file 
used for unit tests is:
[djangollmapi.config](https://github.com/TheBrookhavenGroup/djangollmapi/blob/main/djangollmapi/djangollmapi.config).

Private data should be set in that file.

## Installation

Our installation notes are provided here:

[Server Installation HOWTO](HOWTO.md)