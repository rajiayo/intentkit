from typing import Annotated, Optional, List

import httpx

from langchain_core.tools import tool
from pydantic import Field
from . import *


@tool
async def get_shortcut_route(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    *,  # Separate keyword arguments from positional arguments
    chain_id: Annotated[int, Field(description="The source chain ID", default=None)],
    from_address: Annotated[str, Field(description="The source address")],
    routing_strategy: Annotated[str, Field(description="The routing strategy")],
    token_in: Annotated[
        str, Field(description="The address of the token being swapped from")
    ],
    token_out: Annotated[
        str, Field(description="The address of the token being swapped to")
    ],
    amount_in: Annotated[
        str, Field(description="The amount of tokens to swap (in wei)")
    ],
    fee: Annotated[str, Field(description="The gas fee for the swap (in wei)")],
    fee_receiver: Annotated[
        str, Field(description="The address that will receive the gas fee")
    ],
    disable_rfqs: Annotated[
        bool, Field(description="Whether to disable Request for Quotes (RFQs)")
    ],
    ignore_aggregators: Annotated[
        Optional[str],
        Field(description="Comma-separated list of aggregators to ignore"),
    ],
    ignore_standards: Annotated[
        Optional[str], Field(description="Comma-separated list of standards to ignore")
    ],
) -> dict:
    """Gets information about the optimal route for a token swap using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.
        chain_id (int): The source chain ID.
        from_address (str): The source address.
        routing_strategy (str): Routing strategy to use.
        token_in (str): The address of the token being swapped from.
        token_out (str): The address of the token being swapped to.
        amount_in (str): The amount of tokens to swap (in wei).
        fee (str): The gas fee for the swap (in wei) Fee in basis points (1/10000) for each amountIn value. Must be in range 0-100. If specified, this percentage of each amountIn value will be sent to feeReceiver.
        fee_receiver (str): The address that will receive the gas fee. Required if fee is provided.
        disable_rfqs (bool): Whether to disable Request for Quotes (RFQs).
        ignore_aggregators (str, optional): Comma-separated list of aggregators to ignore.
        ignore_standards (str, optional): Comma-separated list of standards to ignore.


    Returns:
        dict: The API response containing information about the optimal route, or raises an exception on error.
    """

    url = f"{base_url}/shortcuts/quote"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    params = {
        "chainId": chain_id,
        "fromAddress": from_address,
        "routingStrategy": routing_strategy,
        "amountIn": amount_in,
        "fee": fee,
        "feeReceiver": fee_receiver,
        "disableRFQs": disable_rfqs,
        "tokenIn": token_in,
        "tokenOut": token_out,
    }

    if ignore_aggregators:
        params["ignoreAggregators"] = ignore_aggregators

    if ignore_aggregators:
        params["ignoreStandards"] = ignore_standards

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
            return f"error getting swap route {e!s}"


async def get_shortcut_quote(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    *,  # Separate keyword arguments from positional arguments
    chain_id: Annotated[int, Field(description="The source chain ID")],
    from_address: Annotated[str, Field(description="The source address")],
    routing_strategy: Annotated[
        str, Field(description="The routing strategy (e.g., enso wallet)")
    ],
    route: Annotated[List[dict], Field(description="The list of route objects")],
    fee: Annotated[List[str], Field(description="The gas fees (in wei)")],
    fee_receiver: Annotated[
        str, Field(description="The address that will receive the gas fee")
    ],
    disable_rfqs: Annotated[
        bool, Field(description="Whether to disable Request for Quotes (RFQs)")
    ],
    ignore_aggregators: Annotated[
        Optional[List[str]], Field(description="List of aggregators to ignore")
    ],
    block_number: Annotated[
        Optional[str], Field(description="The block number (optional)")
    ],
) -> dict:
    """Gets a quote for a token swap using a custom route definition in the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.
        chain_id (int): The source chain ID.
        from_address (str): The source address.
        routing_strategy (str): The routing strategy (e.g., enso wallet).
        route (List[dict]): The list of route objects, each with information about the swap steps.
        fee (List[str]): The gas fees (in wei) for each step in the route.
        fee_receiver (str): The address that will receive the gas fee.
        disable_rfqs (bool): Whether to disable Request for Quotes (RFQs).
        ignore_aggregators (List[str], optional): List of aggregators to ignore.
        block_number (str, optional): The block number (optional).

    Returns:
        dict: The API response containing the quote information, or raises an exception on error.
    """

    url = f"{base_url}/shortcuts/quote"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    data = {
        "chainId": chain_id,
        "fromAddress": from_address,
        "routingStrategy": routing_strategy,
        "route": route,
        "fee": fee,
        "feeReceiver": fee_receiver,
        "disableRFQs": disable_rfqs,
        "ignoreAggregators": ignore_aggregators,
        "blockNumber": block_number,
    }

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
        except Exception as e:
            return f"error getting swap route {e!s}"
