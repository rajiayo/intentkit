from typing import Annotated

import httpx

from langchain_core.tools import tool
from pydantic import Field
from . import *


@tool
async def get_actions(
    api_token: Annotated[str, Field(description="Enso Finance API token")],
) -> dict:
    """Gets information about wallet actions using the Enso Finance API.

    Args:
        api_token (str): Enso Finance API token.

    Returns:
        dict: The API response containing wallet action information, or raises an exception on error.
    """

    url = f"{base_url}/actions"
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
            return f"error getting the enso actions {e!s}"
