from typing import Annotated

import httpx

from langchain_core.tools import tool
from pydantic import Field
from . import *


@tool
async def get_protocols(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    *,  # Separate keyword arguments from positional arguments
    slug: Annotated[
        str | None,
        Field(description="The protocol slug (e.g., 'uniswap-v2')", default=None),
    ],
) -> dict:
    """Gets information about protocols using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.
        chain_id (int): The chain ID.
        slug (str, optional): The protocol slug (e.g., 'uniswap-v2'). Defaults to None.

    Returns:
        dict: The API response containing protocol information, or raises an exception on error.
    """

    url = f"{base_url}/protocols"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    params = {}

    if slug:
        params["slug"] = slug

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
        except Exception as e:
            return f"error getting the enso tokens {e!s}"
