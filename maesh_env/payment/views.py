from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from payment.models import Credential, Transaction

import json
import jwt
import urllib

import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

import os.path

### ***
#	I Love Lamp Prototype
### ***

#Product page with what's in the cart
def product_page(request):

	return render(request, 'i_love_lamp/product_page.html')

#Payment method is selected here
def payment_method(request):

	return render(request, 'i_love_lamp/payment_method.html')

#Confirmation page
def confirmed(request):

	context = {}
	context['status'] = "Confirmed"

	return render(request, 'i_love_lamp/confirmation_page.html',context)

### ***
#	Maesh Payment
### ***

#The bank to use for PayNow is chosen
def paynow_maesh(request):

	context = {}

	#From the query parameters the transaction details are fetched
	#This can be tampered with, so we'll have to look at a better solution
	#Maybe an API is needed, especially if we're transfering receipt data
	amount = request.GET.get('amount')
	currency = request.GET.get('currency')
	UEN = request.GET.get('UEN')
	redirect_uri  = request.GET.get('redirect_uri')

	#If there are query parameters, then Prestashop
	if amount:
		transaction = Transaction.objects.create(amount=amount,currency=currency,UEN=UEN,redirect_uri=redirect_uri)
	#If not, it's the prototype app
	else:
		context['prototype'] = True
		transaction = Transaction.objects.create(amount='217.00',currency='SGD',UEN='123456789',redirect_uri='http://localhost:8000/confirmed')

	return render(request, 'maesh/paynow_maesh.html', context)

# Connect to bank
def connect_bank(request,bank=None):

	return HttpResponseRedirect(authorize(bank))

#Redirect to bank page for authorization code
def authorize(bank):

	response = ''

	if bank == 'dbs':
		params = (
			('response_type', 'code'),
			('client_id', settings.CLIENTID_DBS),
			('scope', 'Read'),
			('redirect_uri', settings.SITE+'payment_maesh_dbs'),
			('state', '0399'), #I think this number is random
		)
		response = requests.get(settings.API_DBS+'/oauth/authorize', params=params)

	if bank == 'ocbc':
		params = {
			'client_id': settings.CLIENTID_OCBC,
			'redirect_uri': settings.SITE+'payment_maesh_ocbc',
			'scope': 'transactional'
		}
		response = requests.get(settings.API_OCBC+'/ocbcauthentication/api/oauth2/authorize', params=params)

	if bank == 'citi':
		params = {
			'response_type':'code',
			'client_id': settings.CLIENTID_CITI,
			'scope': 'external_domestic_transfers',
			'countryCode':'SG',
			'businessCode':'GCB',
			'locale':'en_SG',
			'state':'12093',
			'redirect_uri': settings.SITE+'payment_maesh_citi'
			}

		response = requests.get(settings.API_CITI+'/authCode/oauth2/authorize', params=params)

	return response.url

class Bank:
	def __init__(self, name, API, client_id, client_secret, grant_type):
		self.name = name
		self.API = API
		self.client_id = client_id
		self.client_secret = client_secret
		self.grant_type = grant_type

#Payment is prepared
def payment_maesh(request):

	context = {}

	#Retrieving the transaction details
	transaction = Transaction.objects.latest('created')
	context['transaction'] = transaction

	#If prototype app is used
	if transaction.UEN == "123456789":
		context['prototype'] = True

	#Check which bank is redirected from
	path = request.path_info
	if "dbs" in path:
		transaction.bank = 'dbs'
		transaction.save()
		context['dbs'] = True
		bank = Bank(transaction.bank,settings.API_DBS+'/oauth/tokens',settings.CLIENTID_DBS,settings.CLIENTSECRET_DBS,'token')
	if "ocbc" in path:
		transaction.bank = 'ocbc'
		transaction.save()
		context['ocbc'] = True
		bank = Bank(transaction.bank,settings.API_OCBC,settings.CLIENTID_OCBC,settings.CLIENTSECRET_OCBC,'token')
	if "citi" in path:
		transaction.bank = 'citi'
		transaction.save()
		context['citi'] = True
		bank = Bank(transaction.bank,settings.API_CITI+'/authCode/oauth2/token/sg/gcb',settings.CLIENTID_CITI,settings.CLIENTSECRET_CITI,'authorization_code')

	#Create or update credential
	auth_code = request.GET.get('code', '')
	#This part for now only works for DBS
	if auth_code:
		credential = check_credential(auth_code,bank)
		#Retrieving deposit accounts that can be charged from
		deposit_accounts = get_deposit_accounts(credential,bank)
		my_json = (deposit_accounts.content.decode('utf8').replace("'", '"'))
		context['deposit_accounts'] = json.loads(my_json)		
	#This is for OCBC
	else:
		credential = None

	return render(request, 'maesh/payment_maesh.html', context)

