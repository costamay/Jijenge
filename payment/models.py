from django.db import models



class LipaOnline(models.Model):
    amount = models.FloatField(blank=True, null=True)
    mobileNumber = models.CharField(max_length=13, blank=True, null=True)
    Reference =  models.CharField(max_length=20, blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.PhoneNumber} has sent {self.Amount} >> {self.Reference}"



class PayBill(models.Model):
    amount = models.FloatField(blank=True, null=True)
    mobileNumber = models.CharField(max_length=13, blank=True, null=True)
    Reference =  models.CharField(max_length=20, blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.PhoneNumber} has sent {self.Amount} >> {self.Reference}"


class EasyPay(models.Model):
    amount = models.FloatField(blank=True, null=True)
    mobileNumber = models.CharField(max_length=13, blank=True, null=True)
    Reference =  models.CharField(max_length=20, blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.PhoneNumber} has sent {self.Amount} >> {self.Reference}"
    
# class MerchantPayment(models.Model):
#     amount = models.FloatField(blank=True, null=True)

class CardPayment(models.Model):
    amount = models.FloatField(blank=True, null=True)
    mobileNumber = models.CharField(max_length=13, blank=True, null=True)
    cardNumber =  models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.PhoneNumber} has sent {self.Amount} >> {self.Reference}"
