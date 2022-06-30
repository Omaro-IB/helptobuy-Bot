# from helptobuy import register_interest
# from helptobuy import findNewest
# import json
# from apscheduler.schedulers.blocking import BlockingScheduler
#
# def alertUser(url):
#     def submit():
#         newCookie = entry.get()
#         dictionary = {"yourAuthCookie": newCookie, "newestLink": url}
#         json_object = json.dumps(dictionary, indent=4)
#         with open("data.json", "x") as dataFile:
#             dataFile.write(json_object)
#         root.destroy()
#
#     import tkinter as tk
#     root = tk.Tk()
#     tk.Label(root, text="ALERT: Your authorization cookie has expired").pack()
#     tk.Label(root, text="Please enter your new cookie below:").pack()
#     entry = tk.Entry()
#     entry.pack()
#     butt = tk.Button(root, text="Submit", command=submit)
#     butt.pack()
#
#
# def runScript():
#     with open(r"data.json", "r") as dataFile:
#         lines = json.load(dataFile)
#
#     yourAuthCookie = lines["yourAuthCookie"]
#     newestLink = lines["newestLink"]
#
#     url, Title = findNewest()
#     if url != newestLink:
#         dictionary = {"yourAuthCookie": yourAuthCookie, "newestLink": url}
#         json_object = json.dumps(dictionary, indent=4)
#         with open(r"data.json", "w") as dataFile:
#             dataFile.write(json_object)
#         try:
#             address = Title.replace(" ", "+")
#             register_interest(yourAuthCookie, url, address)
#         except ValueError:
#             print("Invalid yourAuthCookie")
#             alertUser(url)
#             runScript()
