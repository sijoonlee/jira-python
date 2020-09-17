## Requriements
- python 3.7.2
- pandas 0.25.1
- flask 1.1.1
- flask_restful 0.3.7
- flask_cors 3.0.8
- database: PostgreSQL or Amazon Redshift

## Config
1. use **config.py.example** file
2. change the name as **config.py**
3. open the file and edit below entries
- you can generate api token from [Atlassian account->security menu](https://id.atlassian.com/manage-profile/security/api-tokens)
```
emailAccount = "-----@ratehub.ca"
apiToken = "-----"
```

## How to use
1. run **updateDB.py**
2. It may take less than 5 minutes if you are using local Postgres database
    - if you want to use and don't have local PostgreSQL database yet, see the next section
```
python /path/to/updateDB.py
```

## Using Local PostgreSQL database from Docker image
1. Knowing how to use 'docker-compose' is assumed here in this section
2. go to directory db/postgres, and modify docker-compose.yml
    - DB_DIR should be modified, please use your own directory path
    ```
    volumes:
        - DB_DIR:/use/your/own/directory/path/here
    ```
3. run command 'docker-compose up'

## Configure Database access
1. modify the file, 'config.py.example'
    - username, password, port and so on
2. **change the file name as 'config.py'**
    - this is important, otherwise program will crash

