# 💻 WinPwnage

[![build_status](https://travis-ci.com/rootm0s/WinPwnage.svg?branch=master)](https://travis-ci.com/rootm0s/WinPwnage)

The goal of this repo is to study the Windows penetration techniques.

Techniques are found online, on different blogs and repos here on GitHub. I do not take credit for any of the findings, thanks to all the researchers.

## UAC bypass techniques:
* UAC bypass using fodhelper
* UAC bypass using computerdefaults
* UAC bypass using slui
* UAC bypass using silentcleanup
* UAC bypass using compmgmtlauncher
* UAC bypass using sdclt (isolatedcommand)
* UAC bypass using sdclt (App Paths)
* UAC bypass using perfmon
* UAC bypass using eventviewer
* UAC bypass using sysprep (dll payload supported)
* UAC bypass using migwiz (dll payload supported)
* UAC bypass using mcx2prov (dll payload supported)
* UAC bypass using cliconfg (dll payload supported)
* UAC bypass using token manipulation
* UAC bypass using sdclt and Folder class
* UAC bypass using cmstp
* UAC bypass using .NET Code Profiler (dll payload supported)
* UAC bypass using mocking trusted directories (dll payload supported)
* UAC bypass using wsreset

## Persistence techniques:
* Persistence using userinit key
* Persistence using image file execution option and magnifier
* Persistence using hkey_local_machine run key
* Persistence using hkey_current_user run key
* Persistence using schtask (SYSTEM privileges)
* Persistence using explorer dll hijack
* Persistence using mofcomp and mof file (SYSTEM privileges)
* Persistence using wmic (SYSTEM privileges)
* Persistence using startup files
* Persistence using Cortana App
* Persistence using People App
* Persistence using bitsadmin
* Persistence using Windows Service (SYSTEM privileges)

## Elevation techniques:
* Elevate from administrator to NT AUTHORITY SYSTEM using handle inheritance
* Elevate from administrator to NT AUTHORITY SYSTEM using named pipe impersonation
* Elevate from administrator to NT AUTHORITY SYSTEM using token impersonation
* Elevate from administrator to NT AUTHORITY SYSTEM using schtasks (non interactive)
* Elevate from administrator to NT AUTHORITY SYSTEM using wmic (non interactive)
* Elevate from administrator to NT AUTHORITY SYSTEM using windows service (non interactive)

## Execution techniques:
* Execute payload by calling the RegisterOCX function in Advpack.dll
* Execute payload using appvlp binary
* Execute payload from bash.exe if linux subsystem is installed
* Execute payload using diskshadow.exe from a prepared diskshadow script
* Execute payload as a subprocess of Dxcap.exe
* Execute payload since there is a match for notepad.exe in the system directory
* Execute payload using ftp binary
* Execute payload by calling the RegisterOCX function in ieadvpack.dll
* Execute payload by calling OpenURL in ieframe.dll
* Execute payload using the Program Compatibility Assistant
* Execute payload by calling the LaunchApplication function
* Execute payload by calling OpenURL in shdocvw.dll
* Execute payload using sqltoolsps binary
* Execute payload by calling OpenURL in url.dll
* Execute payload as a subprocess of vsjitdebugger.exe
* Execute payload by calling RouteTheCall in zipfldr.dll

## Installing the Dependencies:
```pip install -r requirements.txt```

## Build with py2exe:
In order for a successful build, install the py2exe (http://www.py2exe.org) module and use the provided build.py script to compile all the scripts in to a portable executable.  This only seems to work on Python 2, not on Python 3.

```python build.py winpwnage.py```

## Build with PyInstaller:
This build works on both Python 2 and Python 3 and puts the .exe file into the __dist__ directory.
```
pip install pyinstaller
pyinstaller --onefile winpwnage.py
```
On Windows 10, Access Denied errors can accure while compiling, rerun until success or elevate the prompt. 

## Read:
* https://wikileaks.org/ciav7p1/cms/page_2621770.html
* https://wikileaks.org/ciav7p1/cms/page_2621767.html
* https://wikileaks.org/ciav7p1/cms/page_2621760.html
* https://msdn.microsoft.com/en-us/library/windows/desktop/bb736357(v=vs.85).aspx
* https://winscripting.blog/2017/05/12/first-entry-welcome-and-uac-bypass/
* https://github.com/winscripting/UAC-bypass/
* https://www.greyhathacker.net/?p=796
* https://github.com/hfiref0x/UACME
* https://bytecode77.com/hacking/exploits/uac-bypass/performance-monitor-privilege-escalation
* https://bytecode77.com/hacking/exploits/uac-bypass/slui-file-handler-hijack-privilege-escalation
* https://media.defcon.org/DEF%20CON%2025/DEF%20CON%2025%20workshops/DEFCON-25-Workshop-Ruben-Boobeb-UAC-0day-All-Day.pdf
* https://lolbas-project.github.io
