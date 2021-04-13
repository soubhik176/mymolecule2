from flask import *
import cirpy
#import sqlite3
import string 
import random 
'''
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
'''
import smtplib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from email.mime.text import MIMEText
from sqlalchemy.dialects.mysql import LONGTEXT
"""
conn=sqlite3.connect('mymolecule.db')
c=conn.cursor()

"""

"""
table creator for compounds

"""
def composition(l):
    l=l.replace("]", ")")
    l=l.replace("[", "(")
    l=l.replace(".", "1")
    l=l.replace(")(", ")1(")
	
    symbol={1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca', 21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn', 31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr', 37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr', 41: 'Nb', 42: 'Mo', 43: 'Tc', 44: 'Ru', 45: 'Rh', 46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In', 50: 'Sn', 51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs', 56: 'Ba', 57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd', 61: 'Pm', 62: 'Sm', 63: 'Eu', 64: 'Gd', 65: 'Tb', 66: 'Dy', 67: 'Ho', 68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu', 72: 'Hf', 73: 'Ta', 74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt', 79: 'Au', 80: 'Hg', 81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At', 86: 'Rn', 87: 'Fr', 88: 'Ra', 89: 'Ac', 90: 'Th', 91: 'Pa', 92: 'U', 93: 'Np', 94: 'Pu', 95: 'Am', 96: 'Cm', 97: 'Bk', 98: 'Cf', 99: 'Es', 100: 'Fm', 101: 'Md', 102: 'No', 103: 'Lr', 104: 'Rf', 105: 'Db', 106: 'Sg', 107: 'Bh', 108: 'Hs', 109: 'Mt', 110: 'Ds', 111: 'Rg', 112: 'Cn', 113: 'Nh', 114: 'Fl', 115: 'Mc', 116: 'Lv', 117: 'Ts', 118: 'Og'}
    l=l.replace("(", " ( ")
    l=l.replace(")", " ) ")


    for i in symbol.values() :
        if len(i)==2:
            l=l.replace(i, f" {i} ")
    l=l.split()


    for i in range(0,len(l)):
        if (len(l[i]) >=2 and l[i][0].isupper() and not l[i][1].islower()) or any( c in "1234567890" for c in l[i]):
            for j in l[i]:
                if j.isupper():
                    l[i]=l[i].replace(j,f" {j} ")

    t=""

    for i in l:
        t+=f" {i} "
    t=t.split()



    def clean(t):
        p=t
        for i in range(0,len(t)-1):
            if t[i] ==")" and (t[i+1] in ("(",")") or t[i+1] in symbol.values()):
                t.pop(i)
                j=i
                c=1
                while True:
                    j-=1
                    if j==-1:
                        break
                    elif c==0:
                        t.pop(j+1)
                        break
                    elif t[j]==")":
                        c+=1
                    elif t[j]=="(":
                        c-=1
                break
        
        return t


    while True:
        g=t
        if any((t[i] ==")" and (t[i+1] in ("(",")") or t[i+1] in symbol.values())) for i in range(0,len(t)-1))==True:
            t=clean(t)
        else:

            
            break
    i=-1
    if t[i]==")":
        t.pop(i)
        j=i
        c=-1
        while True:
            j-=1
            if j==-len(t)-2:
                break
            elif c==0:
                t.pop(j+1)
                break
            elif t[j]==")":
                c-=1
            elif t[j]=="(":
                c+=1

    def clear(t):
        for i in range(0,len(t)-1):
            if t[i+1][0] in  "1234567890" and t[i]==")":
                j=i-len(t)
                c=-1
                while True:
                    j-=1
                    if j==-len(t)-2:
                        break
                    elif c==0:
                        x=t[0:j+1]
                        y=t[(j+1):i+2]
                        z=t[i+2:len(t)]
                        break
                    elif t[j]==")":
                        c-=1
                    elif t[j]=="(":
                        c+=1
                break
        

        a=int(y[-1])
        y.pop(-1)

        y.remove(")")
        y.remove("(")
        if y[-1][0] not in "1234567890":
            y.append(" ")
        for i in range(0,len(y)-1):
            if y[i][0] in "1234567890":
                y[i]=str(int(y[i])*a)
                
            elif y[i][0] not in "1234567890" and y[i+1][0] not in "1234567890":
                y[i]=y[i] +" "+ str(a)

        if y[-1][0] in "1234567890":
            y[-1]=str(int(y[-1])*a)

        j=""
        for i in y:
            j+=f" {i} "
        y=j.split()

        

        t=x+y+z
        return t

    while "(" in t or ")" in t:
        t=clear(t)



    a=[]
    b=dict()

    for i in t:
        if i[0] not in "1234567890":
            a.append(i)

    a=set(a)




    for i in range(0,len(t)-1):
        if t[i] in a and t[i+1] in a:
            t[i]=t[i]+" 1 "
    j=""
    for i in t:
        j+=f" {i} "
    t=j.split()
    if t[-1][0] not in "1234567890":
        t.append("1")


    for i in a:
        b[i]=0

    for i in range(0,len(t)-1):
        if t[i][0] not in "1234567890":
            b[t[i]]+=int(t[i+1])


    c=dict()
    for x,y in symbol.items():
        c[y]=x

    m=dict()
    for i in b:
        m[c[i]]=b[i]

    return m

