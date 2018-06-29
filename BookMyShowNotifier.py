import time
from smtplib import SMTP
from urllib2 import Request
from urllib2 import urlopen
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate

cinema = "PVR"
url = "https://in.bookmyshow.com/buytickets/sanju-hyderabad/movie-hyd-ET00063643-MT/20180707"

web_charset = "utf-8"
mail_charset = "ISO-2022-JP"

from_name = "BMS Notifier"
from_address = "bulk.dealalerts@gmail.com" # Sender address (Gmail address)
from_password = "sarahahconvo" # Sender server password (Gmail password)
to_address   = "akshaydamle95@gmail.com" # Recipient address

def create_message(from_name, to_addr, subject, body, encoding):
	msg = MIMEText(body, 'plain', encoding)
	msg['From'] = from_name
	msg['To'] = to_addr
	msg['Subject'] = Header(subject, encoding)
	msg["Date"] = formatdate(localtime=True)
	return msg

def sendmail(subject, text):
	msg = create_message(from_name, to_address, subject, text, mail_charset)
	s = SMTP('smtp.gmail.com', 587)
	s.ehlo(), s.starttls(), s.ehlo()
	s.login(from_address, from_password)
	s.sendmail(from_address, to_address, msg.as_string())
	s.close()

def get_now_showing():
	req = Request(url, headers={'User-Agent' : "Magic Browser"})
	return urlopen(req).read()

while True:
	try:
		now_showing = get_now_showing()
		if url[-8:] in now_showing and cinema in now_showing:
			break
		time.sleep(30)
	except:
		time.sleep(30)

print "Tickets available."
sendmail(u"Tickets Available!", "Tickets are available on BookMyShow.")