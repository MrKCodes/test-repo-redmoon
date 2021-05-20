import sys
from datetime import datetime
import requests


now = datetime.now()
successMsg = "Product: AdminPanel -- Installation completed successfully."
numberOfTimesToReadFile = 0
successMsgFound = False

logFile = open("C:\\tmp\\admin_panel_packge.log", encoding='UTF-16LE')
lines = logFile.readlines()

for line in lines:
    if successMsg in line:
        print("Success message FOUND!!")
        successMsgFound = True
logFile.close()

# if successMsgFound:
#     print("Found after reading file " + str(numberOfTimesToReadFile) + " times")
#     break

htmFile = open("c:\\tmp\\reports\\report.html","w")
htmFile.write("""<!DOCTYPE html>
            <html>
            <head>
            <style>
            table, th, td {
            border-style: solid;
            border-color: #2F4F4F;
            border-width: 1px;
            }
            </style>
            </head>
            <body>

            <h2>Test for Admin Panel</h2>


            <table style="width:50%">
            <tr bgcolor = #5F9EA0>
                <th>Application</th>
                <th>Timestamp</th>
                <th>Status</th>
            </tr>
            <tr>
                <td bgcolor = #B0E0E6>Admin Panel</td>              
            """)

string = "This is just a test run at: " + str(now)
# Timestamp
htmFile.write("<td bgcolor = #B0E0E6>" + str(now) + "</td>")
response = None
try:
    response = requests.get("http://localhost/Admin/")

except error as e:
    print(e)
finally:
    print("Writing HTML Report")
    if response:
        status = response.status_code
        print("Response: " + str(response))
        # status
        if status == 200:
            htmFile.write("<td bgcolor = #00FA9A>Success</td>")
        else:
            htmFile.write("<td bgcolor = #FFA07A>Fail</td>")
    else:
        htmFile.write("<td bgcolor = #FFA07A>Fail</td>")

htmFile.write("""
                </tr>
            </table>

            </body>
            </html>""")

htmFile.close
