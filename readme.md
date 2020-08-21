## Requriements
- python 3.7.2
- sqlite3 (included in python3)
- pandas 0.25.1
- flask 1.1.1

## Config
1. use **config.py.example** file
2. change the name as **config.py**
3. open the file and edit below entries
- you can generate api token from [Atlassian account->security menu](https://id.atlassian.com/manage-profile/security/api-tokens)
```
emailAccount = "-----@ratehub.ca"
apiToken = "-----"
```

## Setup the initial database
1. Run **initDB.py** to initialize database
2. It may take 20~30 minutes
```
python /path/to/initDB.py
```

## Update after first setup of database
1. If you just run **initDB.py**, you don't need this step
2. use this only when you need to update the existing database
2. run **updateDB.py**
3. It may take 15-20 minutes
```
python /path/to/updateDB.py
```

## Run Flask Server
1. run **server.py**


