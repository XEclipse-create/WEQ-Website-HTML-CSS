from passlib.hash import pbkdf2_sha256
import pymongo
import uuid
# Also need to install dnspython for the pymongo drivers to work.

# Databse User Details for connection

usrnme = "admin_mayesh"
password = "mayesh"

srv = "mongodb+srv://{}:{}@weq.e8lai.gcp.mongodb.net/WeQ?retryWrites=true&w=majority".format(
    usrnme, password)
client = pymongo.MongoClient(srv)
##print("MongoDB Connected!")

db = client['WeQ']
CustRegistrationCollection = db['customer']
ShopRegistrationCollection = db['shop']
LoginRegistrationCollection = db['login']
ShopLoginCollection = db['shoplogin']
CustLoginCollection = db['custlogin']
BookingCollection = db['slots']


def CustRegister(name, email, ph_no, city, pincode, password):
    usr_1 = {"email": email}
    r1 = CustRegistrationCollection.find(usr_1)
    check = False
    for i in r1:
        if(email == i['email']):
            check = True
            break
    if(check):
        print("Email Address already exists")
        return False
    else:
        password = pbkdf2_sha256.hash(password)
        l1 = {"Id": str(uuid.uuid4()), "name": name, "email": email,
              "contact": ph_no, "city": city, "pincode": pincode, "password": password}
        CustRegistrationCollection.insert_one(l1)
        return True


def ShopRegister(name, email, ph_no, city, pincode, password):
    shp_1 = {"email": email}
    r1 = ShopRegistrationCollection.find(shp_1)
    check = False
    for i in r1:
        if(email == i['email']):
            check = True
            break
    if(check):
        print("Email Address already exists")
        return False
    else:
        password = pbkdf2_sha256.hash(password)
        l2 = {"Id": str(uuid.uuid4()), "name": name, "email": email,
              "phone": ph_no,  "city": city, "pincode": pincode, "password": password}
        ShopRegistrationCollection.insert_one(l2)
        return True


def List_Shops(pin):
    li = ShopRegistrationCollection.find({"pincode": pin})


def ShopLogin(usrnme, password):
    li = {"username": usrnme}
    res = ShopRegistrationCollection.find(li)
    data = {}
    data['check'] = False
    for i in res:
        if(pbkdf2_sha256.verify(password, i['password'])):
            data['username'] = i['username']
            data['check'] = True
    print(data)
    return data


def CustLogin(email, password):
    li = {"email": email}
    res = CustRegistrationCollection.find(li)
    data = {}
    data['check'] = False
    for i in res:
        if(pbkdf2_sha256.verify(password, i['password'])):
            data['name'] = i['name']
            data['check'] = True
    print(data)
    return data


def Booking(name, days, ph_no, hours, persons):
    usr_1 = {"name": name}
    r1 = BookingCollection.find(usr_1)
    check = False
    for i in r1:
        if(name == i['name']):
            check = True
            break
    if(check):
        print("Booking exists ")
        return False
    else:
        l1 = {"Id": str(uuid.uuid4()), "name": name, "days": days,
              "contact": ph_no, "hours": hours, "persons": persons}
        BookingCollection.insert_one(l1)
        return True