naam=""
img=""
def molecule(l):
    global img
    global naam
    m=l
    if cirpy.resolve(l,"formula") != None:
        img=cirpy.Molecule(l, width=1000, height=1000, symbolfontsize=12)
        img=img.image_url
        naam=cirpy.resolve(l,"formula")
        
        l=cirpy.resolve(l,"formula")

        k=[]
        s=""
        """
        for i in naam:
            k.append(i)
        for i in range(0,len(k)):
            try:
                if k[i+1] not in ("-",","):
                    k[i]=int(k[i])
                    k[i]="<sub>"+str(k[i])+"</sub>"
            except:
                pass
        
        for i in k:
            s+=i
        naam="("+s+")"
        """
    elif cirpy.resolve(l,"formula") == None:
        naam=""
        img=""        
    try:
        m=composition(m)
        naam=""
        img=""
    except:
        pass

    try:
        t=composition(l)
    except:
        return None
        
    t=composition(l)
    z=t
    mass={1: 1.0, 2: 4.0, 3: 7, 4: 9.0, 5: 11, 6: 12.0, 7: 14.0, 8: 16.0, 9: 19.0, 10: 20, 11: 23.0, 12: 24, 13: 27.0, 14: 28, 15: 31.0, 16: 32, 17: 35.5, 18: 40, 19: 39, 20: 40, 21: 45.0, 22: 48, 23: 51, 24: 52.0, 25: 55, 26: 56, 27: 59, 28: 59, 29: 63.5, 30: 65, 31: 70, 32: 73, 33: 75, 34: 79.0, 35: 80, 36: 84, 37: 85.5, 38: 88, 39: 89, 40: 91, 41: 93, 42: 96.0, 43: 98, 44: 101, 45: 103, 46: 106, 47: 108, 48: 112, 49: 115, 50: 119, 51: 122, 52: 128, 53: 127, 54: 131, 55: 133, 56: 137, 59: 141, 73: 181, 74: 184, 75: 186, 76: 190, 77: 192, 78: 195, 79: 197.0, 80: 201, 82: 207, 83: 209.0, 84: 209.0, 85: 210.0, 86: 222.0, 87: 223.0, 88: 226.0, 104: 267.0, 91: 231.0, 106: 271.0, 107: 274.0, 108: 269.0, 109: 276.0, 110: 281.0, 111: 281.0, 112: 285.0, 113: 286.0, 114: 289.0, 115: 288.0, 116: 293.0, 117: 294.0, 118: 294.0, 57: 139, 58: 140, 60: 144, 61: 145, 62: 150, 63: 152.0, 64: 157, 65: 159, 66: 162.5, 67: 165, 68: 167, 69: 169, 70: 173.0, 71: 175.0, 89: 227.0, 90: 232.0, 92: 238.0, 93: 237.0, 94: 244.0, 95: 243.0, 96: 247.0, 97: 247.0, 98: 251.0, 99: 252.0, 100: 257.0, 101: 258.0, 102: 259.0, 103: 262.0}
    name={1: 'Hydrogen', 2: 'Helium', 3: 'Lithium', 4: 'Beryllium', 5: 'Boron', 6: 'Carbon', 7: 'Nitrogen', 8: 'Oxygen', 9: 'Fluorine', 10: 'Neon', 11: 'Sodium', 12: 'Magnesium', 13: 'Aluminum', 14: 'Silicon', 15: 'Phosphorus', 16: 'Sulfur', 17: 'Chlorine', 18: 'Argon', 19: 'Potassium', 20: 'Calcium', 21: 'Scandium', 22: 'Titanium', 23: 'Vanadium', 24: 'Chromium', 25: 'Manganese', 26: 'Iron', 27: 'Cobalt', 28: 'Nickel', 29: 'Copper', 30: 'Zinc', 31: 'Gallium', 32: 'Germanium', 33: 'Arsenic', 34: 'Selenium', 35: 'Bromine', 36: 'Krypton', 37: 'Rubidium', 38: 'Strontium', 39: 'Yttrium', 40: 'Zirconium', 41: 'Niobium', 42: 'Molybdenum', 43: 'Technetium', 44: 'Ruthenium', 45: 'Rhodium', 46: 'Palladium', 47: 'Silver', 48: 'Cadmium', 49: 'Indium', 50: 'Tin', 51: 'Antimony', 52: 'Tellurium', 53: 'Iodine', 54: 'Xenon', 55: 'Cesium', 56: 'Barium', 57: 'Lanthanum', 58: 'Cerium', 59: 'Praseodymium', 60: 'Neodymium', 61: 'Promethium', 62: 'Samarium', 63: 'Europium', 64: 'Gadolinium', 65: 'Terbium', 66: 'Dysprosium', 67: 'Holmium', 68: 'Erbium', 69: 'Thulium', 70: 'Ytterbium', 71: 'Lutetium', 72: 'Hafnium', 73: 'Tantalum', 74: 'Tungsten', 75: 'Rhenium', 76: 'Osmium', 77: 'Iridium', 78: 'Platinum', 79: 'Gold', 80: 'Mercury', 81: 'Thallium', 82: 'Lead', 83: 'Bismuth', 84: 'Polonium', 85: 'Astatine', 86: 'Radon', 87: 'Francium', 88: 'Radium', 89: 'Actinium', 90: 'Thorium', 91: 'Protactinium', 92: 'Uranium', 93: 'Neptunium', 94: 'Plutonium', 95: 'Americium', 96: 'Curium', 97: 'Berkelium', 98: 'Californium', 99: 'Einsteinium', 100: 'Fermium', 101: 'Mendelevium', 102: 'Nobelium', 103: 'Lawrencium', 104: 'Rutherfordium', 105: 'Dubnium', 106: 'Seaborgium', 107: 'Bohrium', 108: 'Hassium', 109: 'Meitnerium', 110: 'Darmstadtium', 111: 'Roentgenium', 112: 'Copernicium', 113: 'Nihonium', 114: 'Flerovium', 115: 'Moscovium', 116: 'Livermorium', 117: 'Tennessine', 118: 'Oganesson'}
    symbol={1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca', 21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn', 31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr', 37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr', 41: 'Nb', 42: 'Mo', 43: 'Tc', 44: 'Ru', 45: 'Rh', 46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In', 50: 'Sn', 51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs', 56: 'Ba', 57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd', 61: 'Pm', 62: 'Sm', 63: 'Eu', 64: 'Gd', 65: 'Tb', 66: 'Dy', 67: 'Ho', 68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu', 72: 'Hf', 73: 'Ta', 74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt', 79: 'Au', 80: 'Hg', 81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At', 86: 'Rn', 87: 'Fr', 88: 'Ra', 89: 'Ac', 90: 'Th', 91: 'Pa', 92: 'U', 93: 'Np', 94: 'Pu', 95: 'Am', 96: 'Cm', 97: 'Bk', 98: 'Cf', 99: 'Es', 100: 'Fm', 101: 'Md', 102: 'No', 103: 'Lr', 104: 'Rf', 105: 'Db', 106: 'Sg', 107: 'Bh', 108: 'Hs', 109: 'Mt', 110: 'Ds', 111: 'Rg', 112: 'Cn', 113: 'Nh', 114: 'Fl', 115: 'Mc', 116: 'Lv', 117: 'Ts', 118: 'Og'}
    A="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    a="abcdefghijklmnopqrstuvwxyz"

    l=[]
    for i in t:
        l.append(symbol[i])
        l.append(t[i])
    t=l
    l=""
    for i in t:
        l+=str(i)

    l1=[]
    s=l
    for i in range(0,len(l)-1):
        if l[i].isupper() and l[i+1].islower():
            s=l[i]+l[i+1]
            l1.append(s)
        elif l[i].isupper() and l[i+1].isupper():
            s=l[i]
            l1.append(s)
        elif l[i].isupper() and ((l[i-1] and l[i+1]) not in (A or a)):
            l1.append(l[i])
    if l[-1].isupper():
        s=l[-1]
        l1.append(s)


    for i in l1 :
        if l.count(i)==1:
            l=l.replace(i," "+i+" ")
    l=l.split()
    
    d={}
    for i in z:
        #print(z)
        d[symbol[int(i)]]=z[int(i)]

    atm=list(symbol.keys())
    sym=list(symbol.values())
    total=0
    
    #m="""<center><div class="container"><table  class="table table-hover"">
    #"""
    #m=m+"<tr>"+"<th>Element</th>"+ "<th>Atomic no.</th>"+ "<th>Atomic mass</th>"+"<th>No. of atoms</th></tr>"
    m=list()
    for x,y in d.items():
        #m+="<tr>"+"<td>"+name[atm[sym.index(x)]]+","+x+"</td>"+"<td>"+ str(atm[sym.index(x)])+"</td>"+"<td>"+ str(mass[int(atm[sym.index(x)])])+"<td>"+ str(y)+"</tr>"
        m.append((name[atm[sym.index(x)]], x, str(atm[sym.index(x)]), str(mass[int(atm[sym.index(x)])]), str(y)))
        total+=mass[int(atm[sym.index(x)])]*int(y)


    m.append(total)
    return m

