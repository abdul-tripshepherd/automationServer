from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import seleniumScripts.blogLinksChecker as linkAutomation

app = Flask(__name__)
scheduler = BackgroundScheduler()

def run_automation():
    print("Running automation")
    link_checker = linkAutomation.LinkChecker()
    link_checker.check_links()

scheduler.add_job(run_automation, 'cron', day_of_week='mon-sun', hour=17, minute=47)

if __name__ == '__main__':
    scheduler.start()
    app.run()