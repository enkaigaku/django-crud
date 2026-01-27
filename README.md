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
- ✅ Django Admin 后台管理（13 个模型可视化管理）
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

### 4. 数据库迁移（首次运行）

首次运行时需要创建 Django 系统表：

```bash
uv run python manage.py migrate
```

### 5. 创建超级用户（访问 Admin 后台）

```bash
uv run python manage.py createsuperuser
```

按提示输入：
- 用户名（建议：`admin`）
- 邮箱（可选）
- 密码（至少 8 位）

**已创建的测试账号**：
- 用户名：`admin`
- 密码：`admin123456`（建议修改）

## Django Admin 后台管理

### 访问方式

- **URL**: http://localhost:8000/admin/
- **登录**: 使用超级用户账号登录

### 管理功能

项目已配置完整的 Django Admin 后台，提供 **13 个模型的可视化管理界面**：

#### 基础数据管理
- **语言**（6 条）- 搜索、排序
- **电影分类**（16 条）- 搜索、排序
- **国家**（109 条）- 搜索、排序
- **城市**（600 条）- 搜索、按国家过滤、显示国家名

#### 核心业务管理
- **演员**（200 条）- 姓名搜索、全名显示、排序
- **电影**（1000 条）- 标题/描述搜索、按评级/年份/语言过滤、**内联编辑演员和分类**
- **地址**（603 条）- 地址搜索、显示城市/国家

#### 支持性管理
- **商店**（500 条）- 显示完整地址信息
- **员工**（1,500 条）- 姓名/邮箱/用户名搜索、按激活状态/商店过滤
- **客户**（599 条）- 姓名/邮箱搜索、按激活状态/商店/创建日期过滤、**日期层级导航**

#### 交易管理
- **库存**（4,581 条）- 搜索电影标题、按商店过滤
- **租赁**（16,045 条）- 搜索客户名/电影名、**显示归还状态**、按日期/员工过滤、**日期层级导航**
- **支付**（16,049 条）- 按客户/员工/日期过滤、**日期层级导航**

### Admin 特色功能

| 功能 | 说明 |
|------|------|
| **列表显示优化** | 每个模型显示关键字段（5-8 个） |
| **智能搜索** | 按名称、标题、邮箱等关键字段快速搜索 |
| **侧边栏过滤器** | 按评级、状态、日期、门店等快速过滤 |
| **内联编辑** | 电影页面可直接编辑演员和分类关联 |
| **自定义方法** | 显示计算字段（全名、归还状态、地址信息等） |
| **查询优化** | 所有外键使用 select_related 避免 N+1 查询 |
| **日期导航** | 客户/租赁/支付按日期层级快速导航 |
| **批量操作** | 支持批量删除等操作 |
| **只读字段** | 保护自动生成字段（last_update 等） |
| **分组显示** | 使用 fieldsets 将字段分组（基本信息/业务信息/系统信息） |

### Admin 界面预览

- **登录页面**: "DVD 租赁管理系统" 自定义标题
- **管理首页**: 13 个模型按分类显示
- **列表页面**: 优化的列表显示，支持搜索、过滤、排序
- **编辑页面**: 分组的字段显示，内联关联编辑
- **批量操作**: 选择多个记录进行批量操作

## API 端点

**总计 13 个 RESTful API 端点，覆盖所有业务功能**

### 基础数据 API

| 端点 | 描述 | 数据量 | 功能 |
|------|------|--------|------|
| `/api/languages/` | 语言列表 | 6 种语言 | CRUD、搜索、排序 |
| `/api/categories/` | 电影分类 | 16 个分类 | CRUD、搜索、排序 |
| `/api/countries/` | 国家列表 | 109 个国家 | CRUD、搜索、排序 |
| `/api/cities/` | 城市列表 | 600 个城市 | CRUD、搜索、按国家过滤 |

### 核心业务 API

