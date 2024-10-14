# TestRefactorAnalyzer
このプロジェクトは、RefactorHubでアノテーションしたデータを収集し，テストスメルとの関連性を分析するものです．

## ファイル構成
- `data/`: データを格納するディレクトリ
  - `RefactorHub/`: RefactorHubから取得したデータを格納するディレクトリ
  - `TestRefactoring/`: RefactorHubのデータを分析した結果を格納するディレクトリ
- `src/`: ソースコードを格納するディレクトリ
  - `1_test_refactoring_collection/`: RefactorHubからデータを取得するためのスクリプトを格納するディレクトリ
  - `2_test_refactoring_analysis/`: テストリファクタリングの分析を行うスクリプトを格納するディレクトリ


## 使い方
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/1_test_refactoring_collection/collect_data.py
```
