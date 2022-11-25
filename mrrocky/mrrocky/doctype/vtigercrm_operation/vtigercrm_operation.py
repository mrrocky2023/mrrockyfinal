from frappe.model.document import Document
from frappe import get_doc, db, msgprint
import json
import requests
from hashlib import md5
from datetime import datetime
from urllib.parse import urlencode

class VTigerAPI():
    endpoint: str
    username: str
    accessKey: str
    token: str
    sessionName: str

    def __init__(self, endpoint, username, accesskey):
        self.endpoint = endpoint + "/webservice.php?"
        self.username = username
        self.accessKey = accesskey
        values = {'operation': 'getchallenge', 'username': self.username}
        params = urlencode(values)
        url = self.endpoint + params
        response = requests.get(url)
        self.token = response.json()['result']['token']
        tempkey = (self.token + self.accessKey).encode('utf-8')
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
        self.sessionName = response.json()['result']['sessionName']
    
    def getContact(self, limit):
        #ts = datetime.timestamp(datetime.now())
        #values = {'operation': 'sync', 'sessionName': self.values['sessionName'], 'elementType': 'Contacts', 'modifiedTime': ts-5000}
        #last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fieldList = "firstname,lastname"
        values = {'operation': 'query', 'sessionName': self.sessionName}
        params = urlencode(values)
        url = self.endpoint + params
        result = []
        for i in range(0, limit, 100):
            #query = {'query': "SELECT " + fieldList + " FROM Contacts WHERE modifiedtime >= " + last_update + " ORDER BY modifiedtime DESC LIMIT " + str(i) + "," + str(i + 99) + ";"} 
            if (i + 100) < limit:
                query = {'query': "SELECT " + fieldList + " FROM Contacts ORDER BY modifiedtime DESC LIMIT " + str(i + 1) + "," + str(i + 100) + ";"}
            else:
                query = {'query': "SELECT " + fieldList + " FROM Contacts ORDER BY modifiedtime DESC LIMIT " + str(i + 1) + "," + str(limit) + ";"}
            url = url + "&" + urlencode(query)
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code != 204:
                result += response.json()['result']
        return result
        
class VTigerCRMOperation(Document):
    def on_update(self):
        for config in self.get('config'):
            VT = VTigerAPI(config.endpoint, config.username, config.accesskey)
        contacttemp = VT.getContact(self.limit)
        for CT in contacttemp:
            doc = get_doc({
                'doctype': 'Contact',
                'first_name': CT['firstname'],
                'last_name': CT['lastname'],
                'parenttype': 'Test',
                'parent': self.name
            })
            #doc.insert()
            #msgprint(
            #    msg={'doc','doc2'},
            #    title='Error',
            #    as_list=doc
            #)
            #self.result.append(doc)

        
        #data = db.get_list('Contact',
        #    filters={
        #        'import': self.name
        #    },
        #    fields=['name','first_name','last_name','import']
        #)
        #print("data: " + str(data))
        #if data:
        #    for mtc in data:
        #        doc = get_doc({
        #            'doctype': 'Contact',
        #            'first_name': contacttemp[0]['firstname'],
        #            'last_name': contacttemp[0]['lastname'],
        #            'parent': 'Test',
        #            'import': self.name
        #        })
        #        self.result.append(doc)
        #self.result = frappe.db.get_list('Contact',
        #    filters={
        #        'import': self.name
        #    },
        #    fields=['name','first_name','last_name','import']
        #)



