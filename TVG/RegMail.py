import webbrowser
import os
from urllib import parse
import subprocess

def ckuserserial() -> dict:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    pnam = f'powershell -Command  Get-CimInstance -Class Win32_OperatingSystem | Format-List -Property RegisteredUser,SerialNumber'
    prnms = subprocess.run(pnam, startupinfo = startupinfo, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE, text = True)
    ck = dict([tuple(i.replace(' ', '').split(':')) for i in prnms.stdout.split('\n') if 'RegisteredUser' in i or 'SerialNumber' in i])  
    return ck

def composemail():
    b = ckuserserial()
    c = str(b)
    recipient = 'TVG DEV' 
    subject = 'REG:[TVG-Registration]'
    body = f"These are the user and serial number of this PC:\n{c}\n\n"
    webbrowser.open(f'mailto:{recipient}?subject={subject}&body={parse.quote(body)}', new = 1)