"""
end of table creator
"""
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']= "mysql+pymysql://sql6403019:FWjDIxz3zN@sql6.freesqldatabase.com:3306/sql6403019"
#app.config['SQLALCHEMY_DATABASE_URI']= "mysql+pymysql://uaXrEytddV:y3jzavA3RC@remotemysql.com:3306/uaXrEytddV"
#app.config['SQLALCHEMY_DATABASE_URI']= "mysql+pymysql://hellosoubhik:soubhikji@hellosoubhik.mysql.pythonanywhere-services.com:3306/mydatabase"
app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://lcvgmexciwcvgl:30832a2753695c613b70320d46fa6329b7060ea1b9edbe741ac1ac0851f3d059@ec2-54-167-152-185.compute-1.amazonaws.com:5432/dcaglq7g7975aq"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)
app.secret_key = "abc"  

class Users(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable = False) 
    password = db.Column(db.String(200), nullable = False) 
    name = db.Column(db.String(200), nullable = False)

    def __repr__(self) -> str:
        return f"{self.email} - {self.password} - {self.name}"

class Bookmarks(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable = False)
    #bookmark_list = db.Column(db.String(21844), nullable = True)
    bookmark_list = db.Column(db.TEXT, nullable = True)

class Signups(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable = False) 
    password = db.Column(db.String(200), nullable = False) 
    name = db.Column(db.String(200), nullable = False)
    verification_code = db.Column(db.String(200), nullable = False)

