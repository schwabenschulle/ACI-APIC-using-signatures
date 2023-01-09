# Example of how to use private key for API transaction with cisco ACI

* Summary
  This is an example how to sign payload with a private key to communicate without aaa token to cisco APIC.
  For this you need to sign any payload you send and add the signed base64 encode string as cookie
  e.g. self.cookie = {'APIC-Request-Signature' : payloadsign_base64, 'APIC-Certificate-DN' : certdn, 'APIC-Certificate-Algorithm' : 'v1.0', 'APIC-Certificate-Fingerprint' : 'fingerprint'}
  See cisco documentaion or review so code for more details.
  Important is the format of the signed payload.
  * GET Example - "GET/api/class/fvTenant.json"
  * POST EXAMPLE - "POST/api/mo/uni.json{"totalCount": "1", "imdata": [{"fvBD": {"attributes": {"arpFlood": "yes", "dn": "uni/tn-test_tenant/BD-test_bd", "ipLearning": "yes", "ipv6McastAllow": "no", "limitIpLearnToSubnets": "yes", "mac": "00:22:BD:F8:19:FF", "unicastRoute": "yes"}, "children": [{"fvRsCtx": {"attributes": {"annotation": "", "tnFvCtxName": "default", "userdom": "all"}}}]}}]}"
* cisco Documentation for 5.x
  https://www.cisco.com/c/en/us/td/docs/dcn/aci/apic/5x/security-configuration/cisco-apic-security-configuration-guide-release-52x/access-authentication-and-accounting-52x.html#task_EB1F08D384C942FB82554D78CD7FA6D5
* Generate key and certificate
  openssl genrsa -out server.key 4096
  openssl req -new -key server.key -out server.csr -subj '/CN=User certtest/O=BOSCH/C=DE
  openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
