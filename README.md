# Awesome QPet Games

QQ 宠物小游戏与相关资源收集、整理与怀旧归档仓库。

This repository collects, preserves, indexes, and documents QQ Pet game-related resources, including mini games, Flash/SWF files, covers, screenshots, historical pages, installers, packages, and community-sourced materials.

> 非官方项目。本仓库不隶属于腾讯、QQ 或 QQ 宠物官方。

## 当前收录

- 经典小游戏：从 QPetGames 索引和公开 CDN 链接归档 SWF 与封面。
- 换壳小游戏：从 QPetGames 归档 SWF 与封面。
- Q 宠 13 周年页面：归档页面源码和运行资源。
- QPetLover 下载页：索引 Q宠宝贝安装包；大文件使用 Git LFS 归档。
- 来源快照：保留 QPetGames 和 download 仓库中的关键说明、页面和脚本。

QQ 宠物冒险岛单独维护在 [`QPetLover/qqpet-adventure`](https://github.com/QPetLover/qqpet-adventure)，因为它更适合作为独立文件仓库和部署站点。

## Resource Index

| Index | Description |
| --- | --- |
| `metadata/resources.yml` | General archived resource index |
| `metadata/games.yml` | Game-specific index |
| `metadata/downloads.yml` | QPetLover download/CDN package index |
| `metadata/sources.yml` | Source and credit policy index |
| `metadata/checksums.sha256` | Checksums for files stored in this repository |

## Directory Layout

```text
archive/
  downloads/        # large packages, tracked by Git LFS
  games/
    classic/        # classic QQ Pet games
    reskin/         # reskin games
  projects/
    qqpet13/        # QQ Pet 13th anniversary page files
  source-snapshots/ # lightweight source/context snapshots
metadata/
docs/
tools/
```

## Sources And Credits

资源主要来自 QQ 宠物社区补档、QQ 宠物贴吧/公开页面、个人贡献者、公开镜像、CDN 镜像，以及 QPetLover 现有公开仓库。

QQ 群来源只做整体致谢，不公开具体 QQ 群号、QQ 号或群成员昵称，除非相关成员明确要求公开署名。

See [`CREDITS.md`](CREDITS.md) and [`metadata/sources.yml`](metadata/sources.yml).

## Large Files

Installers, DMG files, ZIP files, and RAR files are tracked with Git LFS. Small SWF, image, HTML, JavaScript, JSON, and Markdown files are committed directly unless they become too large.

## Safety

Historical binaries such as SWF, EXE, DMG, ZIP, and RAR files may be unsafe to run directly. Prefer Ruffle, a virtual machine, or a sandbox.

See [`SECURITY.md`](SECURITY.md).

## Notice

This repository is for nostalgia, historical preservation, documentation, indexing, learning, and research. It is not intended for commercial use.

Original QQ Pet related assets belong to their respective rights holders. If you are a rights holder or need a credit/takedown correction, please open an issue.
