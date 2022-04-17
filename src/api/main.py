#==============================================================================#
#                                                                              #
#    Title: Update from Git                                                    #
#    Purpose: Automated process for keeping local Dir updated when             #
#             there is a WebHook call against it. This is useful when          #
#             configuring a WebHook call on GitHub or GitLab or similar Repo.  #
#    Author: chrimaho                                                          #
#    Created: 13/Apr/2022                                                      #
#                                                                              #
#==============================================================================#



#------------------------------------------------------------------------------#
# Setup                                                                     ####
#------------------------------------------------------------------------------#


# Library Imports ----
from sys import exc_info
from os.path import exists
from pydantic import BaseModel
from decouple import config
from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse
from git import Repo
from shutil import rmtree


# Compile Variables ----
TITLE = config(option='TITLE', default='Update from Git', cast=str)
DESCRIPTION = config \
    ( option='DESCRIPTION'
    , default='Automated update process for pulling from Git repo upon webhook call.'
    , cast=str
    )
VERSION = config(option='VERSION', default='0.0.1', cast=str)
GIT_URL = config(option='GIT_URL', cast=str)
API_ENDPOINT = config(option="API_ENDPOINT", cast=str, default="/api/webhook")
REPO_DIR = config(option='REPO_DIR', cast=str)
CONTACT_DETAILS = \
    { "name": config(option='CONTACT_NAME', default=None)
    , "url": config(option='CONTACT_URL', default=None)
    , "email": config(option='CONTACT_EMAIL', default=None)
    }


# Landing Page ----
with open("./templates/landing_page.html") as file:
    LANDING_PAGE = file.read() \
        .format \
            ( TITLE = TITLE
            , DESCRIPTION = DESCRIPTION
            , VERSION = VERSION
            , GIT_URL = GIT_URL
            , API_ENDPOINT = API_ENDPOINT
            , REPO_DIR = REPO_DIR
            , CONTACT_NAME = CONTACT_DETAILS["name"]
            , CONTACT_EMAIL = CONTACT_DETAILS["email"]
            , CONTACT_URL = CONTACT_DETAILS["url"]
            )


# Instantiate App ----
app = FastAPI \
    ( title=TITLE
    , description=DESCRIPTION
    , version=VERSION
    , openapi_tags=\
        [ {"name":"App Info", "description":"Information about the App"}
        , {"name":"Main Process", "description":"The main Endpoints for th App"}
        ]
    , contact=CONTACT_DETAILS
    , docs_url="/swagger"
    , root_path_in_servers=False
    )



#------------------------------------------------------------------------------#
# Functions                                                                 ####
#------------------------------------------------------------------------------#


# Remove all files within a diretory ----
def remove_dir(dir:str) -> None:
    if exists(dir):
        rmtree(dir, ignore_errors=True)
    return None



#------------------------------------------------------------------------------#
# Models                                                                    ####
#------------------------------------------------------------------------------#

# Successful response: status_code=200 ----
class Success(BaseModel):
    Success:str="Response Text"

# Validation Error: status_code=422 ----
class ValidationError(BaseModel):
    Message:str="Details about the validation error"

# Server Error: status_code=500 ----
class InternalServerError(BaseModel):
    Failed:str="The function or URL which was tried"
    Error:str="Name of the error"
    Doc:str="Documentation about the error"
    Message:str="The error message itself"


#------------------------------------------------------------------------------#
# Endpoints                                                                 ####
#------------------------------------------------------------------------------#


# Landing Page ----
@app.get \
    ( path="/"
    , summary="Landing page"
    , description="The landing page for the application"
    , tags=["App Info"]
    , response_class=HTMLResponse
    , responses= \
        { 200: {"content": {"text/html": {"schema": None}}}
        }
    )
def root():
    return HTMLResponse \
        ( content=LANDING_PAGE
        , status_code=200
        , media_type="text/html"
        )


# Health Check ----
@app.get \
    ( path="/api/health"
    , summary="Health check"
    , description="Check to ensure that the app is healthy and ready to run."
    , tags=["App Info"]
    , response_class=HTMLResponse
    , responses= \
        { 200: {"content": {"text/html": {"schema": None}}}
        }
    )
def health():
    return PlainTextResponse \
        ( "App is ready to go."
        , status_code=200
        , media_type="text/plain"
        )


# Main Endpoint ----
@app.post \
    ( path=API_ENDPOINT
    , summary="API Endpoint for Git to Call"
    , description= \
        "Basically, it will:<br><br>" +
        f"1. `clone`/`pull` repo from: `{GIT_URL}`<br><br>" +
        f"2. Save repo to: `{REPO_DIR}`"
    , tags=["Main Process"]
    , response_class=JSONResponse
    , responses= \
        { 200: {"model": Success}
        , 422: {"model": ValidationError, "description": "Validation Error"}
        , 500: {"model": InternalServerError}
        }
    )
def api_endpoint \
    ( git_url:str=Query \
        ( ...
        , example=GIT_URL
        , title="Git URL"
        , description= \
            "The URL from which the Repo will be cloned.<br>" +
            "This is set from the Environment (`.env`) variables."
        )
    , repo_dir:str=Query \
        ( ...
        , example=REPO_DIR
        , title="Repo Dir"
        , description= \
            "The DIR to which the Repo will be cloned.<br>" +
            "This is set from the Environment (`.env`) variables."
        )
    ):
    try:
        remove_dir(repo_dir)
        Repo.clone_from(git_url, repo_dir)
    except:
        e = exc_info()
        return JSONResponse \
            ( { "Failed": f"{git_url}"
              , "Error": f"{e[0].__name__}"
              , "Doc": f"{e[0].__doc__}"
              , "Message": f"{e[1]}"
              }
            , status_code=500
            )
    else:
        return JSONResponse \
            ( {"Success": git_url}
            , status_code=200
            )
