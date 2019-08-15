from django.db import models
from django.utils import timezone

class Credential(models.Model):

    access_token = models.CharField(max_length=500)
    party_id = models.CharField(max_length=10,unique=True)
    expire_in = models.CharField(max_length=13)
    token_type = models.CharField(max_length=6)
    refresh_token = models.CharField(max_length=50)
    cin_party_id = models.CharField(max_length=13, blank=True)
    scope = models.CharField(max_length=50, blank=True)
    bank = models.CharField(max_length=4, blank=True)

class Transaction(models.Model):

	amount = models.FloatField()
	currency = models.CharField(max_length=3)
	UEN = models.CharField(max_length=10)
	company_name = models.CharField(max_length=50)
	created = models.DateTimeField(editable=False, default=timezone.now)
	modified = models.DateTimeField(default=timezone.now)
	redirect_uri = models.CharField(max_length=500,blank=True)
	credential = models.ForeignKey(Credential, on_delete=models.CASCADE, blank=True, null=True)
	reference_code = models.CharField(max_length=10)
	transaction_id = models.CharField(max_length=32)
	paid = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.created = timezone.now()
		self.modified = timezone.now()
		return super(Transaction, self).save(*args, **kwargs)