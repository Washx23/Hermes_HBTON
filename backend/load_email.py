import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Enviar los datos por correo electrónico
gmail_user = 'hermestrimegisto4@gmail.com'  # Reemplaza esto por tu correo electrónico de Gmail
gmail_password = 'cycm pdlp hkke ixlj'  # Reemplaza esto por tu contraseña de Gmail

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = 'washingtonc0023@gmail.com'  # Reemplaza esto por el correo electrónico del destinatario
    msg['Subject'] = 'Resultados'

    # Adjuntar el archivo de texto al correo electrónico
    with open('resultados.txt', 'r') as f:
        attach_file = MIMEText(f.read(), 'plain')
        attach_file.add_header('Content-Disposition', 'attachment', filename=str('result.txt')) 
        msg.attach(attach_file)

    text = msg.as_string()
    server.sendmail(gmail_user, 'washingtonc0023@gmail.com', text)  # Reemplaza esto por el correo electrónico del destinatario
    server.close()

    print('Correo enviado!')
except Exception as e:
    print('Algo salió mal...', e)
