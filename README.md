# ProcessTokenEnumerator
[*] Uses the Windows API to enumerate all possible process token privileges
[*] Active .dll injection will be incorporated in future updates

[*] This project is intended to be a part of a post exploitation framework.
     <md-tab>-> Future work will include:<br /><md-tab>
          1) Process migration<br /><md-tab>
          2) Privilege escalation via named pipe impersonation<br /><md-tab>
          3) RAM dumping<br /><md-tab>
          4) Signal transmission to remote processes<br /><md-tab>
          5) Wifi / network auditing<br /><br />

Requires installation of the following 3rd party libraries:
  psutil    python3 -m pip install psutil
  win32api  python3 -m pip install pywin32
