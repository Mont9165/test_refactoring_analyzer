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


def extract_refactoring_info(annotation, annotator_name):
    """Extract the relevant refactoring information: Type, Code location, and Annotator."""
    type_name = annotation.get('Type Name', 'Unknown Type')
    refactorings = []

    # Safely extract 'after' added codes (handle cases where the key doesn't exist)
    after_codes = annotation.get('Parameter Data', {}).get('after', {}).get('added codes', {}).get('elements', [])

    for code in after_codes:
        location = code.get('location', {})
        path = location.get('path', 'unknown path')
        range_info = location.get('range', {})
        refactorings.append({
            'type': type_name,
            'path': path,
            'range': range_info,
            'annotator': annotator_name  # Add the annotator's name
        })

    return refactorings


def aggregate_annotations_by_commit(json_data, annotator_name):
    """Aggregate annotations by commit URL and include annotator's name."""
    commit_data = defaultdict(list)
    for annotation in json_data:
        commit_url = annotation.get('Commit URL', 'unknown commit')
        refactoring_info = extract_refactoring_info(annotation, annotator_name)
        if refactoring_info:
            commit_data[commit_url].extend(refactoring_info)
    return commit_data


def main(file_paths, annotators, output_file):
    """Main function to aggregate annotations from multiple JSON files."""
    aggregated_data = defaultdict(list)

    # Load and aggregate data from all provided files, associating with annotator names
    for file_path, annotator_name in zip(file_paths, annotators):
        json_data = load_json_file(file_path)
        if json_data:
            commit_data = aggregate_annotations_by_commit(json_data, annotator_name)
            for commit_url, refactorings in commit_data.items():
                aggregated_data[commit_url].extend(refactorings)

    # Save the aggregated results to a JSON file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        json.dump(aggregated_data, out_file, indent=4)

    print(f"Aggregated data saved to {output_file}")


if __name__ == "__main__":
    # List of JSON files to be aggregated and corresponding annotators
    file_paths = [
        '../../data/RefactorHub/Inspected_data_with_commit_urls_2024-10-14-10-25-07.json',
        '../../data/RefactorHub/Inspected_data_with_commit_urls_2024-10-14-10-25-07.json'
    ]

    # List of annotators corresponding to the file_paths
    annotators = [
        'Alice',
        'Bob'
    ]

    output_file = '../../data/Conflicts_data/aggregated_annotations_by_commit_test.json'

    main(file_paths, annotators, output_file)
