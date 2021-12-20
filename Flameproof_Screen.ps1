# Run as Administrator.
# Start-Process powershell -Verb runAs

$shell = New-Object -ComObject "Wscript.Shell"
$count = 1

# Get Screen Resolution.
# $screen = Get-WmiObject win32_videocontroller
# $width = $screen.CurrentHorizontalResolution
# $height = $screen.CurrentVerticalResolution

# Write-Output(">>> Resolution: (" + $width + ", " + $height + ")")
# Write-Output("--------------------------------------------------------")
# Write-Output("")

while ($True){
    $shell.sendkeys("+")
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    Write-Output(">>> " + $time + "   Press [Shift] " + $count + " Times. ")

    $count++
    $sleep = Get-Random -Minimum 0.0 -Maximum 300

    Write-Output(">>> Sleep " + $sleep + " Seconds. ")
    Write-Output("")

    Start-Sleep $sleep
}
