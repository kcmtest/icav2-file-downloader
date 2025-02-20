#!/usr/bin/env python3
import argparse
import subprocess
import json
import re
from pathlib import Path
from typing import List, Set, Tuple, Optional
from collections import defaultdict

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

    def list_files(self, patterns: List[str]) -> List[dict]:
        cmd = [
            self.executable, "projectdata", "list",
            "--match-mode", "FUZZY",
            "--project-id", self.project_id,
            "-o", "json"
        ]
        for pattern in patterns:
            cmd.extend(["--file-name", pattern])

        output = self._run_command(cmd)
        return json.loads(output).get("items", [])

    def download_file(self, file_id: str) -> None:
        cmd = [
            self.executable, "projectdata", "download",
            file_id, "--project-id", self.project_id
        ]
        self._run_command(cmd)

def extract_identifier(path: str) -> str:
    
    match = re.search(r"([^/]+)/", path)  
    if match:
        return match.group(1)  
    return ""


def get_matching_files(files: List[dict], extensions: Set[str], allowed_runs: Set[str]) -> List[Tuple[str, str, str]]:
    matching = []
    for file in files:
        filename = file.get("details", {}).get("name", "")
        path = file.get("details", {}).get("path", "")

        if not filename or not path:
            continue

        identifier = extract_identifier(path)
        
        name_parts = filename.split(".")
        if len(name_parts) > 1:
            double_ext = f".{'.'.join(name_parts[-2:]).lower()}"
            single_ext = f".{name_parts[-1].lower()}"

            if (double_ext in extensions or single_ext in extensions) and any(identifier.startswith(run) for run in allowed_runs):
                matching.append((file["id"], filename, identifier))

    return matching



def main():
    parser = argparse.ArgumentParser(description="Download files using icav2.")
    parser.add_argument("project_id", help="Project ID")
    parser.add_argument("file_patterns", nargs="+", help="Search patterns")
    parser.add_argument("--extensions", nargs="+", required=True, 
                        help="File extensions (e.g., .bam, .vcf.gz, .bed)")
    parser.add_argument("--runs", nargs="*", help="Specific run identifiers to filter (optional)")

    args = parser.parse_args()

    try:
        downloader = KCMICAV2(args.project_id)
        files = downloader.list_files(args.file_patterns)
        extensions = {f".{ext.lstrip('.').lower()}" for ext in args.extensions}
        allowed_runs = set(args.runs) if args.runs else None

        matching_files = get_matching_files(files, extensions, allowed_runs)

        if not matching_files:
            print(f"No files found matching extensions: {', '.join(extensions)}")
            if allowed_runs:
                print(f"Filtering was applied for runs: {', '.join(allowed_runs)}")
            return

        print(f"\nFound {len(matching_files)} matching files count:")
        for _, filename, identifier in matching_files:
            print(f"- {filename} (Run: {identifier})")

        if input("\nAre you sure you want to download these files? (y/N): ").lower() != 'y':
            print("Download canceled.")
            return

        for file_id, filename, identifier in matching_files:
            print(f"\nDownloading file one by one: {filename} (Run: {identifier})")
            downloader.download_file(file_id)

    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
