from typing import Annotated

import httpx

from langchain_core.tools import tool
from pydantic import Field
from . import *


@tool
async def get_supported_networks(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    name: Annotated[str, Field(description="Protocol Name (e.g. Ethereum")],
    chainId: Annotated[str, Field(description="The chain id (e.g. 1")],
) -> dict:
    """Gets a list of supported networks using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.

    Returns:
        dict: The API response containing a list of supported networks, or raises an exception on error.
    """

    url = f"{base_url}/networks"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
    }
    params = {
        "name": name,
        "chainId": chainId,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(
                f"API request failed with status code: {e.status_code}"
            ) from e
        except httpx.HTTPError as e:
            raise Exception(f"An HTTP error occurred: {e}") from e
