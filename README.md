# update-from-git
A Python App, hosted on a Docker Image for listening to, and then pulling from, a git repository.

## The Process

The process is quite simple. It will listen to a URL for a particular `POST` request, and when activated will pull from a given `git` repository on to the docker image which is then persisted to the host machine using volumes.

## Compiling from Local PC

1. Clone the Repo:
    ```bash
    git clone https://github.com/chrimaho/update-from-git.git
    ```
1. Navigate to location:
    ```bash
    cd .../update-from-git
    ```
2. Compile the `docker-compose.yml` file:
   1. Sample file: [./docker/docker-compose-sample.yml](./docker/docker-compose-sample.yml)
   2. Text:
        ```yml
        version: "3.8"
        services:
            listener:
                image: chrimaho/update-from-git
                build:
                    context: ../
                    dockerfile: docker/uvicorn.Dockerfile
                container_name: listener
                environment:
                    - GIT_URL=https://github.com/chrimaho/code-snippets.git
                    - REPO_DIR=repo
                    - VERSION=0.0.1
                    - TITLE=Update from Git
                    - DESCRIPTION=Automated update process for pulling from Git repo upon webhook call.
                    - CONTACT_NAME=Chris Mahoney
                    - CONTACT_URL=https://www.chrimaho.com
                    - CONTACT_EMAIL=chrimaho@chrimaho.com
                volumes:
                    - ../repo:/app/repo
                ports:
                    - 8880:8880
        ```
3. Run the Image:
    ```bash
    docker compose --file ./docker/docker-compose.yml up --detach --build --force-recreate
    ```

## Compile from Container Repository

The main difference from the above version is in the `docker-compose.yml` file, to replace the `build` tag with the `image` tag.

1. Make new directory
    ```bash
    mkdir new-application
    ```
1. Navigate to the directory
    ```bash
    cd new-application
    ```
2. Compile the `docker-compose.yml` file:
   1. Sample file: [./docker/docker-compose-sample.yml](./docker/docker-compose-sample.yml)
   2. Text:
        ```yml
        version: "3.8"
        services:
            listener:
                image: chrimaho/update-from-git
                container_name: listener
                environment:
                    - GIT_URL=https://github.com/chrimaho/code-snippets.git
                    - API_ENDPOINT=/api/webhook
                    - REPO_DIR=repo
                    - VERSION=0.0.1
                    - TITLE=Update from Git
                    - DESCRIPTION=Automated update process for pulling from Git repo upon webhook call.
                    - CONTACT_NAME=Chris Mahoney
                    - CONTACT_URL=https://www.chrimaho.com
                    - CONTACT_EMAIL=chrimaho@chrimaho.com
                volumes:
                    - ../repo:/app/repo
                ports:
                    - 8880:8880
        ```
3. Run the Image:
    ```bash
    docker compose --file ./docker/docker-compose.yml up --detach --build --force-recreate
    ```

## Explanation on the Environment Variables

|        | Variable        | Description                                      | Mandatory | Default                                                                 |
|--------|-----------------|--------------------------------------------------|-----------|-------------------------------------------------------------------------|
| **1.** | `GIT_URL`       | The URL from which the Repo will be cloned       | Yes       |                                                                         |
| **2.** | `API_ENDPOINT`  | The Endpoint which will be called by the Webhook | No        | `/api/webhook`                                                          |
| **3.** | `REPO_DIR`      | The DIR to which the Repo will be cloned         | Yes       |                                                                         |
| **4.** | `VERSION`       | The version number for the app                   | No        | `0.0.1`                                                                 |
| **5.** | `TITLE`         | The title of the app                             | No        | `Update from Git`                                                       |
| **6.** | `DESCRIPTION`   | The description of the app                       | No        | `Automated update process for pulling from Git repo upon webhook call.` |
| **7.** | `CONTACT_NAME`  | The name of the person to contact about the app  | No        | `None`                                                                  |
| **8.** | `CONTACT_URL`   | The website for the contact person               | No        | `None`                                                                  |
| **9.** | `CONTACT_EMAIL` | The email for the contact person                 | No        | `None`                                                                  |

## Contact Details

|        | Method  | Detail                                                |
|--------|---------|-------------------------------------------------------|
| **1.** | Name    | Chris Mahoney                                         |
| **2.** | Website | [www.chrimaho.com](www.chrimaho.com)                  |
| **3.** | Email   | [chrimaho@chrimaho.com](mailto:chrimaho@chrimaho.com) |
