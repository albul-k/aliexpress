"""
parsers.py
"""

import os
import json
from fastapi import HTTPException
import httpx
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from src.models import DeliveryMethod, DeliveryOut, ProductSKU, ProductOut


load_dotenv('.env')
USER_AGENT = os.environ.get('USER_AGENT')


class Parser:
    headers = {
        'User-Agent': USER_AGENT,
    }


class ProductParser(Parser):
    def __init__(self,
                 product_id: int,
                 sku_id: int = None,
                 count: int = 1,
                 country: str = "RU") -> None:
        super().__init__()

        self.product_id = product_id
        self.sku_id = sku_id
        self.count = count
        self.country = country

        self.url = f'https://aliexpress.com/item/{self.product_id}.html?&item_id={self.product_id}'
        if self.sku_id:
            self.url += f'&sku_id={self.sku_id}'

    async def parse(self):
        response = httpx.get(
            self.url,
            headers=self.headers,
            follow_redirects=True
        )
        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code, detail=response.text)

        soup = BeautifulSoup(response.text, 'html.parser')
        soup = soup.select_one('script[id="__AER_DATA__"]')
        if soup is None:
            raise HTTPException(status_code=404, detail='Unable to get data')

        product_data = json.loads(soup.text)
        try:
            product_data = product_data['widgets'][0]['children'][7]['children'][0]['props']
        except KeyError:
            raise HTTPException(
                status_code=404, detail='Unable to get data') from KeyError

        data_sku = []
        for sku in product_data['skuInfo']['priceList']:
            if self.sku_id and sku['skuId'] != str(self.sku_id):
                continue
            item = ProductSKU(
                sku_url=self.url,
                sku_id=sku['skuId'],
                quantity=sku['availQuantity'],
                price=sku['activityAmount']['value'],
            )
            data_sku.append(item.dict())

        result = ProductOut(
            name=product_data['name'],
            description=product_data['description'],
            likes=product_data['likes'],
            rating=product_data['rating']['middle'],
            reviews=product_data['reviews'],
            store_url=product_data['storeUrl'],
            seller_id=product_data['sellerId'],
            sku=data_sku,
        )
        return result


class DeliveryParser(Parser):
    def __init__(self,
                 product_id: int,
                 count: int,
                 country: str = "RU") -> None:
        super().__init__()

        self.product_id = product_id
        self.count = count
        self.country = country

    async def parse(self):
        url = f'https://aliexpress.ru/aer-api/v1/product/detail/freight?product_id={self.product_id}'
        body = {
            "count": self.count,
            "country": self.country,
            "productId": self.product_id,
        }

        response = httpx.post(
            url=url,
            json=body,
            headers=self.headers
        )
        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code, detail=response.text)

        try:
            methods = response.json()['methods']
        except KeyError:
            raise HTTPException(
                status_code=404, detail='Unable to get data') from KeyError

        data_delivery = []
        for method in methods:
            item = DeliveryMethod(
                service=method['service'],
                value=method['amount']['value'],
                currency=method['amount']['currency'],
                date=method['dateDisplay'] if method['dateDisplay'] != '' else None,
            )
            data_delivery.append(item.dict())

        result = DeliveryOut(
            delivery=data_delivery
        )
        return result
