from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils.safestring import mark_safe



class Slip(models.Model):
    Account_Number = models.CharField(primary_key=True,max_length=10, validators=[RegexValidator(r'^\d{1,10}$'),MinLengthValidator(10)])
    Image_Path = models.ImageField(upload_to='image/')
    Current_Date = models.DateTimeField(default=timezone.now)
    Account_Holder_Name = models.CharField(max_length=200, blank=True)
    Bank_Name = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.Account_Number

    def image_tag(self):
        return mark_safe('<a href="/Media/{}"><img src="/Media/{}" width="100" height="50" /></a>'.format((self.Image_Path ),(self.Image_Path)))


