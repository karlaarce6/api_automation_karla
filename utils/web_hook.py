import pymsteams

from config.config import web_hook

teams_message = pymsteams.connectorcard(web_hook)

with open("C:/Users/Karla.Arce/PycharmProjects/JiraAPI/reports/markdown/md_report.md") as f:
    report = f.read()
teams_message.text(report)
teams_message.send()
