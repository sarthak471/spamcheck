from .models import Registor_User,Registor_Contact
from .serializers import Validate_User_Data,Validate_Login_Data,Validate_Name,Validate_Phone_no
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password ,check_password
import logging

from .helper.helper import verify_phoneno , helper_response
from .helper import usermessages,logmessages

logger = logging.getLogger('django')

"""

1>It is assummed that type checking of input values in Json body is done form frontend itself because the CharField data type also accept the integer.
2>I have implement every feature as per requirement accept API Authentication (JWT Token) .

"""


@api_view(['POST'])
def Registor_User_View(request):
        """
            Request url -  http://127.0.0.1:8000/spam_check/registor/
            Json body - {"Name":"sar","Password":"sar","Phone_no":1111122311,"Email":"test"}
            output - {
                    "success": true,
                    "code": 200,
                    "message": "The user is registered successfully",
                    "Data": null
                    }
        """
        logger.info("Executing registor user api")
        # logger.debug('Attempting to connect to API')
        valid_ser = Validate_User_Data(data=request.data)
        if valid_ser.is_valid():
            Name = request.data['Name']
            Password = request.data['Password']
            Phone_no = request.data['Phone_no']
            Email = request.data['Email']
            enc_password = make_password(Password)
            if(verify_phoneno(Phone_no)):
                    response = helper_response(True,None,200,usermessages.Invalid_Phone_no)
                    json_data = JSONRenderer().render(response)
                    logger.info(response['message'])
                    return HttpResponse(json_data,content_type = 'application/json')     
            if Registor_User.objects.filter(Phone_no = Phone_no).exists():
                response = helper_response(True,None,200,usermessages.Phone_no_exist)
            else:
                try:
                    user = Registor_User(Name = Name,Password = enc_password,Phone_no = Phone_no ,Email = Email)
                    user.save()
                    user = Registor_Contact(User_id = None,Name = Name,Contact_no = Phone_no ,spam = False,is_registered=True)
                    user.save()
                    response = helper_response(True,None,200,usermessages.Registered_successfully)
                except:
                    logger.error(Exception)
                    response = helper_response(True,None,500,usermessages.Something_went_wrong)
        else:
            response = helper_response(True,None,400,usermessages.Invalid_body)
        logger.info(response['message'])
        json_data = JSONRenderer().render(response)
        return HttpResponse(json_data,content_type = 'application/json')

@api_view(['POST'])
def Login_View(request):
        """
            Request url -  http://127.0.0.1:8000/spam_check/login/
            Json body - {"Phone_no":6120800971,"Password":"8132320671"}
            output - {
                    "success": true,
                    "code": 200,
                    "message": "You_are_logined",
                    "data": null
                }
        """
        logger.info('Exexcting login Api')
        valid_ser = Validate_Login_Data(data=request.data)
        if valid_ser.is_valid():
            Phone_no = request.data['Phone_no']
            Password = request.data['Password']     
            if(verify_phoneno(Phone_no)):
                    response = helper_response(True,None,200,usermessages.Invalid_Phone_no)
                    logger.info(response['message'])
                    json_data = JSONRenderer().render(response)
                    return HttpResponse(json_data,content_type = 'application/json')     
            try:
                    user_obj = Registor_User.objects.get(Phone_no = Phone_no)
                    if(check_password(Password,user_obj.Password) or user_obj.Password == Password): 
                        response = helper_response(True,None,200,usermessages.logined)
                    else:
                        response = helper_response(True,None,200,usermessages.Email_or_password)
            except Registor_User.DoesNotExist:     
                     response = helper_response(True,None,200,usermessages.Email_or_password)                   
            except:
                logger.error(Exception)
                response = helper_response(True,None,500,usermessages.Something_went_wrong)
        else:
            response = helper_response(False,None,400,usermessages.Invalid_body)
        logger.info(response['message'])
        json_data = JSONRenderer().render(response)
        return HttpResponse(json_data,content_type = 'application/json')

@api_view(['POST'])
def Mark_Spam_View(request):
        """
            Request url - http://127.0.0.1:8000/spam_check/mark_spam/
            Json body - {"Phone_no":"6760309721"}  
            output - {
                    "success": true,
                    "code": 200,
                    "message": "Phone no is marked spam",
                    "Data": null
                    }
        """
        logger.info('Exexcting Mark spam api')
        valid_ser = Validate_Phone_no(data=request.data)
        if valid_ser.is_valid():
            Phone_no = request.data['Phone_no']
            try:
                    user_obj = Registor_Contact.objects.filter(Contact_no = Phone_no)
                    if user_obj:
                        for i in user_obj:
                            print(i.Name)
                            i.spam = True
                            i.save()
                        response = helper_response(True,None,200,usermessages.Phoneno_marked_spam)
                    else:
                        response = helper_response(True,None,200,usermessages.Phoneno_not_exist)
            except:
                logger.error(Exception)
                response = helper_response(True,None,500,usermessages.Something_went_wrong)
        else:
            response = helper_response(True,None,400,usermessages.Invalid_body)
        logger.info(response['message'])
        json_data = JSONRenderer().render(response)
        return HttpResponse(json_data,content_type = 'application/json')


