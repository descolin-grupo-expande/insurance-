import secrets

def create_pin():
    
    secure_range = secrets.SystemRandom()
    return str(secure_range.randrange(100000, 999999))

def success(message, extra=0, status=200):
    message = "Success: " + message 
    answer = {"status":status, "message":message}
    if extra == 0:
        return answer
    else:
        if status != 200:
            extra['status'] = status
        answer.update(extra)
        return answer
    
def errors(type):
    """
    1 User already exists
    2 another account is using the email address
    3 No user found
    4 wrong password
    5 another account is using the national_id
    6 pin doesn't match
    7 case data doesn't match
    8 provider location does not exist
    9 case does not exist
    10 no provider/service found
    11 No sale found
    12 No plan found
    13 No attachment found
    14 No open cases found
    15 Case is closed
    16 User not active
    17 User doesn't match member
    18 Case can't be canceled
    """
    answer = {}
    if type == 1:
        answer["status"]="901"
        answer["message"]="Error: User already exists"
    elif type == 2:
        answer["status"]="902"
        answer["message"]="Error: another account is using the email address"
    elif type == 3:
        answer["status"]="903"
        answer["message"]="Error: No user found"
    elif type == 4:
        answer["status"]="904"
        answer["message"]="Error: wrong password"
    elif type == 5:
        answer["status"]="905"
        answer["message"]="Error: another account is using the national_id"
    elif type == 6:
        answer["status"]="906"
        answer["message"]="Error: Pin doesn't match"
    elif type == 7:
        answer["status"]="907"
        answer["message"]="Error: wrong case data sent"
    elif type == 8:
        answer["status"]="908"
        answer["message"]="Error: Provider location does not exist"        
    elif type == 9:
        answer["status"]="909"
        answer["message"]="Error: Case does not exist"
    elif type == 10:
        answer["status"]="910"
        answer["message"]="Error: No provider/service found"   
    elif type == 11:
        answer["status"]="911"
        answer["message"]="Error: No sale found"
    elif type == 12:
        answer["status"]="912"
        answer["message"]="Error: No plan found"
    elif type == 13:
        answer["status"]="913"
        answer["message"]="Error: No attachment found"
    elif type == 14:
        answer["status"]="914"
        answer["message"]="Error: No open cases found"
    elif type == 15:
        answer["status"]="915"
        answer["message"]="Error: case closed"
    elif type == 16:
        answer["status"]="916"
        answer["message"]="Error: User not active"
    elif type == 17:
        answer["status"]="917"
        answer["message"]="Error: User does not match any members"
    elif type == 18:
        answer["status"]="918"
        answer["message"]="Error: Case cannot be canceled at the moment, plase contact us to cancel."
    elif type == 19:
        answer["status"]="919"
        answer["message"]="Error: No se tienen servicios disponibles."
    elif type == 20:
        answer["status"]="920"
        answer["message"]="Error: no app found."
    elif type == 21:
        answer["status"]="921"
        answer["message"]="Error: app not to date."
    elif type == 22:
        answer["status"]="922"
        answer["message"]="Error: app not active."
    elif type == 23:
        answer["status"]="923"
        answer["message"]="Error: invalid status."
    elif type == 24:
        answer["status"]="924"
        answer["message"]="Error: Ha llegado al límite de usos de este servicio."
    elif type == 25:
        answer["status"]="925"
        answer["message"]="Error: Ha ingresado una póliza o certificado incorrecto."
    else:
        answer["status"]="900"
        answer["message"]="Error: usage"
    
    return answer
