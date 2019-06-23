from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from dbs.models import Credential

import json
import jwt

import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

import os.path

#Landing page
def index(request):

	return render(request, 'landing_page/index.html')

#Product page with what's in the cart
def product_page(request):

	context = {}

	return render(request, 'i_love_lamp/product_page.html', context)

#Payment method is selected here
def payment_method(request):

	context = {}

	return render(request, 'i_love_lamp/payment_method.html', context)

#The bank to use for PayNow is chosen
def paynow_maesh(request):

	context = {}
	context['maesh'] = True

	return render(request, 'i_love_lamp/paynow_maesh.html', context)

#Payment is executed
def payment_maesh(request):

	context = {}
	context['maesh'] = True

	path = request.path_info

	if "dbs" in path:
		bank = 'dbs'
		context['dbs'] = True
	if "ocbc" in path:
		bank = 'ocbc'
		context['ocbc'] = True

	#Once the authorization code is presented, create a credential with the access token
	auth_code = request.GET.get('code', '')
	if auth_code:
		data = get_access_token(auth_code,settings.SITE+'payment_maesh_'+bank)
		decoded_access_token = jwt.decode(data['access_token'], settings.CLIENTSECRET, algorithms=['HS256'], verify=False) #Verification fails??

		cin_party_id = decoded_access_token['cin']
		party_id = decoded_access_token['sub']

		credential, created = Credential.objects.get_or_create(
			party_id=party_id,
			defaults={
				'access_token':data['access_token'],
				'expire_in':data['expire_in'],
				'token_type':data['token_type'],
				'refresh_token':data['refresh_token'],
				'cin_party_id':cin_party_id,
			}
		)
		if created == False:
			credential.access_token = data['access_token']
			credential.expire_in = data['expire_in']
			credential.refresh_token = data['refresh_token']
			credential.save()

	return render(request, 'i_love_lamp/payment_maesh.html', context)

# Connect to DBS account
def dbs_connect_account(request):

	# context = {}

	# credentials = Credential.objects.all()

	# # If there are credentials already, show index page
	# if credentials.exists():
	# 	context['credentials'] = True
	# 	r1 = render(request, 'dbs/index.html', context)
	# # If not, get authorization
	# else:
	# 	r1 = HttpResponseRedirect(authorize())
	
	r1 = HttpResponseRedirect(dbs_authorize())

	return r1

# Connect to OCBC account
def ocbc_connect_account(request):
	return HttpResponseRedirect(ocbc_authorize())

#Redirect to DBS page for authorization code
def dbs_authorize():

	params = (
		('response_type', 'code'),
		('client_id', settings.CLIENTID),
		('scope', 'Read'),
		('redirect_uri', settings.SITE+'payment_maesh_dbs'),
		('state', '0399'),
	)
	response = requests.get(settings.API+'/oauth/authorize', params=params)

	return response.url

# Get OAuth access token
def get_access_token(auth_code,redirect_uri):
	
	data = {
	  'grant_type': 'token',
	  'redirect_uri': redirect_uri,
	  'code': auth_code,
	}

	response = requests.post(settings.API+'/oauth/tokens', auth=HTTPBasicAuth(settings.CLIENTID, settings.CLIENTSECRET), data=data)
	my_json = (response.content.decode('utf8').replace("'", '"'))
	
	return json.loads(my_json)

def ocbc_authorize():

	params = (
		('client_id', '1sQ5xa9nwB9i2E4l3BVAfyLMIe8a'),
		('redirect_uri', settings.SITE+'payment_maesh_ocbc'),
		('scope', 'transactional')
	)
	response = requests.get(settings.API_OCBC+'ocbcauthentication/api/oauth2/authorize', params=params)

	return response.url

