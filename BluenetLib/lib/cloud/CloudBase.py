import hashlib
import requests

from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.topics.SystemCloudTopics import SystemCloudTopics
from BluenetLib.lib.util.JsonFileStore import JsonFileStore


class CloudBase:
    email = None
    password = None
    sha1Password = None
    accessToken = None
    
    userId = None
    
    initialized = False
    
    def __init__(self):
        pass
    
    
    def loadConfigFromFile(self, path):
        fileReader = JsonFileStore(path)
        data = fileReader.getData()

        self.email = None
        self.password = None
        self.sha1Password = None
        self.accessToken = None
        self.userId = False
        self.initialized = False
        
        if "email" in data:
            if data["email"] != "":
               self.email = data["email"]
        
        if "password" in data:
            if data["password"] != "":
                self.password = data["password"]
                
        if "sha1Password" in data:
            if data["sha1Password"] != "":
                self.sha1Password = data["sha1Password"]
                
        if "accessToken" in data:
            if data["accessToken"] != "":
                self.accessToken = data["accessToken"]
        
        
        if self.accessToken is not None:
            self.initialized = True
            return
        
        
        if self.email is None:
            print("Config requires either email or accesstoken fields.")
            return
        
        
        if self.password is None and self.sha1Password is None:
            print("Config requires either password or sha1Password fields to use with the provided email address.")
            return
        
        if self.password is not None and self.sha1Password is None:
            print("self.password", self.password)
            self.sha1Password = hashlib.sha1(self.password.encode('utf-8')).hexdigest()
        
        self.logIn()
        self.initialized = True
        
        
    def logIn(self):
        r = requests.post('https://my.crownstone.rocks/api/users/login', data={"email": self.email, "password": self.sha1Password})
        
        if r.status_code == 200:
            reply = r.json()
            if "id" in reply:
                self.accessToken = reply['id']
    
            if "userId" in reply:
                self.userId = reply['userId']
                
            print("Got Tokens!")
        else:
            print(r.text)
            print("Could not get AccessToken")


    def getSpheres(self):
        r = requests.get(
            'https://my.crownstone.rocks/api/users/' + self.userId + '/spheres?access_token=' + self.accessToken)
        spheres = []
    
        if r.status_code == 200:
            reply = r.json()
        
            for sphere in reply:
                spheres.append({"id": sphere["id"], "name": sphere["name"]})
        else:
            print(r.text)
            print("Could not get Spheres")
    
        return spheres
    
    
    
            
    
    


            
    
    

    





       