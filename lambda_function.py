import dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import os


serviceAccountdet = {
  "type": "service_account",
  "project_id": "track-cowin",
  "private_key_id": "cdaedb0dddae4d00f0b6028643647d5bc3b0f3cd",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDQkwaWqaGCvtTH\nHBaOITTNvY9yXbwbTQ6CUrtVNNFjGou8hGFIFm7Np9jX63QQfYCxpKDRNHG7WGd7\nCUIBFpVDFVsO2TCZZmeAzBWkReAqZHTPKxl5axVt0NCDeIJ9pIAtr5TbMO8cB6g2\nX47FvRu1lPqFFveH1feMSd6JBC4mRzWvXjSGcx45fPMeb+DGe9eo3RWvVOOQOphY\nx9U4IcOoKE4/mL9OJC72tIkCVIjTswJx1BojjOYKJZjpMhdip8675fKmmTsF5To9\nOSFpkXtnsVhrrql0jZmlMV00fVMfIj2Nb+ML49oAkR6xNLvehGaVjtAzqyKPS05g\nJ6S92VFfAgMBAAECggEAP555Bf+byhuXH1yL7LJoPtExLfs1Y0ZvxISjq2u+6nGw\nacIfQjPFfGlUFRg2gMknNgg3HVjX0AM5HShHv7k5sgqTicXpswCvVXPqrf66T3Pw\nxTgqPwTQtnxY/aEGfHhuuICz8N/OL0iOoHcpP1tdVleoymuk+QPkzB/EBxsFUJse\nZLjQa6FH5ganhhUcQ9ycAS3IJBHAW/KwbamhrAroZpsiMWTib8Q65RvT11xj4Q48\no7vBtX5QUk/c1IWcO4r2PG4Qd+G2LmeZaQ/rv2ayDp0b2ir1T4qcYaPCrp+4XngD\nm/Cmfm3Y60rpLddUhTa2EAJmy+dn60i2CYFKVp0mwQKBgQD7npl/je2DbNceuik+\nnuXexA06ymJVMVLttYhpwEy56IFl9LZPLB9wuBknNDUEyDOxxvZ5UmzCFnx6gq6C\nZVJDO4IuNSSEWy9wfJ+uMWubHwfU2chT1VviHbL0HfNP+yHp6Xzi2/0tUt8svxpm\nwPz+8VuJSj/xhKBWEXAVMc9ScQKBgQDUNJXSI1mvTGxIj9xchs2UUKUDd4fsrlEc\nEoJNqLGpPu2QGdJ7wLT59NvCruXsHelUlipfDYUvcaXM0ZhyXzYEtYhOKffgPCR2\noVxALoMJbUYHIGYmJ6kFuNJ+Q9FBHwcJSXtBW54lvFJ66dLKkZcj8AIdnrqrnaBF\nwgJGeZQozwKBgETpmgaqO1ucSop61+Lzp+dL8IeieC329UxvRG4aIalk+VOQIwIq\nBm5brV/kV4T4w9ezsztlDK5XdD4lXmAOGeqZ+LxpB5hMVQDM0PrnRB5W8FEmWExF\nigWytplPPp0wHYivzule8MciBEeAC14LCv9T4QsHz914wmTwH69eVfaxAoGAERSG\ndpqHzndNQ+3oY74p7+Up0wSc+SzytFq9CDkqy5+YCYA6k+Fn77KIubvQH9gsfrVz\nhaEV9kKkgL7iEVqeg3SFGx1/qRnOKYpFXZkgzPJxr4MpFasdjKtarfURc7dmnpW+\niP0x1oG49dG6OLnNO4RG91FeXw/Z5aN/AWMpzLsCgYEAmNCPSoHos8aIFLXXqS2M\nHNERfsA3LUh9mZv20J8Lmev41JIfDgYOJKqVPSSJPBMSi4MQn8Nn3SfduEFm0xZl\no7tmjJZuzzxZan0FmOnLtwuh0hoiil4OhW9moJGubIKe4X7UxyCZ1NIYFvnWe4Ax\n5SvBQbRV6KPK8NlSOm15W6g=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-hvat5@track-cowin.iam.gserviceaccount.com",
  "client_id": "108265141722868825983",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-hvat5%40track-cowin.iam.gserviceaccount.com"
}


#header to show the request is from a website
headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }  

# Use a service account
cred = credentials.Certificate(serviceAccountdet)
firebase_admin.initialize_app(cred)

db = firestore.client()

# todays date
today = date.today()
formateddate = str(today.day)+'-'+str(today.month)+'-'+str(today.year)

