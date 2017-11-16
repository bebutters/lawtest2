"""
This script runs the application using a development server.
"""

import bottle
import os
import sys

import uuid
import timeit
import datetime

import DBController
import stopgap
import RawTestData.DBBuilder as DBBuilder

# routes contains the HTTP handlers for our server and must be imported.
#import routes

if '--debug' in sys.argv[1:] or 'SERVER_DEBUG' in os.environ:
    # Debug mode will enable more verbose output in the console window.
    # It must be set at the beginning of the script.
    bottle.debug(True)

def wsgi_app():
    """Returns the application to make available through wfastcgi. This is used
    when the site is published to Microsoft Azure."""
    return bottle.default_app()

if __name__ == '__main__':
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    @bottle.route('/static/<filepath:path>')
    def server_static(filepath):
        """Handler for static files, used with the development server.
        When running under a production server such as IIS or Apache,
        the server should be configured to serve the static files."""
        return bottle.static_file(filepath, root=STATIC_ROOT)

    # Starts a local test server.
    bottle.run(server='wsgiref', host=HOST, port=PORT)

@bottle.route('/')
def hello():
    try:
        GUID = uuid.uuid4()
        DBController.AddCookie(GUID, unicode("NSW"))
        bottle.response.set_cookie("access", str(GUID), max_age = 28800) #Domain
        return(stopgap.a)
    except Exception as e:
         return(e)

@bottle.post("/Lawyer")
def Lawyer():
    if bottle.request.get_cookie("access"):
        State = DBController.CheckCookie(uuid.UUID(hex = bottle.request.get_cookie("access")))
        if State:
            bottle.response.headers["Content-Type"] = "application/json"
            FirstName = Wildify(bottle.request.forms.get("FirstName"))
            LastName = Wildify(bottle.request.forms.get("LastName"))
            PostCode = Wildify(bottle.request.forms.get("PostCode"))
            Specialty = Wildify(bottle.request.forms.get("Specialty"))
            Language = bottle.request.forms.get("Language")
            return(DBController.QueryLawyer(FirstName, LastName, PostCode, Language, State))
    return({"error": "Sorry you are not authorised to access this data. Please try a page refresh"})

@bottle.post("/Firm")
def Firm():
    if bottle.request.get_cookie("access"):
        State = DBController.CheckCookie(uuid.UUID(hex = bottle.request.get_cookie("access")))
        if State:
            bottle.response.headers["Content-Type"] = "application/json"
            Name = Wildify(bottle.request.forms.get("Name"))
            PostCode = Wildify(bottle.request.forms.get("PostCode"))
            Language = bottle.request.forms.get("Language")
            return(DBController.QueryFirm(Name, PostCode, Language, State))
    return({"error": "Sorry you are not authorised to access this data. Please try a page refresh"})   

@bottle.route('/Build/Test')
def BuildTest():
    DBController.Build(0)

@bottle.route('/Build/Performance')
def BuildPerformance():
    DBBuilder.Build(1)

@bottle.route('/Performance/Test')
def Test():
    stime = datetime.datetime.now()
    res = DBController.QueryFirm('g%', '%', "hindi", 'NSW')
    ftime = datetime.datetime.now()
    print(ftime - stime)
    return(res)

@bottle.route('/AddCookie')
def AddCookie():
    cookie = bottle.request.query["cookie"]
    state = bottle.request.query["state"]
    print(cookie)
    DBController.AddCookie(cookie, state)

