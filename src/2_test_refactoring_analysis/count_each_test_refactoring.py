import json
import os
from urllib.parse import urlparse


def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def extract_owner_and_repo(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    owner, repo = path.split('/')[1:3]
    return owner + "/" + repo


def main():
    file_path = '../../data/RefactorHub/Inspected_changes_with_commit_urls.json'
    output_file = '../../data/TestRefactoring/refactoring_info.json'
    data = load_json(file_path)

    repo_dict = {}
    refactoring_info = {}
    for row in data:
        type_name = row['Type Name']
        if type_name == 'Non-Refactoring':
            continue
        repo_name = extract_owner_and_repo(row['Commit URL'])
        refactoring_type = row['Type Name']

        if refactoring_type in refactoring_info:
            refactoring_info[refactoring_type] += 1
        else:
            refactoring_info[refactoring_type] = 1

    # 結果をJSONファイルに書き込む
    output_data = {
        "refactoring_info": refactoring_info,
        "total_count": sum(refactoring_info.values())
    }

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)

    print(f"Results written to {output_file}")


if __name__ == '__main__':
    main()
