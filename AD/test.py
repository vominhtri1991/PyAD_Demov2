from pyad import *
from pyad import aduser,adquery

#import pyad.adquery

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
user1 = pyad.aduser.ADUser.from_dn("cn=u2, cn=Users"+domain_str)
#user1 = pyad.aduser.ADUser.from_cn("u2")
print(user1.get_attribute("samaccountname"))
print(user1.get_attribute("name"))
print(user1.get_attribute("userPrincipalName")[0])
print(user1.get_attribute("whencreated")[0])
print(user1.get_attribute("whencreated")[0])
print(user1.get_attribute("AccountExpirationDate"))

ou = pyad.adcontainer.ADContainer.from_dn("cn=Users"+domain_str)
newuser=pyad.aduser.ADUser.create("user_test",ou,password="123",enable=True,optional_attributes={"fullName":"Nguyen Van A",'displayName':"Nguyen Van A","givenName":"Nguyen Van A","mail":"nguyenvana@gmail.com"})


