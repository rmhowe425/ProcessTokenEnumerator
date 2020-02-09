try:
    from pywintypes import FALSE
    from win32api import OpenProcess, GetCurrentProcess
    from win32con import TOKEN_ALL_ACCESS, PROCESS_ALL_ACCESS, PROCESS_QUERY_INFORMATION, PROCESS_VM_READ
    from win32security import OpenProcessToken, GetTokenInformation, TokenPrivileges, LookupPrivilegeName
except:
    print("Error importing libraries. Try pip installing win32api.\n")
    
'''
    Class that manages and maintains an individual processes
    privileges and the processes token.
'''
class Privileges:

    '''
        Constructor for the Privilege class
        @param pid: A running processes PID
    '''
    def __init__(self, pid):
        self.process_token = self.setProcessToken(pid)
        self.privileges = self.setTokenInformation(self.process_token)
    
        
    '''
        Saves the processes token, if it exists
        [*] If requested token privileges are not allowed, token is not created.
    '''
    def setProcessToken(self, pid):
        proc_token = None

        try:
            handle = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, pid)
            proc_token = OpenProcessToken(handle, TOKEN_ALL_ACCESS)
        except:
            raise TypeError
        return proc_token
        
    '''
        Returns a processes token
    '''
    def getProcessToken(self):
        return self.process_token

    '''
        Returns contents stored within a process token
    '''
    def setTokenInformation(self, token):
        # Could not get a handle for process token (insufficient privs?)
        if not token:
            return None
        
        privTuple = GetTokenInformation(self.process_token, TokenPrivileges)
        priv_array = []
        
        if privTuple:
            for i in privTuple:
                priv = LookupPrivilegeName(None, i[0])
                if not all(priv):
                    continue
                else:
                    priv_array.append(priv)
        return priv_array

    def getTokenInformation(self):
        return self.privileges
