#!/usr/bin/env python3
import argparse
from qiniu import Auth, BucketManager
import os
import dotenv

# 初始化
dotenv.load_dotenv(dotenv.find_dotenv(), override=True)
access_key = os.getenv('QINIU_ACCESS_KEY')
secret_key = os.getenv('QINIU_SECRET_KEY')
bucket_name = os.getenv('QINIU_BUCKET_NAME')

# 构建鉴权对象
q = Auth(access_key, secret_key)
bucket = BucketManager(q)

def file_exists(key):
    """
    检查文件是否已存在
    :param key: 文件名
    :return: True 如果文件存在，否则 False
    """
    ret, info = bucket.stat(bucket_name, key)
    return info.status_code == 200

def fetch_file(url, bucket_name, key):
    """
    从指定 URL 拉取文件并上传到七牛云存储空间
    :param url: 文件 URL
    :param bucket_name: 存储空间名称
    :param key: 上传后保存的文件名
    :return: 上传文件的信息
    """
    if file_exists(key):
        print(f"文件已存在于云端: {key}")
        confirm = input("确认覆盖该文件? (y/n): ").strip().lower()
        if confirm != 'y':
            print("上传取消")
            return None
    
    ret, info = bucket.fetch(url, bucket_name, key)
    if info.status_code == 200:
        print(f"文件拉取成功: {key}")
        return ret
    else:
        print(f"文件拉取失败: {info}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='从指定 URL 拉取文件并上传到七牛云存储空间的脚本')
    parser.add_argument('url', help='文件 URL')
    parser.add_argument('key', help='上传后的文件路径名')

    args = parser.parse_args()
    fetch_file(args.url, bucket_name, args.key)
