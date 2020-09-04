import requests
from config import *

def phoneVerification(internationalCode, phoneNumber, session):
    postURL = baseURL + '/phoneVerification'
    response = session.post(postURL
                             , json={"internationalCode":internationalCode, "phoneNumber":phoneNumber}
                             , timeout=TIMEOUT)
    if response.status_code == 200:
        print('Got Phone Code')
    else:
        raise ValueError('Server Error, check with backend or template format')
    return
