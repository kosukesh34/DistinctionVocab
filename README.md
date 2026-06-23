# Distinction Vocab

[Distinction App](https://distinction.atsueigo.com/app) 風の英単語学習アプリ（SwiftUI）。

## 機能

- **ブック**: Distinction I〜VI の単語一覧（計 2,128 語）
- **単語詳細**: 見出し語の表示と音声再生、例文（B/C/D）の音声再生
- **学習モード**: フラッシュカード形式の学習
- **検索**: 全ブック横断の見出し語検索

## セットアップ

### クローン（音声データ含む）

音声ファイル（約 1.1GB）は Git LFS で管理しています。

```bash
git clone https://github.com/kosukesh34/DistinctionVocab.git
cd DistinctionVocab
git lfs pull
```

### Xcode でビルド

1. `DistinctionVocab/DistinctionVocab.xcodeproj` を Xcode で開く
2. シミュレータまたは実機で Run

### 音声データの再生成（ZIP から展開する場合）

`~/Downloads/` に ZIP を置いて実行:

```bash
python3 scripts/generate_catalog.py
```

## プロジェクト構成（クリーンアーキテクチャ）

```
DistinctionVocab/
├── App/                    # Composition Root（DI）
├── Domain/                 # エンティティ・リポジトリIF・ユースケース
│   ├── Entities/
│   ├── Repositories/
│   └── UseCases/
├── Data/                   # DTO・マッパー・リポジトリ実装
│   ├── DTOs/
│   ├── Mappers/
│   ├── DataSources/
│   └── Repositories/
├── Infrastructure/         # 外部フレームワーク（AVFoundation 等）
└── Presentation/           # View / ViewModel
```

### SOLID の適用

| 原則 | 適用例 |
|------|--------|
| **S** 単一責任 | `LoadVocabularyUseCase` は読み込みのみ、`AVAudioPlaybackService` は再生のみ |
| **O** 開放/閉鎖 | リポジトリをプロトコル経由で差し替え可能 |
| **L** リスコフ置換 | `BundleVocabularyRepository` を `VocabularyRepositoryProtocol` として注入 |
| **I** インターフェース分離 | `AudioPlaybackManaging` と `AudioResourceRepositoryProtocol` を分離 |
| **D** 依存性逆転 | ViewModel → UseCase → RepositoryProtocol（具象は `DependencyContainer` で注入） |
