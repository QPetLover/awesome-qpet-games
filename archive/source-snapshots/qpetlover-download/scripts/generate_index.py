#!/usr/bin/env python3
import json
import os

# 读取 data.json 文件
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    data.sort(key=lambda x: x['key'], reverse=True)
    
# 创建输出目录
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 生成目录结构和 HTML 页面
files = {}
for item in data:
    parts = item['key'].split('/')
    current = files
    for part in parts[:-1]:
        current = current.setdefault(part, {})
    current[parts[-1]] = item['url']

def generate_html(directory, path=''):
    html = '<html><head><meta charset="utf-8"><title>Index of {}</title></head><body><ul>'.format(path)
    for name, value in sorted(directory.items()):
        if isinstance(value, dict):
            sub_path = os.path.join(path, name)
            sub_dir = os.path.join(output_dir, sub_path)
            if not os.path.exists(sub_dir):
                os.makedirs(sub_dir)
            html += f'<li><a href="{name}/index.html">{name}</a></li>'
            generate_html(value, sub_path)
        else:
            html += f'<li><a href="{value}">{name}</a></li>'
    html += '</ul></body></html>'
    
    index_path = os.path.join(output_dir, path, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)

generate_html(files)

# 生成根目录的HTML
html = '<html><head><meta charset="utf-8"><title>QPetLover 下载页</title></head><body><h1>Q宠相关资源</h1><ul>'
for item in data:
    html += f'<li><a href="{item["url"]}">{item["key"]}</a></li>'
html += '</ul></body></html>'

index_path = os.path.join(output_dir, 'index.html')
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML files generated successfully.")
