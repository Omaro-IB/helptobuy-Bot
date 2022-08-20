from helptobuy import register_interest
from helptobuy import findNewest
from helptobuy import dummy_request
from helptobuy import validate_cookie
import json
import tkinter as tk
from apscheduler.schedulers.blocking import BlockingScheduler

def alertUser(url):
    def submit(newCookie=None):
        if newCookie is None:
            newCookie = entry.get()
        dictionary = {"yourAuthCookie": newCookie, "newestLink": url}
        json_object = json.dumps(dictionary, indent=4)
        with open("data.json", "w") as dataFile:
            dataFile.write(json_object)
        root.destroy()

    try:
        root = tk.Tk()
    except RuntimeError:
        print("================================================= GUI ERROR =================================================")
        newCookie = input("Please input your new yourAuthCookie directly into the console: ")
        submit(newCookie=newCookie)
    tk.Label(root, text="ALERT: Your authorization cookie has expired").grid(row=1, column=1, columnspan=2)
    tk.Label(root, text="Please enter your new cookie below:").grid(row=2, column=1, columnspan=2)
    entry = tk.Entry()
    entry.grid(row=3, column=1)
    butt = tk.Button(root, text="Submit", command=submit)
    butt.grid(row=3, column=2)
    tk.mainloop()


def loadJSON():
    with open(r"data.json", "r") as dataFile:
        lines = json.load(dataFile)
    yourAuthCookie = lines["yourAuthCookie"]
    newestLink = lines["newestLink"]
    return yourAuthCookie, newestLink

def try_interest(yourAuthCookie, url, Title):
    try:
        address = Title.replace(" ", "+")
        register_interest(yourAuthCookie, url, address)
        print("Successfully registered interest to "+Title)
        print("URL Confirmation: "+url)
    except ValueError:
        print("Invalid yourAuthCookie")
        alertUser(url)
        new_yourAuthCookie, new_url = loadJSON()
        try_interest(new_yourAuthCookie, new_url, Title)

def runScript():
    yourAuthCookie, newestLink = loadJSON()
    url, Title = findNewest()
    if url != newestLink:
        print("New listing detected...")
        try_interest(yourAuthCookie, url, Title)
        yourAuthCookie, newestLink = loadJSON()
        dictionary = {"yourAuthCookie": yourAuthCookie, "newestLink": url}
        json_object = json.dumps(dictionary, indent=4)
        with open(r"data.json", "w") as dataFile:
            dataFile.write(json_object)
        print("="*100)
    else:
        while True:
            if validate_cookie(yourAuthCookie, url):
                break
            else:
                print("Invalid yourAuthCookie")
                alertUser(url)
                yourAuthCookie, newestLink = loadJSON()
        print("No new listings; up to date!")
        print("Sent dummy request to keep yourAuthCookie alive - {}".format(dummy_request(url, yourAuthCookie, Title)))
        print("="*100)

runScript()
scheduler = BlockingScheduler({'apscheduler.job_defaults.max_instances': 2})
scheduler.add_job(runScript, 'interval', minutes=1)
scheduler.start()
