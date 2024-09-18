import os
import binascii
from django.db import models


class ApiKey(models.Model):
    key = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    n_allowed_requests = models.IntegerField(default=100, blank=True, null=True)
    n_requests = models.IntegerField(default=0)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.key} - {self.email}"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()


class APIRequest(models.Model):
    key = models.ForeignKey(ApiKey, on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=10000)
    nchars = models.IntegerField()
    nwords = models.IntegerField()
    output = models.IntegerField()

    def __str__(self):
        return f"{self.key} - {self.dt} - {self.nchars} - {self.nwords}"

    def save(self, *args, **kwargs):
        self.nchars = len(self.text)
        self.nwords = len(self.text.split())
        self.text = self.text[:10000]
        return super().save(*args, **kwargs)
