import os
import hashlib
import binascii
import re
import zlib,base64
from unittest import result
from flask import Flask, render_template, request, session, redirect, url_for, flash,g

UPLOAD_FOLDER = 'D:'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','jfif'])

local_server = True
app = Flask(__name__)
app.secret_key = 'rohit'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




@app.route("/")
def home():
    return render_template('home.html')

@app.route("/viewsign")
def searchv():
    return render_template('search.html')

@app.route("/booklist")
def bl():
    return render_template('booklist.html')
    
@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/crud")
def crud():
    return render_template('crud.html')

@app.route("/gallery")
def gallery():
    return render_template('gallery.html')

@app.route("/organ")
def organ():
    return render_template('organ.html')

@app.route("/index")
def index():
    return render_template('index.html')
    

@app.route("/index1")
def index1():
    return render_template('index1.html')

@app.route("/index2")
def index2():
    return render_template('index2.html')

@app.route("/index3")
def index3():
    return render_template('index3.html')

@app.route("/index4")
def index4():
    return render_template('index4.html')

@app.route("/index5")
def index5():
    return render_template('index5.html')

@app.before_request
def before_request():
    if 'user_id' in session:
        file=open('users.txt','r')
  
        
        for line in file:
            fields=line.split('|')
            if fields[0]==session['user_id'] :
                g.user=fields
                
                break
        file.close()
    

@app.route("/logint",methods=['POST', 'GET'])
def Userlogin():
    
    if request.method == "POST":
        session.pop('user_id',None)
        name=request.form.get('name')
        pwd=request.form.get('pwd')
        
        file=open('users.txt','r')
  
        details=''
        for line in file:
            fields=line.split('|')
            if fields[1]==name and verify_password(fields[2], pwd):
                details=fields
                break
        file.close() 
        if details=='':
            return "USer not found"
        else:
            session['user_id']=details[0]
            return redirect('/bookings')   
    return render_template('logint.html')     


@app.route('/signup',methods=['POST','GET'])
def userregister():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        phn=request.form.get('phn')
        gen=request.form.get('gen')
        pwd=request.form.get('pwd')
        file=open('users.txt','r')
  
        k=['']
        for line in file:
            fields=line.split('|')
        
            k.append(fields)
        #k=k.append(fields)
        if k[-1]=='':
            count=0
        else:
            count=k[-1][0]
          
        
        file = open('users.txt', 'a')
        Slno=int(count)+1

        file.write(str(Slno)+"|"+name+"|"+hash_password(pwd)+"|"+phn+"|"+gen+"|"+email+"\n")
        file.close()
        return redirect('/logint')
        

    return render_template('signup.html')

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


@app.route('/bookings',methods=['POST','GET'])
def bookings():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        phn=request.form.get('phn')
        gen=request.form.get('gen')
        bike=request.form.get('bike')
        city=request.form.get('city')
        address=request.form.get('address')

        pos = binary_search('bookings.txt', name)
	    

    		
        file=open('bookings.txt','r')

        k=['']
        for line in file:
            fields=line.split('|')
        
            k.append(fields)
        #k=k.append(fields)
        if k[-1]=='':
            count=0
        else:
            count=k[-1][0]
          
        
        file = open('bookings.txt', 'a')
        pos = file.tell()
        Slno=int(count)+1

        file.write(str(pos)+"20"+"|"+name+"|"+bike+"|"+phn+"|"+gen+"|"+email+"|"+city+"|"+address+ "|"+"$"+"\n")
        file.close() 
        return redirect('/')
        

    return render_template('book.html')

  

def binary_search(fname, search_key):
	t = []
	fin = open(fname,'r')
	for lx in fin:
		lx = lx.rstrip()
		wx = lx.split('|')
		t.append((wx[0], wx[1]))
	fin.close()
	l = 0
	r = len(t) - 1
	while l <= r:
		mid = (l + r)//2
		if t[mid][0] == search_key:
			return int(t[mid][1])
		elif t[mid][0] <= search_key:
			l = mid + 1
		else:
			r = mid - 1
	return -1

def sorting(filename):
    infile = open(filename, 'r')
    words = []
    for line in infile:
        temp = line.split()
        for i in temp:
            words.append(i)
        #words.append('\n')    
    infile.close()
    words.sort()
    outfile = open("temp.txt", "w")
    for i in words:
        outfile.writelines(i)
        outfile.writelines('\n')
    outfile.close()
#----------------------------------------------ADMIN LOGIN ------------------------------------------------------------------#	

