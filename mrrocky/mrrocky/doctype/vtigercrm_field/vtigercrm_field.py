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

class VTigerCRMField(Document):
	@frappe.whitelist()
	def getFields(self, module):
		config = get_doc('VTigerCRM Config', self.config)
		config.on_update()
		values = {'sessionName': config.sessionname, 'operation': 'describe', 'elementType': module}
		params = urlencode(values)
		url = config.endpoint + "/webservice.php?" + params
		response = requests.get(url)
		if response.json()['success'] == True:
			fields = response.json()['result']['fields']
			label = [field['label'] for field in fields]
			return label
		else:
			msgprint(
				msg=response.json()['error']['message'],
				title=response.json()['error']['code'],
			)