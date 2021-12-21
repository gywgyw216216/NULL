# Run as Administrator.
# Start-Process powershell -Verb runAs

$time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Output(">>> " + $time + "   Initializing Process...... `n")
Write-Output(">>>  BIOS: ")
Get-CimInstance Win32_BIOS
Write-Output(">>>  CPU: ")
Get-CimInstance Win32_Processor

$gpu = Get-CimInstance Win32_VideoController
$width = $gpu.CurrentHorizontalResolution
$height = $gpu.CurrentVerticalResolution

Write-Output(">>> GPU: ")
Write-Output($gpu)
Write-Output(">>> Resolution: " + $width + " X " + $height + "`n")
Write-Output(">>>  Memory: ")
Get-CimInstance Win32_PhysicalMemory
Write-Output(">>>  Disk: ")
Get-CimInstance Win32_DiskDrive
Write-Output(">>>  Operating System: ")
Get-CimInstance Win32_OperatingSystem

$powershell = @(Get-Process powershell)
$time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Output(">>> " + $time + "   Initialize Process Successfully! PID: " + $powershell.Get($powershell.Count - 1).Id)
Write-Output("`n--------------------------------------------------------------------------------------------------`n")

$shell = New-Object -ComObject "Wscript.Shell"
$count = 1

while ($True) {
    $shell.sendkeys("+")
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    Write-Output(">>> " + $time + "   Press [Shift] " + $count + " Times. ")

    $count++
    $sleep = Get-Random -Minimum 0.0 -Maximum 300

    Write-Output(">>> Sleep " + $sleep + " Seconds. `n")

    Start-Sleep $sleep
}
