'''
    @file ProcessExecute
    @author Richard Howe
    Enumerates individual process tokens using WIN API function calls
'''
from Process import Process
from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess

'''
    Starting point of the program.
    Iterates through all running processes and creates an
    array of Process objects then enumerates their process tokens.
'''
def main():
    p_array = []
    
    for proc in process_iter():
        try:
            p = Process(proc)
            p_array.append(p)
        except(NoSuchProcess, AccessDenied, ZombieProcess):
            pass

    for i in p_array:
        print i.priv.getTokenInformation()
              
main()
