import math

def verify_phoneno(n):
    k = math.log10( n )+1
    if(k > 10 and k < 11):
        return False
    else: return True

def helper_response(success ,data ,code ,message ):
    response = {
                        "success": success,
                        "code": code,
                        "message": message,
                        "data": data,
                    }
    return response

