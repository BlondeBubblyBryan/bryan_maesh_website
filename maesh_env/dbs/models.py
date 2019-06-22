from django.db import models

class Credential(models.Model):

    access_token = models.CharField(max_length=500)
    party_id = models.CharField(max_length=10,unique=True)
    expire_in = models.CharField(max_length=13)
    token_type = models.CharField(max_length=6)
    refresh_token = models.CharField(max_length=50)
    cin_party_id = models.CharField(max_length=13)
