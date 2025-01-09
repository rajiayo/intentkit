from typing import Annotated

import httpx

from langchain_core.tools import tool
from pydantic import Field
from . import *


@tool
async def get_wallet_info(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    *,  # Separate keyword arguments from positional arguments
    chain_id: Annotated[int, Field(description="The chain ID", default=None)],
    from_address: Annotated[
        str,
        Field(
            description="The from Address (default: 0xd8da6bf26964af9d7eed9e03e53415d37aa96045)"
        ),
    ],
    routing_strategy: Annotated[str, Field(description="The Routing Strategy")],
) -> dict:
    """Gets information about a wallet using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.
        chain_id (int, optional): The chain ID. Defaults to None.
        from_address (str): The wallet address (default: 0xd8da6bf26964af9d7eed9e03e53415d37aa96045).
        routing_strategy (str): Routing Strategy (supported values: ensowallet, router, delegate)

    Returns:
        dict: The API response containing wallet information, or raises an exception on error.
    """

    url = f"{base_url}/wallet"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    params = {
        "fromAddress": from_address,
    }

    if chain_id:
        params["chainId"] = chain_id
    if routing_strategy:
        params["routingStrategy"] = routing_strategy

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
            return f"error getting the enso wallet {e!s}"


@tool
async def approve_wallet_token(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    *,  # Separate keyword arguments from positional arguments
    chain_id: Annotated[int, Field(description="The chain ID", default=None)],
    from_address: Annotated[str, Field(description="The wallet address")],
    routing_strategy: Annotated[str, Field(description="The Routing Strategy")],
    token_address: Annotated[str, Field(description="The token address")],
    amount: Annotated[str, Field(description="The amount to approve (in wei)")],
) -> dict:
    """Approves a token for a wallet using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.
        chain_id (int): The chain ID. Defaults to None.
        from_address (str): The wallet address.
        token_address (str): The token address.
        routing_strategy (str): Routing Strategy (supported values: ensowallet, router, delegate)
        amount (str): The amount to approve (in wei).

    Returns:
        dict: The API response containing approval information, or raises an exception on error.
    """

    url = f"{base_url}/wallet/approve"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    params = {
        "chainId": chain_id,
        "fromAddress": from_address,
        "routingStrategy": routing_strategy,
        "tokenAddress": token_address,
        "amount": amount,
    }

    if chain_id:
        params["chainId"] = chain_id
    if routing_strategy:
        params["routingStrategy"] = routing_strategy

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
            return f"error getting the enso wallet {e!s}"


@tool
async def approvals_wallet_token(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    *,  # Separate keyword arguments from positional arguments
    chain_id: Annotated[int, Field(description="The chain ID", default=None)],
    from_address: Annotated[str, Field(description="The wallet address")],
    routing_strategy: Annotated[str, Field(description="The Routing Strategy")],
) -> dict:
    """Approves a token for a wallet using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.
        chain_id (int): The chain ID. Defaults to None.
        from_address (str): The wallet address.
        routing_strategy (str): Routing Strategy (supported values: ensowallet, router, delegate)

    Returns:
        dict: The API response containing approval information, or raises an exception on error.
    """

    url = f"{base_url}/wallet/approvals"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    params = {
        "chainId": chain_id,
        "fromAddress": from_address,
    }

    if chain_id:
        params["chainId"] = chain_id
    if routing_strategy:
        params["routingStrategy"] = routing_strategy

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
            return f"error getting the enso wallet {e!s}"


@tool
async def get_wallet_balances(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
    *,  # Separate keyword arguments from positional arguments
    chain_id: Annotated[int, Field(description="The chain ID")],
    eoa_address: Annotated[
        str, Field(description="The externally owned account (EOA) address")
    ],
    use_eoa: Annotated[
        bool, Field(description="Whether to use the EOA address (default: True)")
    ],
) -> dict:
    """Gets information about a wallet's token balances using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.
        chain_id (int): The chain ID.
        eoa_address (str): The externally owned account (EOA) address.
        use_eoa (bool, optional): Whether to use the EOA address (default: True)..

    Returns:
        dict: The API response containing wallet balance information, or raises an exception on error.
    """

    url = f"{base_url}/wallet/balances"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_token}",
    }

    params = {
        "chainId": chain_id,
        "eoaAddress": eoa_address,
        "useEoa": use_eoa,
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
        except Exception as e:
            return f"error getting the enso wallet {e!s}"
