import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        uname = req_body.get("username")
        password = req_body.get("password")
        print (uname.upper())
        print (password)
        if (uname.upper() == 'ADFLAB' and password == 'Password.1!'):
            response = json.dumps({"token" : "Ei9QUGYtgHY60xmGLQhmVnOnI1STqMZphxMlGT6pQgD8AzFuUqc89A=="})
            return func.HttpResponse(
                response,
                mimetype="application/json",        
                status_code=200)
        else:
            return func.HttpResponse("Invalid Username or Password", status_code=401)
             
            
    except ValueError:
        return func.HttpResponse(
             "Please pass a username (username) and password (password) in the request body",
             status_code=400
        )
    
