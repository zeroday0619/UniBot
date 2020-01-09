![Python - 3.6 | 3.7](https://img.shields.io/badge/Python-3.6%20%7C%203.7-blue)

Uni Bot
=======
Discord Bot ( Music, Manager, Anti Chat,  . . .)

# Project setup
- Python 3.5.3 or higher is required
- pipenv

## install & Run
 0. Create Virtual Environment
    ```shell script
       $ git clone https://github.com/TeamUni-Dev/UniBot.git
       $ cd UniBot/
       $ pip3 install pipenv
       $ pipenv install -r requirements.txt
       $ pipenv shell
    ```
2. Create config.json
   ```shell script
   $ vi config.json
   ```
   ```json
   {
     "token": "<Token>",
     "prefix": "<command prefix>",
     "owner": "<owner>"
   }
   ```
3. run
    ```shell script
    Python3 start.py
    ```