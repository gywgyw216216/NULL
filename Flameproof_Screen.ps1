#Start-Process powershell -Verb runAs

$shell = New-Object -com "Wscript.Shell"

while($True)
{
    Start-Sleep -Seconds 255
    $shell.sendkeys(" ")
}
