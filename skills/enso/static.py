from typing import Annotated

import httpx

from langchain_core.tools import tool
from pydantic import Field
from . import *


async def post_static_ipor_info(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    *,  # Separate keyword arguments from positional arguments
    chain_id: Annotated[int, Field(description="The chain ID")],
    address: Annotated[str, Field(description="The ISPO address")],
) -> dict:
    """Gets static IPOR information using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.
        chain_id (int): The chain ID.
        address (str): The ISPO address.

    Returns:
        dict: The API response containing static IPOR information, or raises an exception on error.
    """

    url = f"{base_url}/static/ipor"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    data = {"chainId": chain_id, "address": address}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(
                f"API request failed with status code: {e.status_code}"
            ) from e
        except httpx.HTTPError as e:
            raise Exception(f"An HTTP error occurred: {e}") from e