@api_view(['POST'])
def Phone_No_Search_View(request):
        """
            Request url -  http://127.0.0.1:8000/spam_check/phoneno_search/
            Json body - {"Name":"sar","Password":"sar","Phone_no":1111122311,"Email":"test"}
            Response {
                "success": true,
                "code": 200,
                "message": null,
                "Data": {
                    "isregistered": [
                        {
                            "contact_no": 5461821261,
                            "name": "James Castro",
                            "Email": "thomassmith@example.org",
                            "spam_status": true
                        }
                    ]
                }
            }
        """
        logger.info('Exexcting Phone No Search API')
        valid_ser = Validate_Phone_no(data=request.data)
        if valid_ser.is_valid():
            Phone_no = request.data['Phone_no']
            try:
                user_obj = Registor_Contact.objects.filter(Contact_no = Phone_no)
                if user_obj:
                    isregistered_result = []
                    notregistered_result = []
                    isregistered = False
                    for i in user_obj:
                        Email = None
                        if(i.is_registered):
                            value=Registor_User.objects.get(Phone_no = Phone_no)
                            Email =  value.Email
                            temp = {"contact_no":value.Phone_no,"name":value.Name,"Email":Email,"spam_status":i.spam}
                            isregistered_result.append(temp)
                            isregistered = True
                            break
                        else:
                            temp = {"contact_no":i.Contact_no,"name":i.Name,"Email":Email,"spam_status":i.spam}
                            notregistered_result.append(temp)
                    if(isregistered):
                        payload = {}
                        payload['isregistered'] = isregistered_result
                    else:
                        payload['notregistered_result'] = notregistered_result
                    response = helper_response(True,payload,200,None)   
                else:
                    response = helper_response(True,None,200,usermessages.Phoneno_not_exist)
            except:
                logger.error(Exception)
                response = helper_response(True,None,500,usermessages.Something_went_wrong)
        else:
            response = helper_response(True,None,400,usermessages.Invalid_body)
        logger.info(response['message'])
        json_data = JSONRenderer().render(response)
        return HttpResponse(json_data,content_type = 'application/json')

@api_view(['POST'])
def Name_Search_View(request):
        """
            Request url -  http://127.0.0.1:8000/spam_check/name_search/
            Json body - {"Name":"sar"}
            output - {
                    "success": true,
                    "code": 200,
                    "message": null,
                    "data": {
                        "exact_result_registered": [
                            {
                                "contact_no": 1111122311,
                                "name": "sar",
                                "Email": "test",
                                "spam_status": false
                            }
                        ],
                        "similar_result_registered": [],
                        "similar_result": [
                            {
                                "contact_no": 7938418121,
                                "name": "Sarah Robbins",
                                "Email": null,
                                "spam_status": true
                            }
                        ]
                    }
                }
        """
        logger.info('Exexcting Name Search API')
        valid_ser = Validate_Name(data=request.data)
        if valid_ser.is_valid():
            Name = request.data['Name']
            try:
                user_obj = Registor_Contact.objects.filter(Name__contains=Name)
                print(user_obj)
                if user_obj:
                    exact_result_registered = []
                    similar_result_registered = []
                    similar_result = []
                    for i in user_obj:
                        Email = None
                        if(i.Name == Name):  
                            if(i.is_registered):
                                if(Registor_User.objects.filter(Phone_no = i.Contact_no).exists()):
                                    registered_user =  Registor_User.objects.get(Phone_no = i.Contact_no)
                                    temp = {"contact_no":registered_user.Phone_no,"name":registered_user.Name,"Email":registered_user.Email,"spam_status":i.spam}
                                    exact_result_registered.append(temp)
                            else:
                                temp = {"contact_no":i.Contact_no,"name":i.Name,"Email":Email,"spam_status":i.spam}
                                similar_result_registered.append(temp)
                        else:
                            temp = {"contact_no":i.Contact_no,"name":i.Name,"Email":Email,"spam_status":i.spam}
                            similar_result.append(temp)
                    
                    if(exact_result_registered or similar_result_registered or similar_result ):
                        payload = {}
                        payload['exact_result_registered'] = exact_result_registered
                        payload['similar_result_registered'] = similar_result_registered
                        payload['similar_result'] = similar_result
                        response = helper_response(True,payload,200,None)   
                else:
                    response = helper_response(True,None,200,usermessages.Name_does_not_exist)
            except:
                logger.error(Exception)
                response = helper_response(True,None,500,usermessages.Something_went_wrong)
            json_data = JSONRenderer().render(response)
            return HttpResponse(json_data,content_type = 'application/json')
        else:
            response = helper_response(True,None,400,usermessages.Invalid_body)
        logger.info(response['message'])
        json_data = JSONRenderer().render(response)
        return HttpResponse(json_data,content_type = 'application/json')







