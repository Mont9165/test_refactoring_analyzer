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


def save_commit_info_json(output_file, data):
    commit_info = {}

    for row in data:
        commit_url = row['Commit URL']
        type_name = row['Type Name']

        if commit_url not in commit_info:
            commit_info[commit_url] = {
                "refactorings": {},
                "non_refactoring_count": 0
            }

        if type_name == 'Non-Refactoring':
            commit_info[commit_url]["non_refactoring_count"] += 1
        else:
            if type_name in commit_info[commit_url]["refactorings"]:
                commit_info[commit_url]["refactorings"][type_name] += 1
            else:
                commit_info[commit_url]["refactorings"][type_name] = 1

    # Write the results to a JSON file
    output_data = {
        "commit_info": commit_info
    }

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)


def save_json(output_file, data):
    refactoring_info = {}
    non_refactoring_count = 0

    for row in data:
        type_name = row['Type Name']
        repo_name = extract_owner_and_repo(row['Commit URL'])

        if type_name == 'Non-Refactoring':
            non_refactoring_count += 1
        else:
            if type_name in refactoring_info:
                refactoring_info[type_name] += 1
            else:
                refactoring_info[type_name] = 1

    # 結果をJSONファイルに書き込む
    output_data = {
        "refactoring_info": refactoring_info,
        "non_refactoring_count": non_refactoring_count,
        "total_count": sum(refactoring_info.values()) + non_refactoring_count
    }

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)


def main():
    # TODO change the file path
    file_name = "Inspected_data_with_commit_urls_2024-10-14-10-25-07.json"

    file_path = '../../data/RefactorHub/' + file_name
    commits_output_file = '../../data/TestRefactoring/number_of_each_test_refactoring_types.json'
    output_file = '../../data/TestRefactoring/test_refactorings_each_commits.json'
    data = load_json(file_path)
    save_commit_info_json(commits_output_file, data)
    save_json(output_file, data)


if __name__ == '__main__':
    main()
