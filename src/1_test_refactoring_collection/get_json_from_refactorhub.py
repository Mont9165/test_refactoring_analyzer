import json
import os.path
from datetime import datetime
from os import getenv
import psycopg2


def save_to_json(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    conn = psycopg2.connect(
        database="refactorhub",
        user="rhuser",
        password="rhpass",
        host="localhost",
        port="5433"
    )
    cursor = conn.cursor()

    # SQLクエリを実行してすべてのchange_idと対応するコミットURLを取得
    query = """
    SELECT ch.id, ch.snapshot_id, ch.order_index, ch.type_name, ch.description, ch.parameter_data, c.url
    FROM changes ch
    JOIN snapshots s ON ch.snapshot_id = s.id
    JOIN annotations a ON s.annotation_id = a.id
    JOIN commits c ON a.commit_id = c.id;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    data = []
    for row in rows:
        change_id, snapshot_id, order_index, type_name, description, parameter_data, commit_url = row
        data.append({
            "Change ID": change_id,
            "Snapshot ID": snapshot_id,
            "Order Index": order_index,
            "Type Name": type_name,
            "Description": description,
            "Parameter Data": parameter_data,
            "Commit URL": commit_url
        })
    now = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    save_to_json(data, filename='../../data/RefactorHub/Inspected_data_with_commit_urls_' + now + '.json')


if __name__ == '__main__':
    main()
