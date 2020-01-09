![Python - 3.6 | 3.7](https://img.shields.io/badge/Python-3.6%20%7C%203.7-blue)

Uni Bot
=======
Discord Bot ( Music, Manager, Anti Chat,  . . .)

# Project setup
- Python 3.5.3 or higher is required
- pipenv

0. install & Run
    - Create Virtual Environment
    -
       ```shell script
       git clone https://github.com/TeamUni-Dev/UniBot.git
       cd UniBot/
       pip3 install pipenv
       pipenv install -r requirements.txt
       pipenv shell
       ```
     - Create config.json
     -
       ```shell script
       vi config.json
       ```
       - config.json
           ```json
           {
             "token": "<Token>",
             "prefix": "<command prefix>",
             "owner": "<owner>"
           }
           ```
     - run
     -
        ```shell script
        Python3 start.py
        ```