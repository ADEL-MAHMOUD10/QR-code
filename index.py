from flask import Flask,render_template,send_file,request
import qrcode,io 
from vobject import vCard
from PIL import Image


app = Flask(__name__)
@app.route("/")
def main():
    return render_template("index.html")
@app.route("/home")
def main_1():
    return render_template("index.html")

# URL qrcode
@app.route("/QR")
def Home():
  return render_template("qrcode1.html")

@app.route("/QR/download", methods=["POST"])
def generate_qrcode():
  url = request.form.get("url")
  if not url:
    return render_template("error-q.html")

  qr = qrcode.QRCode(version=5)
  qr.add_data(url)
  qr.make()
  qr_co = "Green"
  img = qr.make_image(fill_color = qr_co ,back_color = "white").convert("RGB")
  buffer = io.BytesIO()
  img.save(buffer,format="PNG")
  buffer.seek(0)
  return send_file(buffer, mimetype="image/png", as_attachment=True,download_name="URL-QR.png")


# Vcard qrcode
@app.route("/vcard")
def V_card():
  return render_template("vcard.html")
@app.route("/vcard/download",methods=["POST"])
def card():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    contact = [f"FN:{name}", f"EMAIL:{email}", f"TEL:{phone}"]
    vcard_info = "BEGIN:VCARD\n" + "\n".join(contact) + "\nEND:VCARD\n"
    
    if not name or not email or not phone:
      return render_template("error-v.html") 
    qr_color = "Green"
    qr = qrcode.QRCode(version=5)
    qr.add_data(vcard_info)
    qr.make()
    img = qr.make_image(fill_color = qr_color , back_color ="white").convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png", as_attachment=True,download_name="VCARD-QR.png")

# WIFI qrcode

@app.route("/WIFI")
def wifi():
    return render_template("wifi.html")

@app.route("/WIFI/download", methods=["POST"])
def generate_qr_code():
    ssid = request.form.get("SSID")
    password = request.form.get("Password")
    T_wifi = request.form.get("T_wifi")
# التحقق من صحة المدخلات
    while T_wifi == "None":
        data = "WIFI:S"+ssid+";T:"+T_wifi+";;"
        if not ssid or not T_wifi:
            return render_template("error-w.html")
        break
    else:
        data = "WIFI:S:" + ssid + ";T:"+ T_wifi +";P:" + password + ";;"
        if not ssid or not password or not T_wifi:
            return render_template("error-w.html")
    QRcode = qrcode.QRCode( version = 5,
      error_correction=qrcode.constants.ERROR_CORRECT_H
    )
 
# adding data or text to QRcode
    QRcode.add_data(data)
 
# generating QR code
    QRcode.make()
 
# taking color For QR
    QRcolor = 'Green'
 
# adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGB')
 
# save the QR code generated
    buffer = io.BytesIO()
    QRimg.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png", as_attachment=True,download_name="WIFI-QR.png")
