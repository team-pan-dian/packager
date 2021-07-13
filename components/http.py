import logging

import httpx


async def get_file(url: str) -> bytes:
    logging.info(f"ready to fetch: {url}")
    async with httpx.AsyncClient() as client:  # type: httpx.AsyncClient
        response = await client.get(url, headers={
            "User-Agent": "hackathon-packager/1.0"
        })

        logging.info(f"status code: {response.status_code}")
        return response.content
