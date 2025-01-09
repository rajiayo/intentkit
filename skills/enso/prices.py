from typing import Annotated, Union

import httpx

from langchain_core.tools import tool
from pydantic import Field
from . import *


@tool
async def get_token_prices(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    *,  # Separate keyword arguments from positional arguments
    chain_id: Annotated[int, Field(description="The chain ID (e.g. 1)")],
    address: Annotated[
        str,
        Field(
            description="The Address (e.g. 0x030bA81f1c18d280636F32af80b9AAd02Cf0854e)"
        ),
    ],
) -> dict:
    """Gets token prices using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.
        chain_id (int): The chain ID.
        address (str): token address.

    Returns:
        dict: The API response containing token prices, or raises an exception on error.
    """

    url = f"{base_url}/shortcuts/route/{chain_id}/{address}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
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
