from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import pymongo

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
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            db = client['mydb']
            users = db.users
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
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            db = client['mydb']
            users = db.users
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
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            db = client['mydb']
            chats = db.chats
            output = []
            try:
                output.append(chats.find({'member':data['user']}))
            except:
                print('No messages found')
            self.wfile.write(json.dumps(output))

        if self.path.endswith('/getMessages'):
            self._set_headers()
            post_data = self.rfile.read('content_length')
            data = json.loads(post_data)
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            db = client['mydb']
            messages = db.messages
            output = []
            try:
                output.append(messages.find({'sender':data['sender'],'recipient':data['recipient']}))
                output.append(messages.find({'sender':data['recipient'],'recipient':data['sender']}))
            except:
                print('No messages found')
            self.wfile.write(json.dumps(output))

        if self.path.endswith('/sendMessage'):
            self._set_headers()
            post_data = self.rfile.read('content_length')
            data = json.loads(post_data)
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            db = client['mydb']
            messages = db.messages
            try:
                messages.insert_one(data)
            except:
                print('message failed')
            

def run(server_class=HTTPServer,handler_class=messengerer,port=""):
    server_address = ('',port)
    httpd = server_class(server_address,handler_class)
    print("Starting server on port " + port)
    httpd.serve_forever()

if __name__ == "__main__":
    run()