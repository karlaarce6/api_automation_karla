### Add Worklog
```shell
curl -X POST "https://jira-jaggaer.atlassian.net/rest/api/3/issue/$ticketid/worklog" -u "karce@jaggaer.com:$token" -H "Accept: application/json" -H "Content-Type: application/json" --data '{"started": "2025-06-04T13:30:00.000-0400", "timeSpent": "1h"}'
```
![image](https://github.com/user-attachments/assets/5db5c91b-3ed8-483b-b815-31455ef0597d)

### Get Worklog
```shell
curl -X GET "https://jira-jaggaer.atlassian.net/rest/api/3/issue/$ticketid/worklog/$worklogid" -u "karce@jaggaer.com:$token" -H "Accept: application/json"
```
![image](https://github.com/user-attachments/assets/a82afe5a-0d48-4a58-873d-8b96a0585d4e)

### Update Worklog
```shell
curl -X PUT "https://jira-jaggaer.atlassian.net/rest/api/3/issue/$ticketid/worklog/$worklogid" -u "karce@jaggaer.com:$token" -H "Accept: application/json" -H "Content-Type: application/json" --data '{"started": "2025-06-04T13:30:00.000-0400", "timeSpent": "2h"}'
```
![image](https://github.com/user-attachments/assets/302106f3-7bbc-45e0-95f0-36b7f0a3f88d)

### Delete Worklog
```shell
curl -X DELETE "https://jira-jaggaer.atlassian.net/rest/api/3/issue/$ticketid/worklog/$worklogid" -u "karce@jaggaer.com:$token"
```
![image](https://github.com/user-attachments/assets/5b8a09c2-b1a8-4688-9326-23a7e5fbc901)

### Negative tests:
Wrong ticket ID at adding a worklog:
```shell
curl -X POST "https://jira-jaggaer.atlassian.net/rest/api/3/issue/123/worklog" -u "karce@jaggaer.com:$token" -H "Accept: application/json" -H "Content-Type: application/json" --data '{"started": "2025-06-04T13:30:00.000-0400", "timeSpent": "1h"}'
```
![image](https://github.com/user-attachments/assets/b7aca13c-3aca-4baa-b8c0-edb6c3230547)

Incorrect body parameter "timeSpents":
```shell
curl -X POST "https://jira-jaggaer.atlassian.net/rest/api/3/issue/$ticketid/worklog" -u "karce@jaggaer.com:$token" -H "Accept: application/json" -H "Content-Type: application/json" --data '{"started": "2025-06-04T13:30:00.000-0400", "timeSpents": "1h"}'
```
![image](https://github.com/user-attachments/assets/7683e43f-078d-439d-a2f2-5890017d6df2)

Incorrect API token:
```shell
curl -X POST "https://jira-jaggaer.atlassian.net/rest/api/3/issue/$ticketid/worklog" -u "karce@jaggaer.com:123" -H "Accept: application/json" -H "Content-Type: application/json" --data '{"started": "2025-06-04T13:30:00.000-0400", "timeSpent": "1h"}'
```
![image](https://github.com/user-attachments/assets/8e24f140-9f8b-4054-b341-bb520cf72319)

Wrong worklog ID at getting worklog:
```shell
curl -X GET "https://jira-jaggaer.atlassian.net/rest/api/3/issue/$ticketid/worklog/123" -u "karce@jaggaer.com:$token" -H "Accept: application/json"
```
![image](https://github.com/user-attachments/assets/ca73a0cd-a0af-45f6-a24b-6e04b68e5fca)

Unnecessary comma in the body of the request:
```shell
curl -X PUT "https://jira-jaggaer.atlassian.net/rest/api/3/issue/$ticketid/worklog/$worklogid" -u "karce@jaggaer.com:$token" -H "Accept: application/json" -H "Content-Type: application/json" --data '{"started": "2025-06-04T13:30:00.000-0400", "timeSpent": "2h",}'
```
![image](https://github.com/user-attachments/assets/6b8eece2-5d21-459a-83ee-f69d17e0ab4e)
