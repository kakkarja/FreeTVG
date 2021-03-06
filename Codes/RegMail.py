import webbrowser
from Ck_user_serialNum import RegKey
import os

def composemail(pth: str):
    a = RegKey()
    b = a.ckuserserial()
    c = str(a.writeck(b)).replace('&', '%26')
    pth = os.path.join(pth, 'Registration.txt')
    with open(pth, 'w') as reg:
        reg.write(c)
    recipient = 'kakkarja.minder@gmail.com' 
    subject = 'REG:[TVG-Registration]'
    body = f"This is encryption of the User and Serial number of this PC:%0A{c}%0A%0A"
    webbrowser.open(f'mailto:?to={recipient}&subject={subject}&body={body}', new = 1)