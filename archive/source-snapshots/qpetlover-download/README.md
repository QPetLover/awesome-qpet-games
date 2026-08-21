# CDN 资源管理

使用七牛云作为 CDN 服务，管理静态资源。

## 基本用法

安装 Python 依赖：

```bash
pip install qiniu tqdm
```

主要脚本：

- `get_list_files.py`：获取 `prefix` 目录下的文件列表
- `upload_single_file.py`：上传单个文件
- `upload_path.py`：上传目录中的所有文件
- `fetch_file.py`：通过链接拉取文件
- `generate_index.py`：生成网站索引

使用 `-h` 可以查看脚本用法。

### 配置环境变量

环境变量：

```bash
export QINIU_ACCESS_KEY=''
export QINIU_SECRET_KEY=''
export QINIU_BUCKET_NAME=''
export QINIU_URL_PREFIX='' 
```

## 使用示例

上传单个文件：

```bash
python upload_single_file.py demo.svg
```

![upload_single_file](assets/upload_single.svg)

上传目录下的所有文件：

```bash
python upload_path.py assets
```

![upload_path](assets/upload_path.svg)

查看目录下的文件：

```bash
python get_list_files.py --prefix assets
```

![get_list_files](assets/get_list.svg)

通过链接拉取文件：

```bash
python fetch_file.py https://github.com/QPetLover/download/blob/main/scripts/assets/demo.svg demo.svg
```

![fetch_file](assets/fetch_file.svg)

一些情况，比如通过 GitHub Action 生成的文件，可通过链接拉取，而不必先下载再上传。

## 注意事项

默认地，文件/文件夹的相对路径将作为链接的相对路径，单个文件可用 `--prefix` 指定上传后的链接路径。

方便起见，可将脚本放到 `PATH` 路径中，比如

```bash
# export PATH=$PATH:$HOME/.local/bin
cp scripts/upload_path.py $HOME/.local/bin/upload_path
```

或者：

```bash
ln -s scripts/upload_path.py $HOME/.local/bin/upload_path
```

然后在需要的目录下直接运行命令。

## 生成网站索引

主要用于 GitHub Action 的自动生成：

```bash
python get_list_files.py --prefix Q宠宝贝 --raw-json > data.json
python generate_index.py
```