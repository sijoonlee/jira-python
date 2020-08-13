from config import config
method = "GET"
url = config["agileApiAddress"] + "board?maxResults={maxResults}&startAt={startAt}"