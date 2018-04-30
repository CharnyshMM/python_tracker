import json

class FileIO:
    def __init__(self):
        self.file_name = "tasks_storage.txt"

    def readString(self):
        contents = ""
        with open(self.file_name,"r") as file:
            contents = file.read()
        return contents

    def writeString(self, string):
        with open(self.file_name,"w") as file:
            file.write(string)

    def getJsonDict(self):
        contents = self.readString()
        return json.loads(contents)

    def writeJsonDict(self, j_dict):
        self.writeString(json.JSONEncoder().encode(j_dict))

