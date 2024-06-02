from django import forms
from .models import CustomerProfile

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = [
            'name',
            'arabicName',
            'visaId',
            'borderNumber',
            'nationality',
            'arabicNationality',
            'gender',
            'arabicGender',
            
            'serviceProvider',
            'serviceCenter',
            'serviceCenterLocation',
            'serviceCenterContact',
            
            'housingMakkahLocation',
            'housingMinaLocation',
            'housingMadinahLocation',
            'housingArafatLocation',
            'picture',
            
            'visaStatus',

            'dob',
        ]
        required_fields = [
            'name',
            'arabicName',
            'visaId',
            'borderNumber',
            'nationality',
            'arabicNationality',
            'gender',
            'arabicGender',

            'serviceProvider',
            'serviceCenter',
            'serviceCenterLocation',
            'serviceCenterContact',
            
            'housingMakkahLocation',
            'housingMinaLocation',
            'housingMadinahLocation',
            'housingArafatLocation',
            'picture',
            
            'visaStatus',

            'dob',
        ]
        labels = {
            'name': 'الاسم (الإنجليزية)',
            'arabicName': 'الاسم (عربي)',
            'visaId': 'رقم التأشيرة',
            'borderNumber': 'رقم الحدود ( الرقم الموحد )',
            'nationality': 'الجنسية',
            'arabicNationality': 'الجنسية بالعربية',
            'gender': 'الجنس',
            'arabicGender': 'الجنس بالعربية',
            
            'serviceProvider': 'مقدم الخدمة',
            'serviceCenter': 'مركز تقديم الخدمة الميداني',
            'serviceCenterLocation': 'موقع مركز تقديم الخدمة الميداني',
            'serviceCenterContact': 'بيانات الاتصال بمركز تقديم الخدمة الميداني',
            
            'housingMakkahLocation': 'موقع السكن في مكة',
            'housingMinaLocation': 'موقع السكن في منى',
            'housingMadinahLocation': 'موقع السكن في المدينة',
            'housingArafatLocation': 'موقع السكن في عرفات',
            'picture': 'الصورة',
            
            'visaStatus': 'حالة التأشيرة',

            'dob': 'تاريخ الميلاد',
            

            # 'nationalID': 'الرقم الوطني',
            # 'gwazzID': 'رقم الجواز',
            # 'permitType': 'نوع الرخصة',
            # 'permitCode': 'رقم الرخصة',
            # 'allowedLoccation': 'المواقع المسموحة',
            # 'career': 'المهنة',
            # 'birthDate': 'تاريخ الميلاد',
            # 'fromDate': 'من تاريخ',
            # 'toDate': 'إلى تاريخ'
        }
