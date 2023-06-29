# Define the prefix
$prefix = "10.150.104."

# Define the output file
$outputFile = "FailedPings.txt"

# Clear the output file
Clear-Content $outputFile

# Define the room numbers and associated LANs
$roomLans = @{
    # ER
    # 118 & 122 are at Desks
    "ER" = 89..117 + 118 + 122

    # CTICU A
    "CTICU A" = 143..152

    # CTICU B
    "CTICU B" = 153..162

    # ASU
    "ASU" = 69..84

    # NSICU
    "NSICU" = 171..178

    # MICU
    # Desks
    "MICU" = 163..164
}

# Loop over each area
foreach ($area in $roomLans.Keys) {
    # Add the area title to the output file
    Add-Content -Path $outputFile -Value "----------------------"
    Add-Content -Path $outputFile -Value "Area: $area"
    Add-Content -Path $outputFile -Value "----------------------"

    # Get the LAN list for the area
    $lanList = $roomLans[$area]

    # Initialize the room number
    $roomNumber = 1

    # Initialize a flag to track if all printers are online
    $allPrintersOnline = $true

    # Loop over each LAN
    foreach ($lan in $lanList) {
        # Construct the full IP address
        $ipAddress = $prefix + $lan.ToString()

        # Ping the IP address
        $pingResult = Test-Connection -ComputerName $ipAddress -Count 1 -Quiet

        # If the ping failed, write the room number and IP address to the output file
        if (-not $pingResult) {
            $message = "Room Number: " + $roomNumber.ToString() + ", IP: " + $ipAddress
            Add-Content -Path $outputFile -Value $message
            $allPrintersOnline = $false
        }

        # Increment the room number
        $roomNumber++
    }

    # If all printers are online, add that message to the output file
    if ($allPrintersOnline) {
        Add-Content -Path $outputFile -Value "All Printers Online"
    }
}
