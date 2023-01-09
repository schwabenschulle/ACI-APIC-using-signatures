'''
cisco Documentation
https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/security-configuration/cisco-apic-security-configuration-guide-release-52x/access-authentication-and-accounting-52x.html#task_EB1F08D384C942FB82554D78CD7FA6D5
'''

'''
generate key and certificate
openssl genrsa -out server.key 4096
openssl req -new -key server.key -out server.csr -subj '/CN=User certtest/O=BOSCH/C=DE
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
'''

import OpenSSL   
from OpenSSL import crypto    # pip install pyOpenSSL
import base64
import requests
import json
requests.packages.urllib3.disable_warnings()

class aci:
    def __init__(self, **kwargs):
        self.session = requests.Session()
        self.url = kwargs.get("url", None)

    def sign(self, payload, certdn, key_file):
        key_file = open(key_file)
        key = key_file.read()
        key_file.close()

        privatekey = crypto.load_privatekey(crypto.FILETYPE_PEM, key)
        payloadsign = OpenSSL.crypto.sign(privatekey, bytes(payload, 'UTF-8'), "sha256")
        payloadsign_base64 = base64.b64encode(payloadsign).decode()
        self.cookie = {'APIC-Request-Signature' : payloadsign_base64, 'APIC-Certificate-DN' : certdn, 'APIC-Certificate-Algorithm' : 'v1.0', 'APIC-Certificate-Fingerprint' : 'fingerprint'}

        
    def get(self, classdn):
        self.response = self.session.get(f"{self.url}{classdn}", verify=False, cookies=self.cookie)
        
    def post(self, uri, data):
        self.response = self.session.post(f"{self.url}{uri}", data=json.dumps(data), verify=False, cookies=self.cookie)


# Set some base variables
url = "https://si-cc18-sddc-apic1.net-mgmt.bosch.com"
certdn = "uni/userext/user-certtest/usercert-certtest"  # you can retrieve by downloading the certifcate in Cisco APIC 
keyfile = "server.key"

#Example for GET
uri = "/api/class/fvTenant.json"
payload = "GET/api/class/fvTenant.json"
aci_session = aci(**{"url" : url})
aci_session.sign(payload, certdn, keyfile)
aci_session.get(uri)
print (aci_session.response.status_code)
print (aci_session.response.content)

#Example for POST
uri = "/api/mo/uni.json"

data = {
    "totalCount": "1",
    "imdata": [
        {
            "fvBD": {
                "attributes": {
                    "arpFlood": "yes",
                    "dn": "uni/tn-test_tenant/BD-test_bd",
                    "ipLearning": "yes",
                    "ipv6McastAllow": "no",
                    "limitIpLearnToSubnets": "yes",
                    "mac": "00:22:BD:F8:19:FF",
                    "unicastRoute": "yes",
                },
                "children": [
                    {
                        "fvRsCtx": {
                            "attributes": {
                                "annotation": "",
                                "tnFvCtxName": "default",
                                "userdom": "all"
                            }
                        }
                    }
                ]
            }
        }
    ]
}
payload = f'POST{uri}{json.dumps(data)}'
print (payload)
aci_session.sign(payload, certdn, keyfile)
aci_session.post(uri,data)
print (aci_session.response.status_code)
print (aci_session.response.content)

#Example with cobra
#!/usr/bin/env python
# It is assumed the user has the X.509 certificate already added to
# their local user configuration on the APIC
#from cobra.mit.session import CertSession
#from cobra.mit.access import MoDirectory

#def readFile(fileName=None, mode="r"):
#    if fileName is None:
#        return ""
#    fileData = ""
#    with open(fileName, mode) as aFile:
#        fileData = aFile.read()
#    return fileData

#pkey = readFile("server.key")
#csession = CertSession("https://si-cc18-sddc-apic1.net-mgmt.bosch.com/",
#                       "uni/userext/user-certtest/usercert-certtest", pkey)

#modir = MoDirectory(csession)
#resp = modir.lookupByDn('uni/fabric')
#resp2 = modir.lookupByClass('fvTenant')
#for e in resp2:
#    print (e.dn)

# End of script