"""Core disk analyzer functionality."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

@dataclass
class Entry:
    path: str
    size: int

def get_size(path: str) -> int:
    """Return size in bytes for a file or directory recursively."""
    if os.path.isfile(path):
        return os.path.getsize(path)
    total = 0
    for root, dirs, files in os.walk(path, topdown=True, onerror=None):
        for f in files:
            fp = os.path.join(root, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
    return total

def find_largest_entries(path: str, top_n: int = 10) -> List[Entry]:
    """Return the largest entries under *path*.

    Parameters
    ----------
    path : str
        Directory to scan.
    top_n : int, default 10
        Number of entries to return.

    Returns
    -------
    List[Entry]
        List sorted by size descending.
    """
    entries: List[Entry] = []
    with os.scandir(path) as it:
        for entry in it:
            try:
                size = get_size(entry.path)
            except OSError:
                # skip items we cannot access
                continue
            entries.append(Entry(entry.path, size))
    entries.sort(key=lambda e: e.size, reverse=True)
    return entries[:top_n]

