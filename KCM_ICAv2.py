#!/usr/bin/env python3
import argparse
import subprocess
import json
from pathlib import Path
from typing import List, Set, Tuple

class KCMICAV2:
    def __init__(self, project_id: str, executable: str = "./icav2.exe"):
        self.project_id = project_id
        self.executable = executable
        
    def _run_command(self, cmd: List[str]) -> str:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command not working: {e.stderr}")

    def list_files(self, patternss: List[str]) -> List[dict]:
        cmd = [
            self.executable, "projectdata", "list",
            "--match-mode", "FUZZY",
            "--project-id", self.project_id,
            "-o", "json"
        ]
        for pattern in patternss:
            cmd.extend(["--file-name", pattern])
            
        output = self._run_command(cmd)
        return json.loads(output).get("items", [])

    def download_file(self, file_id: str) -> None:
        cmd = [
            self.executable, "projectdata", "download",
            file_id, "--project-id", self.project_id
        ]
        self._run_command(cmd)

def get_matching_files(files: List[dict], extensions: Set[str]) -> List[Tuple[str, str]]:
    matching = []
    for file in files:
        filename = file.get("details", {}).get("name", "")
        if not filename:
            continue
            
        name_parts = filename.split(".")
        if len(name_parts) > 1:
            double_ext = f".{'.'.join(name_parts[-2:]).lower()}"
            single_ext = f".{name_parts[-1].lower()}"
            if double_ext in extensions or single_ext in extensions:
                matching.append((file["id"], filename))
    return matching

def main():
    parser = argparse.ArgumentParser(description="Download files using icav2.")
    parser.add_argument("project_id", help="Project ID")
    parser.add_argument("file_patterns", nargs="+", help="Search patterns")
    parser.add_argument("--extensions", nargs="+", required=True, 
                       help="File extensions (like., .bam .vcf.gz.bed)")
    
    args = parser.parse_args()
    
    try:
        downloader = KCMICAV2(args.project_id)
        
        files = downloader.list_files(args.file_patterns)
        extensions = {f".{ext.lstrip('.').lower()}" for ext in args.extensions}
        matching_files = get_matching_files(files, extensions)
        
        if not matching_files:
            print(f"No files found matching extensions: {', '.join(extensions)}")
            return
        
        print(f"\nThere are {len(matching_files)} matching files:")
        for _, filename in matching_files:
            print(f"- {filename}")
            
        if input("\nare you sure  these files? (y/N): ").lower() != 'y':
            print("canceled.")
            return
        
        for file_id, filename in matching_files:
            print(f"\nDownloading one by one : {filename}")
            downloader.download_file(file_id)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())