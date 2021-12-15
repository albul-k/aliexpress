# Aliexpress Product Card Parser

## Table of contents

* [Description](#description)
* [Used stack](#used-stack)
* [How to run](#how-to-run)
* [REST API](#rest-api)
* [Examples of usage](#examples-of-usage)

## Description

Simple parser of product card with delivery information and REST API to get of parsed information.

## Used stack

* FastAPI, HTTPX, BeautifulSoup

## How to run

### Clone repository and install requirements

```bash
git clone https://github.com/albul-k/aliexpress
cd aliexpress

python -m venv venv
source venv/bin/activate
## for Win
# source venv/Scripts/activate

pip install -r requirements.txt
```

### Create `.env` file in the root direcory with `X_TOKEN` and `USER_AGENT`

```text
X_TOKEN=my_secret_token
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36
```

### Run FastAPI server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## REST API

### Documentation available after you run server here: <http://127.0.0.1:8000/docs>

## Examples of usage

Request

```curl
curl --location --request POST 'http://127.0.0.1:8000/product/' \
--header 'X-Token: my_secret_token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "product_id": 1005003615978631,
    "sku_id": 12000026508559913
}'
```

Response

```json
{
    "name": "Новинка, повседневный Модный пуловер с логотипом Github, худи, уличная одежда, свитшоты, мужской/женский пуловер, худи, пуловер, худи",
    "description": "Новинка, повседневный Модный пуловер с логотипом Github, худи, уличная одежда, свитшоты, мужской/женский пуловер, худи, пуловер, худи, Наслаждайся ✓Бесплатная доставка по всему миру! ✓Предложение ограничено по времени! ✓Удобный возврат!\nНаслаждайся ✓Бесплатная доставка по всему миру! ✓Предложение ограничено по времени! ✓Удобный возврат!",
    "likes": 0,
    "rating": 0.0,
    "reviews": 0,
    "store_url": "//www.aliexpress.ru/store/912518055",
    "seller_id": 239080561,
    "sku": [
        {
            "sku_url": "https://aliexpress.com/item/1005003615978631.html?&item_id=1005003615978631&sku_id=12000026508559913",
            "sku_id": 12000026508559913,
            "quantity": 9999,
            "price": 1288.95
        }
    ]
}
```

----

Request

```curl
curl --location --request POST 'http://127.0.0.1:8000/delivery/' \
--header 'X-Token: my_secret_token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "product_id": 1005003615978631,
    "count": 3,
    "country": "RU"
}'
```

Response

```json
{
    "delivery": [
        {
            "service": "AliExpress стандартная доставка",
            "value": 1201.45,
            "currency": "RUB",
            "date": "2022-01-09"
        }
    ]
}
```
