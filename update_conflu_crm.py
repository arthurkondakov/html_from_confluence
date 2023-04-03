#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import write_conflu
from ldap3 import Server, Connection, ALL
import data_source

server = Server("ldap_address", get_info=ALL)
auth_dn = "login_ldap_user"
secret = "password_ldap_user"
conn = Connection(server, auth_dn, secret, auto_bind=True)

endpoint = 'https://confluence.ru:8090/rest/api/content'
pageid = 'id_page_one'
pageid2 = 'id_page_two'
headers = {'Content-Type': 'application/json'}
auth = ('login_user', 'password_user')

url = '{endpoint}/{pageid}?expand=ancestors'.format(endpoint=endpoint, pageid=pageid)

r = requests.get(url, headers=headers, auth=auth)
print(r)
web_confing = json.load(open('conf_jun.json'))


policies = data_source.get_policies(web_confing)
table_policies = data_source.convert_to_table(policies)
table_policies_with_keys = data_source.add_keys_to_table(table_policies)

html_policies = data_source.convert_to_html(policies)
html_table = data_source.convert_to_html(table_policies_with_keys)

write_conflu.write_data(auth, headers, endpoint, pageid, html_policies)
write_conflu.write_data(auth, headers, endpoint, pageid2, html_table)
