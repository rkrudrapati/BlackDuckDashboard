from os import system

# batch code
# @echo off
# dir /b /ad > dir_list.txt
#
# set project_name = $1
# set version_name = $2
# set scan_target = $3
#
# #Multiple projects
# FOR /F "tokens=* delims=" %%x in (dir_list.txt) DO (
# 	java -jar "C:\Scanners\synopsys-detect-6.2.1.jar" --blackduck.url=https://blackduckweb.philips.com --blackduck.api.token=xyz== --detect.project.name=$1 --detect.project.version.name=$2 --blackduck.trust.cert=true --detect.blackduck.signature.scanner.paths=$3 --blackduck.offline.mode=true
# )
#
# del dir_list.txt

#
# batch code version 2
# @echooff
#
# set
# argC = 0
# for % % x in ( % * ) do Set / A argC += 1
#
# if % argC %= =3 (
# set project_name= % 1
# set version_name= % 2
# set scan_target= % 3
# set % 1
# set % 2
# set % 3
# echo project_name: %
#     project_name %
#     echo
# version_name: % version_name %
#                 echo
# scan_target: % scan_target %
#
#                C:\Scanners\scan.cli - 2019.8
# .1\bin\scan.cli.bat - -host
# blackduckweb.philips.com - -port
# 443 - -scheme
# HTTPS - -project % project_name % --release % version_name % % scan_target % --insecure - v
#
# REM
# java - jar
# "C:\Scanners\synopsys-detect-6.2.1.jar" - -blackduck.url = https: // blackduckweb.philips.com - -blackduck.api.token = xyz == --detect.project.name = % 1 - -detect.project.version.name = % 2 - -blackduck.trust.cert = true - -detect.blackduck.signature.scanner.paths = % 3 - -blackduck.offline.mode = true
# ) else (echo Wrong input)
