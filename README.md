# disk_analyzer

A disk analyzer in Python.

It efficiently finds the biggest files and folders on a file system. Has a dedicated API for both Windows, Linux and MacOS.

## Usage

```python
from disk_analyzer import find_largest_entries

for entry in find_largest_entries('/path/to/scan', top_n=5):
    print(entry.path, entry.size)
```