class Forgots(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable = False) 
    verification_code = db.Column(db.String(200), nullable = False)

def code_gen():
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))
    return res

def email_sender(process,email,res=code_gen()):


	'''
    message = Mail(
        from_email='soubhik176@gmail.com',
        to_emails=email,
        subject='mymolecule verification link',
        html_content='<strong>Please click the given link to verify your account at mymolecule {}</strong>'.format(res))
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    print("email sending...")
    
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.ehlo()
	s.starttls()
	s.ehlo

	# Authentication
	s.login("soubhik176@gmail.com", "soubhikji1234")
	  
	# message to be sent
	message = res
	  
	# sending the mail
	s.sendmail("soubhik176@gmail.com", email, message)
	  
	# terminating the session
	s.close()'''
	if process=="verification":
		y="verification"
	elif process=="resetsuccess":
		y="resetsuccess"
	server = smtplib.SMTP("smtp.gmail.com",587)
	server.ehlo() # Can be omitted
	server.starttls() # Secure the connection
	server.login('sahisoubhik@gmail.com',"soubhiksahihai")
	message = u"""


	<center>
	<h1>This is a verification e-mail message from my molecule</h1>
	<h2>For email -- {x}</h2>
	<br>
	<br>
	<h2>
	<a href="https://my-molecule2.herokuapp.com/{y}/{x}/{z}"> verification link</a>
	</h2>
	</center>
	""".format(y=y,x=email,z= res)
	msg=MIMEText(message, 'html')
	msg['Subject']= y+" "+"Mymolecule"
	server.sendmail('soubhik176@gmail.com',email, msg.as_string())
	return res



