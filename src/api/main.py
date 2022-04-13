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
from ctypes import Union
import os, sys
from fastapi import FastAPI, Query
from fastapi.responses import *
from git import Repo
import shutil
from decouple import config


# Compile Variables ----
GIT_URL = config('GIT_URL', cast=str)
REPO_DIR = config('REPO_DIR', cast=str)
VERSION = config('VERSION', default='0.0.1', cast=str)
TITLE = config('TITLE', default='Update from Git', cast=str)
DESCRIPTION = config('DESCRIPTION', default='Automated update process for pulling from Git repo upon webhook call.', cast=str)
CONTACT_NAME = config('CONTACT_NAME', default=None)
CONTACT_URL = config('CONTACT_URL', default=None)
CONTACT_EMAIL = config('CONTACT_EMAIL', default=None)
CONTACT = {}
if CONTACT_NAME: CONTACT["name"] = CONTACT_NAME
if CONTACT_URL: CONTACT["url"] = CONTACT_URL
if CONTACT_EMAIL: CONTACT["email"] = CONTACT_EMAIL
print(CONTACT)
print(CONTACT_NAME)
print(CONTACT_URL)
print(CONTACT_EMAIL)


# Instantiations ----
app = FastAPI \
    ( title=TITLE
    , description=DESCRIPTION
    , version=VERSION
    , openapi_tags=\
        [ {"name":"App Info", "description":"Information about the App"}
        , {"name":"Main Process", "description":"The main Endpoints for th App"}
        ]
    , contact=CONTACT
    , docs_url="/swagger"
    , root_path_in_servers=False
    )



#------------------------------------------------------------------------------#
# Endpoints                                                                 ####
#------------------------------------------------------------------------------#


@app.get \
    ( path="/api/health"
    , summary="Health check"
    , description="Check to ensure that the app is healthy and ready to run."
    , tags=["App Info"]
    )
def root():
    return PlainTextResponse("App is ready to go.", status_code=200)


@app.post \
    ( "/api/clone_repo"
    , summary="Clone Repo"
    , description=f"Clone repo from: `{os.environ['GIT_URL']}`<br><br>And save to: `{os.environ['REPO_DIR']}`"
    , tags=["Main Process"]
    )
def clone_repo \
    ( git_url:str=Query(..., example=os.environ["GIT_URL"], title="Git URL", description="The URL from which the Repo will be cloned")
    , repo_dir:str=Query(..., example=os.environ["REPO_DIR"], title="Repo Dir", description="The DIR to which the Repo will be cloned", )
    ):
    try:
        if os.path.exists(repo_dir):
            shutil.rmtree(repo_dir, ignore_errors=True)
        Repo.clone_from \
            ( git_url
            , repo_dir
            )
    except:
        e = sys.exc_info()
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
            ( { "Success": git_url
              }
            , status_code=200
            )
