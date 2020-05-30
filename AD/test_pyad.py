from pyad import *


#import pyad.adquery
class ADUser:
	def __init__(self,Name,SammAccountName,email):
		self.name=Name
		self.SamAccountName=SammAccountName
		self.email=email

def getDomain(dc):
	domain_lst=dc.split(".")
	domain_str=""
	for i in domain_lst[1::]:
		domain_str=domain_str+" , dc="+i
	return domain_str


DC="DC01.vmt.local"
username="Administrator"
password="P@ssword"
domain_str=getDomain(DC)

pyad.set_defaults(ldap_server=DC, username=username, password=password)
#user = pyad.aduser.ADUser.from_cn("u1@vmt.local")
#user1 = pyad.aduser.ADUser.from_dn("cn=u2, cn=Users, dc=vmt, dc=local")

#List AD user attribute
user1 = pyad.aduser.ADUser.from_dn("cn=u2, cn=Users"+domain_str)
#user1 = pyad.aduser.ADUser.from_cn("u2")
print(user1.get_attribute("samaccountname"))
print(user1.get_attribute("name"))
print(user1.get_attribute("userPrincipalName")[0])
print(user1.get_attribute("whencreated")[0])
print(user1.get_attribute("whencreated")[0])
print(user1.get_attribute("AccountExpirationDate"))

#List all Users
ou = pyad.adcontainer.ADContainer.from_dn("cn=Users"+domain_str)
#newuser=pyad.aduser.ADUser.create("user_test",ou,password="123",enable=True,optional_attributes={'displayName':"Nguyen Van A","givenName":"Nguyen Van A","mail":"nguyenvana@gmail.com"})

AD_Users=[]

for obj in ou.get_children():
	#print(type(obj))
	if(type(obj)==pyad.aduser.ADUser):
		#print(obj.get_attribute("samaccountname"))
		#print(obj.get_attribute("userPrincipalName"))
		#print(obj.get_attribute("whencreated"))
		samaccountname=obj.get_attribute("samaccountname")[0]
		name=obj.get_attribute("name")
		email=obj.get_attribute("whenCreated")
		AUser=ADUser(name,samaccountname,email)
		AD_Users.append(AUser)
print(len(AD_Users))

#Create new OU
print(domain_str[2::])
ou = pyad.adcontainer.ADContainer.from_dn(domain_str[2::])
print(ou)
c = ou.create_container(
	name = 'Accounting',
	#type_ == 'organizationalUnit'
	optional_attributes = dict(
                description = "Accounting OU"
        )
)

#List OUs
for obj in ou.get_children():
	if("OU=" in str(obj)):
		print(obj.get_attribute("name")[0])
		print(obj.get_attribute("distinguishedName")[0])

#Create user in OU
ou = pyad.adcontainer.ADContainer.from_dn("OU=Accounting"+domain_str)
print(ou)
newuser=pyad.aduser.ADUser.create("user_outest",ou,password="123",enable=True,optional_attributes={'displayName':"Nguyen Van A","givenName":"Nguyen Van A","mail":"nguyenvana@gmail.com"})
newuser.rename('NGUYEN VAN A')


