'''
    @file ProcessExecute
    @author Richard Howe
    Enumerates individual process tokens using WIN API function calls
'''
from os import getpid
from Process import Process
from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess  
    
'''
    Check all running process privileges against self,
    Inject when possible.
    @param victim: Process to be hollowed.
    @return inject: True of dll injection is successful.
'''
def checkAndInject(victim, c_proc):
    # True if victim is injectable
    inject = False
    # Abbreviation for victim proc privs
    v_privs = victim.priv.getTokenInformation()
    # Abbreviation for self proc privs
    c_privs = c_proc.priv.getTokenInformation()
    
    # If owners are the same, process is injectable (same proc context)
    if victim.getOwner() == c_proc.getOwner():
        inject = True
        # Do inject
    
    # Check for equivalent proc privs using list comprehension  
    elif not [item for item in v_privs if item not in c_privs]:
        inject = True
        # Do inject

    return inject

'''
    Starting point of the program.
    Iterates through all running processes and creates an
    array of Process objects then enumerates their process tokens.
'''
def main():
    # Pid of ProcessExecute
    c_pid= getpid()
    # Process instance of current running process
    c_proc = None  
    # List of Process Instances
    p_array = []
    # List of victim processes
    proc_injections = []

    # Create list of running processes and their privileges / tokens
    for proc in process_iter():
        try:
            p = Process(proc)
        except (NoSuchProcess, AccessDenied, ZombieProcess, TypeError):
            continue
        
         # Dont add current running process to list
        if p.getPID() == c_pid:
            c_proc = p
        else:
            p_array.append(p)

    # Check if processes are injectable & inject when possible
    for i in p_array:
        if checkAndInject(i, c_proc):
            proc_injections.append(i)
    for i in proc_injections:
        print "[*]Name: {}\n[*]PID: {}\n[*]Owner: {}\n\n".format(i.getName(), i.getPID(), i.getOwner())
        
main()
