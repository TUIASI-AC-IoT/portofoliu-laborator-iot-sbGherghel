import os
from pathlib import Path
from typing import List, Optional


class FileManager:
    def __init__(self, base_dir: str = "files"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)

    def list_files(self) -> List[str]:
        """List all files in the directory"""
        return [f.name for f in self.base_dir.iterdir() if f.is_file()]

    def read_file(self, filename: str) -> str:
        """Read content of a text file"""
        file_path = self.base_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File {filename} not found")
        return file_path.read_text()

    def create_file(self, filename: Optional[str], content: str) -> str:
        """Create a new file with given content"""
        if not filename:
            # Generate a unique filename if none provided
            filename = f"file_{len(self.list_files()) + 1}.txt"

        file_path = self.base_dir / filename
        if file_path.exists():
            raise FileExistsError(f"File {filename} already exists")

        file_path.write_text(content)
        return filename

    def update_file(self, filename: str, content: str) -> None:
        """Update content of an existing file"""
        file_path = self.base_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File {filename} not found")
        file_path.write_text(content)

    def delete_file(self, filename: str) -> None:
        """Delete a file"""
        file_path = self.base_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File {filename} not found")
        file_path.unlink()