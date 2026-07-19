# IssueFlow Lite

IssueFlow Lite 是一个面向小型研发团队的轻量缺陷协作平台，也是用于实践 Python Web 后端开发的学习项目。

## 技术栈

- Python 3.12+
- FastAPI、Jinja2、Bootstrap
- SQLAlchemy 2、Alembic、PostgreSQL
- pytest、Docker Compose、GitHub Actions

## 项目结构

```text
issueFlow/
├── .github/workflows/       # GitHub Actions 持续集成配置
├── alembic/versions/        # 数据库迁移版本
├── app/
│   ├── api/routes/          # HTTP 路由模块
│   ├── api/deps.py          # 路由共用依赖
│   ├── core/                # 配置、安全和日志等基础设施
│   ├── db/                  # 数据库连接、会话和模型基类
│   ├── models/              # SQLAlchemy 数据库模型
│   ├── repositories/        # 数据持久化和查询逻辑
│   ├── schemas/             # Pydantic 请求、响应结构
│   ├── services/            # 业务规则和用例编排
│   ├── static/              # CSS 与浏览器端 JavaScript
│   ├── templates/           # Jinja2 页面模板
│   └── main.py              # FastAPI 应用入口
├── docs/                    # 需求、架构和接口设计文档
├── scripts/                 # 初始化、维护和部署辅助脚本
├── tests/
│   ├── integration/         # 接口、数据库等集成测试
│   └── unit/                # 函数和业务规则单元测试
├── .env.example             # 环境变量示例，不包含真实密钥
├── .gitignore               # Git 忽略规则
├── alembic.ini              # Alembic 配置入口
├── compose.yaml             # 本地 PostgreSQL 服务编排
├── Dockerfile               # 应用容器构建文件
├── pyproject.toml           # 依赖、测试和工具配置
└── README.md                # 项目说明
```

## 分层约定

```text
routes → services → repositories → database
           ↕              ↕
        schemas         models
```

- `routes` 处理 HTTP 输入输出，不堆放业务规则。
- `services` 实现创建缺陷、分配负责人、变更状态等业务流程。
- `repositories` 隔离数据库查询。
- `schemas` 描述接口数据，`models` 描述数据库表，两者不要混用。

## 本地启动

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
docker compose up -d db test_db
alembic upgrade head
uvicorn app.main:app --reload
```

`docker compose up -d db test_db` 会在后台启动两个 PostgreSQL 容器：

- `db`：开发数据库，Windows 本机端口是 `5432`，数据库名是 `issueflow`。
- `test_db`：测试数据库，Windows 本机端口是 `5433`，数据库名是 `test_issueflow`。

`alembic upgrade head` 会把开发数据库升级到最新表结构。本项目不使用 `Base.metadata.create_all()` 创建正式表结构，数据库结构变化都应通过 Alembic 迁移管理。

启动后可以访问：

- 首页：<http://127.0.0.1:8000/>
- 健康检查：<http://127.0.0.1:8000/api/health>
- API 文档：<http://127.0.0.1:8000/docs>

## 数据库命令

启动数据库：

```powershell
docker compose up -d db test_db
```

查看容器状态：

```powershell
docker compose ps
```

检查开发库是否可连接：

```powershell
docker compose exec db pg_isready -U issueflow -d issueflow
```

检查测试库是否可连接：

```powershell
docker compose exec test_db pg_isready -U issueflow -d test_issueflow
```

查看当前迁移版本：

```powershell
alembic current
```

升级到最新迁移：

```powershell
alembic upgrade head
```

回退一个迁移版本：

```powershell
alembic downgrade -1
```

停止容器但保留数据：

```powershell
docker compose down
```

删除容器和数据库数据卷：

```powershell
docker compose down -v
```

`docker compose down -v` 会删除 PostgreSQL 数据卷，开发库和测试库里的数据都会丢失；只有在你明确想重置本地数据库时再使用。

运行测试：

```powershell
pytest
```

测试会连接 `.env` 或 `.env.example` 中的 `TEST_DATABASE_URL`。测试夹具会检查数据库名必须包含 `test`，避免误连开发库。

## 开发流程

1. 从最新 `main` 创建 `feature/*` 或 `fix/*` 分支。
2. 完成功能并补充测试。
3. 推送分支并创建 Pull Request。
4. 检查变更和 CI 后合并到受保护的 `main`。
5. 删除已合并分支并同步本地 `main`。

## 分功能阶段规划

项目的完整开发路线已拆分为可以独立开发、测试和提交 Pull Request 的功能阶段。开始下一项功能前，请先阅读 [分功能阶段实现规划](./分功能阶段实现规划/README.md)，每次只实施其中一个规划文件。

## 当前状态

项目处于基础工程初始化阶段。当前骨架提供应用入口、健康检查和目录职责约定，用户、项目、缺陷等领域功能将在后续迭代中实现。
