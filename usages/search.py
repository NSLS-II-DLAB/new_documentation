import os
import re
import argparse
import sys

def find_keywords_in_file(file_path, keywords):
    result = {}
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        for line_number, line in enumerate(lines, 1):
            for keyword in keywords:
                if keyword == 't':
                    if re.match(r'^t\d+', line.strip()):
                        if keyword not in result:
                            result[keyword] = []
                        result[keyword].append((line.strip(), line_number))
                elif keyword == 'l':
                    if re.match(r'^l\d+', line.strip()):
                        loop_start_line = line_number
                        for sub_line_number in range(line_number + 1, len(lines)):
                            if lines[sub_line_number].strip() == 'n':
                                if keyword not in result:
                                    result[keyword] = []
                                result[keyword].append((line.strip(), loop_start_line))
                                result[keyword].append((lines[sub_line_number].strip(), sub_line_number + 1))
                                break
                else:
                    if re.match(rf'^{keyword}\b', line.strip()):
                        if keyword not in result:
                            result[keyword] = []
                        result[keyword].append((line.strip(), line_number))
    return result

def write_output(output_path, results, keywords, file_paths, simple):
    with open(output_path, 'w') as output_file:
        for keyword in keywords:
            if keyword in results:
                occurrences = len(results[keyword])
                output_file.write(f"--- {keyword} --- occurrence: {occurrences}\n")
                if not simple:
                    for line, file_path in zip(results[keyword], file_paths[keyword]):
                        output_file.write(f"{line[0]} (found in {file_path}, line {line[1]})\n")
                output_file.write("\n\n\n")  

def get_keywords_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def search_directory(directory, keywords):
    results = {}
    file_paths = {}
    
    for keyword in keywords:
        print(f"\n--- Searching for keyword '{keyword}' ---")  
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    relative_file_path = os.path.relpath(file_path, directory)
                    keyword_results = find_keywords_in_file(file_path, [keyword])
                    for key, lines in keyword_results.items():
                        if key not in results:
                            results[key] = []
                            file_paths[key] = []
                        results[key].extend(lines)
                        file_paths[key].extend([relative_file_path] * len(lines))
        
        print("\n")  

    return results, file_paths

def main():
    parser = argparse.ArgumentParser(description="Search text files for keywords and output results.")
    parser.add_argument('source', help="Source directory to search")
    parser.add_argument('--keywords', nargs='+', help="List of keywords to search for")
    parser.add_argument('--keywords-file', help="Path to a file containing keywords (one per line)")
    parser.add_argument('--output', help="Output file path", required=True)
    parser.add_argument('--simple', action='store_true', help="Only count occurrences and don't print full matches")
    
    args = parser.parse_args()

    if args.keywords_file:
        keywords = get_keywords_from_file(args.keywords_file)
    elif args.keywords:
        keywords = args.keywords
    else:
        print("You must provide either a list of keywords or a file containing keywords.")
        return

    print("Starting search...")
    results, file_paths = search_directory(args.source, keywords)
    
    print("Writing results to output file...")
    write_output(args.output, results, keywords, file_paths, args.simple)
    print("Search complete! Results saved to", args.output)

if __name__ == "__main__":
    main()
