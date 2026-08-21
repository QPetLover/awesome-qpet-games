#!/usr/bin/env python3
import os
import argparse
from tqdm import tqdm
from qiniu import Auth, put_file, etag, BucketManager
import qiniu.config
import dotenv

# 初始化
dotenv.load_dotenv(dotenv.find_dotenv(), override=True)
access_key = os.getenv('QINIU_ACCESS_KEY')
secret_key = os.getenv('QINIU_SECRET_KEY')
bucket_name = os.getenv('QINIU_BUCKET_NAME')
url_prefix = os.getenv('QINIU_URL_PREFIX')

# 构建鉴权对象
q = Auth(access_key, secret_key)
bucket = BucketManager(q)

class ProgressBar:
    def __init__(self, total_size):
        self.pbar = tqdm(total=total_size, unit='B', unit_scale=True, desc='上传进度')

    def progress_handler(self, progress, total):
        self.pbar.update(progress - self.pbar.n)

def file_exists(key):
    """
    检查文件是否已存在
    :param key: 文件名
    :return: True 如果文件存在，否则 False
    """
    ret, info = bucket.stat(bucket_name, key)
    return info.status_code == 200

def upload_file_with_progress(localfile, key, skip_existing):
    """
    上传文件到七牛云并显示上传进度
    :param localfile: 本地文件路径
    :param key: 上传后保存的文件名
    :param skip_existing: 是否跳过已存在的文件
    :return: 上传文件的信息
    """
    if file_exists(key):
        if skip_existing:
            print(f"文件已存在，跳过上传: {key}")
            return
        else:
            print(f"文件已存在: {key}")
            confirm = input("确认覆盖该文件? (y/n): ").strip().lower()
            if confirm != 'y':
                print("跳过文件")
                return
    print(f"开始上传文件: {key}")
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    
    # 获取文件大小
    total_size = os.path.getsize(localfile)
    progress_bar = ProgressBar(total_size)
    
    try:
        ret, info = put_file(token, key, localfile, version='v2', progress_handler=progress_bar.progress_handler)
        progress_bar.pbar.close()
        if info.status_code == 200:
            print(f"上传成功: {key}")
            return ret
        else:
            print(f"上传失败: {info}")
            return None
    except Exception as e:
        progress_bar.pbar.close()
        print(f"上传出错: {e}")
        return None

def upload_folder(localfolder, skip_existing=True):
    """
    上传文件夹中的所有文件
    :param localfolder: 本地文件夹路径
    :param skip_existing: 是否跳过已存在的文件
    """
    for root, dirs, files in os.walk(localfolder):
        for file in files:
            localfile = os.path.join(root, file)
            # key = os.path.relpath(localfile, localfolder).replace("\\", "/")
            # print(file, key, localfile)
            # input(f"按回车键上传文件: {key}")
            upload_file_with_progress(localfile, localfile, skip_existing)

def list_files(prefix=None, limit=1000, delimiter=None, marker=None):
    """
    获取指定前缀的文件列表
    :param prefix: 文件前缀
    :param limit: 列举条目数
    :param delimiter: 分隔符
    :param marker: 标记
    :return: 文件列表
    """
    file_list = []
    while True:
        ret, eof, info = bucket.list(bucket_name, prefix, marker, limit, delimiter)
        if info.status_code == 200:
            items = ret.get('items', [])
            file_list.extend(items)
            marker = ret.get('marker', None)
            if eof:
                break
        else:
            print(f"获取文件列表失败: {info}")
            break
    return file_list

def print_uploaded_files(prefix=None):
    files = list_files(prefix)
    if files:
        print("-" * 30)
        print("已上传的文件列表:")
        print("-" * 30)
        for file in files:
            print(file.get('key'))
        print("-" * 30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='七牛云文件夹上传脚本')
    parser.add_argument('folder_path', help='要上传的本地文件夹路径')
    parser.add_argument('--skip-existing', action='store_true', help='跳过已存在的文件')

    args = parser.parse_args()
    
    localfolder = args.folder_path
    skip_existing = args.skip_existing
    
    if os.path.isdir(localfolder):
        while True:
            print(f"即将上传文件夹到云端，路径为: {localfolder}")
            print("输入 y 覆盖，n 跳过覆盖，c 查看已上传列表，默认为 n")
            option = input("是否覆盖同名文件? (y/N/c): ").strip().lower()
            if option == 'y':
                skip_existing = False
                break
            elif option == 'c':
                print_uploaded_files(localfolder)
            else:
                skip_existing = True
                break

        upload_folder(localfolder, skip_existing)
    else:
        print("文件夹不存在，请检查文件夹路径")
