from credentials import *
from bs4 import BeautifulSoup
from geolocation.main import GoogleMaps
import threading
import requests
import tweepy
import re
import time

google_maps = GoogleMaps(api_key='')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
oldCall1 = None
calls1 = []

def checkCalls():
  threading.Timer(10, checkCalls).start()
  global oldCall1
  global calls1

  url = "https://webapp.pulsepoint.org/active_incidents.php?agencyid=AGENCYIDHERE&tz=420"
  html = requests.post(url).text
  soup = BeautifulSoup(html, 'html.parser')
  table = soup.findChildren('rows')[0]
  rows = table.findChildren('row')

  for row in rows:
      temprow = []
      cells = row.findChildren('cell')
      for cell in cells:
        cell_content = cell.getText()
        clean_content = re.sub( '<[^<>]+>', '', cell_content).strip()
        temprow.append(clean_content)
      calls1.append(temprow)

  #print calls[0][0] # Date / Time
  #print calls[0][1] # Call Acronym
  #print calls[0][2] # Location
  #print calls[0][3] # Units
  #print calls[0][4] # Location Coordinates
  #print calls[0][5] # Call Name

  if (oldCall1 != calls1[0][0]):
      time.sleep(5)
      try:
          latitude,longnitude = calls1[0][4].split(',')
          location = google_maps.search(lat=latitude, lng=longnitude).first()
          print "CALL: [" + calls1[0][1] + "] " + calls1[0][5] + " \nADDR: " + calls1[0][2] + " \nUNITS: " + calls1[0][3] + " \nD/T: " + calls1[0][0] + " \n#" + re.sub('\W', '', location.city)
          api.update_status("CALL: [" + calls1[0][1] + "] " + calls1[0][5] + " \nADDR: " + calls1[0][2] + " \nD/T: " + calls1[0][0] + " \n#" + re.sub('\W', '', location.city))
      except:
          print "ERROR"

  oldCall1 = calls1[0][0]
  calls1 = []
  print oldCall1

checkCalls()
