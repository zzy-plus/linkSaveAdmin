import winreg
import paramiko
import os
import requests
import shutil
import json

def hex2Text(hexStr):
    byteData = bytes.fromhex(hexStr)
    return byteData.decode('utf-8')


# 获取用户文件夹
def getUserDoc():
    subkey = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
    # 打开注册表键
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, subkey)
    # 读取注册表值
    value, _ = winreg.QueryValueEx(registry_key, "Personal")
    # 关闭注册表键
    winreg.CloseKey(registry_key)
    print(value)
    return value

def ftpUpload(localPath, remotePath):
    # 建立SSH连接
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('errorserver.top', username='sftp', password='sftp')
    # 建立SFTP连接
    sftp = ssh.open_sftp()
    # 上传文件
    sftp.put(localPath, remotePath)
    # 关闭连接
    sftp.close()
    ssh.close()

# 获取档案
def getProfiles():
    profilePath = getUserDoc() + r'\Euro Truck Simulator 2\profiles'
    ls = os.listdir(profilePath)
    profiles = []
    profilesMap = {}
    for item in ls:
        try:
            if os.path.isdir(os.path.join(profilePath, item)):
                text = hex2Text(item)
                profiles.append(text)
                profilesMap[text] = item
        except:
            pass
    return profiles, profilesMap

def zipFile(filePath:str, zipPath:str):
    tempDir = getUserDoc() + r'\linkSavaTemp'
    if not os.path.exists(tempDir):
        os.makedirs(tempDir)
    # 复制整个目录结构到临时目录
    shutil.copytree(filePath, os.path.join(tempDir, os.path.basename(filePath)))

    shutil.make_archive(zipPath, 'zip', tempDir)
    # 删除临时目录
    shutil.rmtree(tempDir)


def updateData(profileName):
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        data['saveName'] = profileName
        resp = requests.post('http://121.37.222.191:8020/updatedata',json=data)
        if resp.status_code != 200 or resp.text != 'ok':
            return False
        else:
            return True

# 清除data.json里的内容
def cleanData():
    data = {
        'points': []
    }
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)


# 给data.json增加一条内容
def addData(newData):
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['points'].append(newData)

    print(data)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


# 获取当前位置信息
def getCurLocation(profileName):
    profilePath = getUserDoc() + r'\Euro Truck Simulator 2\profiles'
    savePath = f'{profilePath}\\{profileName}\\save\\1'    #只读取第一个存档，后续可能会优化
    gameSiiPath = f'{savePath}\\game.sii'
    # 解密
    os.system(f'SII_Decrypt \"{gameSiiPath}\"')
    # 读取
    dataLines = {}
    with open(gameSiiPath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.replace('\n', '')
            if line.strip().startswith('truck_placement'):
                dataLines['truck'] = line
            elif line.strip().startswith('trailer_placement'):
                dataLines['trailer'] = line
                break
    return dataLines


def getAccess(pwd):
    data = {'pwd': pwd}
    resp = requests.post('http://121.37.222.191:8020/access', json=data)
    if resp.status_code != 200:
        return False
    return resp.json()['status'] == 0




if __name__ == '__main__':
    resp = getAccess('12321')
    print(resp)