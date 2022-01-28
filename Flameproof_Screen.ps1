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
$total_sleep_seconds = 0
$average_sleep_seconds = 0



while ($True) {
    $shell.sendkeys("+")
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    Write-Output(">>> " + $time + "   Press [Shift] " + $count + " Times. ")

    $sleep_seconds = Get-Random -Minimum 0.0 -Maximum 300
    $total_sleep_seconds += $sleep_seconds
    $average_sleep_seconds = $total_sleep_seconds / $count
    $count++

    Write-Output(">>> Sleep " + $sleep_seconds + " Seconds. ")
    Write-Output(">>> Average Sleep " + $average_sleep_seconds + " Seconds. `n")

    Start-Sleep $sleep_seconds
}
