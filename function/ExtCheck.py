# ExtCheck.py

import os
import sys
import time
import binascii

global detectlist
global aliaslist #확장자 훼손 목록
global badsiglist #시그니처 훼손 목록

detectlist = []
aliaslist = []
badsiglist = []

def file_Load(path):
    print("[*] File Load ...")

    file_list = os.listdir(path)
    file = []
    for i in file_list:
        print("[+] File Name >>> "+i)
        file.append(i)
    return file


def search(file_li, path):
    print("\n[*] File Signature Searching ...\n")

    for f in file_li:
        file_r = open(path+"\\"+f, "rb")
        
        ## JPG ##
        file_h = file_r.read(4) #JPG 헤더 시그니처
        file_f = file_r.read()[-2:] #JPG 푸터 시그니처
        sig_h = binascii.b2a_hex(file_h).decode("utf-8")
        sig_f = binascii.b2a_hex(file_f).decode("utf-8")

        if (sig_h == 'ffd8ffe0') or (sig_h == 'ffd8ffe8'): #JPG 헤더 O
            detectlist.append(f)
            detectlist.append('JPG')
            if (sig_f == 'ffd9'): #JPG 푸터 O
                if (f[-3:] == 'jpg') or (f[-3:] == 'JPG'): #JPG 확장자 O
                    detectlist.append('Match')
                    pass
                else: #<확장자 훼손>
                    aliaslist.append(f)
                    aliaslist.append('JPG')
                    detectlist.append('Alias')
                    pass
            else: #<푸터 시그니처 훼손>
                if (f[-3:] == 'jpg') or (f[-3:] == 'JPG'): #JPG 확장자 O
                    detectlist.append('Bad Signature (Footer)')
                    badsiglist.append(f)
                    badsiglist.append('JPG')
                    badsiglist.append('Footer Signature')
                    pass
                else: #<확장자, 푸터 시그니처 훼손>
                    detectlist.append('Alias, Bad Signature (Footer)')
                    aliaslist.append(f)
                    aliaslist.append('JPG')
                    badsiglist.append(f)
                    badsiglist.append('JPG')
                    badsiglist.append('Footer Signature')
                    pass
        else:
            if (sig_f == 'ffd9'): #JPG 푸터 O
                detectlist.append(f)
                detectlist.append('JPG')
                if (f[-3:] == 'jpg') or (f[-3:] == 'JPG'): #JPG 확장자 O
                    detectlist.append('Bad Signature (Header)') #<헤더 시그니처 훼손>
                    badsiglist.append(f)
                    badsiglist.append('JPG')
                    badsiglist.append('Header Signature')
                    pass
                else: #<확장자, 헤더 시그니처 훼손>
                    detectlist.append('Alias, Bad Signature (Header)')
                    aliaslist.append(f)
                    aliaslist.append('JPG')
                    badsiglist.append(f)
                    badsiglist.append('JPG')
                    badsiglist.append('Header Signature')
        
        ## GIF ##
        file_r = open(path+"\\"+f, "rb")
        file_h = file_r.read(6) #GIF 헤더 시그니처
        sig_h = binascii.b2a_hex(file_h).decode("utf-8")

        if (sig_h == '474946383761') or (sig_h == '474946383961'): #GIF 헤더 O
            detectlist.append(f)
            detectlist.append('GIF')
            if (sig_f == '003b'): #GIF 푸터 O
                if (f[-3:] == 'gif') or (f[-3:] == 'GIF'): #GIF 확장자 O
                    detectlist.append('Match')
                    pass
                else: #<확장자 훼손>
                    aliaslist.append(f)
                    aliaslist.append('GIF')
                    detectlist.append('Alias')
                    pass
            else: #<푸터 시그니처 훼손>
                if (f[-3:] == 'gif') or (f[-3:] == 'GIF'): #GIF 확장자 O
                    detectlist.append('Bad Signature (Footer)')
                    badsiglist.append(f)
                    badsiglist.append('GIF')
                    badsiglist.append('Footer Signature')
                    pass
                else: #<확장자, 푸터 시그니처 훼손>
                    detectlist.append('Alias, Bad Signature (Footer)')
                    aliaslist.append(f)
                    aliaslist.append('GIF')
                    badsiglist.append(f)
                    badsiglist.append('GIF')
                    badsiglist.append('Footer Signature')
                    pass
        else: 
            if (sig_f == '003b'): #JPG 푸터 O
                detectlist.append(f)
                detectlist.append('GIF')
                if (f[-3:] == 'gif') or (f[-3:] == 'GIF'): #GIF 확장자 O
                    detectlist.append('Bad Signature (Header)') #<헤더 시그니처 훼손>
                    badsiglist.append(f)
                    badsiglist.append('GIF')
                    badsiglist.append('Header Signature')
                    pass
                else: #<확장자, 헤더 시그니처 훼손>
                    detectlist.append('Alias, Bad Signature (Header)')
                    aliaslist.append(f)
                    aliaslist.append('GIF')
                    badsiglist.append(f)
                    badsiglist.append('GIF')
                    badsiglist.append('Header Signature')

        ## PNG ##
        file_r = open(path+"\\"+f, "rb")
        file_h = file_r.read(8) #PNG 헤더 시그니처
        file_f = file_r.read()[-8:] #PNG 푸터 시그니처
        sig_h = binascii.b2a_hex(file_h).decode("utf-8")
        sig_f = binascii.b2a_hex(file_f).decode("utf-8")
            
        if (sig_h == '89504e470d0a1a0a'): #PNG 헤더 O
            detectlist.append(f)
            detectlist.append('PNG')
            if (sig_f == '49454e44ae426082'): #PNG 푸터 O
                if (f[-3:] == 'png') or (f[-3:] == 'PNG'): #PNG 확장자 O
                    detectlist.append("Match")
                    pass
                else: #<확장자 훼손>
                    aliaslist.append(f)
                    aliaslist.append('PNG')
                    detectlist.append('Alias')
                    pass
            else: #<푸터 시그니처 훼손>
                if (f[-3:] == 'png') or (f[-3:] == 'PNG'): #PNG 확장자 O
                    detectlist.append('Bad Signature (Footer)')
                    badsiglist.append(f)
                    badsiglist.append('PNG')
                    badsiglist.append('Footer Signature')
                    pass
                else: #<확장자, 푸터 시그니처 훼손>
                    detectlist.append('Alias, Bad Signature (Footer)')
                    aliaslist.append(f)
                    aliaslist.append('PNG')
                    badsiglist.append(f)
                    badsiglist.append('PNG')
                    badsiglist.append('Footer Signature')
                    pass
        else:
            if (sig_f == '49454e44ae426082'): #PNG 푸터 O
                detectlist.append(f)
                detectlist.append('PNG')
                if (f[-3:] == 'png') or (f[-3:] == 'PNG'): #PNG 확장자 O
                    detectlist.append('Bad Signature (Header)') #<헤더 시그니처 훼손>
                    badsiglist.append(f)
                    badsiglist.append('PNG')
                    badsiglist.append('Header Signature')
                    pass
                else: #<확장자, 헤더 시그니처 훼손>
                    detectlist.append('Alias, Bad Signature (Header)')
                    aliaslist.append(f)
                    aliaslist.append('PNG')
                    badsiglist.append(f)
                    badsiglist.append('PNG')
                    badsiglist.append('Header Signature')
            
        file_r.close()
    finished()


