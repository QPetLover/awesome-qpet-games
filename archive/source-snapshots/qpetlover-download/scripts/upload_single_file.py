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

def upload_file_with_progress(localfile, key=None):
    """
    上传文件到七牛云并显示上传进度
    :param localfile: 本地文件路径
    :param key: 上传后保存的文件名。如果为 None，则使用本地文件名
    :return: 上传文件的信息
    """
    if not key:
        key = localfile

    if file_exists(key):
        print(f"文件已存在于云端: {key}")
        confirm = input("确认覆盖该文件? (y/n): ").strip().lower()
        if confirm != 'y':
            print("上传取消")
            return

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='七牛云文件上传脚本')
    parser.add_argument('file_path', help='要上传的本地文件路径')
    parser.add_argument('--key', help='上传后保存的文件名', default=None)

    args = parser.parse_args()
    
    localfile = args.file_path
    key = args.key
    
    if not key:
        key = localfile
    
    if os.path.isfile(localfile):
        print(f"即将上传文件到云端，路径为: {key}")
        confirm = input("确认继续上传? (y/n): ").strip().lower()
        if confirm == 'y':
            upload_file_with_progress(localfile, key)
        else:
            print("上传取消")
    else:
        print("文件不存在，请检查文件路径")
