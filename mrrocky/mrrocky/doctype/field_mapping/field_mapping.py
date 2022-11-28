# Copyright (c) 2022, Jorge Devia and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe import get_doc, db, msgprint, get_meta
import requests
from json import dumps
from numpy import array
from hashlib import md5
from datetime import datetime
from urllib.parse import urlencode

class FieldMapping(Document):
	@frappe.whitelist()
	def get_fields(self, module):
		config = get_doc('VtigerCRM Settings')
		config.on_update()
		values = {'sessionName': config.sessionname, 'operation': 'describe', 'elementType': module}
		params = urlencode(values)
		url = 'http://' + config.host + '/' + config.path + '/webservice.php?' + params
		response = requests.get(url)
		if response.json()['success'] == True:
			fields = response.json()['result']['fields']
			label = [field['label'] + ' (' + field['name'] + ')' for field in fields]
			return label
		else:
			msgprint(
				msg=response.json()['error']['message'],
				title=response.json()['error']['code'],
			)

	def get_module_vtigercrm(self, module, fieldDocType, fieldModule):
        #ts = datetime.timestamp(datetime.now())
        #values = {'operation': 'sync', 'sessionName': self.values['sessionName'], 'elementType': 'Contacts', 'modifiedTime': ts-5000}
        #last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		# fieldList = "firstname,lastname"
		config = get_doc('VtigerCRM Settings')
		config.on_update()
		values = {'operation': 'query', 'sessionName': config.sessionname}
		params = urlencode(values)
		url = 'http://' + config.host + '/' + config.path + '/webservice.php?' + params
		results = []
		i = 0
		limit = 100
		while True:
			query = {'query': "SELECT " + ','.join(fieldModule) + " FROM " + module + " ORDER BY modifiedtime DESC LIMIT " + str(i + 1) + "," + str(i + 100) + ";"}
			url_query = url + "&" + urlencode(query)
			response = requests.get(url_query)
			limit = len(response.json()['result'])
			if limit == 0:
				break
			else:
				print("i ------------------------------------> " + str(i))
				response.raise_for_status()
				if response.status_code != 204:
					results = response.json()['result']
					i += 100
					for result in results:
						listDocType = {'doctype':'Contact'}
						for i in range(0, len(fieldDocType)):
							listDocType[fieldDocType[i - 1]] = result[fieldModule[i - 1]]
						print(listDocType)
						self.create_contact(listDocType)
				break

	@frappe.whitelist()
	def create_contact(self, listDocType):
		get_doc(listDocType).insert(ignore_permissions=True)

	def on_update(self):
		if self.enabled:
			lfContact_VT = []
			lfContact_EN = []
			for relationField in self.get('contacts_fields'):
				lfContact_VT.append(relationField.vtigercrm_contact[relationField.vtigercrm_contact.find('(') + 1:len(relationField.vtigercrm_contact)-1])
				lfContact_EN.append(relationField.erpnext_contact[relationField.erpnext_contact.find('(') + 1:len(relationField.erpnext_contact)-1])
			self.get_module_vtigercrm('Contacts', lfContact_EN, lfContact_VT)
				#results = self.get_module_vtigercrm('Contacts', fieldList)
			if self.schedule:
				"""event = frappe.get_doc(
					{
						"doctype": "Event",
						"owner": self.owner,
						"subject": 'description',
						"description": 'description',
						"starts_on": 'cstr(key["scheduled_date"])' + " 10:00:00",
						"event_type": "Private",
					}
				)
				event.add_participant(self.doctype, self.name)
				event.insert(ignore_permissions=1)"""
				pass
			else:
				pass
