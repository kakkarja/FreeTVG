import webbrowser
from Ck_user_serialNum import RegKey
import os
from urllib import parse

def composemail(pth: str):
    a = RegKey()
    b = a.ckuserserial()
    c = str(a.writeck(b))
    pth = os.path.join(pth, 'Registration.txt')
    with open(pth, 'w') as reg:
        reg.write(c)
    recipient = 'kakkarja.minder@gmail.com' 
    subject = 'REG:[TVG-Registration]'
    body = f"This is encryption of the User and Serial number of this PC:\n{c}\n\n"
    webbrowser.open(f'mailto:{recipient}?subject={subject}&body={parse.quote(body)}', new = 1)

if __name__ == '__main__':
    composemail(os.getcwd())