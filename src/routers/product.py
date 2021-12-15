"""
product.py
"""

from fastapi import APIRouter, Depends

from src.dependencies import get_token_header
from src.models import ProductIn, ProductOut
from src.parsers import ProductParser


router = APIRouter(dependencies=[Depends(get_token_header)])


@router.post("/product/", response_model=ProductOut)
async def product(query: ProductIn) -> ProductOut:
    """Product endpoint

    Parameters
    ----------
    query : ProductIn
        Query fields

    Returns
    -------
    ProductOut
        JSON response
    """
    parser = ProductParser(**query.dict())
    result = await parser.parse()
    return result
