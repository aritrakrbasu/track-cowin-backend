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


#header to show the request is from a website
headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }  

# Use a service account
cred = credentials.Certificate(os.getenv('serviceAccountdet'))
firebase_admin.initialize_app(cred)

db = firestore.client()

# todays date
today = date.today()
formateddate = str(today.day)+'-'+str(today.month)+'-'+str(today.year)

#function to send email 
def sendEmail(user,availableCenters):
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
        <p><strong>If you want to stop getting notifications <a href="https://track-cowin.web.app/unsubscribe/${email}" target="_blank" rel="noopener">click here</a> . </strong></p>
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
        <p><strong>If you want to stop getting notifications <a href="https://track-cowin.web.app/unsubscribe/${email}" target="_blank" rel="noopener">click here</a> . </strong></p>
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

        #get each user details
        for user in listofuser:
            availableCenters = list() 
            if not "pincode" in user:
                # get data statewise 
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
                sendEmail(user,availableCenters)

