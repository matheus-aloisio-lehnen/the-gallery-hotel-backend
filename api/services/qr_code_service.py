import qrcode
import base64
import io

def generate_qr_code_base64(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill='black', back_color='white')
    buffered = io.BytesIO()
    qr_image.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return qr_code_base64