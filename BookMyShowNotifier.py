import re
import urllib2
import datetime
import locale
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate

web_charset = "utf-8"
mail_charset = "ISO-2022-JP"

from_name = "BMS Notifier"
from_address = "disposableemailaccount@gmail.com" # Sender address (Gmail address)
from_password = "disposableemailaccountpassword" # Sender server password (Gmail password)
to_address   = "myemailaccount@gmail.com" # Recipient address

def create_message(from_name, to_addr, subject, body, encoding):
	msg = MIMEText(body, 'plain', encoding)
	msg['From'] = from_name
	msg['To'] = to_addr
	msg['Subject'] = Header(subject, encoding)
	msg["Date"] = formatdate(localtime=True)
	return msg

def sendmail(subject, text):
	msg = create_message(from_name, to_address, subject, text, mail_charset)
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(from_address, from_password)
	s.sendmail(from_address, to_address, msg.as_string())
	s.close()

class BookMyShowClient(object):
  def __init__(self):
    self.__url = "https://in.bookmyshow.com/buytickets/deadpool-2-hyderabad/movie-hyd-ET00049430-MT/20180523"
    self.__html = None

  def __download(self):
    req = urllib2.Request(self.__url, headers={'User-Agent' : "Magic Browser"})
    html = urllib2.urlopen(req).read()
    return html

  def get_now_showing(self):
    if not self.__html:
      self.__html = self.__download()
    return self.__html

bms_client = BookMyShowClient()

while True:
  now_showing = bms_client.get_now_showing()
  if "PVR ICON" in now_showing:
    print "Tickets available."
	mailsubject = u"Tickets Available!"
	sendmail(mailsubject, "Tickets are available on BookMyShow.")
	break