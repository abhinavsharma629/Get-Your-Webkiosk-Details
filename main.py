import os
import mechanicalsoup
import requests
from bs4 import BeautifulSoup
import re
import urllib
import sys
import linecache
from prettytable import PrettyTable
import smtplib
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders


headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}

browser=mechanicalsoup.StatefulBrowser()
browser.open("https://webkiosk.juet.ac.in/index.jsp")
browser.select_form('form[name="LoginForm"]')
browser['InstCode']="JUET"
#ch=input("Enter S,E,G,P")
browser['UserType']="S"
browser['MemberCode']="171B009"
browser['DATE1']="23/08/1998"
browser['Password']="abhinavsharma629@"
browser.submit_selected()
#print(browser.get_url())


def attendance():
    r1=browser.get("https://webkiosk.juet.ac.in/StudentFiles/StudentPage.jsp",headers=headers)
    soup=BeautifulSoup(r1.content,'lxml')
    #print(soup)
    r2=browser.get("https://webkiosk.juet.ac.in/StudentFiles/../StudentFiles/FrameLeftStudent.jsp",headers=headers)
    soup2=BeautifulSoup(r2.content,'lxml')
    #print(soup3.prettify())
    r3=browser.get("https://webkiosk.juet.ac.in/StudentFiles/Academic/StudentAttendanceList.jsp",headers=headers)
    soup3=BeautifulSoup(r3.content,'lxml')
    #print(soup3.prettify())

    atten=[]
    for i in soup3.find_all('td'):
        string=i.get_text().strip()
        string=re.sub(r"[\t\xa0]*","", string)
        atten.append(string)

    #print(atten)
    i=0
    attendance=PrettyTable(['S_No.','Subject Name + Code','Tutorial+Lecture','Lecture','Tutorial','Practical'])
    if(len(atten)<=12):
        attendance.add_row(['','','','','',''])
    else:
        array=[]
        st=""
        count=0
        k=12
        for i in range(12,len(atten)-6):
            attendance.add_row([atten[k],atten[k+1],atten[k+2],atten[k+3],atten[k+4],atten[k+5]])
            attendance.add_row(['','','','','',''])
            k=k+6
            if(k>=len(atten)):
                break
    print("ATTENDANCE IS:- ")
    print(attendance,"\n\n")
    f=open("attendance.txt","w+")
    f.write(attendance.get_string())
    f.close()

attendance()


def result():
    browser.open("https://webkiosk.juet.ac.in/StudentFiles/Exam/StudentEventMarksView.jsp")
    browser.select_form('form[name="frm"]')
    browser["exam"]="2018ODDSEM"
    browser.submit_selected()
    #print(browser.get_url())
    r4=browser.get("https://webkiosk.juet.ac.in/StudentFiles/Exam/StudentEventMarksView.jsp?x=&exam=2018ODDSEM",headers=headers)
    soup4=BeautifulSoup(r4.content,'lxml')

    res=[]
    for i in soup4.find_all('td'):
        string=i.get_text().strip()
        string=re.sub(r"[\t\xa0]*","", string)
        res.append(string)

    #print(res)
    i=0
    result=PrettyTable(["S_No.","Subject Name + Code",'P1','P2','T1','T2','T3'])
    if(len(res)<=10):
        result.add_row(['','','','','','',''])
    else:
        array=[]
        st=""
        count=0
        k=10
        for i in range(10,len(res)-7):
            result.add_row([res[k],res[k+1],res[k+2],res[k+3],res[k+4],res[k+5],res[k+6]])
            result.add_row(['','','','','','',''])
            k=k+7
            if(k>=len(res)):
                break
    
    print("RESULT IS:-")
    print(result,"\n\n")
    f=open("result.txt","w+")
    f.write(result.get_string())
    f.close()

result()


def seatingplan():
    r5=browser.get("https://webkiosk.juet.ac.in/StudentFiles/Exam/StudViewSeatPlan.jsp",headers=headers)
    soup5=BeautifulSoup(r5.content,'lxml')
    #print(soup.prettify())
    s=""
    seat=[]
    a2=[]
    for i in soup5.find_all('tr'):
        seat.append(i.get_text())

    for sj in seat:
        for sjk in sj:
            if(sjk=='\n'):
                a2.append(s)
                s=""
            else:
                s=s+sjk
        s=""

    #print(a2)
    c=0
    for i in a2:
        if("Paper ID" in i):
            c=c+1
    #print(c)

    seating_plan=PrettyTable(['Paper ID','Date','Exam Center Name','Room Name','Row','Column','Seat Number'])

    j=0
    i=0
    for j in range(0,c):
        seating_plan.add_row([a2[10+i],a2[10+i+1],a2[10+i+9],a2[10+i+10],a2[10+i+11],a2[10+i+12],a2[10+i+13]])
        seating_plan.add_row(['','','','','','',''])
        i=i+14
    print("SEATING PLAN IS:-")
    print(seating_plan)
    print()
    print()

    f=open("seating_plan.txt","w+")
    f.write(seating_plan.get_string())
    f.close()

seatingplan()


def send_mail(send_from, send_to, subject, message, files=[],
              server="smtp.gmail.com", port=587, username='', password='',
              use_tls=True):
    '''Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (str): to name
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    '''
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(op.basename(path)))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
    print("DETAILS SENT TO YOUR EMAIL SUCCESSFULLY")

send_mail("abhinavsharma629@gmail.com","abhinavsharma629@gmail.com","Details", '''
Name:- Abhinav Sharma
Er_No:- 171B009
Batch:- BX-B1''', 
["C:/Users/User/Desktop/webkiosk/attendance.txt","C:/Users/User/Desktop/webkiosk/result.txt","C:/Users/User/Desktop/webkiosk/seating_plan.txt"],
              "smtp.gmail.com",587, 'abhinavsharma629@gmail.com', 'meripehalimohobbat1234@@',True)