from app.extensions import db
from app import models as m
from app.config import config
import datetime
import requests
import json

def send_sms(sentInfo):

    webServiceLog = m.WebServiceLog(
        name='SMS_TRANSACTION',
        from_=config.WS_APOLO11,
        to_=config.WS_SMS,
        request_=json.dumps(sentInfo),
        response_=None,
        datetime=datetime.datetime.now()
    )

    try:

        number = sentInfo["phone"]

        if number is None or number == "":
            return 0

        if "country_id" in sentInfo:
            number = verifyCountryCode(number, sentInfo["country_id"])

        text = sentInfo["text"]
        text = replaceText(text,sentInfo)

        # clean text
        text =  prepareTextSMS(text)

        country_code = getCountryIdbyNumber(number) 
        
        country = db.session.execute(db.select(m.Country).where(m.Country.s6_equivalence_code == country_code)).scalar()
        
        sms_data = {
            "type_sms":country.sms_client,
            "country":str(country.iso3166_1).upper(),
            "text":text,
            "number": "+"+number if country.sms_client == 'twilio' else int(number),
            "priority": sentInfo["priority"] if 'priority' in sentInfo else False
        }
        print("REQUEST_SMS", sms_data)
        response = requests.post(config.VPS_APOLO_URL+'/api/vps/sendsms', json=sms_data)
        print('RESPONSE_SMS', response.content.decode('utf-8'))

        setattr(webServiceLog, 'response_', response.content.decode('utf-8'))
        db.session.add(webServiceLog)
        db.session.flush()
        
        return response.json().get('status')

    except Exception as e:
        setattr(webServiceLog, 'response_', str(e))
        db.session.add(webServiceLog)
        db.session.flush()

        return 0
    
def verifyCountryCode(number, country_id):
    """
    checks if the phone number
    already has the country code
    if it doesnt it will be added
    if it has it returns a clean version
    """
    myCode = ""
    chars = '+(-)qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,. '
    for c in chars:
        number = number.replace(c,"")
    codes = m.Country.country_phone_code
    for c in codes:
        if c["country_id"] == country_id:
            myCode = c["phone_code"]

    if number[0:3] == myCode:
        if len(number) <= 8:
            number = myCode+number
        return number

    else:
        number = myCode+number
        return number
    
def replaceText(text, vars):
    # Bienvenido #nombre# a #producto# tienes tu plan #plan# a nombre de #nombrecompleto#, saludos #apellido#
    if "#nombre#" in text:
        text = text.replace("#nombre#", vars["name"])

    if "#apellido#" in text:
        text = text.replace("#apellido#", vars["last_name"])

    if "#nombrecompleto#" in text:
        text = text.replace("#nombrecompleto#", vars["full_name"])

    if "#plan#" in text:
        text = text.replace("#plan#", vars["plan"])

    if "#producto#" in text:
        text = text.replace("#producto#", vars["product"])

    if "#code#" in text:
        text = text.replace("#code#", vars["code"])     

    return text

def prepareTextSMS(text):
    #text = text.replace(" ", "%20")
    # text = text.replace('"',"%22")
    # text = text.replace("#","%23")
    # text = text.replace("$","%24")
    # text = text.replace("%","%25")
    # text = text.replace("&","%26")
    # text = text.replace("'","%27")
    # text = text.replace("(","%28")
    # text = text.replace(")","%29")
    # text = text.replace("*","%2A")
    # text = text.replace("+","%2B")
    # text = text.replace(",","%2C")
    # text = text.replace("-","%2D")
    # text = text.replace(".","%2E")
    # text = text.replace("/","%2F")
    # text = text.replace(":","%3A")
    # text = text.replace(";","%3B")
    # text = text.replace("=","%3D")
    # text = text.replace("@","%40")
    # text = text.replace("¿?","")
    
    text = text.replace("_","%5F") #for survey
    text = text.replace("Á","A")
    text = text.replace("É","E")
    text = text.replace("Í","I")
    text = text.replace("Ó","O")
    text = text.replace("Ú","U")
    text = text.replace("á","a")
    text = text.replace("é","e")
    text = text.replace("í","i")
    text = text.replace("ó","o")
    text = text.replace("ú","u")

    return text

def getCountryIdbyNumber(number):
    code = number[0:3]
    if len(number[3:]) >= 8:
        if code == '502':
            return 'GT'
        if code == '503':
            return 'ES'
        if code == '504':
            return 'HO'
        if code == '505':
            return 'NI'
        if code == '506':
            return 'CR'
        if code == '507':
            return 'PA'  
        if code == '595':
            return 'PY'  