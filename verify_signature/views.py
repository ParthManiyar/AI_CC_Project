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
from .utils import Signature_Matching,Account_Number_Extraction,ImageSegmentation
import logging
import sys
from imageio import imread, imsave
from PIL import Image

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
    if request.user.is_superuser:
        return render(request,'sigver/myadmin.html')
    else:
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
            [sign2,acc] = ImageSegmentation(tmp_file)
            img = Image.fromarray(sign2)
            acc_num  = Account_Number_Extraction(acc)
            img = Image.fromarray(sign2)
            img_path = os.path.join(settings.MEDIA_ROOT, 'tmp/'+acc_num+'.jpg')
            img.save(img_path)
            if(Slip.objects.filter(Account_Number = acc_num).exists()):
                sp = Slip.objects.get(Account_Number = acc_num)
                sign1 = imread(sp.Image_Path.path)
                dist = Signature_Matching(sign1,sign2)
                response['status']=200
                response['Account_Number']=acc_num
                response['Difference']=dist
                if(dist>Threshold):
                    response['Verdict']="Rejected"
                else:
                    response['Verdict']="Accepted"
                response['sign1']=sp.Image_Path.url
                response['sign2']="/Media/"+'tmp/'+acc_num+'.jpg'
            else:
                response["status"]=404
                response['Account_Number']=acc_num
            
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
            [sign2,acc] = ImageSegmentation(tmp_file)
            acc_num  = Account_Number_Extraction(acc)
            response['status']=200
            response['Account_Number']=acc_num
            
        except Exception as e:
            error()
            print("ERROR IN = Account_Number_ExtractionAPI", str(e))

        return Response(data=response)

Account_Number = Account_Number_ExtractionAPI.as_view()

class Match_SignatureAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,BasicAuthentication)
    def post(self, request, *args, **kwargs):
        response = {}
        response["status"] = 500

        try:
            sign1 = request.FILES['sign1'] 
            sign2 = request.FILES['sign2']
            path = default_storage.save('tmp/sign1.jpg', ContentFile(sign1.read()))
            sign1 = os.path.join(settings.MEDIA_ROOT, path)
            sign1 = imread(sign1)
            path = default_storage.save('tmp/sign2.jpg', ContentFile(sign2.read()))
            sign2 = os.path.join(settings.MEDIA_ROOT, path)
            sign2 = imread(sign2)
            dist = Signature_Matching(sign1,sign2)    
            response['status']=200
            response['Difference']=dist
            
        except Exception as e:
            error()
            print("ERROR IN = Match_SignatureAPI", str(e))

        return Response(data=response)

Match_Signature = Match_SignatureAPI.as_view()

class Add_SignatureAPI(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,BasicAuthentication)
    def post(self, request, *args, **kwargs):
        response = {}
        response["status"] = 500
        try:
            data = request.FILES['Image']
            path = default_storage.save('tmp/somename.jpg', ContentFile(data.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            [sign2,acc] = ImageSegmentation(tmp_file)
            acc_num  = Account_Number_Extraction(acc)
            if(Slip.objects.filter(Account_Number = acc_num).exists()):
                response['status']=409
                response['Account_Number']=acc_num
            else:
                sp = Slip.objects.create(Account_Number=acc_num)
                img = Image.fromarray(sign2)
                img_path = os.path.join(settings.MEDIA_ROOT, 'image/'+acc_num+'.jpg')
                img.save(img_path)
                sp.Image_Path = 'image/'+acc_num+'.jpg'
                sp.save()
                response['status']=201
                response['Account_Number']=acc_num
                response['sign1']=sp.Image_Path.url

        except Exception as e:
            error()
            print("ERROR IN = Add_SignatureAPI", str(e))

        return Response(data=response)
Add_Signature = Add_SignatureAPI.as_view()