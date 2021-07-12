from typing import Optional
import requests


def get_file(url: str) -> Optional[bytes]:
    response = requests.get(url, headers={
        "User-Agent": "hackathon-packager/1.0"
    })

    return response.content if response.ok else None
