import requests
from config import *
import json

def postCommodity(idPair, payload, session):
    businessId = idPair[0]
    categoryId = idPair[1]
    postURL = baseURL + '/businesses/' + businessId + '/commodityCategories/' + categoryId + '/commodities'
    response = session.post(postURL, json=json.dumps(payload), timeout=TIMEOUT)
    if response.status_code == 200:
        print('Commodity posting for ', businessId, ' is a success')
    else:
        raise ValueError('Server Error, check with backend or template format')
    return

def postAddOn(businessId, payload, session):
    postURL = baseURL + '/businesses/' + businessId + '/addOnTemplates'
    response = session.post(postURL, json=json.dumps(payload), timeout=TIMEOUT)
    print('getting JSON...', response.json())
    addOnId = str(response.json()['_id'])
    if response.status_code == 200:
        print('AddOn', addOnId, ' posting for ', businessId, ' is a success')
    else:
        raise ValueError('Server Error, check with backend or template format')
    return addOnId