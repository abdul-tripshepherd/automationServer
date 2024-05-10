from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
import seleniumScripts.blogLinksChecker as linkAutomation
import triggerScripts.new_blog as newBlogCheck
import subprocess
import time
import json

app = Flask(__name__)
scheduler = BackgroundScheduler()

time.sleep(5)

ngrok_command = "ngrok http --domain=crucial-penguin-secretly.ngrok-free.app 5000"
# ngrok_process = subprocess.Popen(ngrok_command.split())

@app.route('/automation/new_blog', methods=['POST'])
def new_blog_event():
    data = request.json
    timestamp = int(time.time())
    filename = f"blog_payload_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(data)
    newBlogCheck.CanonicalVerifier().check_link(data['event']['data']['new']['canonical'])

@app.route('/automation/new_product', methods=['POST'])
def new_product_event():
    data = request.json
    timestamp = int(time.time())
    filename = f"product_payload_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(data)

def scheduled_automation():
    print("Running automation")
    link_checker = linkAutomation.LinkChecker()
    link_checker.check_links()

scheduler.add_job(scheduled_automation, 'cron', day_of_week='mon-sun', hour=13, minute=20)

if __name__ == '__main__':
    scheduler.start()
    app.run(debug=True)