# DVD Rental API



## プロジェクト概要

Django 6.0.1 + Django REST Framework で構築された、完全な DVD レンタルサービス RESTful API で、映画、俳優、顧客、レンタルなどのデータ管理インターフェースを提供します。

### 技術スタック

- **Python**: 3.13.9
- **Django**: 6.0.1
- **Django REST Framework**: 3.16.1
- **データベース**: PostgreSQL 17.6 (Docker)
- **パッケージ管理**: uv
- **API ドキュメント**: drf-spectacular (OpenAPI 3.0/Swagger)

### コア機能

- ✅ RESTful API 設計
- ✅ Django Admin 管理画面（13 モデルの可視化管理）
- ✅ 自動ページネーション（1ページ 20 件）
- ✅ 検索機能（キーワード検索）
- ✅ フィルタリング機能（フィールドフィルタ）
- ✅ ソート機能（複数フィールドソート）
- ✅ OpenAPI ドキュメント（Swagger UI + ReDoc）
- ✅ ORM クエリ最適化（select_related）

## プロジェクト構造

```
django-crud/
├── dvd_rental/          # Django プロジェクト設定
│   ├── settings.py      # 設定ファイル
│   ├── urls.py          # メインルーティング
│   └── ...
├── apps/                # アプリケーションモジュール
│   ├── catalog/         # カタログ管理 (Film, Actor, etc.)
│   ├── geo/             # 地理情報管理 (City, Country, etc.)
│   ├── account/         # アカウント管理 (Customer, Staff)
│   └── operation/       # 業務処理 (Rental, Payment, Inventory)
├── .env.example         # 環境変数
├── .gitignore           # Git 除外設定
├── requirements.txt     # 本番用 Python 依存関係
├── requirements-dev.txt # 開発用 Python 依存関係（ruff, coverage含む）
├── .coveragerc          # Coverage 設定ファイル
├── ruff.toml            # Ruff Linter 設定ファイル
├── pyproject.toml       # プロジェクトメタデータ（設定用）
├── Makefile             # 開発タスク自動化
├── manage.py            # Django 管理スクリプト
└── README.md            # プロジェクトドキュメント
```

## 開発環境のセットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/enkaigaku/django-crud
cd django-crud
```

### 2. 仮想環境の作成

プロジェクト専用の仮想環境を作成します。

**pip を使用する場合**

```bash
# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化（Mac/Linux）
source .venv/bin/activate

# 仮想環境の有効化（Windows）
.venv\Scripts\activate
```

**uv を使用する場合（推奨）**

```bash
# uv は自動的に仮想環境を管理するため、手動での作成は不要です
# uv が .venv を自動的に作成・管理します
```

### 3. 依存関係のインストール

開発に必要なすべての依存関係（Django、DRF、ruff、coverageなど）をインストールします。

```bash
# pip を使用する場合（仮想環境を有効化した状態で）
pip install -r requirements-dev.txt

# uv を使用する場合（推奨）
uv pip install -r requirements-dev.txt
```

### 4. データベースの起動

Docker Compose を使用してPostgreSQLを起動します。

```bash
docker compose up -d postgres
```

データベースコンテナは起動時に自動的に以下を実行します：
- スキーマの作成（`migrations/001_initial_schema.sql`）
- テーブルの作成（`migrations/002_pagila_schema.sql`）
- サンプルデータの投入（`migrations/003_pagila_data.sql`）
- 認証データの設定（`migrations/004_customer_auth.sql`, `005_staff_auth.sql`）

※ 手動でのマイグレーション実行は不要です。

### 5. 開発サーバーの起動

```bash
uv run python manage.py runserver
```

## 開発ワークフロー

### コードの品質チェック（Lint）

コードスタイルと潜在的なエラーをチェックします。

```bash
# Makefile を使用（推奨）
make lint

