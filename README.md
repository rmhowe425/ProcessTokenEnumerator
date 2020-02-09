# ProcessTokenEnumerator
[*] Uses the Windows API to enumerate all possible process token privileges
[*] Active .dll injection will be incorporated in future updates

[*] This project is intended to be a part of a post exploitation framework.
    -> Future work will include:
          1) Process migration
          2) Privilege escalation via named pipe impersonation
          3) RAM dumping
          4) Signal transmission to remote processes
          5) Wifi / network auditing

Requires installation of the following 3rd party libraries:
  psutil    python3 -m pip install psutil
  win32api  python3 -m pip install pywin32
