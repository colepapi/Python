# a) data - takes you to the place based on what the user has input (https://extratorrent.st)
# b) image qr code pretty straightforward
# c) on the image qr code do we need to utilize file opening & accessing in python? --> yes

import qrcode
import os

data = input('Enter the text or URL: ').strip()

while True:
    img_qr_filename = input('Enter the filename: ').strip()
    
    target_folder = r".\Python\qr_code_generator\qr_codes"
    full_path = os.path.join(target_folder, img_qr_filename)
    
    try:
        if os.path.exists(full_path):
            raise FileExistsError(f"Error: The file '{img_qr_filename}' already exists in your target folder!")
        break
    except FileExistsError as e:
        print(e)
        print("Please choose a different name.\n")

qr = qrcode.QRCode(box_size = 10, border = 4, error_correction=qrcode.constants.ERROR_CORRECT_M)

qr.add_data(data)
qr.make(fit = True)

img_qr_code = qr.make_image(fill_color = 'black', back_color = 'white')
img_qr_code.save(full_path)

print(f'QR code successfully saved as {img_qr_filename}')