from config import config
method = "GET"
url = config["agileApiAddress"] + "board/{boardId}/sprint/{sprintId}/issue?maxResults={maxResults}&startAt={startAt}"
