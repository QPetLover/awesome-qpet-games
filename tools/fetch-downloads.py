#!/usr/bin/env python3
"""Download package files listed in metadata/downloads.yml."""

from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = ROOT / 'metadata/downloads.yml'
UA = 'awesome-qq-pet-fetch-downloads/1.0'


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def yaml_quote(value: object) -> str:
    if value is None:
        return '""'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, int):
        return str(value)
    text = str(value)
    if text == '':
        return '""'
    return json.dumps(text, ensure_ascii=False)


def items_to_yaml(items: list[dict[str, object]]) -> str:
    lines: list[str] = []
    for item in items:
        first = True
        for key, value in item.items():
            prefix = '- ' if first else '  '
            first = False
            lines.append(f'{prefix}{key}: {yaml_quote(value)}')
    return '\n'.join(lines) + '\n'


def parse_scalar(value: str) -> object:
    value = value.strip()
    if value == '""':
        return ''
    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value.strip('"')
    if value.isdigit():
        return int(value)
    return value


def get_items() -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    cur: dict[str, object] = {}
    for line in DOWNLOADS.read_text(encoding='utf-8').splitlines():
        if line.startswith('- '):
            if cur:
                items.append(cur)
            cur = {}
            line = line[2:]
        elif line.startswith('  '):
            line = line[2:]
        else:
            continue
        if ': ' in line:
            key, value = line.split(': ', 1)
            cur[key] = parse_scalar(value)
    if cur:
        items.append(cur)
    return items


def extension_from_url(url: str, title: str) -> str:
    for value in (urllib.parse.urlparse(url).path, title):
        name = urllib.parse.unquote(value.rsplit('/', 1)[-1])
        if '.' in name:
            ext = '.' + name.rsplit('.', 1)[-1]
            if 2 <= len(ext) <= 10:
                return ext
    return '.bin'


def dest_for(item: dict[str, object]) -> Path:
    item_id = str(item.get('id', 'download'))
    title = str(item.get('title', ''))
    url = str(item.get('url', ''))
    return ROOT / 'archive/downloads' / f'{item_id}{extension_from_url(url, title)}'


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        print(f'skip existing {dest.relative_to(ROOT)}')
        return
    tmp = dest.with_suffix(dest.suffix + '.part')
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=120) as r, tmp.open('wb') as f:
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
    tmp.replace(dest)
    print(f'downloaded {dest.relative_to(ROOT)}')


def rewrite_checksums() -> None:
    lines = []
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '.git' not in p.parts and not p.name.endswith('.part'):
            rel = p.relative_to(ROOT)
            if str(rel) == 'metadata/checksums.sha256':
                continue
            lines.append(f'{sha256_file(p)}  {rel.as_posix()}')
    (ROOT / 'metadata/checksums.sha256').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> int:
    items = get_items()
    for item in items:
        url = str(item.get('url', ''))
        if not url:
            continue
        dest = dest_for(item)
        for attempt in range(3):
            try:
                download(url, dest)
                item['local_path'] = str(dest.relative_to(ROOT))
                item['sha256'] = sha256_file(dest)
                item['size_bytes'] = dest.stat().st_size
                item['archive_status'] = 'archived-lfs'
                break
            except Exception as exc:  # noqa: BLE001
                print(f'failed attempt {attempt + 1}: {item.get("label", url)}: {exc}', file=sys.stderr)
                time.sleep(2 * (attempt + 1))
        else:
            item['archive_status'] = 'download-failed'
            DOWNLOADS.write_text(items_to_yaml(items), encoding='utf-8')
            return 1
    DOWNLOADS.write_text(items_to_yaml(items), encoding='utf-8')
    rewrite_checksums()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
