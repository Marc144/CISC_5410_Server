from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import pymongo

mongoURI = "mongodb://cosmosrgeastus84ace774-df7d-4274-88a1db:x1tIVM8HBIH5J8sF20oXD4vNYVLpUHuoPjLgqS31oQDBAvdQnIocM9yUBtmTJV3hxE8lmBXn5rNBACDbthcD2A==@cosmosrgeastus84ace774-df7d-4274-88a1db.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cosmosrgeastus84ace774-df7d-4274-88a1db@"

class messengerer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_headers('Content-type','application/json')
        self.end_headers()

    def do_POST(self):
        
        if self.path.endswith('/login'):
            self._set_headers()
            post_data = self.rfile.read('content_length')
            data = json.loads(post_data)
            client = pymongo.MongoClient(mongoURI)
            db = client['mydb']
            users = db['users']
            output = []
            try:
                output.append(users.find_one({'username':data['username'],'password':data['password']}))
            except:
                print('No user found')
            self.wfile.write(json.dumps(output))

        if self.path.endswith('/createAccount'):
            self._set_headers()
            post_data = self.rfile.read('content_length')
            data = json.loads(post_data)
            client = pymongo.MongoClient(mongoURI)
            db = client['mydb']
            users = db['users']
            output = {}
            try:
                checkUser = output.append(users.find_one({'username':data['username'],'password':data['password']}))
                if checkUser != {}:
                    users.insert_one(data)
            except:
                print('Account creation failed')

        if self.path.endswith('/getChats'):
            self._set_headers()
            post_data = self.rfile.read('content_length')
            data = json.loads(post_data)
            client = pymongo.MongoClient(mongoURI)
            db = client['mydb']
            chats = db["chats"]
            output = []
            try:
                results = chats.find({"$or": [{'participant1':data['participant1']},{"participant2": data['participant2']}]})
                for i in results:
                    output.append(i)
            except:
                print('No messages found')
            self.wfile.write(json.dumps(output))

        if self.path.endswith('/getAllMessages'):
            self._set_headers()
            post_data = self.rfile.read('content_length')
            data = json.loads(post_data)
            client = pymongo.MongoClient(mongoURI)
            db = client['mydb']
            messages = db['messages']
            output = []
            try:
                results = messages.find({"$and" : [{"sender" : {"$or" : [data['sender'],data['recipient']]}} , {"recipient" : {"$or" : [data['sender'], data['recipient']]}}]}).sort['time']
                for i in results:
                    output.append(i)
            except:
                print('No messages found')
            self.wfile.write(json.dumps(output))

        if self.path.endswith('/sendMessage'):
            self._set_headers()
            post_data = self.rfile.read('content_length')
            data = json.loads(post_data)
            client = pymongo.MongoClient(mongoURI)
            db = client['mydb']
            messages = db['messages']
            try:
                messages.insert_one(data)
            except:
                print('message failed')

        if self.path.endswith('/newChat'):
            self._set_headers()
            post_data = self.rfile.read('content_length')
            data = json.loads(post_data)
            client = pymongo.MongoClient(mongoURI)
            db = client['mydb']
            chats = db['chats']
            try:
                chats.insert_one(data)
            except:
                print('chat creation failed')
            

def run(server_class=HTTPServer,handler_class=messengerer,port=""):
    server_address = ('',port)
    httpd = server_class(server_address,handler_class)
    print("Starting server on port " + port)
    httpd.serve_forever()

if __name__ == "__main__":
    run()