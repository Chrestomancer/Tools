import os
import argparse
from pathlib import Path
from logging import basicConfig, getLogger

def get_files(directory, include_subdirs, include_patterns, exclude_patterns):
    files = []
    for root, _, filenames in os.walk(directory):
        if not include_subdirs and root != directory:
            continue
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if Path(filepath).is_file():
                if (not include_patterns or any(Path(filename).match(pat) for pat in include_patterns)) and \
                   (not exclude_patterns or not any(Path(filename).match(pat) for pat in exclude_patterns)):
                    files.append(filepath)
    return files

def process_file(filepath, outfile, log, encoding='utf-8'):
    try:
        with open(filepath, 'r', encoding=encoding) as infile:
            for line in infile:
                outfile.write(line)
    except Exception as e:
        log.warning(f"Skipping {filepath}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Combine multiple files into a single file.")
    parser.add_argument('directory', help="Directory containing files to combine")
    parser.add_argument('output_file', help="Output file path")
    parser.add_argument('--include-subdirs', action='store_true', help="Include subdirectories")
    parser.add_argument('--include-patterns', nargs='*', help="Patterns of files to include")
    parser.add_argument('--exclude-patterns', nargs='*', help="Patterns of files to exclude")
    parser.add_argument('--log-file', default='file_combiner.log', help="Log file path")
    args = parser.parse_args()

    basicConfig(filename=args.log_file, level='INFO', format='%(asctime)s - %(levelname)s - %(message)s')
    log = getLogger()

    files = get_files(args.directory, args.include_subdirs, args.include_patterns, args.exclude_patterns)
    log.info(f"Files to be combined: {len(files)}")

    if files:
        with open(args.output_file, 'w', encoding='utf-8') as outfile:
            for file in files:
                process_file(file, outfile, log)
                log.info(f"Processed {file}")
    else:
        log.info("No files to combine.")

if __name__ == "__main__":
    main()
