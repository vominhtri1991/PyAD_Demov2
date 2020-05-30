from django.shortcuts import render
from pyad import *
import pythoncom 

DC=""
username=""
password=""

class ADUser:
	def __init__(self,name,SammAccountName,created):
		self.name=name
		self.SamAccountName=SammAccountName
		self.created=created

class OU:
	def __init__(self,name,dn_string):
		self.name=name
		self.dn_string=dn_string

def home(request):
	return render(request,'AD/home.html')

def getDomain(dc):
	domain_lst=dc.split(".")
	domain_str=""
	for i in domain_lst[1::]:
		domain_str=domain_str+" , dc="+i
	return domain_str


def listusers(request):
	global DC,username,password
	AD_Users=[]
	DC=request.POST.get('DC')
	username=request.POST.get('username')
	password=request.POST.get('password')
	domain_str=getDomain(DC)
	pyad.set_defaults(ldap_server=DC, username=username, password=password)
	try:
		pythoncom.CoInitialize()
		ou=pyad.adcontainer.ADContainer.from_dn("cn=Users"+domain_str)
		pythoncom.CoUninitialize()
		for obj in ou.get_children():
			#print(obj)
			if(type(obj)==pyad.aduser.ADUser):
				samaccountname=obj.get_attribute("samaccountname")
				name=obj.get_attribute("name")
				print(name)
				created=obj.get_attribute("whenCreated")[0]
				AUser=ADUser(name,samaccountname,created)
				AD_Users.append(AUser)
		#print("Length:"+str(AD_Users.length()))
		
		return render(request,'AD/listusers.html',{"DC":DC,"ADUsers":AD_Users})
	except:	
		return render(request,'AD/error_connect.html')

def createou(request):
	global DC,username,password
	if(request.method=="POST"):
		name=request.POST.get('name')
		description=request.POST.get('description')
		pyad.set_defaults(ldap_server=DC, username=username, password=password)
		domain_str=getDomain(DC)
		pythoncom.CoInitialize()
		ou = pyad.adcontainer.ADContainer.from_dn(domain_str[2::])
		ou.create_container(name=name,optional_attributes = dict(description=description))
		pythoncom.CoUninitialize()
		return render(request,'AD/createou.html',{"infor":"Create OU sucessfully!"})
	else:
		return render(request,'AD/createou.html')

def createuser(request):
	global DC,username,password
	if(request.method=="POST"):
		name=request.POST.get('name')
		fullname=request.POST.get('fullname')
		password_user=request.POST.get('password')
		user_ou=request.POST.get('ou')
		print(user_ou)
		pyad.set_defaults(ldap_server=DC, username=username, password=password)
		pythoncom.CoInitialize()
		ou = pyad.adcontainer.ADContainer.from_dn(user_ou)
		newuser=pyad.aduser.ADUser.create(name,ou,password=password_user,enable=True,
		optional_attributes={'displayName':fullname})
		#newuser.rename(fullname)
		pythoncom.CoUninitialize()
		return render(request,'AD/createuser.html',{"infor":"Create User sucessfully!"})
	else:
		OUs=[]	
		pyad.set_defaults(ldap_server=DC, username=username, password=password)
		domain_str=getDomain(DC)
		pythoncom.CoInitialize()
		print(domain_str[2::])
		ou = pyad.adcontainer.ADContainer.from_dn(domain_str[2::])
		for obj in ou.get_children():
			if("OU=" in str(obj)):
				a_ou=OU(obj.get_attribute("name")[0],obj.get_attribute("distinguishedName")[0])
				print(a_ou)
				OUs.append(a_ou)
		pythoncom.CoUninitialize()
		return render(request,'AD/createuser.html',{"OUs":OUs})
# Create your views here.