# または直接実行
uv run ruff check .
```

**Ruff 設定**（`ruff.toml`）:
- 1行の最大文字数: 120
- チェック対象: エラー（E）、致命的エラー（F）、import順序（I）、命名規則（N）、警告（W）
- 除外: `*/migrations/*`
- import順序: dvd_rental, apps を first-party として認識

### コードの自動修正（Format）

自動で修正可能な問題を修正します。

```bash
# Makefile を使用（推奨）
make format

# または直接実行
uv run ruff check . --fix
```

### テストの実行

テストを実行し、カバレッジレポートを生成します。

```bash
# Makefile を使用（推奨）
make test

# または直接実行
uv run coverage run manage.py test --testrunner=dvd_rental.test_runner.ExistingDBTestRunner
uv run coverage report -m
```

**Coverage 設定**（`.coveragerc`）:
- 対象ソース: プロジェクト全体
- 除外パターン: migrations、tests、manage.py、wsgi.py、asgi.py
- レポート設定:
  - `show_missing = True`: カバレッジされていない行番号を表示
  - `skip_covered = False`: カバレッジ100%のファイルも表示
  - `fail_under = 80`: カバレッジ率80%未満で失敗

### カバレッジレポートの確認

```bash
# ターミナルでレポート表示
uv run coverage report -m

# HTMLレポート生成（詳細な行単位のカバレッジ）
uv run coverage html
# 生成されたレポートを開く
open htmlcov/index.html
```

## Makefile コマンド一覧

開発タスクを簡単に実行できるように、Makefileが用意されています。

| コマンド | 説明 |
|---------|------|
| `make test` | テストを実行し、カバレッジレポートを生成（80%未満で失敗） |
| `make lint` | コードの静的解析を実行（エラーがあれば表示） |
| `make format` | 自動修正可能な問題を修正 |

## CI/CD

GitHub Actions を使用して、プルリクエストとmainブランチへのプッシュ時に自動テストとビルドを実行します。

**ワークフロー**（`.github/workflows/ci-cd.yml`）:
1. PostgreSQLデータベースの起動
2. Python 3.13 のセットアップ
3. 依存関係のインストール（`requirements-dev.txt`）
4. Ruff によるコードチェック
5. テストの実行とカバレッジレポート
6. Dockerイメージのビルドとプッシュ（mainブランチのみ）

## 設定ファイルの説明

### `requirements.txt`
本番環境で必要な依存関係のリスト。Django、DRF、PostgreSQLドライバなどが含まれます。

### `requirements-dev.txt`
開発環境で必要な追加の依存関係。`requirements.txt` を含み、ruff と coverage が追加されています。

### `.coveragerc`
Coverage.py の設定ファイル。テストカバレッジの計測対象と除外パターンを定義します。

### `ruff.toml`
Ruff linter/formatter の設定ファイル。コードスタイル、チェックルール、import順序などを定義します。

### `pyproject.toml`
プロジェクトのメタデータと設定を含むファイル。現在は最小限の設定のみを保持しています。

## ブランチ戦略

- `main`: 本番環境用の安定版ブランチ
- `develop`: 開発用ブランチ（未導入の場合）
- `feature/*`: 新機能開発用のブランチ
- `bugfix/*`: バグ修正用のブランチ

## プルリクエストのガイドライン

1. **コードチェック**: `make lint` がエラーなく通ること
2. **テスト**: `make test` が成功し、カバレッジが80%以上であること
3. **コミットメッセージ**: わかりやすく簡潔に記述
4. **説明**: PRの目的と変更内容を明確に記載

## トラブルシューティング

### PostgreSQLへの接続エラー

```bash
# PostgreSQLが起動しているか確認
docker compose ps

# ログを確認
docker compose logs postgres

# 再起動
docker compose restart postgres
```

### 依存関係のエラー

```bash
# 依存関係を再インストール
pip install -r requirements-dev.txt --force-reinstall

# または uv の場合
uv pip install -r requirements-dev.txt --reinstall
```

#### データベースのリセット

```bash
# データベースコンテナを削除して再作成
docker compose down -v
docker compose up -d postgres

# データベースが完全に起動するまで待機（15秒程度）
sleep 15
```

## Django Admin 管理画面

### スーパーユーザーの作成

```bash
uv run python manage.py createsuperuser
```

プロンプトに従って入力してください：
- ユーザー名（推奨：`admin`）
- メールアドレス（任意）
- パスワード（8文字以上）

**作成済みのテストアカウント**：
- ユーザー名：`admin`
- パスワード：`admin123456`（変更を推奨）

### アクセス方法

- **URL**: http://localhost:8000/admin/
- **ログイン**: スーパーユーザーアカウントでログイン

### 管理機能

プロジェクトには完全な Django Admin 管理画面が設定されており、**13 モデルの可視化管理インターフェース**を提供しています：

#### 基礎データ管理
- **言語 (Language)**（6 件）- 検索、ソート
- **映画カテゴリ (Category)**（16 件）- 検索、ソート
- **国 (Country)**（109 件）- 検索、ソート
- **都市 (City)**（600 件）- 検索、国によるフィルタリング、国名の表示

#### コア業務管理
- **俳優 (Actor)**（200 件）- 名前検索、フルネーム表示、ソート
- **映画 (Film)**（1000 件）- タイトル/説明検索、レーティング/年/言語によるフィルタリング、**俳優とカテゴリのインライン編集**
- **住所 (Address)**（603 件）- 住所検索、都市/国の表示

#### サポート管理
- **店舗 (Store)**（500 件）- 完全な住所情報の表示
- **スタッフ (Staff)**（1,500 件）- 名前/メール/ユーザー名検索、アクティブ状態/店舗によるフィルタリング
- **顧客 (Customer)**（599 件）- 名前/メール検索、アクティブ状態/店舗/作成日によるフィルタリング、**日付階層ナビゲーション**

#### 取引管理
- **在庫 (Inventory)**（4,581 件）- 映画タイトル検索、店舗によるフィルタリング
- **レンタル (Rental)**（16,045 件）- 顧客名/映画名検索、**返却状態の表示**、日付/スタッフによるフィルタリング、**日付階層ナビゲーション**
- **支払い (Payment)**（16,049 件）- 顧客/スタッフ/日付によるフィルタリング、**日付階層ナビゲーション**

### Admin 特徴機能

| 機能 | 説明 |
|------|------|
| **リスト表示最適化** | 各モデルで重要なフィールド（5-8 個）を表示 |
| **スマート検索** | 名前、タイトル、メールなどの主要フィールドで高速検索 |
| **サイドバーフィルタ** | レーティング、ステータス、日付、店舗などで素早くフィルタリング |
| **インライン編集** | 映画ページで俳優やカテゴリの関連付けを直接編集可能 |
| **カスタムメソッド** | 計算フィールド（フルネーム、返却状態、住所情報など）を表示 |
| **クエリ最適化** | 全ての外キーで select_related を使用し、N+1 問題を回避 |
| **日付ナビゲーション** | 顧客/レンタル/支払いを日付階層で素早くナビゲート |
| **一括操作** | 一括削除などの操作をサポート |
| **読み取り専用フィールド** | 自動生成フィールド（last_update 等）を保護 |
| **グループ表示** | fieldsets を使用してフィールドをグループ化（基本情報/業務情報/システム情報） |

### Admin 画面プレビュー

- **ログインページ**: "DVD Rental Management System" カスタムタイトル
- **管理トップ**: 13 モデルをカテゴリ別に表示
- **リストページ**: 最適化されたリスト表示、検索、フィルタ、ソート対応
- **編集ページ**: グループ化されたフィールド表示、インライン関連編集
- **一括操作**: 複数のレコードを選択して一括操作を実行

## API エンドポイント

**全 13 の RESTful API エンドポイントで、すべての業務機能をカバー**

### カタログ管理 API (Catalog)

| エンドポイント | 説明 | データ量 | 機能 |
|------|------|--------|------|
| `/api/languages/` | 言語リスト | 6 言語 | CRUD、検索、ソート |
| `/api/categories/` | 映画カテゴリ | 16 カテゴリ | CRUD、検索、ソート |
| `/api/actors/` | 俳優管理 | 200 名 | CRUD、名前検索、ソート |
| `/api/films/` | 映画管理 | 1000 作品 | CRUD、検索、レーティング/年/言語フィルタ |

### 地理情報 API (Geo)

| エンドポイント | 説明 | データ量 | 機能 |
|------|------|--------|------|
| `/api/countries/` | 国リスト | 109 カ国 | CRUD、検索、ソート |
| `/api/cities/` | 都市リスト | 600 都市 | CRUD、検索、国フィルタ |
| `/api/addresses/` | 住所管理 | 603 住所 | CRUD、検索、都市/地区フィルタ |
| `/api/stores/` | 店舗管理 | 500 店舗 | CRUD、店舗詳細確認 |

### アカウント管理 API (Account)

| エンドポイント | 説明 | データ量 | 機能 |
|------|------|--------|------|
| `/api/customers/` | 顧客管理 | 599 名 | CRUD、名前/メール検索、ステータスフィルタ |
| `/api/staff/` | スタッフ管理 | 1,500 名 | CRUD、検索、店舗/ステータスフィルタ |

### 業務処理 API (Operation)

| エンドポイント | 説明 | データ量 | 機能 |
|------|------|--------|------|
| `/api/rentals/` | レンタル管理 | 16,045 件 | CRUD、検索、顧客/在庫/スタッフフィルタ |
| `/api/inventory/` | 在庫管理 | 4,581 件 | CRUD、映画/店舗フィルタ |
| `/api/payments/` | 支払い記録 | 16,049 件 | CRUD、顧客/スタッフ/レンタルフィルタ |

## API 使用例

### 1. 全映画の取得（ページネーション）

```bash
curl http://localhost:8000/api/films/
```

### 2. 映画の検索（タイトル）

```bash
curl "http://localhost:8000/api/films/?search=LOVE"
```

### 3. 映画のフィルタリング（レーティング）

```bash
curl "http://localhost:8000/api/films/?rating=G"
```

### 4. 映画のフィルタリング（公開年）

```bash
curl "http://localhost:8000/api/films/?release_year=2023"
```

### 5. 俳優の検索（名前）

```bash
curl "http://localhost:8000/api/actors/?search=WAHLBERG"
```

### 6. 特定の都市を取得（国でフィルタ）

```bash
curl "http://localhost:8000/api/cities/?country=1"
```

### 7. 顧客の検索

```bash
curl "http://localhost:8000/api/customers/?search=MARY"
```

### 8. レンタル記録の取得（顧客でフィルタ）

```bash
curl "http://localhost:8000/api/rentals/?customer=1"
```

### 9. 在庫の確認（映画でフィルタ）

```bash
curl "http://localhost:8000/api/inventory/?film=1"
```

### 10. 支払い記録の取得（日付順）

```bash
curl "http://localhost:8000/api/payments/?ordering=-payment_date"
```

## API ドキュメント

プロジェクトは完全なインタラクティブ API ドキュメントを提供します：

- **Swagger UI**: http://localhost:8000/api/docs/
  - インタラクティブな API テストインターフェース
  - ブラウザ上で全エンドポイントを直接テスト可能

- **ReDoc**: http://localhost:8000/api/redoc/
  - 見やすい API ドキュメント閲覧インターフェース

- **OpenAPI Schema**: http://localhost:8000/api/schema/
  - 標準 OpenAPI 3.0 仕様

## データベース構造

### 現在実装済みのテーブル

1. **Language** - 言語（6件）
   - サポート：クエリ、検索、ソート

2. **Category** - 映画カテゴリ（16件）
   - サポート：クエリ、検索、ソート

3. **Country** - 国（109件）
   - サポート：クエリ、検索、ソート

4. **City** - 都市（600件）
   - サポート：クエリ、検索、フィルタ（国別）、ソート
   - 最適化：select_related('country')

5. **Actor** - 俳優（200件）
   - サポート：クエリ、名前検索、ソート
   - 特徴：full_name 計算フィールド

6. **Film** - 映画（1000件）
   - サポート：クエリ、タイトル/説明検索、レーティング/年/言語フィルタ、ソート
   - 最適化：select_related('language', 'original_language')
   - 特徴：言語名のネスト表示

7. **Address** - 住所（603件）
   - サポート：クエリ、検索、都市/地区フィルタ
   - 最適化：select_related('city', 'city__country')

8. **Store** - 店舗（500件）
   - サポート：完全な CRUD 操作
   - 最適化：select_related('address')

9. **Staff** - スタッフ（1500件）
   - サポート：クエリ、名前/メール検索、店舗/ステータスフィルタ
   - 特徴：full_name 計算フィールド

10. **Customer** - 顧客（599件）
    - サポート：クエリ、名前/メール検索、店舗/ステータスフィルタ
    - 特徴：full_name 計算フィールド

11. **Inventory** - 在庫（4581件）
    - サポート：クエリ、映画/店舗フィルタ
    - 最適化：select_related('film', 'store')

12. **Rental** - レンタル（16045件）
    - サポート：クエリ、検索、顧客/在庫/スタッフフィルタ
    - 最適化：select_related('customer', 'inventory__film', 'staff')
    - 特徴：レンタル状態、顧客名、映画名、スタッフ名の表示

13. **Payment** - 支払い（16049件）
    - サポート：クエリ、顧客/スタッフ/レンタルフィルタ、日付ソート
    - 特徴：金額クエリのサポート

## 開発進捗

### ✅ 完了（全機能実装済み）

- [x] プロジェクト初期化（Django 6.0.1 + DRF + uv）
- [x] データベース接続設定（PostgreSQL effect_crud）
- [x] モデル生成（inspectdb - 17 モデル）
- [x] **全 13 API エンドポイントの実装**
  - [x] カタログ管理 API（Language, Category, Actor, Film）
  - [x] 地理情報 API（Country, City, Address, Store）
  - [x] アカウント管理 API（Customer, Staff）
  - [x] 業務処理 API（Rental, Inventory, Payment）
- [x] 検索、フィルタリング、ソート機能
- [x] ページネーション機能（1ページ 20 件）
- [x] ORM クエリ最適化（select_related, prefetch_related）
- [x] API ドキュメント（Swagger UI + ReDoc + OpenAPI Schema）
- [x] ネストされたシリアライゼーション（関連データの表示）
- [x] 計算フィールド（full_name, is_returned 等）

### 📋 今後の拡張（オプション）

- [ ] 認証・認可（JWT Token）
- [ ] ロールベース権限管理（管理者、スタッフ、顧客）
- [ ] ユニットテスト
- [ ] API レート制限
- [ ] Docker コンテナ化
- [ ] ビジネスロジック強化（延滞料金の自動計算、在庫アラート等）
- [ ] 統計レポート API（収益統計、人気映画、アクティブ顧客）

## ライセンス

本プロジェクトは学習およびデモンストレーション目的でのみ使用されます。
