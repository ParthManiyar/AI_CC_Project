from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .utils import Signature_Extraction,Account_Number_Extraction
import logging
import sys
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import traceback
Threshold = 30
# CLASSES BELOW

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

# LOGGER

def error():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print("\nLINE = :", exc_traceback.tb_lineno)
    formatted_lines = traceback.format_exc().splitlines()
    print("ERROR = ", formatted_lines[-1],end="\n")

def Home(request):
    return render(request,'sigver/base.html')

class Signature_VerficationAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,BasicAuthentication)
    def post(self, request, *args, **kwargs):
        response = {}
        response["status"] = 500
        try:
            data = request.FILES['Image'] 
            path = default_storage.save('tmp/somename.jpg', ContentFile(data.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            acc_num  = Account_Number_Extraction(tmp_file)
            if(Slip.objects.filter(Account_Number = acc_num).exists()):
                sp = Slip.objects.get(Account_Number = acc_num)
                dist = Signature_Extraction(tmp_file,sp)
                response['status']=200
                response['Account_Number']=acc_num
                response['Difference']=dist
                if(dist>Threshold):
                    response['Result']="Rejected"
                else:
                    response['Result']="Accepted"
            else:
                response["status"]=400
            
        except Exception as e:
            error()
            print("ERROR IN = Singature_VerificationAPI", str(e))

        return Response(data=response)


Signature_Verfication = Signature_VerficationAPI.as_view()

class Account_Number_ExtractionAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,BasicAuthentication)
    def post(self, request, *args, **kwargs):
        response = {}
        response["status"] = 500
        try:
            data = request.FILES['Image'] 
            path = default_storage.save('tmp/somename.jpg', ContentFile(data.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            acc_num  = Account_Number_Extraction(tmp_file)
            response['status']=200
            response['Account_Number']=acc_num
            
        except Exception as e:
            error()
            print("ERROR IN = Singature_VerificationAPI", str(e))

        return Response(data=response)

Account_Number = Account_Number_ExtractionAPI.as_view()

