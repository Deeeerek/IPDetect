import socket
import fcntl
import time
import struct
import smtplib
import urllib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import subprocess

def sendEmail(smtpserver,username,password,sender,receiver,subject,msghtml):
    msgRoot = MIMEMultipart('related')
    msgRoot["To"] = ','.join(receiver)
    msgRoot["From"] = sender
    msgRoot['Subject'] = subject
    msgText = MIMEText(msghtml,'html','utf-8')
    msgRoot.attach(msgText)
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msgRoot.as_string())
    smtp.quit()

def check_network():
    while True:
        try:
            result=urllib.urlopen('http://baidu.com').read()
            print result
            print "Network is Ready!"
            break
        except Exception , e:
            print e
            print "Network is not ready,Sleep 5s...."
            time.sleep(5)
            return True

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1",80))
    ipaddr=s.getsockname()[0]
    s.close()
    return ipaddr

def get_pub_ip(server):
    pubip=subprocess.check_output('curl '+server, shell=True)
    return server+': '+pubip

if __name__ == '__main__':
    check_network()
    ipaddr=get_ip_address()
    print(ipaddr)
    msg="private ip: "+ipaddr+"\n"
    pubip=get_pub_ip("ident.me")    
    # a little slow
    #pubip=get_pub_ip("ifconfig.me")
    print(pubip)
    msg+=pubip+"\n"
    pubip=get_pub_ip("icanhazip.com")
    print(pubip)
    msg+=pubip+"\n"
    pubip=get_pub_ip("whatismyip.akamai.com")
    print(pubip)
    msg+=pubip+"\n"
    print(msg)
    sendEmail('smtp.126.com','xxxxx@126.com','passwd','xxxxxx@126.com',['receive@xxx.com','receive2@xxx.com'],'IP Address Of Raspberry Pi',msg)
