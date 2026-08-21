#!/usr/bin/env python3
import argparse
from qiniu import Auth, BucketManager
from urllib.parse import quote
import dotenv
import os, json

# 初始化
dotenv.load_dotenv(dotenv.find_dotenv(), override=True)
access_key = os.getenv('QINIU_ACCESS_KEY')
secret_key = os.getenv('QINIU_SECRET_KEY')
bucket_name = os.getenv('QINIU_BUCKET_NAME')
url_prefix = os.getenv('QINIU_URL_PREFIX')

# 构建鉴权对象
q = Auth(access_key, secret_key)
bucket = BucketManager(q)

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

def generate_markdown(file_list):
    """
    生成 Markdown 格式的文件列表
    :param file_list: 文件列表
    :return: Markdown 格式的字符串
    """
    markdown_lines = ["| Key | URL |", "| --- | --- |"]
    for file in file_list:
        key = file.get('key', '')
        # hash_val = file.get('hash', '')
        url = file.get('url', '')
        markdown_lines.append(f"| {key} | {url} |")
    return "\n".join(markdown_lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='七牛云文件列表获取脚本')
    parser.add_argument('--prefix', help='文件前缀', default=None)
    parser.add_argument('--limit', help='列举条目数', type=int, default=1000)
    parser.add_argument('--delimiter', help='分隔符', default=None)
    parser.add_argument('--marker', help='标记', default=None)
    parser.add_argument('--raw-json', action='store_true', help='输出原始 JSON 数据')

    args = parser.parse_args()

    files = list_files(args.prefix, args.limit, args.delimiter, args.marker)
    files_with_url = []
    for file in files: # add url
        key = file['key']
        if key.endswith('/'): continue # skip directory
        files_with_url.append({'key':key, 'url':f"{url_prefix}/{quote(file['key'])}"})
    if args.raw_json:
        print(json.dumps(files_with_url, indent=2, ensure_ascii=False))
    else:
        markdown = generate_markdown(files_with_url)
        print(markdown)
