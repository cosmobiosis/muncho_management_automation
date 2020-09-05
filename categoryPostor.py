import requests
from config import *

def postCategory(businessId, payload, session):
    postURL = baseURL + '/businesses/' + businessId + '/commodityCategories'
    response = session.post(postURL, json=payload, timeout=TIMEOUT)
    categoryId = str(response.json()['id'])
    if response.status_code == 200:
        print('Category', categoryId, ' posting for ', businessId, ' is a success')
    else:
        raise ValueError('Server Error, check with backend or template format')
    return categoryId

def getCategoryPayload(rowData):
    # params: data from parsed pandas
    return {
        'name': {
            'en-US': rowData['nameEN'],
            'zh-CN': rowData['nameCN']
        }
    }