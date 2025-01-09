from typing import Annotated

import httpx

from langchain_core.tools import tool
from pydantic import Field
from . import *


@tool
async def get_swap_tokens(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    *,  # Separate keyword arguments from positional arguments
    chain_id: Annotated[int, Field(description="The chain ID")],
    from_address: Annotated[str, Field(description="The source address")],
    spender: Annotated[str, Field(description="The spender address")],
    receiver: Annotated[str, Field(description="The recipient address")],
    token_in: Annotated[list[str], Field(description="The token to swap from")],
    amount_in: Annotated[
        list[str], Field(description="The amount of tokens to swap in")
    ],
    token_out: Annotated[list[str], Field(description="The token to swap to")],
    routing_strategy: Annotated[str, Field(description="The routing strategy")],
    amount_out: Annotated[
        list[str], Field(description="The desired amount of tokens out")
    ],
    min_amount_out: Annotated[
        str | None, Field(description="The minimum amount of tokens out")
    ],
    slippage: Annotated[str, Field(description="The slippage tolerance")],
    fee: Annotated[list[str], Field(description="The swap fee")],
    fee_receiver: Annotated[str, Field(description="The recipient of the swap fee")],
    disable_rfqs: Annotated[bool, Field(description="Whether to disable RFQs")],
    ignore_aggregators: Annotated[
        list[str], Field(description="Aggregators to ignore")
    ],
    ignore_standards: Annotated[list[str], Field(description="Standards to ignore")],
    variable_estimates: Annotated[str | None, Field(description="Variable estimates")],
) -> dict:
    """Swaps tokens using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.
        chain_id (int): The chain ID.
        from_address (str): The source address.
        routing_strategy (str): The routing strategy.
        receiver (str): The recipient address.
        spender (str): The spender address.
        amount_in (list[str]): The amount of tokens to swap in.
        amount_out (list[str]): The desired amount of tokens out.
        min_amount_out (str, optional): The minimum amount of tokens out. Defaults to None.
        slippage (str): The slippage tolerance.
        fee (list[str]): The swap fee.
        fee_receiver (str): The recipient of the swap fee.
        disable_rfqs (bool): Whether to disable RFQs. Defaults to False.
        ignore_aggregators (list[str]): Aggregators to ignore. Defaults to [].
        ignore_standards (list[str]): Standards to ignore. Defaults to [].
        token_in (list[str]): The token to swap from.
        token_out (list[str]): The token to swap to.
        variable_estimates (str, optional): Variable estimates. Defaults to None.

    Returns:
        dict: The API response containing swap details, or raises an exception on error.
    """

    url = f"{base_url}/shortcuts/route"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    data = {
        "chainId": chain_id,
        "fromAddress": from_address,
        "routingStrategy": routing_strategy,
        "receiver": receiver,
        "spender": spender,
        "amountIn": amount_in,
        "amountOut": amount_out,
        "minAmountOut": min_amount_out,
        "slippage": slippage,
        "fee": fee,
        "feeReceiver": fee_receiver,
        "disableRFQs": disable_rfqs,
        "ignoreAggregators": ignore_aggregators,
        "ignoreStandards": ignore_standards,
        "tokenIn": token_in,
        "tokenOut": token_out,
        "variableEstimates": variable_estimates,
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


@tool
async def post_swap_tokens(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    *,  # Separate keyword arguments from positional arguments
    chain_id: Annotated[int, Field(description="The chain ID")],
    from_address: Annotated[str, Field(description="The source address")],
    routing_strategy: Annotated[str, Field(description="The routing strategy")],
    receiver: Annotated[str, Field(description="The recipient address")],
    spender: Annotated[str, Field(description="The spender address")],
    amount_in: Annotated[
        list[str], Field(description="The amount of tokens to swap in")
    ],
    amount_out: Annotated[
        list[str], Field(description="The desired amount of tokens out")
    ],
    min_amount_out: Annotated[
        str | None, Field(description="The minimum amount of tokens out")
    ],
    slippage: Annotated[str, Field(description="The slippage tolerance")],
    fee: Annotated[list[str], Field(description="The swap fee")],
    fee_receiver: Annotated[str, Field(description="The recipient of the swap fee")],
    disable_rfqs: Annotated[bool, Field(description="Whether to disable RFQs")],
    ignore_aggregators: Annotated[
        list[str], Field(description="Aggregators to ignore")
    ],
    ignore_standards: Annotated[list[str], Field(description="Standards to ignore")],
    token_in: Annotated[list[str], Field(description="The token to swap from")],
    token_out: Annotated[list[str], Field(description="The token to swap to")],
    variable_estimates: Annotated[str | None, Field(description="Variable estimates")],
) -> dict:
    """Swaps tokens using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.
        chain_id (int): The chain ID.
        from_address (str): The source address.
        routing_strategy (str): The routing strategy.
        receiver (str): The recipient address.
        spender (str): The spender address.
        amount_in (list[str]): The amount of tokens to swap in.
        amount_out (list[str]): The desired amount of tokens out.
        min_amount_out (str, optional): The minimum amount of tokens out. Defaults to None.
        slippage (str): The slippage tolerance.
        fee (list[str]): The swap fee.
        fee_receiver (str): The recipient of the swap fee.
        disable_rfqs (bool): Whether to disable RFQs. Defaults to False.
        ignore_aggregators (list[str]): Aggregators to ignore. Defaults to [].
        ignore_standards (list[str]): Standards to ignore. Defaults to [].
        token_in (list[str]): The token to swap from.
        token_out (list[str]): The token to swap to.
        variable_estimates (str, optional): Variable estimates. Defaults to None.

    Returns:
        dict: The API response containing swap details, or raises an exception on error.
    """

    url = f"{base_url}/shortcuts/route"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    data = {
        "chainId": chain_id,
        "fromAddress": from_address,
        "routingStrategy": routing_strategy,
        "receiver": receiver,
        "spender": spender,
        "amountIn": amount_in,
        "amountOut": amount_out,
        "minAmountOut": min_amount_out,
        "slippage": slippage,
        "fee": fee,
        "feeReceiver": fee_receiver,
        "disableRFQs": disable_rfqs,
        "ignoreAggregators": ignore_aggregators,
        "ignoreStandards": ignore_standards,
        "tokenIn": token_in,
        "tokenOut": token_out,
        "variableEstimates": variable_estimates,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for unsuccessful status codes
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(
                f"API request failed with status code: {e.status_code}"
            ) from e
        except httpx.HTTPError as e:
            raise Exception(f"An HTTP error occurred: {e}") from e
        except Exception as e:
            return f"error getting swap route {e!s}"