#Can use this index to check a couple of things in the DBS Sandbox
def index(request):

	context = {}

	#If an authorization code is presented, create a credential with the access token
	auth_code = request.GET.get('code', '')
	if auth_code:
		data = get_access_token(auth_code,settings.SITE)

		decoded_access_token = jwt.decode(data['access_token'], settings.CLIENTSECRET, algorithms=['HS256'], verify=False) #Verification fails??
		cin_party_id = decoded_access_token['cin']

		credential, created = Credential.objects.get_or_create(
			party_id=settings.PARTY_ID,
			defaults={
				'access_token':data['access_token'],
				'expire_in':data['expire_in'],
				'token_type':data['token_type'],
				'refresh_token':data['refresh_token'],
				'cin_party_id':cin_party_id,
			}
		)
		if created == False:
			credential.access_token = data['access_token']
			credential.expire_in = data['expire_in']
			credential.refresh_token = data['refresh_token']
			credential.save()

	credentials = Credential.objects.all()

	#If there are credentials, show other buttons
	if credentials.exists():
		context['credentials'] = True
	#If there are no credentials, first connect with DBS
	else:
		context['credentials'] = False
		
	# deposit_accounts = get_deposits_accounts(credential)

	# accountIDList = list()
	# for (k, v) in deposit_accounts.items():
	# 	if (k == 'savingsAccounts' or k == 'currentAccounts'):
	# 		for account in v:
	# 			accountID = account.get('id')
	# 			accountIDList.append(accountID)
	# 			account_details = get_account_details(credential.access_token,accountID)
	# 			# otherAccountID = account_details.get('accounts').get('accountDetl').get('currentAccount').get('id')
	# 			# transaction_history = get_transaction_history(access_token,accountID)
				
	# context['deposit_accounts'] = deposit_accounts

	# make_transfer(access_token,accountIDList[0])

	return render(request, 'dbs/index.html', context)

# If access token has expired, refresh token
def refresh_access_token(credential):

	headers = {
		'content-type': "application/x-www-form-urlencoded",
		'clientId': settings.CLIENTID,
		'accessToken': credential.access_token,
		'cache-control': "no-cache"
	}

	payload = 'refresh_token='+credential.refresh_token+'&grant_type=refresh_token'

	response = requests.post(settings.API+'/access/refresh', auth=HTTPBasicAuth(settings.CLIENTID, settings.CLIENTSECRET), headers=headers, data=payload)

	#If access token could not be refreshed (because expired or invalidated), get new authorization
	if response.status_code == 403:
		r1 = HttpResponseRedirect(authorize())
	#If refresh is successful
	else:
		r1 = response

	return r1

# Retrieve deposit accounts
def get_deposits_accounts(credential):

	headers =   {
		'Content-Type':'application/json',
		'clientId': settings.CLIENTID,
		'accessToken': credential.access_token,
	}

	response = requests.get(settings.API+'/parties/'+credential.cin_party_id+'/deposits', headers=headers)

	#If response indicates that the access token has expired
	if response.status_code == 403:
		refresh_token = refresh_access_token(credential)
		#If access token has not been refreshed, get new authorization
		if refresh_token.status_code != 200:
			r1 = refresh_token
	#If everything is normal
	else:
		r1 = response

	return r1

# Show account balance data
def account_balance(request):

	context = {}

	credentials = Credential.objects.all()

	response = get_deposits_accounts(credentials.first())
	
	if response.status_code == 200:
		my_json = (response.content.decode('utf8').replace("'", '"'))
		context['deposit_accounts'] = json.loads(my_json)
		r1 = render(request, 'dbs/account_balance.html', context)
	else:
		r1 = response

	return r1

def payNow_transfer_lamp(request):
	return transfer(request,True,True)

def payNow_transfer(request):
	return transfer(request,True,False)

