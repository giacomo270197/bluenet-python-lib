import json


class JsonFileStore:
    memoryStore = {}
    filename = None
    
    
    def __init__(self, filename):
        self.filename = filename
        self._loadData()
    
    
    def _loadData(self):
        fileHandle = open(self.filename,'r')
        data = fileHandle.read()
        self.memoryStore = json.loads(data)
        fileHandle.close()
        
    
    def addEntry(self, key, value):
        self.memoryStore[key] = value
        self._persist()


    def updateEntry(self, key, value):
        self.addEntry(key, value)


    def removeEntry(self, key):
        del self.memoryStore[key]
     
     
    def _persist(self):
        jsonString = json.dumps(self.memoryStore)
        
        fileHandle = open(self.filename, 'w')
        fileHandle.write(jsonString)
        fileHandle.close()
        
    
    def clear(self):
        fileHandle = open(self.filename, 'w')
        fileHandle.write("")
        fileHandle.close()
        self.memoryStore = {}
    