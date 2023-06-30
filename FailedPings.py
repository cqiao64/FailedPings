import os
import subprocess
import requests
import re
from collections import OrderedDict

# Define the prefix
prefix = "10.150.104."

# Define the output file
outputFile = "FailedPings.txt"

# Clear the output file
open(outputFile, 'w').close()

# Define the room numbers and associated LANs
roomLans = OrderedDict([
    ("ER", list(range(89, 118)) + [118, 119, 122, 125]),
    ("CTICU A", list(range(143, 153))),
    ("CTICU B", list(range(153, 163))),
    ("ASU", list(range(69, 85))),
    ("NSICU", list(range(171, 179))),
    ("MICU", [163, 164])
])

# Function to get the battery health status of a printer with a given IP address
def get_battery_health(ip_address):
    # Send a GET request to the printer's web page
    response = requests.get(f"http://{ip_address}")
    # Search for the battery health status in the response
    match = re.search(r'<TD>Battery Health</TD>\s+<TD>(\w+)</TD>', response.text)
    # Return the battery health status if found, otherwise return "Unknown"
    if match:
        return match.group(1)
    else:
        return "Unknown"

# Loop over each area
for area, lanList in roomLans.items():
    with open(outputFile, 'a') as f:
        f.write("----------------------\n")
        f.write(f"Area: {area}\n")
        f.write("----------------------\n")

    roomNumber = 1
    # For CTICU B, start roomNumber from 11
    if area == "CTICU B":
        roomNumber = 11

    allPrintersOnline = True
    allPrintersGoodHealth = True

    for lan in lanList:
        ipAddress = prefix + str(lan)
        pingResult = subprocess.call(['ping', '-n', '1', ipAddress])

        if pingResult != 0:
            # For 118, 122 and all the ips in MICU, specify as "Desks" not "Room Numbers"
            if area == "MICU" or lan in [118, 119, 122, 125]:
                identifier = "Desk"
            else:
                identifier = "Room Number"

            message = f"{identifier}: {roomNumber}, IP: {ipAddress}\n"
            with open(outputFile, 'a') as f:
                f.write(message)
            allPrintersOnline = False
        else:
            try:
                # Get the battery health status of the printer
                battery_health = get_battery_health(ipAddress)
                if battery_health != "good":
                    allPrintersGoodHealth = False
                    with open(outputFile, 'a') as f:
                        f.write(f"IP: {ipAddress}, Battery Health: {battery_health}\n")
            except Exception as e:
                with open(outputFile, 'a') as f:
                    f.write(f"Could not get battery health for IP: {ipAddress}, Error: {str(e)}\n")

        roomNumber += 1

    if allPrintersOnline:
        with open(outputFile, 'a') as f:
            f.write("All Printers Online\n")

    if allPrintersGoodHealth:
        with open(outputFile, 'a') as f:
            f.write("All Printers Health: Good\n")