#Show transfer page
def transfer(request,payNow=False,lamp=True):

	context = {}

	credentials = Credential.objects.all()
	credential = credentials.first()

	auth_code = request.GET.get('code', '')	

	if payNow == True:
		response = make_paynow_transfer(credential)
		my_json = (response.content.decode('utf8').replace("'", '"'))
		data = json.loads(my_json)

		context['success'] = data['status']
		if lamp == True:
			r1 = render(request, 'i_love_lamp/confirmation_page.html',context)
		else:
			r1 = render(request, 'dbs/transfer.html',context)
	else:
		#If no auth_code is available, initiate transfer, but catch error
		if not auth_code:
			response = make_transfer(credential)	
			#If response is an error, then 2FA needs to be granted
			if response.status_code == 403:
				my_json = (response.content.decode('utf8').replace("'", '"'))
				data = json.loads(my_json)
				url = data.get('Error').get('url')+'&client_id='+settings.CLIENTID+'&state=3309&redirect_uri='+settings.SITE+'transfer'
				r1 = HttpResponseRedirect(url)
		#If there is an auth_code available, make a transfer
		if auth_code:
			access_token_2FA = get_access_token(auth_code,settings.SITE+'transfer')
			credential.access_token = access_token_2FA['access_token']

			response = make_transfer(credential)
			my_json = (response.content.decode('utf8').replace("'", '"'))
			data = json.loads(my_json)

			context['success'] = data['status']
			r1 = render(request, 'dbs/transfer.html',context)

	return r1

def make_transfer(credential):

	headers = {
		'Content-Type':'application/json',
		'clientId': settings.CLIENTID,
		'accessToken': credential.access_token,
	}

	debitAccountId = "16614260647620470151013"

	payload = {
 		"fundTransferDetl":
 			{"debitAccountId": debitAccountId,
 			"creditAccountNumber":"02880112750003",
 			"bankCode":"DBSSSGS0XXX",
 			"payeeName":"ABC",
 			"paymentChannel":"03",
 			"alternatePayeeReference":{
 				"alternateReferenceType":"MOBILE",
 				"alternateReferenceDesc":"MOBILE",
 				"alternateReference":"9790888878"
 				},
 			"amount":"1",
 			"sourceCurrency":"SGD",
 			"destinationCurrency":"SGD",
 			"transferCurrency":"SGD",
 			"comments":"thanks",
 			"purpose":"FCCC",
 			"transferType":"INSTANT",
 			"partyId":credential.cin_party_id,
 			"referenceId":"93292721C392459086146",
			}
 	}

	response = requests.post(settings.API+'/transfers/adhocTransfer', headers=headers, json=payload)
	print(response)

	return response

# Retrieve transaction history
def transaction_history(request):
	
	context = {}

	credentials = Credential.objects.all()
	credential = credentials.first()
	accountId = '16614260647620470151013'

	headers = {
		'Content-Type':'application/json',
		'clientId': settings.CLIENTID,
		'accessToken': credential.access_token,
	}
	
	parameters = {
		'startDate':'2019-05-21',
		'endDate': '2019-06-04',
	}

	response = requests.get(settings.API+'/accounts/'+accountId+'/transactions', headers=headers, params=parameters)
	my_json = (response.content.decode('utf8').replace("'", '"'))
	my_json = my_json[:-15]+'}}}' #This is needed because the JSON from DBS is ungrammatical
	data = json.loads(my_json)

	context['data'] = data

	return render(request, 'dbs/transaction_history.html', context)

def make_paynow_transfer(credential):

	headers = {
		'Content-Type':'application/json',
		'clientId': settings.CLIENTID,
		'accessToken': credential.access_token,
	}

	debitAccountId = "16614260647620470151013"

	payload = {
 		"fundTransferDetl": {
    		"partyId": credential.cin_party_id,
		    "debitAccountId": debitAccountId,
		    "payeeReference": {
		      "referenceType": "NRIC",
		      "referenceDesc": "NRIC",
		      "reference": "S1069604F"
		    },
		    "amount": "3",
		    "transferCurrency": "SGD",
		    "comments": "for roti",
		    "purpose": "Transfer",
		    "referenceId": "4P3EDAB1C853A004117A32"
		}
	}

	response = requests.post(settings.API+'/transfers/payNow', headers=headers, data=payload)

	return response

# def get_account_details(access_token,accountId):

# 	headers = {
# 		'Content-Type':'application/json',
# 		'clientId': settings.CLIENTID,
# 		'accessToken': access_token,
# 	}

# 	response = requests.get(settings.API+'/accounts/'+accountId, headers=headers)

# 	my_json = (response.content.decode('utf8').replace("'", '"'))

# 	return json.loads(my_json)