#Once the authorization code is presented, create/update credential with the access token
def check_credential(auth_code,bank):

	data = get_access_token(auth_code,settings.SITE+'payment_maesh_'+bank.name,bank)
	if bank.name == 'dbs':
		decoded_access_token = jwt.decode(data['access_token'], settings.CLIENTSECRET_DBS, algorithms=['HS256'], verify=False) #Verification fails??
		cin_party_id = decoded_access_token['cin']
		party_id = decoded_access_token['sub']
		scope = ""

	if bank.name == 'citi':
		cin_party_id = "Unknown"
		party_id = "Unknown"
		scope = data['scope']

	try:
		expires_in = data['expire_in'] 
	except:
		expires_in = data['expires_in']
		print(data['scope'])

	credential, created = Credential.objects.get_or_create(
		party_id=party_id,
		defaults={
			'access_token':data['access_token'],
			'expire_in':expires_in,
			'token_type':data['token_type'],
			'refresh_token':data['refresh_token'],
			'cin_party_id':cin_party_id,
			'scope':scope
		}
	)
	#If credential is not new, then update
	if created == False:
		credential.access_token = data['access_token']
		credential.expire_in = expires_in
		credential.refresh_token = data['refresh_token']
		credential.save()

	return credential

# Get OAuth access token
def get_access_token(auth_code,redirect_uri,bank):
	
	data = {
	  'grant_type': bank.grant_type,
	  'redirect_uri': redirect_uri,
	  'code': auth_code,
	}

	response = requests.post(bank.API, auth=HTTPBasicAuth(bank.client_id, bank.client_secret), data=data)
	my_json = (response.content.decode('utf8').replace("'", '"'))
	
	return json.loads(my_json)

# Retrieve deposit accounts
def get_deposit_accounts(credential,bank):

	headers =   {
		'Content-Type':'application/json',
		'clientId': bank.client_id,
		'accessToken': credential.access_token,
	}

	if bank.name == 'dbs':
		response = requests.get(settings.API_DBS+'/parties/'+credential.cin_party_id+'/deposits', headers=headers)
	if bank.name == 'citi':
		response = requests.get(settings.API_DBS+'/parties/'+credential.cin_party_id+'/deposits', headers=headers)

	# #If response indicates that the access token has expired
	# if response.status_code == 403:
	# 	refresh_token = refresh_access_token(credential)
	# 	#If access token has not been refreshed, get new authorization
	# 	if refresh_token.status_code != 200:
	# 		r1 = refresh_token
	# #If everything is normal
	# else:
	# 	r1 = response
	r1 = response

	return r1

# If access token has expired, refresh token
def refresh_access_token(credential):

	headers = {
		'content-type': "application/x-www-form-urlencoded",
		'clientId': settings.CLIENTID_DBS,
		'accessToken': credential.access_token,
		'cache-control': "no-cache"
	}

	payload = 'refresh_token='+credential.refresh_token+'&grant_type=refresh_token'

	response = requests.post(settings.API_DBS+'/access/refresh', auth=HTTPBasicAuth(settings.CLIENTID_DBS, settings.CLIENTSECRET_DBS), headers=headers, data=payload)

	#If access token could not be refreshed (because expired or invalidated), get new authorization
	if response.status_code == 403:
		r1 = HttpResponseRedirect(authorize())
	#If refresh is successful
	else:
		r1 = response

	return r1