def finished():
    os.chdir(path)
    time2 = time.strftime("%H-%M (%Y-%m-%d)")
    skiptime = time2+".txt"

    try:
        i = len(detectlist)
        x = 0
        j = 1
        if (i > 0):
            file = open("Detection-List "+skiptime, "w")
            while x < i:
                fname = detectlist[x]
                x = x + 1
                exttype = detectlist[x]
                x = x + 1
                result = detectlist[x]
                file.write(str(j)+"\t파일명: "+str(fname)+"\t\t확장자: "+exttype+"\t\tSignature Analysis: "+result+"\n")
                x = x + 1
                j = j + 1
            file.close()
            print("[+] 탐지 목록이 'Detection-List "+skiptime+"'에 성공적으로 기록됨.\n")
    except OSError:
        print("[-] ERROR WRITING DETECT-LIST")
        pass

    try:
        i = len(aliaslist)
        x = 0
        j = 1
        if (i > 0):
            file = open("Alias-List "+skiptime, "w")
            while x < i:
                fname = aliaslist[x]
                x = x + 1
                exttype = aliaslist[x]
                file.write(str(j)+"\t파일명: "+str(fname)+"\t\t확장자: "+exttype+"\n")
                x = x + 1
                j = j + 1
            file.close()
            print("[+] 탐지 목록이 'Alias-List "+skiptime+"'에 성공적으로 기록됨.\n")
    except OSError:
        print("[-] ERROR WRITING ALIAS-LIST")
        pass

    try:
        i = len(badsiglist)
        x = 0
        j = 1
        if (i > 0):
            file = open("BadSignature-List "+skiptime, "w")
            while x < i:
                fname = badsiglist[x]
                x = x + 1
                exttype = badsiglist[x]
                x = x + 1
                loc = badsiglist[x]
                file.write(str(j)+"\t파일명: "+str(fname)+"\t\t확장자: "+exttype+"\t\t훼손된 시그니처: "+loc+"\n")
                x = x + 1
                j = j + 1
            file.close()
            print("[+] 탐지 목록이 'BadSignature-List "+skiptime+"'에 성공적으로 기록됨.\n")
    except OSError:
        print("[-] ERROR WRITING BADSIGNATURE-LIST")
        pass

    print("[*] 프로그램 작업 완료 ...")


def main():
    global path
    path = 'C:\\Test'
    print("\n[*] '"+path+"' 에 존재하는 모든 파일을 검사합니다.\n")
    file_li = file_Load(path)
    search(file_li, path)
    sys.exit()

if __name__ == '__main__':
    main()
