# DVD Rental API

完整的 DVD 租赁服务 RESTful API，使用 Django 6.0.1 + Django REST Framework 构建。

## 项目概述

基于现有 PostgreSQL 数据库 `effect_crud` 构建的完整 CRUD API，提供电影、演员、客户、租赁等数据的管理接口。

### 技术栈

- **Python**: 3.13.9
- **Django**: 6.0.1
- **Django REST Framework**: 3.16.1
- **数据库**: PostgreSQL 17.6 (Docker)
- **包管理**: uv
- **API 文档**: drf-spectacular (OpenAPI 3.0/Swagger)

### 核心功能

- ✅ RESTful API 设计
- ✅ 自动分页（每页 20 条）
- ✅ 搜索功能（关键词搜索）
- ✅ 过滤功能（字段过滤）
- ✅ 排序功能（多字段排序）
- ✅ OpenAPI 文档（Swagger UI + ReDoc）
- ✅ ORM 查询优化（select_related）

## 快速开始

### 1. 克隆项目

```bash
cd /Users/tokyoyuan/Workspace/claude/django-crud
```

### 2. 配置环境

项目使用 `.env` 文件管理环境变量：

```bash
# 数据库已配置，无需修改
# 查看 .env 文件确认配置
cat .env
```

### 3. 启动开发服务器（推荐使用 uv）

**方式 1: 使用 uv（推荐）**
```bash
# uv 会自动使用虚拟环境，无需手动激活
uv run python manage.py runserver

# 或者更简洁
uv run manage.py runserver
```

**方式 2: 传统方式**
```bash
# 激活虚拟环境
source .venv/bin/activate

# 启动服务器
python manage.py runserver
```

服务器将在 `http://localhost:8000` 启动。

## API 端点

### 基础数据 API

| 端点 | 描述 | 数据量 |
|------|------|--------|
| `/api/languages/` | 语言列表 | 6 种语言 |
| `/api/categories/` | 电影分类 | 16 个分类 |
| `/api/countries/` | 国家列表 | 109 个国家 |
| `/api/cities/` | 城市列表 | 600 个城市 |

### 核心业务 API

| 端点 | 描述 | 数据量 | 功能 |
|------|------|--------|------|
| `/api/actors/` | 演员管理 | 200 位演员 | 搜索、排序 |
| `/api/films/` | 电影管理 | 1000 部电影 | 搜索、过滤、排序 |

## API 使用示例

### 1. 获取所有电影（分页）

```bash
curl http://localhost:8000/api/films/
```

### 2. 搜索电影（按标题）

```bash
curl "http://localhost:8000/api/films/?search=LOVE"
```

### 3. 过滤电影（按评级）

```bash
curl "http://localhost:8000/api/films/?rating=G"
```

### 4. 过滤电影（按发行年份）

```bash
curl "http://localhost:8000/api/films/?release_year=2023"
```

### 5. 搜索演员（按姓名）

```bash
curl "http://localhost:8000/api/actors/?search=WAHLBERG"
```

### 6. 获取特定城市（按国家过滤）

```bash
curl "http://localhost:8000/api/cities/?country=1"
```

## API 文档

项目提供完整的交互式 API 文档：

- **Swagger UI**: http://localhost:8000/api/docs/
  - 交互式 API 测试界面
  - 可直接在浏览器中测试所有端点

- **ReDoc**: http://localhost:8000/api/redoc/
  - 美观的 API 文档阅读界面

- **OpenAPI Schema**: http://localhost:8000/api/schema/
  - 标准 OpenAPI 3.0 规范

## 数据库结构

### 当前已实现的表

1. **Language** - 语言（6条）
   - 支持：查询、搜索、排序

2. **Category** - 电影分类（16条）
   - 支持：查询、搜索、排序

3. **Country** - 国家（109条）
   - 支持：查询、搜索、排序

4. **City** - 城市（600条）
   - 支持：查询、搜索、过滤（按国家）、排序
   - 优化：select_related('country')

5. **Actor** - 演员（200条）
   - 支持：查询、姓名搜索、排序
   - 特性：full_name 计算字段

6. **Film** - 电影（1000条）
   - 支持：查询、标题/描述搜索、评级/年份/语言过滤、排序
   - 优化：select_related('language', 'original_language')
   - 特性：嵌套显示语言名称

## 项目结构

```
django-crud/
├── dvd_rental/          # Django 项目配置
│   ├── settings.py      # 配置文件
│   ├── urls.py          # 主路由
│   └── ...
├── api/                 # API 应用
│   ├── models.py        # 数据模型（17个模型）
│   ├── serializers.py   # DRF 序列化器
│   ├── views.py         # DRF 视图集
│   ├── urls.py          # API 路由
│   └── ...
├── .env                 # 环境变量
├── .gitignore          # Git 忽略文件
├── requirements.txt     # Python 依赖
├── manage.py           # Django 管理脚本
└── README.md           # 项目文档
```

## 开发进度

### ✅ 已完成

- [x] 项目初始化（Django 6.0.1 + DRF + uv）
- [x] 数据库连接配置（PostgreSQL effect_crud）
- [x] 模型生成（inspectdb - 17个模型）
- [x] 基础 CRUD API（Language, Category, Country, City）
- [x] 核心业务 API（Actor, Film）
- [x] API 文档（Swagger + ReDoc）
- [x] 搜索、过滤、排序功能
- [x] 分页功能
- [x] ORM 查询优化

### 🚧 进行中

- [ ] 其他表的 CRUD（Customer, Store, Staff, Address, Inventory）
- [ ] 业务逻辑实现（Rental, Payment）
- [ ] 高级过滤功能
- [ ] 性能优化

### 📋 计划中

- [ ] 认证授权（JWT）
- [ ] 角色权限管理
- [ ] 单元测试
- [ ] API 速率限制
- [ ] Docker 部署

## 测试验证

所有 API 端点已通过测试：

```bash
# API 根端点
✅ GET /api/ - 返回所有可用端点

# 基础数据
✅ GET /api/languages/ - 6种语言
✅ GET /api/categories/ - 16个分类
✅ GET /api/countries/ - 109个国家
✅ GET /api/cities/ - 600个城市（带国家关联）

# 核心业务
✅ GET /api/actors/ - 200位演员（支持搜索）
✅ GET /api/films/ - 1000部电影（支持搜索、过滤）

# 搜索功能
✅ GET /api/films/?search=LOVE - 标题搜索
✅ GET /api/actors/?search=WAHLBERG - 姓名搜索

# 过滤功能
✅ GET /api/films/?rating=G - 按评级过滤（178部）
✅ GET /api/films/?release_year=2023 - 按年份过滤

# API 文档
✅ GET /api/docs/ - Swagger UI
✅ GET /api/redoc/ - ReDoc
✅ GET /api/schema/ - OpenAPI 3.0 Schema
```

## Git 提交记录

项目使用 Conventional Commits 规范：

1. `chore: initialize Django project with uv package manager`
2. `feat: configure Django settings and database connection`
3. `feat: generate Django models from PostgreSQL database`
4. `feat: implement basic CRUD for simple models`
5. `feat: add Actor and Film CRUD endpoints`

## 许可证

本项目仅用于学习和演示目的。

## 作者

Developed with Craft Agent
