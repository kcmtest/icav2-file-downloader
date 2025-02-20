# ICAV2 File Downloader

A Python utility script for downloading files from ICAV2 projects based on file patterns and extensions. This tool is particularly useful for batch downloading specific file types from  illumina connected analytics projects using icav2 cli tool.

## Features

- Search for files using fuzzy pattern matching
- Filter files by single or double extensions (e.g., `.bed`, `.vcf.gz`)
- Interactive confirmation before downloading
- Batch download multiple files
- JSON output 

## Prerequisites

- Python 3.6 or higher
- ICAV2 CLI tool installed and configured
- Valid illumina connected analytics project access and project ID

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

### Test Example

To download .bed and .vcf.gz files containing "Seraseq-v2 Brain" in their names:
```bash
python KCM_ICAv2.py dfd7b3d4-0a20-4614-b587-6068d4c9caa3 "Seraseq-v2 Brain" --extensions .bed .vcf.gz

python added_func_V3.py dfd7b3d4-0a20-4614-b587-6068d4c9caa3 "Brain HD798" --extensions .bed .bai --runs SA500LB_NXP82_LR1
59

Found 5 matching files:
- HD798-10ng-E07C-G12.target_bed_somatic_callable_regions.bed (Run: SA500LB_NXP82_LR159_demux3_U7N1Y143_CTGTCTCTTATACACATCT_downsampledfastq-remaining-analysis-4-b735dbac-3849-42bc-981d-1421b2c3a9bc)
- HD798-10ng-E07C-G12.wgs_somatic_callable_regions.bed (Run: SA500LB_NXP82_LR159_demux3_U7N1Y143_CTGTCTCTTATACACATCT_downsampledfastq-remaining-analysis-4-b735dbac-3849-42bc-981d-1421b2c3a9bc)
- HD798-10ng-E07C-G12.target_bed_cov_report.bed (Run: SA500LB_NXP82_LR159_demux3_U7N1Y143_CTGTCTCTTATACACATCT_downsampledfastq-remaining-analysis-4-b735dbac-3849-42bc-981d-1421b2c3a9bc)
- HD798-10ng-E07C-G12.target_bed_read_cov_report.bed (Run: SA500LB_NXP82_LR159_demux3_U7N1Y143_CTGTCTCTTATACACATCT_downsampledfastq-remaining-analysis-4-b735dbac-3849-42bc-981d-1421b2c3a9bc)
- HD798-10ng-E07C-G12_tumor.bam.bai (Run: SA500LB_NXP82_LR159_demux3_U7N1Y143_CTGTCTCTTATACACATCT_downsampledfastq-remaining-analysis-4-b735dbac-3849-42bc-981d-1421b2c3a9bc)

Are you sure you want to download these files? (y/N): n
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
- `--extensions`: File extensions to filter by (example., .bed .vcf.gz)

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