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

## クイックスタート

### 1. プロジェクトのクローン

```bash
git clone https://github.com/enkaigaku/django-crud
```

### 2. 環境設定

プロジェクトは `.env` ファイルで環境変数を管理しています：

```bash
# データベースは設定済みのため、変更は不要です
# .env ファイルを確認
cat .env
```

### 3. 開発サーバーの起動（uv 推奨）

**方法 1: uv を使用（推奨）**
```bash
# uv は自動的に仮想環境を使用するため、手動でのアクティベートは不要です
uv run python manage.py runserver

# またはより簡潔に
uv run manage.py runserver
```

**方法 2: 従来の方法**
```bash
# 仮想環境のアクティベート
source .venv/bin/activate

# サーバーの起動
python manage.py runserver
```

サーバーは `http://localhost:8000` で起動します。

### 4. データベースマイグレーション（初回実行時）

初回実行時は Django システムテーブルを作成する必要があります：

```bash
uv run python manage.py migrate
```

### 5. スーパーユーザーの作成（Admin 管理画面アクセス用）

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

## Django Admin 管理画面

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
├── .env                 # 環境変数
├── .gitignore           # Git 除外設定
├── requirements.txt     # Python 依存関係
├── manage.py            # Django 管理スクリプト
└── README.md            # プロジェクトドキュメント
```

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