def feed_sender(email, feed):


	server = smtplib.SMTP("smtp.gmail.com",587)
	server.ehlo() # Can be omitted
	server.starttls() # Secure the connection
	server.login('sahisoubhik@gmail.com',"soubhiksahihai")
	message = u"""
	<center>
	{email}<br><br>
	{feed}
	</center>
	""".format(feed=feed, email=email)
	msg=MIMEText(message, 'html')
	msg['Subject']="Mymolecule feedback -- "+email
	server.sendmail('soubhik176@gmail.com','hellosoubhik@protonmail.com', msg.as_string())
	




@app.route('/', methods=["POST", "GET"])
def index():
	global naam
	global img

	if 'search_item' in session:
		search_item=session['search_item']
		session.pop('search_item')
		if search_item.strip() != "":
			table=molecule(search_item)
			mass_number=None
			if table != None:
				mass_number=table[-1]
				table.pop()
				if "user" in session:
					lst=Bookmarks.query.filter_by(email=session["user"]).first()
					if search_item.strip() not in json.loads(lst.bookmark_list).values() :
						listed=False
						date_time=None
						return render_template("output.html", search_item=search_item, table=table, mass_number=mass_number, naam=naam, image=img, listed=listed, date_time=date_time)
					else:
						listed=True
						date_time=None
						for i in json.loads(lst.bookmark_list).items():
							if i[1]==search_item.strip():
								date_time=i[0]
								break

						return render_template("output.html", search_item=search_item, table=table, mass_number=mass_number, naam=naam, image=img, listed=listed, date_time=date_time)
			else:
				return render_template("output.html", search_item=search_item, table=table, mass_number=mass_number, naam=naam, image=img)


	if request.method == "POST":
		search_item=request.form["search_item"]
		if search_item.strip() != "":
			table=molecule(search_item)
			mass_number=None
			if table != None:
				mass_number=table[-1]
				table.pop()
				if "user" in session:
					lst=Bookmarks.query.filter_by(email=session["user"]).first()
					if search_item.strip() not in json.loads(lst.bookmark_list).values() :
						listed=False
					else:
						listed=True
					return render_template("output.html", search_item=search_item, table=table, mass_number=mass_number, naam=naam, image=img, listed=listed)

				else:
					listed=False
					return render_template("output.html", search_item=search_item, table=table, mass_number=mass_number, naam=naam, image=img, listed=listed)
			else:
				return render_template("output.html", search_item=search_item, table=table, mass_number=mass_number, naam=naam, image=img)
	else:
		return render_template("index.html", session=session)


