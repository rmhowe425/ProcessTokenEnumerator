import ctypes
from Privileges import Privileges
from ctypes import wintypes

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
        self.name = proc.name()
        self.pid = proc.pid
        self.owner = proc.username()
        self.priv = Privileges(self.pid)
        

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
