# TestRefactorAnalyzer
このプロジェクトは、RefactorHubでアノテーションしたデータを収集し，テストスメルとの関連性を分析するものです．

## ファイル構成
- `data/`: データを格納するディレクトリ
  - `RefactorHub/`: RefactorHubから取得したデータを格納するディレクトリ
  - `TestRefactoring/`: RefactorHubのデータを分析した結果を格納するディレクトリ
- `src/`: ソースコードを格納するディレクトリ
  - `1_test_refactoring_collection/`: RefactorHubからデータを取得するためのスクリプトを格納するディレクトリ
  - `2_test_refactoring_analysis/`: テストリファクタリングの分析を行うスクリプトを格納するディレクトリ
  - `3_smell_analysis/`: テストリファクタリングとテストスメルの関連性分析を行うスクリプトを格納するディレクトリ**(改良中)**

## 使い方
1. get_json_from_refactorhub.pyを実行し，RefactorHubからデータを取得する．
2. count_each_test_refactoring.pyを実行し，テストリファクタリングの数をカウントする．