#Initiate PayNow transfer
def payNow_transfer(request):

	context = {}

	#Get all information needed to perform transaction
	credentials = Credential.objects.all()
	credential = credentials.first()
	transaction = Transaction.objects.latest('created')
	account_number = request.POST.get('account')

	response = make_paynow_transfer(credential,transaction,account_number)
	my_json = (response.content.decode('utf8').replace("'", '"'))
	data = json.loads(my_json)

	if transaction.bank == 'dbs':
		successful = data['status'] == 'Successful'
	if transaction.bank == 'ocbc':
		successful = data['Success'] == True

	if successful:
		r1 = HttpResponseRedirect(transaction.redirect_uri)
	else:
		context['status'] = successful
		r1 = render(request, 'i_love_lamp/confirmation_page.html',context)

	return r1

#Make PayNow transfer
def make_paynow_transfer(credential,transaction,account_number):

	if transaction.bank == 'dbs':
		r1 = make_paynow_transfer_DBS(credential,transaction,account_number)
	if transaction.bank == 'ocbc':
		r1 = make_paynow_transfer_OCBC(credential,transaction,account_number)

	return r1

#Make PayNow transfer DBS
def make_paynow_transfer_DBS(credential,transaction,account_number):

	headers = {
		'Content-Type':'application/json',
		'clientId': settings.CLIENTID_DBS,
		'accessToken': credential.access_token,
	}

	payload = {
		"fundTransferDetl": {
			"partyId": credential.cin_party_id,
			"debitAccountId": account_number,
			"payeeReference": {
			  "referenceType": "UEN",
			  "referenceDesc": "UEN",
			  "reference": transaction.UEN
			},
			"amount": transaction.amount,
			"transferCurrency": transaction.currency,
			"comments": "for roti",
			"purpose": "Transfer",
			"referenceId": "4P3EDAB1C853A004117A32"
		}
	}

	response = requests.post(settings.API_DBS+'/transfers/payNow', headers=headers, data=payload)

	return response

#Make PayNow transfer OCBC
def make_paynow_transfer_OCBC(credential,transaction,account_number):

	headers = {
		"Content-Type": "application/json",
		"Accept": "application/json",
		"Authorization": "Bearer "+settings.ACCESS_TOKEN_OCBC
	}

	payload = {
		"TransactionDescription": "Pay taxes",
		"Amount": transaction.amount,
		"ProxyType": "UEN",
		"ProxyValue": transaction.UEN,
		"FromAccountNo": "1795-XXX900",
		"PurposeCode": "OTHR",
		"TransactionReferenceNo": "OrgXYZ1212xxx"
	}

	response = requests.post("https://api.ocbc.com:8243/transactional/corporate/paynowpayment/1.0", headers=headers, data=json.dumps(payload))

	return response

### ***
#	Check statuses in DBS Sandbox
### ***

#Can use this index page to check a couple of things in the DBS Sandbox. It's not part of the prototype or the Prestashop module
def index(request):

	context = {}

	#If an authorization code is presented, create a credential with the access token
	auth_code = request.GET.get('code', '')
	if auth_code:
		credential = check_credential(auth_code)

	credentials = Credential.objects.all()

	#If there are credentials, show other buttons
	if credentials.exists():
		context['credentials'] = True
	#If there are no credentials, first connect with DBS
	else:
		context['credentials'] = False
		
	return render(request, 'dbs/index.html', context)

# Show account balance data
def account_balance(request):

	context = {}

	credentials = Credential.objects.all()

	response = get_deposit_accounts(credentials.first())
	
	if response.status_code == 200:
		my_json = (response.content.decode('utf8').replace("'", '"'))
		context['deposit_accounts'] = json.loads(my_json)
		r1 = render(request, 'dbs/account_balance.html', context)
	else:
		r1 = response

	return r1

