

def create_random_code(num):
    import random
    num-=1
    return random.randint(10**num,10**(num+1)-1)



from sms_ir import SmsIr
import time
import threading
import argparse
import requests
from requests.exceptions import RequestException, JSONDecodeError

def send_sms(number, code):
    pass
#     sms_ir = SmsIr('he4QV5RJiXYsfgjHBpgjpJ2GMFtemy28GSEcDlCpEweK9q0ahroGcmgT5kexuJUR')

#     while True:
#         try:
#             # تلاش برای ارسال پیامک
#             result = sms_ir.send_verify_code(
#                 number=str(number),
#                 template_id=172582,
#                 parameters=[
#                     {
#                         "name": "CODE",
#                         "value": str(code)
#                     }
#                 ],
#             )

#             # تلاش برای تجزیه JSON
#             result_data = result.json()
#             status = result_data.get('status')
#             message = result_data.get('message')

#             if status == 1:
#                 print("پیامک با موفقیت ارسال شد!")
#                 break
#             elif status in {400, 401, 429, 500}:
#                 print(f"ارسال پیامک شکست خورد: {message}. 20 ثانیه دیگر تلاش می‌کنیم...")
#                 time.sleep(20)
#             else:
#                 print("پاسخ غیرمنتظره. دوباره تلاش می‌کنیم...")
#                 time.sleep(20)

#         except JSONDecodeError:
#             print("خطا در تجزیه JSON. احتمالاً پاسخ معتبری از سرور دریافت نشده.")
#             time.sleep(20)
#         except RequestException:
#             print("اتصال اینترنتی مشکل دارد یا سرور در دسترس نیست. 20 ثانیه دیگر تلاش می‌کنیم...")
#             time.sleep(20)
#         except Exception as e:
#             print(f"خطای غیرمنتظره: {e}")
#             time.sleep(20)

# def start_sms_thread(number, code):
#     sms_thread = threading.Thread(target=send_sms, args=(number, code))
#     sms_thread.start()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Send SMS verification code.')
#     parser.add_argument('phone_number', type=str, help='Phone number to send SMS to')
#     parser.add_argument('verification_code', type=str, help='Verification code to send')

#     args = parser.parse_args()
#     phone_number = args.phone_number
#     verification_code = args.verification_code

#     start_sms_thread(phone_number, verification_code)




    
def send_ticket(number,name,subject):
    pass
    print('FFFFFFFFFFFFFFFFFFF',name,number,subject)

    sms_ir = SmsIr('he4QV5RJiXYsfgjHBpgjpJ2GMFtemy28GSEcDlCpEweK9q0ahroGcmgT5kexuJUR')

    result = sms_ir.send_verify_code(
    number= str(number),
    template_id=259743,
    parameters=[
        {
            
            "name" : "NAME",
            "value": str(name)
        },
        {

            "name" : "SUBJECT",
            "value": str(subject)
        }
    ],
)
        
#-=============================
import os
from uuid import uuid4
class FileUpload:
    
    
    def __init__(self,dir,prefix):
        self.dir = dir
        self.prefix = prefix
        
        
        
    def upload_to(self,instance,filename):
        filename,ext=os.path.splitext(filename)
        return f'{self.dir}/{self.prefix}/{uuid4()}{filename}{ext}'
    
    
#==========================
def price_by_final_price(price,discount=0):
    pass




import socket

def has_internet_connection():
    """
    Check if the device has an active internet connection.
    
    Returns:
        bool: True if the device has an active internet connection, False otherwise.
    """
    try:
        # Try to connect to a well-known website
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    
    try:
        # Try to connect to a different well-known website
        socket.create_connection(("www.example.com", 80))
        return True
    except OSError:
        pass
    
    return False
# ===================================

def price_by_delivery_tax(price,discount=0):
    delivery =25000
    if price > 700000:
        delivery = 0
    tax = (price+delivery)*0.09
    sum = price+delivery+tax
    sum = sum-(sum*discount/100)
    return int(sum),delivery,int(tax)