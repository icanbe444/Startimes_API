from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework import generics, status
from .serializers import ValidationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import os
import requests, json
import sys
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning



requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



base_url            = os.getenv('base_url')

headers = {
            # 'Authorization': f'Basic {auth}',
            'Content-Type': 'application/json',
            'Username' : os.getenv('USERNAME'),
            'Password' : os.getenv('PASSWORD')
}



    

class ValidationView(GenericAPIView):
    """
    To validat
    """
   
    # permission_classes = (IsAuthenticated, )
    serializer_class    = ValidationSerializer
    status_url          = f"{str(base_url)}/v1/service-status"
    validation_url      = f"{str(base_url)}/v1/subscribers/"

    def get(self, request, *args, **kwargs):
        
        data = request.data
        print (f"data in validate: {data}")
        try:
            serialized_data = self.serializer_class(data = data)
            print (f"serialized data in validate: {serialized_data}")
            if not serialized_data.is_valid(raise_exception=True):
                return Response({"Message" : "Please enter correct details", "status":"Failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print (f"error in first try block of validate: {e.args[0]}")
            return Response({"message" : "An error occurred while validating. Please try again later", "status":"Failed"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
                    "service_code": data["service_code"]
                }
        print (f"Payload in validate: {payload}")
        try:
            # import pdb
            # pdb.set_trace()
            ca          = os.path.abspath("ca.pem")
            key         = os.path.abspath("uba-mtls.key")
            pem_file    = os.path.abspath("uba-mtls.pem")
            response    = requests.request("GET", self.status_url,verify=False, cert= (pem_file,key) )
            print (f"response from service_status: {response.text}")
            if response.status_code != 200:
                return Response({"Response":{"message": "An error occurred while connecting to host server","status":"Failed"}} , status=status.HTTP_400_BAD_REQUEST)
            url = self.validation_url + data["service_code"]
           
            response = requests.request("GET", url,verify=False, cert= (pem_file,key, ca) )
            print (f"response in validate: {response.text}")
            if response.status_code != 200:
                return Response({"Response":{"message": "An error occurred while connecting to host server","status":"Failed"}} , status=status.HTTP_400_BAD_REQUEST)
           
            print("Validation successfully done")
            res = response.json()
            print (f"res in validate: {res}")
            
        except Exception as e:
            print (f"error in second try block of validate: {e.args[0]}")
            return Response({"Response":{"message": "An error occurred while connecting to host server","status":"Failed"}} , status=status.HTTP_400_BAD_REQUEST)
       
            
        # VAS requirement
        print({
            "vendor_url": self.status_url,
            "res": str(res) or None,
            "vas_payload": str(request.data),
            "vas_url": str(request.path),
        }, file=sys.stdout)
        res_message = f"SUBSCRIBER ID: {res.get('subscriber_id')} | SERVICE CODE: {res.get('service_code')} | CUSTOMER NAME: {res.get('customer_name')} | MOBILE: {res.get('mobile')} | CONTACT_ADDRESS: {res.get('contact_address')} | SUBSCRIBER_STATUS: {res.get('subscriber_status')} | EXPIRATION_DATE: {res.get('expiration_date')} | BASIC_OFFER_DISPLAY_NAME: {res.get('basic_offer_display_name')} | BASIC_OFFER_BUSINESS_CLASS: {res.get('basic_offer_business_class')} | OTHER_INFO: {res.get('other_info')}"
        return Response({"Response":{"message":res_message,"status":"Success"}}) 
        
















