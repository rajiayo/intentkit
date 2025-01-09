from typing import Annotated, Union

import httpx

from langchain_core.tools import tool
from pydantic import Field

from . import *


@tool
async def get_tokens_info(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    *,  # Separate keyword arguments from positional arguments
    chain_id: Annotated[int, Field(description="The chain ID")],
    underlying_tokens: Union[str, list[str]],
    protocol_slug: Annotated[
        str | None,
        Field(
            description="The protocol slug (e.g., 'aave-v2', 'compound')", default=None
        ),
    ],
    primary_address: Annotated[
        str | None,
        Field(description="The primary address of the protocol", default=None),
    ],
    type: Annotated[
        str | None,
        Field(description="The type of the token (e.g., 'defi', 'nft')", default=None),
    ],
    page: Annotated[int, Field(description="Page number (default: 1)")],
    per_page: Annotated[
        int, Field(description="Number of tokens per page (default: 100)")
    ],
) -> dict:
    """Gets information about tokens using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.
        chain_id (int): The chain ID.
        underlying_tokens (Union[str, list[str]]): A single token contract address or a list of addresses.
        protocol_slug (str, optional): The protocol slug (e.g., 'aave-v2', 'compound'). Defaults to None.
        primary_address (str, optional): The primary address of the protocol. Defaults to None.
        type (str, optional): The type of the token (e.g., 'defi', 'nft'). Defaults to None.
        page (int, optional): Page number (default: 1).
        per_page (int, optional): Number of tokens per page (default: 100).

    Returns:
        dict: The API response containing token information, or raises an exception on error.
    """

    url = f"{base_url}/tokens"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    params = {
        "chainId": chain_id,
        "page": page,
        "perPage": per_page,
    }

    if protocol_slug:
        params["protocolSlug"] = protocol_slug
    if primary_address:
        params["primaryAddress"] = primary_address
    if type:
        params["type"] = type

    if isinstance(underlying_tokens, str):
        params["underlyingTokens"] = underlying_tokens
    elif isinstance(underlying_tokens, list):
        params["underlyingTokens"] = ",".join(underlying_tokens)

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
