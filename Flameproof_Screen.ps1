#Start-Process powershell -Verb runAs

$shell = New-Object -com "Wscript.Shell"
$count = 1

while ($True) {
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    Write-Output (">>> " + $time + "   Press Space " + $count + " Times. ")

    Start-Sleep -Seconds 295
    $shell.sendkeys(" ")
    $count++
}