#function to send email 
def sendEmail(usersDetails,availableCenters):

    for user in usersDetails :
        gmail_user = os.getenv('email')
        gmail_pwd = os.getenv('password')
        TO = user['email']
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        html ="""
        <p><strong><span style="color: #e03e2d;">Note: This websites sends you an automated email whenever their is a availability of vaccine in your area . We use COWIN Api and is not atall an official website for covid vaccine registration . You can book your appointment for covid vaccine by registering at </span> <a href="https://www.cowin.gov.in/home" target="_blank" rel="noopener">COWIN</a></strong></p>
            <br>
            <p><strong>If you want to stop getting notifications <a href='https://track-cowin.web.app/unsubscribe/"""+user['email']+"""' target="_blank" rel="noopener">click here</a> . </strong></p>
            <br><br>
            <Strong> Details of available centers </strong>

            <table border='2'>"""
        html +="""<tr> 
                    <th> Center Name </th> 
                    <th> Center Address</th> 
                    <th>Available Capacity</th> 
                    <th>Fee</th> 
                    <th>Details</th> 
                    <th>slots</th>
                    </tr>"""
        for center in availableCenters:
            html+="<tr>"
            html+="<td>"+center["name"]+"</td>"
            html+="<td>"+center["address"]+"<br> <strong>Pincode:</strong>"+str(center["pincode"])+"<br> <strong>State:</strong> "+center["state_name"]+"<br> <strong>District: </strong> "+center["district_name"]+"</td>"
            html+="<td>"+str(center["available_capacity"])+"</td>"
            html+="<td>"+center["fee_type"]+"<br> Rs "+str(center["fee"])+"/- </td>"
            html+="<td> <Strong>Minimum Age : </strong> "+str(center["min_age_limit"])+"  <br> <strong>Vaccine Type: </strong> "+center["vaccine"]+"</td>"
            html+="<td>"
            for slot in center["slots"]:
                html+=slot+"<br>"
            html+="</td>"
            html+="</tr>"
        html +="""</table>
        <br><br>
            <p><strong><span style="color: #e03e2d;">Note: This websites sends you an automated email whenever their is a availability of vaccine in your area . We use COWIN Api and is not atall an official website for covid vaccine registration . You can book your appointment for covid vaccine by registering at </span> <a href="https://www.cowin.gov.in/home" target="_blank" rel="noopener">COWIN</a></strong></p>
            <br>
            <p><strong>If you want to stop getting notifications <a href='https://track-cowin.web.app/unsubscribe/"""+user['email']+"""' target="_blank" rel="noopener">click here</a> . </strong></p>
        """

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Vaccine available " + user["name"]
        msg['From'] = os.getenv('email')
        msg['To'] =  user['email']
        messagebody = MIMEText(html, 'html')
        msg.attach(messagebody)
        server.sendmail(gmail_user, [TO], msg.as_string())
        server.close()
        print("sent")
    return True                

def lambda_handler(event,context):
    #doc reference
    doc_ref = db.collection('userData').document('userData')

    #get list of users 
    doc = doc_ref.get()

    if doc.exists:
        listofuser = doc.to_dict()['list']

        userDetailsPincode = {}
        userDetailsDistrict = {}
        
        for user in listofuser:
            if "pincode" in user:
                if(user['pincode'] in userDetailsPincode):
                    userDetailsPincode[user['pincode']].append(user)
                else:
                    userDetailsPincode[user['pincode']] =[]
                    userDetailsPincode[user['pincode']].append(user)
            elif "district" in user:
                if(user['district'] in userDetailsDistrict):
                    userDetailsDistrict[user['district']].append(user)
                else:
                    userDetailsDistrict[user['district']] = []
                    userDetailsDistrict[user['district']].append(user)

        for district in userDetailsDistrict: 
            availableCenters = list() 
            URL ="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id="+str(district)+"&date="+str(formateddate)
                #requesting data
            r = requests.get(URL,headers=headers)
            if r.status_code == 200:
                sessions = r.json()["sessions"]
                if(len(sessions) > 0):
                    for session in sessions:
                        if(session["available_capacity"] > 0):
                            availableCenters.append(session)
            if(len(availableCenters) > 0):
                sendEmail(userDetailsDistrict[district],availableCenters)
        
        for pincode in userDetailsPincode:
            availableCenters = list() 
            URL ="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id="+str(user['district'])+"&date="+str(formateddate)
                #requesting data
            r = requests.get(URL,headers=headers)
            if r.status_code == 200:
                sessions = r.json()["sessions"]
                if(len(sessions) > 0):
                    for session in sessions:
                        if(session["available_capacity"] > 0):
                            availableCenters.append(session)
            if(len(availableCenters) > 0):
                sendEmail(userDetailsDistrict[district],availableCenters)


        # #get each user details
        # for user in listofuser:
        #     availableCenters = list() 
        #     if not "pincode" in user:
        #         # get data statewise 
        #         URL ="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id="+str(user['district'])+"&date="+str(formateddate)
        #         #requesting data
        #         r = requests.get(URL,headers=headers)
        #         if r.status_code == 200:
        #             sessions = r.json()["sessions"]
        #             if(len(sessions) > 0):
        #                 for session in sessions:
        #                     if(session["available_capacity"] > 0):
        #                         availableCenters.append(session)
        #     else:
        #         # get data pincodewise 
        #         URL ="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+str(user['pincode'])+"&date="+str(formateddate)
        #         #requesting data
        #         r = requests.get(URL,headers=headers)
        #         if r.status_code == 200:
        #             sessions = r.json()["sessions"]
        #             if(len(sessions) > 0):
        #                 for session in sessions:
        #                     if(session["available_capacity"] > 0):
        #                         availableCenters.append(session)
        #     if(len(availableCenters) > 0):
        #         sendEmail(user,availableCenters)