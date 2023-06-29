# Failed Pings Reporter

The Failed Pings Reporter is a PowerShell script designed to monitor the connectivity of MobiLab printers in a hospital environment. By pinging the IP addresses associated with each printer, the script provides an efficient method to check if the printers are online. The printers are located in various areas or departments within the hospital, including the Emergency Room (ER), CTICU A, CTICU B, ASU, NSICU, and MICU.

When a printer is found to be offline (evidenced by a failed ping), the script logs the room number and IP address in an output file, `FailedPings.txt`. This allows for quick identification of offline printers, facilitating swift troubleshooting and maintenance by the hospital IT staff. 

In the case that all printers within a specific area are online, the script will include a status message "All Printers Online" in the output file. This feature provides immediate feedback about the operational status of printers, enhancing the efficiency of IT maintenance and troubleshooting tasks.

## How to Use

1. Ensure that PowerShell is installed on your machine.
2. Open a PowerShell terminal.
3. Navigate to the directory containing the `FailedPings.ps1` script (or whatever you've named the script).
4. Run the script by typing `./FailedPings.ps1` and pressing Enter.
5. Check the `FailedPings.txt` file in the same directory for the results. The file will be cleared and rewritten each time the script runs.

## Script Details

The script begins by defining a prefix for the IP addresses, followed by defining the range of LANs (last segment of the IP address) for each area. These ranges are stored in a dictionary, with the area names acting as keys. The script proceeds to loop over each area and each LAN within the area, constructing the full IP address and pinging it. If the ping fails, it records the room number and IP address to the output file. The room number is incremented after each LAN. If all printers in an area are online, the script will append the message "All Printers Online" to the output file.

## Configuration

You can configure the LAN ranges for each area by editing the `$roomLans` dictionary in the script. The key should be the area name, and the value should be the range of LANs in that area. For example, `"ER" = 89..117 + 118 + 122`. This flexibility ensures that the tool can easily adapt to evolving network infrastructure and printer deployment within the hospital. 

The aim of the Failed Pings Reporter is to aid in proactive printer connectivity management, ensuring the reliable availability of printing services in a fast-paced hospital environment.
