These r copy files for mail and ip detect
note:

1.put mail.py & mail_check.py under /home/pi.
2.put mail under /etc/init.d/
3.run chmod +x mail.py 
      chmod +x /etc/init.d/mail.py
4.auto start: sudo update-rc.d mail defaults
5.sudo crontab -e :
	0 * * * * root python /home/pi/mail_check.py

vnc notice:
After default installation, you may need to change the last line of ~/.vnc/xstartup into 
"/usr/bin/lxsession -s LXDE"
to avoid gray screen