| 端点 | 描述 | 数据量 | 功能 |
|------|------|--------|------|
| `/api/actors/` | 演员管理 | 200 位演员 | CRUD、姓名搜索、排序 |
| `/api/films/` | 电影管理 | 1000 部电影 | CRUD、搜索、按评级/年份/语言过滤 |
| `/api/customers/` | 客户管理 | 599 位客户 | CRUD、姓名/邮箱搜索、按状态过滤 |
| `/api/rentals/` | 租赁管理 | 16,045 条记录 | CRUD、搜索、按客户/库存/员工过滤 |
| `/api/inventory/` | 库存管理 | 4,581 条记录 | CRUD、按电影/商店过滤 |
| `/api/payments/` | 支付记录 | 16,049 条记录 | CRUD、按客户/员工/租赁过滤 |

### 支持性 API

| 端点 | 描述 | 数据量 | 功能 |
|------|------|--------|------|
| `/api/addresses/` | 地址管理 | 603 个地址 | CRUD、搜索、按城市/地区过滤 |
| `/api/stores/` | 商店管理 | 500 个商店 | CRUD、查看商店详情 |
| `/api/staff/` | 员工管理 | 1,500 名员工 | CRUD、搜索、按商店/状态过滤 |

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

### 7. 搜索客户

```bash
curl "http://localhost:8000/api/customers/?search=MARY"
```

### 8. 获取租赁记录（按客户过滤）

```bash
curl "http://localhost:8000/api/rentals/?customer=1"
```

### 9. 查看库存（按电影过滤）

```bash
curl "http://localhost:8000/api/inventory/?film=1"
```

### 10. 获取支付记录（按日期排序）

```bash
curl "http://localhost:8000/api/payments/?ordering=-payment_date"
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

7. **Address** - 地址（603条）
   - 支持：查询、搜索、按城市/地区过滤
   - 优化：select_related('city', 'city__country')

8. **Store** - 商店（500条）
   - 支持：完整 CRUD 操作
   - 优化：select_related('address')

9. **Staff** - 员工（1500条）
   - 支持：查询、姓名/邮箱搜索、按商店/状态过滤
   - 特性：full_name 计算字段

10. **Customer** - 客户（599条）
    - 支持：查询、姓名/邮箱搜索、按商店/状态过滤
    - 特性：full_name 计算字段

11. **Inventory** - 库存（4581条）
    - 支持：查询、按电影/商店过滤
    - 优化：select_related('film', 'store')

12. **Rental** - 租赁（16045条）
    - 支持：查询、搜索、按客户/库存/员工过滤
    - 优化：select_related('customer', 'inventory__film', 'staff')
    - 特性：显示租赁状态、客户名、电影名、员工名

13. **Payment** - 支付（16049条）
    - 支持：查询、按客户/员工/租赁过滤、按日期排序
    - 特性：支持金额查询

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

### ✅ 已完成（全部功能实现）

- [x] 项目初始化（Django 6.0.1 + DRF + uv）
- [x] 数据库连接配置（PostgreSQL effect_crud）
- [x] 模型生成（inspectdb - 17个模型）
- [x] **所有 13 个 API 端点实现**
  - [x] 基础数据 API（Language, Category, Country, City）
  - [x] 核心业务 API（Actor, Film, Customer, Rental, Inventory, Payment）
  - [x] 支持性 API（Address, Store, Staff）
- [x] 搜索、过滤、排序功能
- [x] 分页功能（每页 20 条）
- [x] ORM 查询优化（select_related, prefetch_related）
- [x] API 文档（Swagger UI + ReDoc + OpenAPI Schema）
- [x] 嵌套序列化（显示关联数据）
- [x] 计算字段（full_name, is_returned 等）

### 📋 后续扩展（可选）

- [ ] 认证授权（JWT Token）
- [ ] 角色权限管理（管理员、员工、客户）
- [ ] 单元测试
- [ ] API 速率限制
- [ ] Docker 容器化
- [ ] 业务逻辑增强（自动计算延期费用、库存预警等）
- [ ] 统计报表 API（收入统计、热门电影、活跃客户）

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
