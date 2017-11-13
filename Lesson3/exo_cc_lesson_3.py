#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:12:50 2017

@author: olivier
@desc: discount on dell and acer computers on cdiscount
"""

import json
import requests
import numpy as np

product = ['ordinateur']
marque = ['dell','acer']
url = 'https://api.cdiscount.com/OpenApi/json/Search'
token = 'b7fd90dd-c719-4419-bed0-82119fcb71df'
page = 5

def getMeanDiscountByProductForABrand(url, apiKey, product, brand, number_of_pages):
    discounts = []
    for nb in range(page) :
        postData = {
                "ApiKey":apiKey,
                "SearchRequest":
                    {
                        "Keyword":product, "SortBy":"relevance", "Pagination":{"ItemsPerPage":10, "PageNumber":nb},
                        "Filters":
                            {
                                "Price":{"Min":0, "Max":9999},
                                "Navigation":"all", "IncludeMarketPlace":"false", "Brands":[brand], "Condition":"new"
                            }
                    }
            }

        jsonData = json.dumps(postData, ensure_ascii = False)
        request = requests.post(url, jsonData)
        result = json.loads(request.text)

        try:
            for prod in result.get('Products'):
                name = prod.get('Name')
                bestOffer = prod.get('BestOffer')
                priceDetails = bestOffer.get('PriceDetails')
                refPrice = float(priceDetails.get('ReferencePrice').split('.')[0])
                saving = priceDetails.get('Saving')

                if not(saving):
                    continue

                discount = float(saving.get('Value').split('\\.')[0])
                discountRate = 1.0 - (refPrice - discount) / refPrice
                discounts.append(discountRate)
        except:
                continue

        res = (np.mean(discounts)*100)
    return res

for m in marque:
    print(m)
    print(getMeanDiscountByProductForABrand(url, token, product[0], m, page))
