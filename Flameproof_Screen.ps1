#Start-Process powershell -Verb runAs

$shell = New-Object -com "Wscript.Shell"

while($True)
{
    Start-Sleep -Seconds 295
    $shell.sendkeys(" ")
}
