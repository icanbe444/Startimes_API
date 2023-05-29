from rest_framework import serializers
from datetime import datetime
from rest_framework.exceptions import ValidationError
   

class PaymentSerializer(serializers.Serializer):
   payer_number         = serializers.RegexField(required=False, regex=r"[0-9]+")
   payment_number       = serializers.RegexField(required=False, regex=r"[0-9A-Za-z]+")
   tranref              = serializers.RegexField(required=False, regex=r"[0-9A-Za-z]+")
   amount               = serializers.DecimalField(max_digits=20, decimal_places=2)
   payment_description  = serializers.CharField(required=False)
   
class ValidationSerializer(serializers.Serializer):
   service_code         = serializers.RegexField(required = True, regex=r"[0-9A-Za-z]+")
   

  
    
   def validate(self, data):
   

      
      service_code      = data.get("service_code")
                
      return ((
            "success", True
            if service_code else "Service code number cannot be empty", False
         )
         
      )