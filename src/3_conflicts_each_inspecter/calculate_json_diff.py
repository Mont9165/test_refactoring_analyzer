import json
import os


def load_json_file(filepath):
    """Load a JSON file and return its content."""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {filepath}")
        return None


def compare_json(json1, json2):
    """Compare two JSON objects and return a list of differences."""
    differences = []
    max_length = max(len(json1), len(json2))

    for index in range(max_length):
        if index < len(json1) and index < len(json2):
            if json1[index] != json2[index]:
                differences.append((index, json1[index], json2[index]))
        elif index >= len(json1):
            differences.append((index, None, json2[index]))
        else:
            differences.append((index, json1[index], None))

    return differences


def save_differences_to_file(differences, output_file):
    """Save the differences to a file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        if differences:
            for index, item1, item2 in differences:
                file.write(f"Difference at index {index}:\n")
                file.write("File 1:\n")
                file.write(json.dumps(item1, indent=2) if item1 is not None else "No data")
                file.write("\nFile 2:\n")
                file.write(json.dumps(item2, indent=2) if item2 is not None else "No data")
                file.write("\n\n")
        else:
            file.write("The JSON files are identical.\n")

    print(f"Differences saved to {output_file}")


def main(file1, file2, output_file):
    """Main function to load and compare two JSON files."""
    json1 = load_json_file(file1)
    json2 = load_json_file(file2)

    if json1 is None or json2 is None:
        print("Error loading JSON files.")
        return

    differences = compare_json(json1, json2)

    if differences:
        for index, item1, item2 in differences:
            print(f"Difference at index {index}:")
            print("File 1:", json.dumps(item1, indent=2) if item1 is not None else "No data")
            print("File 2:", json.dumps(item2, indent=2) if item2 is not None else "No data")
    else:
        print("The JSON files are identical.")

    # Save differences to a file
    save_differences_to_file(differences, output_file)


if __name__ == "__main__":
    # Replace these paths with the actual paths of your JSON files and the output file
    file1 = '../../data/RefactorHub/Inspected_data_with_commit_urls_2024-10-14-10-25-07.json'
    file2 = '../../data/RefactorHub/Inspected_data_with_commit_urls_2024-10-14-10-25-07.json'
    output_file = '../../data/Conflicts_data/result/differences_output.txt'

    main(file1, file2, output_file)
