import pandas as pd
from commodityPostor import *

def processOneCommodity(dataTrunk, businessId, categoryNameToIdMapping, session):
    print('getting commodity')
    # params: data from parsed pandas with the format of template
    attributes = []
    specifications = []
    addOnIds = []

    attrStart = 7
    attrEnd = 7
    specStart = 7
    specEnd = 7
    addonStart = 7
    addonEnd = 7

    while attrStart + 1 < dataTrunk.shape[0] and dataTrunk.iloc[attrStart, 0] == 'attribute':
        attrEnd += 1
        if attrEnd >= dataTrunk.shape[0] or dataTrunk.iloc[attrEnd, 0] != 'value':
            attribute = getAttribute(dataTrunk.iloc[attrStart: attrEnd, :])
            attributes.append(attribute)

            attrStart = attrEnd
            specStart = attrEnd
            addonStart = attrEnd
            specEnd = attrEnd
            addonEnd = attrEnd

        if attrEnd >= dataTrunk.shape[0]:
            break

    while specStart + 1 < dataTrunk.shape[0] and dataTrunk.iloc[specStart, 0] == 'specification':
        specEnd += 1
        if specEnd >= dataTrunk.shape[0] or dataTrunk.iloc[specEnd, 0] != 'value':
            specification = getSpecification(dataTrunk.iloc[specStart: specEnd, :])
            specifications.append(specification)

            specStart = specEnd
            addonStart = specEnd
            addonEnd = specEnd

        if specEnd >= dataTrunk.shape[0]:
            break

    while addonStart + 1 < dataTrunk.shape[0] and dataTrunk.iloc[addonStart, 0] == 'addOn':
        addonEnd += 1
        if addonEnd >= dataTrunk.shape[0] or dataTrunk.iloc[addonEnd, 0] != 'value':
            addOn = getAddOn(dataTrunk.iloc[addonStart: addonEnd, :])
            # addOnId = postAddOn(businessId, addOn, session)
            # addOnIds.append(addOnId)

            addonStart = addonEnd

        if addonEnd >= dataTrunk.shape[0]:
            break

    commodity = {}
    commodity['name'] = {
        "en-US": dataTrunk.iloc[1, 2],
        "zh-CN": dataTrunk.iloc[1, 4],
    }
    commodity['price'] = int(dataTrunk.iloc[2, 1])

    if not pd.isna(dataTrunk.iloc[3, 1]):
        commodity['stockNumber'] = int(dataTrunk.iloc[3, 1])
    commodity["minBuyNumber"] = int(dataTrunk.iloc[4, 1])
    if not pd.isna(dataTrunk.iloc[5, 1]):
        commodity["maxBuyNumber"] = int(dataTrunk.iloc[5, 1])

    commodity['description'] = {
        "en-US": dataTrunk.iloc[6, 2],
        "zh-CN": dataTrunk.iloc[6, 4],
    }
    commodity['thumbnail'] = ''
    commodity['images'] = []
    commodity['attributes'] = attributes
    commodity['specifications'] = specifications
    commodity['addOnIds'] = addOnIds

    commodityCategoryName = dataTrunk.iloc[0, 1]
    categoryId = categoryNameToIdMapping[commodityCategoryName]
    print('uploading commodity...', commodity)
    postCommodity((businessId, categoryId), commodity, session)

def getAttribute(dataTrunk):
    numValues = dataTrunk.shape[0]-1
    if numValues < 1:
        raise ValueError('Must have at least one value')
    attributeName = {
        "en-US": dataTrunk.iloc[0, 2],
        "zh-CN": dataTrunk.iloc[0, 4],
    }
    singularity = True if int(dataTrunk.iloc[0, 6]) == 1 else False
    values = []
    for i in range(1, numValues+1):
        valueName = {
            "en-US": dataTrunk.iloc[i, 2],
            "zh-CN": dataTrunk.iloc[i, 4],
        }
        values.append({
            "name": valueName,
            "price": int(dataTrunk.iloc[i, 6])
        })
    return {
        "name" : attributeName,
        "singularity": singularity,
        "values": values
    }

def getSpecification(dataTrunk):
    numValues = dataTrunk.shape[0] - 1
    if numValues < 1:
        raise ValueError('Must have at least one value')
    specificationName = {
        "en-US": dataTrunk.iloc[0, 2],
        "zh-CN": dataTrunk.iloc[0, 4],
    }
    singularity = True if int(dataTrunk.iloc[0, 6]) == 1 else False
    values = []
    for i in range(1, numValues + 1):
        valueName = {
            "en-US": dataTrunk.iloc[i, 2],
            "zh-CN": dataTrunk.iloc[i, 4],
        }
        values.append(valueName)
    return {
        "name": specificationName,
        "singularity": singularity,
        "values": values
    }

def getAddOn(dataTrunk):
    numValues = dataTrunk.shape[0] - 1
    if numValues < 1:
        raise ValueError('Must have at least one value')
    addonName = {
        "en-US": dataTrunk.iloc[0, 2],
        "zh-CN": dataTrunk.iloc[0, 4],
    }
    addOnStatus = True if int(dataTrunk.iloc[0, 6]) == 1 else False
    values = []
    for i in range(1, numValues+1):
        value = {}

        if not pd.isna(dataTrunk.iloc[i, 8]):
            value["stockNumber"] = int(dataTrunk.iloc[i, 8])
        value["minBuyNumber"] = int(dataTrunk.iloc[i, 10])
        if not pd.isna(dataTrunk.iloc[i, 12]):
            value["maxBuyNumber"] = int(dataTrunk.iloc[i, 12])

        value["name"] = {
            "en-US": dataTrunk.iloc[i, 2],
            "zh-CN": dataTrunk.iloc[i, 4],
        }
        value["price"] = int(dataTrunk.iloc[i, 6])
        value["valueStatus"] = True if int(dataTrunk.iloc[i, 14]) == 1 else False
        values.append(value)
    return {
        "name": addonName,
        "values": values,
        "addOnStatus": addOnStatus
    }