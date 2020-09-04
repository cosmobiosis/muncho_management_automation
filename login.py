import requests
from config import *

def login(fullPhoneNumber, session):
    postURL = baseURL + '/login'
    response = session.post(postURL
                             , json={"verificationCode":testingVerificationCode, "fullPhoneNumber":fullPhoneNumber}
                             , timeout=TIMEOUT)
    if response.status_code == 200:
        print('Login Successful')
    else:
        raise ValueError('Server Error, check with backend or template format')
    return