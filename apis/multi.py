
import requests
import httpx
import asyncio


def sequential_query(data):
    """
    data: list of tuples containing url, headers, and data
    """

    responses = []
    for key in data:
        url, headers, data = key
        if data:
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.get(url, headers=headers)
        responses.append(response)

    return responses


async def request_it(url, headers, data):
    async with httpx.AsyncClient() as client:
        # print(f'starting {url}')
        # await asyncio.sleep(5)
        if data is None:
            response = await client.get(url, headers=headers,
                                        follow_redirects=True)
        else:
            response = await client.post(url, headers=headers, json=data,
                                         follow_redirects=True)
    return response


def get_parallel_query(data):
    """
    data: list of tuples containing url, headers, and data
    """

    async def parallel_query():
        tasks = [request_it(url, headers, data) for url, headers, data in data]
        responses = await asyncio.gather(*tasks)

        return responses

    return parallel_query


def run_parallel_query(data):
    parallel_query = get_parallel_query(data)
    return asyncio.run(parallel_query())
