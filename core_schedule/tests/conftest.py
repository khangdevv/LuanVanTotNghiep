import io
import sys

# Fix encoding cho Windows terminal (cp1252 không encode được tiếng Việt)
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
