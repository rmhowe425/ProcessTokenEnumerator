try:
    from ctypes import wintypes
    from Privileges import Privileges
except:
    print("Error importing libraries.\n")

'''
    Class responsible for managing relevant Process Information.
    Keeps track of an individual processe's: name, PID, owner, and its privileges (token information)
'''
class Process:

    '''
        Constructor for the Process class
        @param proc: PSutil process object
    '''
    def __init__(self, proc):
        self.name  = self.setName(proc.name())
        self.pid   = self.setPID(proc.pid)
        self.owner = self.setOwner(proc.username())
        self.priv  = Privileges(self.pid)
        
    '''
        Sets the value of the process name
        @param name: Human readable name assigned to a process
    '''
    def setName(self, name):
        if not name:
            raise TypeError
        return name

    '''
        Sets the value of a process PID
        @param pid: Job number of a process
    '''
    def setPID(self, pid):
        if not pid:
            raise TypeError
        return pid

    '''
        Sets the value of the process owner
        @param owner: User interacting with this process
    '''
    def setOwner(self, owner):
        if not owner:
            raise TypeError
        return owner
    
    '''
        Returns a Process object's PID
    '''
    def getPID(self):
        return self.pid

    '''
        Returns a Process object's unique name
    '''
    def getName(self):
        return self.name

    '''
        Returns a Process objects owner.
        [*]The owner of the running process.
    '''
    def getOwner(self):
        return self.owner

    '''
        Returns the privileges of the Process oject.
        The process privileges assigned by the OS
    '''
    def getPrivileges(self):
        return self.priv.getProcessToken()
