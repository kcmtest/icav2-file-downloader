# ICAV2 File Downloader

A Python utility script for downloading files from ICAV2 projects based on file patterns and extensions. This tool is particularly useful for batch downloading specific file types from ICAV2 projects.

## Features

- Search for files using fuzzy pattern matching
- Filter files by single or double extensions (e.g., `.bed`, `.vcf.gz`)
- Interactive confirmation before downloading
- Batch download multiple files
- JSON output support

## Prerequisites

- Python 3.6 or higher
- ICAV2 CLI tool installed and configured
- Valid ICAV2 project access and project ID

## Installation

1. Clone this repository:
```bash
git clone https://github.com/kcmtest/icav2-file-downloader.git
cd icav2-file-downloader
```

2. Ensure you have the ICAV2 CLI tool installed and properly configured.

## Usage

Basic syntax:
```bash
python KCM_ICAv2.py PROJECT_ID [FILE_PATTERNS ...] --extensions [EXTENSIONS ...]
```

### Real-world Example

To download .bed and .vcf.gz files containing "Seraseq-v2 Brain" in their names:
```bash
python KCM_ICAv2.py dfd7b3d4-0a20-4614-b587-6068d4c9caa3 "Seraseq-v2 Brain" --extensions .bed .vcf.gz
```

This command will:
1. Connect to the specified project (dfd7b3d4-0a20-4614-b587-6068d4c9caa3)
2. Search for files containing "Seraseq-v2 Brain" in their names
3. Filter for files ending in either .bed or .vcf.gz
4. Display matching files
5. Prompt for confirmation before downloading
6. Download the confirmed files

### Arguments

- `PROJECT_ID`: Your ICAV2 project identifier (UUID format)
- `FILE_PATTERNS`: One or more file name patterns to search for (use quotes for patterns with spaces)
- `--extensions`: File extensions to filter by (include the dot, e.g., .bed .vcf.gz)

## Error Handling

The script includes error handling for:
- Invalid command execution
- File not found
- Permission issues
- Invalid project ID
- ICAV2 CLI tool errors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.