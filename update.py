import base64
import time
import requests
import json
import os
from datetime import datetime

# 网站地址
website = "http://localhost:8090"
# halo2备份文件夹路径
# backup_halo_path = "/root/halo/backups"
backup_api = website + "/apis/migration.halo.run/v1alpha1/backups"
check_api = website + "/apis/migration.halo.run/v1alpha1/backups?sort=metadata.creationTimestamp%2Cdesc"

user = "1103536250"
password = "3214569987Zz"

# 获取现在的时间 2023-09-24T13:14:18.650Z
now_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
print(now_time)
# 构建认证头部
auth_header = "Basic " + base64.b64encode((user + ":" + password).encode()).decode()
payload = json.dumps({
    "apiVersion": "migration.halo.run/v1alpha1",
    "kind": "Backup",
    "metadata": {
        "generateName": "backup-",
        "name": ""
    },
    "spec": {
        "expiresAt": now_time,
    }
})
headers = {
    'User-Agent': '',
    'Content-Type': 'application/json',
    'Authorization': "Basic " + base64.b64encode((user + ":" + password).encode()).decode(),
}
response = requests.request("POST", backup_api, headers=headers, data=payload)
print(response.text)
if response.status_code == 201:
    print("备份请求成功！")
    new_backup_name = ""
    while True:
        check_response = requests.request("GET", check_api, headers=headers)
        if check_response.status_code == 200:
            backup_data = json.loads(check_response.text)
            items = backup_data.get("items", [])
            if items[0]["status"]["phase"] == "SUCCEEDED":
                print("备份完成！")
                new_backup_name = items[0]["status"]["filename"]
                break
            if items[0]["status"]["phase"] == "RUNNING":
                print("正在备份！")
                time.sleep(10)
    git_add_file = os.system('git add *')
    time.sleep(10)
    git_commit_file = os.system('git commit -m "update all time backup"')
    time.sleep(10)
    git_push = os.system('git push -u origin main')
    print("上传成功")