@app.before_request
def before_request():
    if 'user_id' in session:
        file=open('users.txt','r')
  
        
        for line in file:
            fields=line.split('|')
            if fields[0]==session['user_id'] :
                g.user=fields
                
                break
        file.close()
    if 'aduser_id' in session:
            file=open('admin.txt','r')
  
        
            for line in file:
                fields=line.split('|')
                if fields[0]==session['aduser_id'] :
                    g.user=fields
                    
                    break
            file.close() 

@app.route("/logina",methods=['POST', 'GET'])
def adUserlogin():
    
    if request.method == "POST":
        session.pop('aduser_id',None)
        name=request.form.get('name')
        pwd=request.form.get('pwd')
        
        file=open('admin.txt','r')
  
        details=''
        for line in file:
            fields=line.split('|')
            if fields[1]==name and verify_password(fields[2], pwd):
                details=fields
                break
        file.close() 
        if details=='':
            return "USer not found"
        else:
            session['aduser_id']=details[0]
            return redirect('/crud')   
    return render_template('admin.html')     


@app.route('/signupa',methods=['POST','GET'])
def aduserregister():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        phn=request.form.get('phn')
        gen=request.form.get('gen')
        pwd=request.form.get('pwd')
        file=open('admin.txt','r')
  
        k=['']
        for line in file:
            fields=line.split('|')
        
            k.append(fields)
        #k=k.append(fields)
        if k[-1]=='':
            count=0
        else:
            count=k[-1][0]
          
        
        file = open('admin.txt', 'a')
        Slno=int(count)+1

        file.write(str(Slno)+"|"+name+"|"+hash_password(pwd)+"|"+phn+"|"+gen+"|"+email+"\n")
        file.close()
        return redirect('/logina')
        

    return render_template('adminsign.html')

#--------------------------------------------------views-----------------------------------------------------------------------------#


@app.route('/viewbooks')
def viewbookings():
 
    file=open('bookings.txt','r')
    k=[]
    for line in file:
        fields=line.split('|')
        k.append(fields)
      

    return render_template('booklist.html',books=k)  

@app.route('/viewusers')
def usersview():
 
    file=open('users.txt','r')
    k=[]
    for line in file:
        fields=line.split('|')
        k.append(fields)
      

    return render_template('userlist.html',users=k)  

@app.route('/viewbikes')
def viewbikes():
 
    file=open('bikes.txt','r')
    k=[]
    for line in file:
        fields=line.split('|')
        k.append(fields)
      

    return render_template('viewbikes.html',bikes=k)      
#-----------------------------------------ADD BIKES------------------------------------------------#

@app.route("/addbike" ,methods=['POST', 'GET'])
def addbike():
     if request.method=='POST':
        cmp=request.form.get('cmp')
        mod=request.form.get('mod')
        xs=request.form.get('xs')
        onr=request.form.get('onr')
        col=request.form.get('col')
        avl=request.form.get('avl')
        bs=request.form.get('bs')
        ec=request.form.get('ec')
        ml=request.form.get('ml')
        fc=request.form.get('fc')
        file=open('bikes.txt','r')
        pos1 = binary_search('bikes.txt', mod)

	    
  
        k=['']
        for line in file:
            fields=line.split('|')
        
            k.append(fields)
        #k=k.append(fields)
        if k[-1]=='':
            count=0
        else:
            count=k[-1][0]
          
        
        file = open('bikes.txt', 'a')
        file1=open('bike1.txt','a')
        pos1 = file.tell()
        Slno=int(count)+1

        file.write(str(pos1)+"01"+"|"+ cmp +"|"+ mod+"|"+xs+"|"+onr+"|"+col+"|"+avl+"|"+bs+"|"+ec+"|"+ml+"|"+fc+"|"+ "#" +"\n")
        file1.write(cmp +"|"+ mod+"|"+xs+"|"+onr+"|"+col+"|"+avl+"|"+bs+"|"+ec+"|"+ml+"|"+fc+"|"+ "#" +"\n")
        file.close()
        sorting('bike1.txt')
        return redirect('/addbike')
        
     file=open('bikes.txt','r')
     k=[]
     for line in file:
        fields=line.split('|')
        k.append(fields)
       
   
     return render_template('addbike.html',bikes=k)


@app.route('/delete/<pos1>')
def pos(pos1):
    a=open("bikes.txt")
    lines=a.readlines()
    a.close()
    p=-1
    q=0
    for i in lines:
        q=q+1
        p=i.find(pos1)
        if p!=-1:
            flag=i
            break
    if p!=-1:
        del lines[q-1]
        b=open("bikes.txt","w+")
        for line in lines:
            b.write(line)
        b.close()    
    return redirect("/addbike")  


		

  #--------------------------------search-----------------------------------------#





		

 




if __name__ == "__main__":
    app.run(debug=True,port=1000)
    