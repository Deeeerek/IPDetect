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
# check if pub ip addr has changed
# if cha    currentip[1]=pubip 
# else
#	ip addr didn't change, do not send mail
# Timer= 1 hour is fine ?
def record_pub_ip(pub_ip):
    record_file=open("/home/pi/ip_log.txt","r+")
    record=[" "," "," "," "]
    record[0]=record_file.readline().strip('\n')
    record[1]=record_file.readline().strip('\n')
    record[2]=record_file.readline().strip('\n')
    record[3]=record_file.readline().strip('\n')
    step=0
    print("New ip :")
    for x in range(4):
	print(pub_ip[x])
    print("Old ip :")
    for x in range(4):
	print(record[x])
	if record[x]==pub_ip[x]:
	     step=step+1
    record_file.close()
    print(step)
    if step==4:
	return True
    else:
	return False
    
    
if __name__ == '__main__':
    currentip=[" "," "," "," "]
    check_network()
    ipaddr=get_ip_address()
    currentip[0]=ipaddr
    print(ipaddr)
    msg="private ip: "+ipaddr+"\n"
    pubip=get_pub_ip("ident.me")    
    # a little slow
    #pubip=get_pub_ip("ifconfig.me")
    currentip[1]=pubip
    print(pubip)
    msg+=pubip+"\n"
    pubip=get_pub_ip("icanhazip.com")
    currentip[2]=pubip 
    print(pubip)
    msg+=pubip+"\n"
    pubip=get_pub_ip("whatismyip.akamai.com")
    currentip[3]=pubip 
    print(pubip)
    msg+=pubip+"\n"
    print(msg)
    for x in range(4):
	currentip[x]=currentip[x].strip("\n")
    if record_pub_ip(currentip)==False:
      	#print("False")
      	sendEmail('smtp.126.com','xxxx@126.com','passwd','xxxxxxx@126.com',['receive1@hotmail.com','receive2@xxx.com'],'IP Address Of Raspberry Pi',msg)
    now = time.strftime("%x %X")
    f=open("/home/pi/ip_log.txt","w")
    for x in range(4):
        f.write(currentip[x]+"\n")
    f.write(now+"\n")
    f.close()
    
