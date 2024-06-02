from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpResponseForbidden
from .forms import CustomerProfileForm
from .models import CustomerProfile
from .utils import generate_qr_code, generate_barcode_image
from django.db.models import Q

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from bidi.algorithm import get_display
import arabic_reshaper
from django.conf import settings



def test(request):
    pass

def homepage(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")
    search_query = request.GET.get('search', '')
    if search_query:
        customers = CustomerProfile.objects.filter(
            Q(name__icontains=search_query) | Q(arabicName__icontains=search_query)
        )
    else:
        customers = CustomerProfile.objects.all()
    return render(request, 'homepage.html', {'customers': customers})

def add_customer(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form directly
            return redirect('success')  # Use redirect instead of render
    else:
        form = CustomerProfileForm()
    
    return render(request, 'add_form.html', {'form': form})

def edit_customer(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    customer = get_object_or_404(CustomerProfile, pk=pk)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('homepage') 
    else:
        form = CustomerProfileForm(instance=customer)
    return render(request, 'edit_form.html', {'form': form})

def get_customer_detail(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    # Retrieve the CustomerProfile object using the provided ID
    customer = get_object_or_404(CustomerProfile, pk=pk)
    
    # Render the template with the customer object in the context
    return render(request, 'customer_detail.html', {'customer': customer})

def delete_customer(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    customer = get_object_or_404(CustomerProfile, pk=pk)
    customer.delete()
    return redirect('homepage')

def create_tasreh(request, pk):
    customer = CustomerProfile.objects.get(pk=pk)
    context = {
        'user': customer
    }
    return render(request, 'tasreeh.html', context)

def create_card(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    customer = get_object_or_404(CustomerProfile, pk=pk)

    # Define the absolute paths to the images
    image_path = os.path.join(settings.BASE_DIR, 'static','images', 'new-front.png')
    modified_image_path = os.path.join(settings.BASE_DIR, 'output_cards', f'modified_card_{customer.name}_{pk}.png')

    # Define the text data
    if customer.picture:
        print(1111111111)
        profile_photo_path = settings.BASE_DIR +  f'/{customer.picture.url}'.replace('/','\\')
    else:
        print(22222222222)
        profile_photo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'default_image.png')
        print(profile_photo_path)
        
    english_name = customer.name
    arabic_name = customer.arabicName
    english_nationality = customer.nationality
    arabic_nationality = customer.arabicNationality
    nationality = str(english_nationality) + '|' + str(arabic_nationality)
    dob = customer.dob.strftime('%Y-%m-%d')
    Haj_id = customer.visaId
    service_provider = customer.serviceProvider
    service_contact = customer.serviceCenterContact
    qr_text = request.scheme + '://' + request.get_host() + f'/customer/create_tasreh/{customer.id}/'
    barcode_text = customer.visaId
    

    # Check if the files exist
    if not os.path.exists(image_path) or not os.path.exists(profile_photo_path):
        return HttpResponse("Image or profile photo not found.", status=404)
    
    # Load the images using OpenCV
    image = cv2.imread(image_path)
    profile_photo = cv2.imread(profile_photo_path)

    # Check if the images were loaded properly
    if image is None or profile_photo is None:
        return HttpResponse("Error loading image or profile photo.", status=500)

    # Resize the profile photo to fit in the grey rectangle
    profile_photo_resized = cv2.resize(profile_photo, (380, 420))  # Adjust the size as needed

    # Define the position where the profile photo will be placed
    x_offset = 291  # Adjust these values based on your layout
    y_offset = 190

    # Place the profile photo in the specified position
    image[y_offset:y_offset+profile_photo_resized.shape[0], x_offset:x_offset+profile_photo_resized.shape[1]] = profile_photo_resized

    # Convert the image to RGB (OpenCV uses BGR by default)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert the image to a PIL image
    pil_image = Image.fromarray(image)

    # Prepare the draw object
    draw = ImageDraw.Draw(pil_image)

    

    # Define the font and size
    font_path = "arial.ttf"  # Path to a TTF font file
    font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'DejaVuSans-Bold.ttf')
    font = ImageFont.truetype(font_path, 26)

    # Calculate the width of the image
    image_height, image_width, _ = image.shape
    # Calculate the width of each text string
    english_name_width = draw.textlength(english_name, font=font)
    arabic_name_width = draw.textlength(arabic_name, font=font)
    nationality_width = draw.textlength(nationality, font=font)
    dob_width = draw.textlength(dob, font=font)
    Haj_id_width = draw.textlength(Haj_id, font=font)
    service_provider_width = draw.textlength(service_provider, font=font)
    service_contact_width = draw.textlength(service_contact, font=font)
    

    # Calculate the starting x-coordinate to center-align each text
    english_name_x = (image_width - english_name_width) // 2
    arabic_name_x = (image_width - arabic_name_width) // 2
    nationality_x = (image_width - nationality_width) // 2
    dob_x = ((image_width // 2 - dob_width) // 2 ) + 30 #- (image_width // 2)
    Haj_id_x = (image_width // 2 ) + (((image_width // 2) - Haj_id_width) // 2) - 10
    service_provider_x = image_width - service_provider_width - 130
    service_contact_x = image_width - service_contact_width - 232


    # Add the English text
    draw.text((dob_x, 870), dob, font=font, fill="black")  # Adjusted position
    draw.text((Haj_id_x, 870), Haj_id, font=font, fill="black")  # Adjusted position
    draw.text((service_contact_x, 1045), service_contact, font=font, fill="black")  # Adjusted position
    draw.text((english_name_x, 727), english_name, font=font, fill="black")  # Adjusted position

    # service_provider
    reshaped_text = arabic_reshaper.reshape(service_provider)
    bidi_text = get_display(reshaped_text)
    draw.text((service_provider_x, 990), bidi_text, font=font, fill="black")
    # arabic_name
    reshaped_text = arabic_reshaper.reshape(arabic_name)
    bidi_text = get_display(reshaped_text)
    draw.text((arabic_name_x, 690), bidi_text, font=font, fill="black")
    # nationality
    reshaped_text = arabic_reshaper.reshape(nationality)
    bidi_text = get_display(reshaped_text)
    draw.text((nationality_x, 760), bidi_text, font=font, fill="black")

    

    # Generate the barcode image
    barcode_image = generate_barcode_image(barcode_text, width=380, height=131)  # Adjust the size as needed

    # Paste the barcode image onto the main image at a desired position
    barcode_x_offset = 291
    barcode_y_offset = 610
    pil_image.paste(barcode_image, (barcode_x_offset, barcode_y_offset))

    # Generate the QR code image
    qr_image = generate_qr_code(qr_text, size=140)  # Adjust the size as needed

    # Define the position where the QR code will be placed
    qr_x_offset = (image_width - 140) // 2 + 30   # Adjust these values based on your layout
    qr_y_offset = 1120

    # Paste the QR code image onto the main image
    pil_image.paste(qr_image, (qr_x_offset, qr_y_offset))


    # Convert the PIL image back to an OpenCV image
    image = np.array(pil_image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Save the modified image
    cv2.imwrite(modified_image_path, image)

    # Provide the image for download
    with open(modified_image_path, "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")


def success_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, 'success.html')



























    """if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            customer_profile = CustomerProfile(
                name=form.cleaned_data['name'],
                arabicName=form.cleaned_data.get('arabicName', ''),
                visaId=form.cleaned_data.get('visaId', ''),
                borderNumber=form.cleaned_data.get('borderNumber', ''),
                nationality=form.cleaned_data.get('nationality', ''),
                arabicNationality=form.cleaned_data.get('arabicNationality', ''),
                gender=form.cleaned_data.get('gender', ''),
                arabicGender=form.cleaned_data.get('arabicGender', ''),
                serviceProvider=form.cleaned_data.get('serviceProvider', ''),
                serviceCenter=form.cleaned_data.get('serviceCenter', ''),
                serviceCenterLocation=form.cleaned_data.get('serviceCenterLocation', ''),
                serviceCenterContact=form.cleaned_data.get('serviceCenterContact', ''),
                housingMakkahLocation=form.cleaned_data.get('housingMakkahLocation', ''),
                housingMinaLocation=form.cleaned_data.get('housingMinaLocation', ''),
                housingMadinahLocation=form.cleaned_data.get('housingMadinahLocation', ''),
                housingArafatLocation=form.cleaned_data.get('housingArafatLocation', ''),
                visaStatus=form.cleaned_data.get('visaStatus', ''),
                nationalID=form.cleaned_data['nationalID'],
                gwazzID=form.cleaned_data['gwazzID'],
                picture=form.cleaned_data['picture'],
                permitType=form.cleaned_data.get('permitType', 'الأفراد'),
                permitCode=form.cleaned_data.get('permitCode', 'الأفراد'),
                allowedLoccation=form.cleaned_data.get('allowedLoccation', 'منى-عرفات-مزدلفه'),
                career=form.cleaned_data['career'],
                birthDate=form.cleaned_data.get('birthDate', None),
                fromDate=form.cleaned_data.get('fromDate', None),
                toDate=form.cleaned_data.get('toDate', None)
            )

            customer_profile.save()
            return render(request, 'success.html')
    else:
        form = CustomerProfileForm()
    return render(request, 'combined_form.html', {'form': form})"""
