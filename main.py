import pandas as pd
from sys import argv
from categoryPostor import *
from phoneVerification import *
from login import *
from config import *
from commodityProcessor import *

session = requests.Session()
phoneVerification('86', '13590956966', session)
login("8613590956966", session)
categoryNameToIdMapping = {}
addOnNameToIdMapping = {}
xl = pd.ExcelFile('upload.xlsx')
businessId = str(xl.parse("business", header=None).iloc[0,0])

categoryData = xl.parse("category")
numCategories = len(categoryData['nameEN'])
print(categoryData)

for i in range(numCategories):
    record = categoryData.iloc[i]
    categoryName = record['nameEN']
    if categoryName in categoryNameToIdMapping:
        print('Duplicated Category Found, ignored')
        continue
    print(categoryName)
    payload = getCategoryPayload(record)
    categoryId = postCategory(businessId, payload, session)
    categoryNameToIdMapping[categoryName] = categoryId
""""""

commodityData = xl.parse("commodity", header=None)
start = 0
end = 0
while True:
    end += 1
    if end >= commodityData.shape[0] or pd.isna(commodityData.iloc[end, 0]):
        processOneCommodity(commodityData.iloc[start : end, :], businessId, categoryNameToIdMapping, session)
        start = end + 1
    if end >= commodityData.shape[0]:
        break











