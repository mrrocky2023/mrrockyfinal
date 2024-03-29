# Copyright (c) 2022, Jorge Devia and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe import msgprint
import requests
from hashlib import md5
from datetime import datetime
from urllib.parse import urlencode

class VtigerCRMSettings(Document):
	def get_sessionname(self):
		token: str
		values = {'operation': 'getchallenge', 'username': self.username}
		params = urlencode(values)
		url = 'http://' + self.host + '/' + self.path + '/webservice.php?' + params
		response = requests.get(url)
		token = response.json()['result']['token']
		tempkey = (token + 'MFaeyxCMTmRrUZiE').encode('utf-8')
		key = md5(tempkey)
		tokenizedAccessKey = key.hexdigest()
		values['accessKey'] = tokenizedAccessKey
		payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; " \
				"name=\"operation\"\r\n\r\nlogin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: " \
				"form-data; name=\"username\"\r\n\r\n" + \
				self.username + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; " \
							"name=\"accessKey\"\r\n\r\n" + \
				tokenizedAccessKey + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
		headers = {
			'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
			'Cache-Control': "no-cache"
		}
		response = requests.request("POST", url, data=payload, headers=headers)
		print(response.json())
		if response.json()['success'] == True:
			self.sessionname = response.json()['result']['sessionName']
		else:
			msgprint(
				msg=response.json()['error']['message'],
				title=response.json()['error']['code'],
			)
