# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#!/usr/bin/env python3

import jwt
import uuid
import datetime
import json
import sys
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

app_access_key = 'o3292djknqwnf32oiwckm'
app_secret = 'erknjefeilmlweknjlma'



  

class TokenGenerator:
    def generateManagementToken(self):
        expires = 24 * 3600
        now = datetime.datetime.utcnow()
        exp = now + datetime.timedelta(seconds=expires)
        return jwt.encode(payload={
            'access_key': app_access_key,
            'type': 'management',
            'version': 2,
            'jti': str(uuid.uuid4()),
            'iat': now,
            'exp': exp,
            'nbf': now
            }, key=app_secret)
    def generateAccessToken(self,room_id, user_id, role):
         expires = 24 * 3600
         now = datetime.datetime.utcnow()
         exp  = now+ datetime.timedelta(seconds=expires)
         return jwt.encode(payload={
                    "access_key": app_access_key,
                    "type":"app",
                    "version":2,
                    "room_id": room_id,
                    "user_id": user_id,
                    "role":role,
                    "jti": str(uuid.uuid4()),
                    "exp": exp,
                    "iat": now,
                    "nbf": now,
                    }, key=app_secret)
         if len(sys.argv) == 3:
             room_id = sys.argv[0]
             user_id = sys.argv[1]
             role = sys.argv[2]

        
class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        
        if self.path.endswith('/getManagementToken'):
            tokenGen = TokenGenerator()
            managementToken = tokenGen.generateManagementToken()
       
            response = {
                 "token": str(managementToken)
            }
            jsonResponse = json.dumps(response)
            
            self.send_response(200)
            self.send_header("content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(jsonResponse ,"utf-8"))
       
    def do_POST(self):
        #TODO implement
      
        # process request body
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
        
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        
        room_id = message['room_id']
        user_id = message['user_id']
        role = message['role']
       
        
        # send the appropriate response
        tokenGen = TokenGenerator()
        accessToken = tokenGen.generateAccessToken(room_id, user_id, role)
       
        response = {
            "token": str(accessToken)
        }
        
        jsonResponse = json.dumps(response)
        
        
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(jsonResponse ,"utf-8"))

         
# add get token access



if __name__ == '__main__':
     
    server = HTTPServer((HOST, PORT), HTTPHandler)
    print("Server started on port " + str(PORT))
    server.serve_forever()
   
    server.server_close()
    print(" Server stopped!")
    