@app.route('/redir/<search_item>', methods=["POST", "GET"])
def redir(search_item):
	session['search_item']=search_item
	return redirect(url_for('index'))


@app.route('/bookmarks', methods=["POST", "GET"])
def bookmarks():
	if "user" not in session:
		return redirect(url_for('signin'))
	else:
		lst=Bookmarks.query.filter_by(email=session['user']).first()
		if lst == None or len(json.loads(lst.bookmark_list)) == 0:
			bookmark_list=json.loads(lst.bookmark_list)
			return render_template("bookmarks.html", bookmark_list=bookmark_list)
		else:
			bookmark_list=json.loads(lst.bookmark_list)
			return render_template("bookmarks.html", bookmark_list=bookmark_list)

@app.route('/newmark/<search_item>', methods=["POST", "GET"])
def newmark(search_item):
	if "user" not in session:
		return redirect(url_for('signin'))
	else:
		session["search_item"]=search_item
		lst=Bookmarks.query.filter_by(email=session['user']).first()
		x=lst.bookmark_list
		y = json.loads(x)
		y[datetime.now().strftime("%c")] = search_item.strip() 
		print(y)
		x = json.dumps(y)
		lst.bookmark_list = x
		db.session.commit()
	return redirect(url_for('index'))

@app.route('/removemark/<date_time>/<place>', methods=["POST", "GET"])
def removemark(date_time, place):
	if "user" not in session:
		return redirect(url_for('signin'))
	else:
		lst=Bookmarks.query.filter_by(email=session['user']).first()
		x=lst.bookmark_list
		y = json.loads(x)
		search_item=y[date_time]
		session["search_item"]=search_item
		y.pop(date_time)
		print(y)
		x = json.dumps(y)
		lst.bookmark_list = x
		db.session.commit()
	if place == "bookmarks":
		return redirect(url_for('bookmarks'))
	elif place == "output":

		print(search_item)
		return redirect(url_for('index'))







@app.route('/signin', methods=["POST", "GET"])
def signin():
	if "user" in session:
		return redirect(url_for('index'))

	elif request.method == "POST":
		email=request.form["email"]
		password=request.form["password"]
		user = Users.query.filter_by(email=email).first()
		if (user != None) and (password == user.password) :
			session['user'] = email
			session['password'] = password
			session['name'] = user.name

			return redirect(url_for('index'))
		else:
			return render_template('signin/signin.html', alert=True)
	else :
		return render_template('signin/signin.html')
        
@app.route('/signout')
def signout():
	if "user" in session:

		
		session.pop('user')
		session.pop('password')
		session.pop('name')
		return redirect(url_for('index'))
	elif "user" not in session:
		return redirect(url_for('index'))









@app.route('/signup', methods=["POST", "GET"])
def signup():

    #conn=sqlite3.connect('mymolecule.db')
    #c=conn.cursor()

    if "user" in session:
        return redirect(url_for('index'))

    else :
        if request.method == "POST":
            email=request.form["email"]
            password=request.form["password"]
            passwordcon=request.form["passwordcon"]
            name=request.form["name"]
            if password != passwordcon or name.strip()=="":
                return render_template('signup/signup.html', alert=True)

            elif Users.query.filter_by(email=email).first() != None:
                return render_template('signup/signup.html', alert=True)


            else:
                
                #c.execute("select email from signup;")
                present = Signups.query.filter_by(email=email).first()

                if present is None:
                                       
                    #c.execute("INSERT INTO SIGNUP (email, password, verification_code) VALUES ({}, {}, {});".format("bitadox958@naymio.com", str(password), res))
                    #conn.commit()

                    new_signup = Signups(email=email, password=password, name=name, verification_code=email_sender(email=email, process='verification'))
                    db.session.add(new_signup)
                    db.session.commit()

                elif present is not None:
                    update_signup=Signups.query.filter_by(email=email).first()
                    update_signup.verification_code = email_sender(email=email, process='verification')
                    update_signup.password = password
                    update_signup.name = name

                    db.session.commit()
                    #c.execute("UPDATE signup SET verification_code ={} WHERE email ={};".format(res, email))
                    #conn.commit()

            return render_template('signup/signup.html', sent=True)
        else:
            return render_template('signup/signup.html', alert=False)






