$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
& python (Join-Path $package 'install.py') --restore