#Show transfer page
def transfer(request):

	context = {}

	credentials = Credential.objects.all()
	credential = credentials.first()
	transaction = Transaction.objects.latest('created')
	account_number = request.POST.get('account')

	auth_code = request.GET.get('code', '') 

	#If no auth_code is available, initiate transfer, but catch error
	if not auth_code:
		response = make_transfer(credential,transaction)    
		#If response is an error, then 2FA needs to be granted
		if response.status_code == 403:
			my_json = (response.content.decode('utf8').replace("'", '"'))
			data = json.loads(my_json)
			url = data.get('Error').get('url')+'&client_id='+settings.CLIENTID_DBS+'&state=3309&redirect_uri='+settings.SITE+'transfer'
			r1 = HttpResponseRedirect(url)
	#If there is an auth_code available, make a transfer
	else:
		access_token_2FA = get_access_token(auth_code,settings.SITE+'transfer')
		credential.access_token = access_token_2FA['access_token']

		response = make_transfer(credential,transaction)
		my_json = (response.content.decode('utf8').replace("'", '"'))
		data = json.loads(my_json)

		context['success'] = data['status']
		r1 = render(request, 'dbs/transfer.html',context)

	return r1

def make_transfer(credential,transaction):

	headers = {
		'Content-Type':'application/json',
		'clientId': settings.CLIENTID_DBS,
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
			"amount":transaction.amount,
			"sourceCurrency":transaction.currency,
			"destinationCurrency":transaction.currency,
			"transferCurrency":transaction.currency,
			"comments":"thanks",
			"purpose":"FCCC",
			"transferType":"INSTANT",
			"partyId":credential.cin_party_id,
			"referenceId":"93292721C392459086146",
			}
	}

	response = requests.post(settings.API_DBS+'/transfers/adhocTransfer', headers=headers, json=payload)

	return response

# Retrieve transaction history
def transaction_history(request):
	
	context = {}

	credentials = Credential.objects.all()
	credential = credentials.first()
	accountId = '16614260647620470151013'

	headers = {
		'Content-Type':'application/json',
		'clientId': settings.CLIENTID_DBS,
		'accessToken': credential.access_token,
	}
	
	parameters = {
		'startDate':'2019-05-21',
		'endDate': '2019-06-04',
	}

	response = requests.get(settings.API_DBS+'/accounts/'+accountId+'/transactions', headers=headers, params=parameters)
	my_json = (response.content.decode('utf8').replace("'", '"'))
	my_json = my_json[:-15]+'}}}' #This is needed because the JSON from DBS is ungrammatical
	data = json.loads(my_json)

	context['data'] = data

	return render(request, 'dbs/transaction_history.html', context)

# #This doesn't seem to be working in Sandbox. Get a webpage as response
# def payLah_transfer(request):

# 	credentials = Credential.objects.all()
# 	credential = credentials.first()
# 	transaction = Transaction.objects.latest('created')

# 	#Account number to be used is posted
# 	account_number = request.POST.get('account')

# 	response = make_paylah_transfer(credential,transaction,account_number)
# 	my_json = (response.content.decode('utf8').replace("'", '"'))
# 	data = json.loads(my_json)

# 	return HttpResponseRedirect(response)

# #This doesn't seem to be working in Sandbox. Get a webpage as response
# def make_paylah_transfer(credential,transaction,account_number):
	
# 	headers = {
# 		"msgId": "string",
# 		"orgId": "string",
# 		"timeStamp": "2019-07-04T12:15:35Z"
# 	}
	
# 	txnInfo = {
# 		"txnMsgId": "string",
# 		"txnSource": 0,
# 		"txnType": "s",
# 		"txnCcy": transaction.currency,
# 		"txnAmount": transaction.amount,
# 		"returnUrl": "string",
# 		"phoneNumber": 0,
# 		"payeeShippingAddress": "st",
# 		"address": {
# 		  "blockNo": "string",
# 		  "levelUnit": "string",
# 		  "address1": "string",
# 		  "address2": "string",
# 		  "postalCode": 0
# 		},
# 		"rmtInf": {
# 		  "invoiceDetails": "string",
# 		  "paymentDetails": {
# 			"referenceNumber2": "string",
# 			"referenceNumber3": "string",
# 			"referenceNumber4": "string",
# 			"referenceNumber5": "string"
# 		  },
# 		  "qrCode": "string"
# 		}
# 	}

# 	response = requests.post(settings.API_DBS+'/paylah/v1/purchase/webCheckout', headers=headers, data=txnInfo)

# 	return response