@app.route('/forgotpassword', methods=["POST", "GET"])
def forgotpassword():
    if "user" in session:
        return redirect(url_for('index'))


    if request.method == "POST":
    	email=request.form["email"]
    	update_user=Users.query.filter_by(email=email).first()
    	update_pass=Forgots.query.filter_by(email=email).first()
    	
    	if update_user == None:
    		return render_template('forgot_password/forgotpassword.html', alert=True)
    	else:

	    	if update_pass != None and update_user.email == email:
	    		update_pass.verification_code=email_sender(email=email, process='resetsuccess' )
	    		db.session.commit()
	    		return render_template('forgot_password/forgotpassword.html', alert=False)
	    	

	    	elif update_pass == None and update_user.email == email:

	    		new_forgot = Forgots(email=email, verification_code=email_sender(email=email, process='resetsuccess' ))
	    		db.session.add(new_forgot)
	    		db.session.commit()



	    		return render_template('forgot_password/forgotpassword.html', alert=False)
    	'''else:
    		return render_template('forgot_password/forgotpassword.html', alert=True)'''
    else :
        return render_template('forgot_password/forgotpassword.html')

@app.route('/resetsuccess/<email>/<verification_code>', methods=["POST", "GET"])
def resetsuccess(email, verification_code):
	if "user" in session:
		return redirect(url_for('index'))
	update_pass=Forgots.query.filter_by(email=email).first()
	if update_pass.verification_code == verification_code:
		
		

		update_user=Users.query.filter_by(email=email).first()

		if update_user.email == email:
			if request.method=="POST":
				password=request.form["password"]
				passwordcon=request.form["passwordcon"]

				if password != "" and password==passwordcon:
					update_user.password=password
					db.session.delete(update_pass)

					db.session.commit()
					return render_template('signup/verified.html', success=True)
				else:
					return render_template('forgot_password/resetsuccess.html', alert=True)
			return render_template('forgot_password/resetsuccess.html')

	else:
		return render_template('signup/verified.html', success=False)



        


@app.route('/verification/<email>/<verification_code>', methods=["POST", "GET"])
def verification(email, verification_code):
    if "user" in session:
        return redirect(url_for('index'))

    else :
        #return render_template('signin/signin.html')
        
        present=Signups.query.filter_by(email=email).first()

        if present != None and verification_code== present.verification_code:
            password=present.password
            name=present.name
            new_user = Users(email=email, password=password, name=name )
            x=dict()
            y = json.dumps(x)
            new_mark = Bookmarks(email=email, bookmark_list=y )
            db.session.add(new_user)
            db.session.add(new_mark)
            db.session.delete(present)
            db.session.commit()
            return render_template('signup/verified.html', success=True)
        else:
            return render_template('signup/verified.html', success=False)



@app.route('/feedback', methods=["POST", "GET"])
def feedback():
	present=False
	if "user" in session:
		present=True


	if request.method == "POST" :
		feed=request.form['feedback']
		email=request.form['email']
		if "user" in session:
			email=session["user"]
		if feed.strip() == "" or email.strip() == "":
			return render_template('feedback.html',present=present, alert=True )
		else:
			feed_sender(email=email, feed= feed)
			return render_template('feedback.html',present=present, alert=False )


	else:
		return render_template('feedback.html', present=present)

if __name__ == "__main__":
    app.run(debug=True, port=5000)


'''
if __name__ == "__main__" :

	app.run(debug=True, port=5000)
'''