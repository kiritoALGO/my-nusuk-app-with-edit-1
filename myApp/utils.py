import io
import barcode
from barcode.writer import ImageWriter
def generate_barcode_image(text, width=200, height=100):
    code128 = barcode.get_barcode_class('code128')
    barcode_instance = code128(text, writer=ImageWriter())
    image_stream = io.BytesIO()
    barcode_instance.write(image_stream)
    image_stream.seek(0)
    barcode_image = Image.open(image_stream)
    
    # Resize the barcode image
    barcode_image = barcode_image.resize((width, height))
    
    # Crop the barcode image to remove the bottom text
    width, height = barcode_image.size
    barcode_image = barcode_image.crop((0, 0, width, height - 75))  # Adjust the cropping area as needed
    
    return barcode_image

import qrcode

"""import pyqrcode
from PIL import Image

def generate_qr_code(data, size=200):
    # Generate the QR code
    qr = pyqrcode.create(data)

    # Create a white image with an alpha channel (transparent background)
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))

    # Get the QR code as a PIL image
    qr_img = qr.get_image(fill_color="black", back_color=(255, 255, 255, 0))

    # Resize the QR code image to fit the desired size
    qr_img = qr_img.resize((size, size))

    # Paste the QR code onto the transparent image
    img.paste(qr_img, (0, 0))

    return img"""



def generate_qr_code(data, size=200):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    

    img = qr.make_image(fill_color=(0,0, 0), back_color="white")
    img = img.convert("RGBA")
    img = img.resize((size, size))
    return img





from PIL import Image