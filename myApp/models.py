from django.db import models
import datetime
from django.conf import settings
import os


GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female')
]

ARABIC_GENDER_CHOICES = [
    ('ذكر', 'ذكر'),
    ('انثى', 'انثى')
]

VISA_STATUS_CHOICES = [
    ('ACTIVE', 'ACTIVE')
]

class CustomerProfile(models.Model):
    name                = models.CharField(max_length=350)
    arabicName          = models.CharField(max_length=350)
    visaId              = models.CharField(max_length=20 )
    borderNumber        = models.CharField(max_length=20 )
    nationality         = models.CharField(max_length=20 , default="Egypt")
    arabicNationality   = models.CharField(max_length=20 , default="مصر")
    gender              = models.CharField(max_length=20 , choices=GENDER_CHOICES)
    arabicGender        = models.CharField(max_length=20 , choices=ARABIC_GENDER_CHOICES)

    serviceProvider     = models.CharField(max_length=350 , default="شركة رحلات ومنافع للسياحة")
    serviceCenter       = models.CharField(max_length=350 , default="مركز الخدمة 239")
    serviceCenterLocation= models.CharField(max_length=350 , default="ام الجود")
    serviceCenterContact= models.CharField(max_length=350 , default="966541670802+")

    housingMakkahLocation= models.CharField(max_length=350 , default='اجياد البيت')
    housingMinaLocation= models.CharField(max_length=350 , default='-')
    housingMadinahLocation= models.CharField(max_length=350 , default='-')
    housingArafatLocation= models.CharField(max_length=350 , default='-')
    picture             = models.ImageField(upload_to="uploaded_images", blank=True, null=True)

    visaStatus          = models.CharField(max_length=20, blank=True, null=True, default='ACTIVE', choices=VISA_STATUS_CHOICES)

    dob                 = models.DateField(blank=True, null=True, default=datetime.date.today)

    def __str__(self):
        return self.name + " - Customer"


    def delete(self, *args, **kwargs):
        if self.picture:
            if os.path.isfile(self.picture.path):
                os.remove(self.picture.path)

        card_file_path = os.path.join(settings.BASE_DIR, 'output_cards', f'modified_card_{self.name}_{self.id}.png')

        if os.path.isfile(card_file_path):
            os.remove(card_file_path)

        super().delete(*args, **kwargs)