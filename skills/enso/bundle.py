from typing import Annotated

import httpx

from langchain_core.tools import tool
from pydantic import Field
from . import *


@tool
async def post_bundle_info(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    *,  # Separate keyword arguments from positional arguments
    chain_id: Annotated[int, Field(description="The chain ID")],
    from_address: Annotated[str, Field(description="The from address")],
    routing_strategy: Annotated[str, Field(description="The routing strategy")],
    receiver: Annotated[str, Field(description="The receiver")],
    spender: Annotated[str, Field(description="The spender")],
) -> dict:
    """Gets bundle information using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.
        chain_id (int): Chain ID of the network to execute the transaction on.
        from_address (str): reum address of the wallet to send the transaction from.
        routing_strategy (str): Routing strategy to use (router cannot be used here).
        receiver (str): Ethereum address of the receiver of the tokenOut.
        spender (str): Ethereum address of the spender of the tokenIn.

    Returns:
        dict: The API response containing bundle information, or raises an exception on error.
    """

    url = f"{base_url}/shortcuts/bundle"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    params = {
        "fromAddress": from_address,
        "routingStrategy": routing_strategy,
        "receiver": receiver,
        "spender": spender,
    }
    if chain_id:
        params["chainId"] = chain_id

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(
                f"API request failed with status code: {e.status_code}"
            ) from e
        except httpx.HTTPError as e:
            raise Exception(f"An HTTP error occurred: {e}") from e
