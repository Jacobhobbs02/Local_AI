steps for local ai

You can use an device for this (PC, raspberry pi, etc)

STEP #1: Starting out

Main link: https://ollama.com/

Documentation: https://docs.ollama.com/

Download: https://ollama.com/download

Download Ubuntu Linux Server: https://ubuntu.com/download/server

Install Linux onto computer.


Step 2: Hardware


1. Give you device a static IP

2. Open up terminal in device and run following command:
curl -fsSL https://ollama.com/install.sh | sh

3. Once that goes through, you will need to pull the model you want, for example:
ollama pull codeqwen:latest


4. Then to test you will need to run your model in the CLI:
ollama run codeqwen


Once it works, you'll need to edit some files

5. Run this command:
sudo systemctl edit ollama


6. Delete all the code in there and post this: 
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"


7. then run these commands: 
sudo systemctl daemon-reload
sudo systemctl restart ollama

8. Verify it by running this command: sudo ss -ltnp | grep 11434


Step 3: Setting up the MySQL server

sudo apt update && sudo apt upgrade -y

2. sudo apt install mysql-server

3. sudo systemctl status MySQL

4. sudo MySQL

5. Post this command: 

CREATE DATABASE IF NOT EXISTS ai_app;
USE ai_app;

-- 1. Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Groups table
CREATE TABLE `groups` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    group_number INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    user_id INT NOT NULL,

    CONSTRAINT fk_groups_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    UNIQUE KEY unique_user_group_number (user_id, group_number)
) ENGINE=InnoDB;

-- 3. Conversations table
CREATE TABLE conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    user_id INT NOT NULL,
    group_id INT NOT NULL,

    CONSTRAINT fk_conversations_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_conversations_group
        FOREIGN KEY (group_id)
        REFERENCES `groups`(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;


6. then run this command:

CREATE DATABASE IF NOT EXISTS ai_app;

CREATE USER IF NOT EXISTS 'admin'@'localhost'
IDENTIFIED BY 'password';

GRANT ALL PRIVILEGES ON ai_app.*
TO 'admin'@'localhost';


The admin and password made here will go into the mysqlconnection.py file


Step 4: App Configuration

Local AI GitHub Code: https://github.com/Jacobhobbs02/Local_AI


THIS NEXT STEP IS FOR GMAILS (if you use a different email you should just be able to use your email's password)


1. Log into google account and to Manage your Google Account

2. search for App Passwords and make a new app password for the app.

3. Once you have that password, post it in the areas of the code that ask for APP_PASSWORD and post your email everywhere it says EMAIL which should only be these two files:

controllers/users.py 
__init__.py

4. Once all the code has been completed you need to install the dependencies in the requirements.txt. 


5. Once everything is installed run this command:
pipenv run python server.py

6. Once the page appears, you'll need to register an account, it will send you an email and you will then make a password, after password has been made log in and it should connect you to the ai.




