These r copy files for mail and ip detect
note:

1.put mail.py & mail_check.py under /home/pi.
2.put mial under /etc/init.d/
3.use chmod +x mail.py commond setup mial.py
      chmod +x /etc/init.d/mail.py
4. auto start: sudo update-rc.d mail defaults
5.sudo crontab -e :
	48 * * * * root python /home/pi/mail_check.py

