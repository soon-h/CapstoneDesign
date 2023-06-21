import os




global path
def findFile():
    filepath=(os.listdir('./downloaded_files'))
    print(filepath)
    for i in filepath:
        path,ext = os.path.splitext(i)
        if(ext=='.zip'):
            check = path


    os.system('powershell.exe Expand-Archive ./downloaded_files/%s.zip'%check)



    return check






