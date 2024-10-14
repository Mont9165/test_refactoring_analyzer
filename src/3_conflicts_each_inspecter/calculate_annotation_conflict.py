import json
from collections import defaultdict


def load_json_file(filepath):
    """Load a JSON file and return its content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filepath}: {e}")
        return None


def find_annotation_discrepancies(annotations):
    """Find discrepancies in annotations (different type for same or overlapping ranges and paths)."""
    discrepancies = defaultdict(list)

    # Group annotations by path, startLine, endLine
    for annot in annotations:
        # Ensure 'path' and 'range' keys exist
        if 'path' in annot and 'range' in annot and 'startLine' in annot['range'] and 'endLine' in annot['range']:
            key = (annot['path'], annot['range']['startLine'], annot['range']['endLine'])
            discrepancies[key].append(annot)
        else:
            print(f"Skipping annotation with missing path or range: {annot}")

    conflicts = []

    # Check for discrepancies in annotation types for the same or overlapping path and range
    for key, annot_list in discrepancies.items():
        types = set([annot['type'] for annot in annot_list])
        if len(types) > 1:
            conflicts.append({
                'path': key[0],
                'startLine': key[1],
                'endLine': key[2],
                'annotations': annot_list
            })

    # Check for overlapping ranges (e.g., if start/end lines are overlapping but not identical)
    for key1, annot_list1 in discrepancies.items():
        for key2, annot_list2 in discrepancies.items():
            if key1 != key2 and key1[0] == key2[0]:  # Check same file (same path)
                # Check if ranges overlap
                if (key1[1] <= key2[2] and key1[2] >= key2[1]):
                    conflicts.append({
                        'path': key1[0],
                        'startLine1': key1[1],
                        'endLine1': key1[2],
                        'startLine2': key2[1],
                        'endLine2': key2[2],
                        'annotations1': annot_list1,
                        'annotations2': annot_list2
                    })

    return conflicts


def save_conflicts_to_file(conflicts, output_file):
    """Save the conflicts to a file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(conflicts, file, indent=4)
    print(f"Conflicts saved to {output_file}")


def main(file_paths, annotators, output_file):
    """Main function to load annotations and check for discrepancies."""
    all_annotations = []

    # Load and collect all annotations from the files
    for file_path, annotator_name in zip(file_paths, annotators):
        json_data = load_json_file(file_path)
        if json_data:
            # Check if json_data is a list or dictionary
            if isinstance(json_data, list):
                # If it's a list, loop through it directly
                for annotation in json_data:
                    annotation['annotator'] = annotator_name
                    all_annotations.append(annotation)
            elif isinstance(json_data, dict):
                # If it's a dictionary, process as originally expected
                for commit_url, annotations in json_data.items():
                    for annotation in annotations:
                        annotation['annotator'] = annotator_name
                        all_annotations.append(annotation)

    # Find discrepancies (conflicting annotations)
    conflicts = find_annotation_discrepancies(all_annotations)

    # Save conflicts to a file
    save_conflicts_to_file(conflicts, output_file)


if __name__ == "__main__":
    # List of JSON files and corresponding annotators
    file_paths = [
        '../../data/RefactorHub/Inspected_data_with_commit_urls_2024-10-14-10-25-07.json',
        '../../data/RefactorHub/Inspected_data_with_commit_urls_2024-10-14-10-25-07.json'
    ]

    annotators = [
        'Alice',
        'Bob'
    ]

    output_file = '../../data/Conflicts_data/annotation_conflicts.json'

    main(file_paths, annotators, output_file)
