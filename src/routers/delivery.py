"""
delivery.py
"""

from fastapi import APIRouter, Depends

from src.dependencies import get_token_header
from src.models import DeliveryIn, DeliveryOut
from src.parsers import DeliveryParser


router = APIRouter(dependencies=[Depends(get_token_header)])


@router.post("/delivery", response_model=DeliveryOut)
async def delivery(query: DeliveryIn) -> DeliveryOut:
    """Delivery endpoint

    Parameters
    ----------
    query : DeliveryIn
        Query fields

    Returns
    -------
    DeliveryOut
        JSON response
    """
    parser = DeliveryParser(**query.dict())
    result = await parser.parse()
    return result
