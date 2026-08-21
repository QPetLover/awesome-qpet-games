#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = root / 'metadata/checksums.sha256'
errors: list[str] = []

for line in manifest.read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    digest, rel = line.split('  ', 1)
    path = root / rel
    if not path.exists():
        errors.append(f'missing: {rel}')
        continue
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    if h.hexdigest() != digest:
        errors.append(f'mismatch: {rel}')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print('checksums ok')
