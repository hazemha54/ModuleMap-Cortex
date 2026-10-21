"""
Cross-Workspace Diff Engine using difflib
"""

import difflib
from pathlib import Path
from typing import Dict, List, Tuple


class DiffEngine:
    """Compares files or modules across source and target workspaces"""

    @staticmethod
    def compare_files(file1_path: str, file2_path: str, label1: str = "Source", label2: str = "Target") -> List[str]:
        """Generate unified diff lines between two files"""
        try:
            p1 = Path(file1_path)
            p2 = Path(file2_path)

            lines1 = p1.read_text(encoding="utf-8", errors="ignore").splitlines(keepends=True) if p1.exists() else []
            lines2 = p2.read_text(encoding="utf-8", errors="ignore").splitlines(keepends=True) if p2.exists() else []

            diff = difflib.unified_diff(
                lines1, lines2,
                fromfile=f"{label1}: {p1.name}",
                tofile=f"{label2}: {p2.name}",
                n=3
            )
            return list(diff)
        except Exception as e:
            return [f"Error generating diff: {e}"]

    @staticmethod
    def compare_texts(text1: str, text2: str, label1: str = "Source", label2: str = "Target") -> List[str]:
        """Generate unified diff lines between two text strings"""
        lines1 = text1.splitlines(keepends=True)
        lines2 = text2.splitlines(keepends=True)
        return list(difflib.unified_diff(lines1, lines2, fromfile=label1, tofile=label2, n=3))
