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
uvicorn app.main:app --reload
```

启动后可以访问：

- 首页：<http://127.0.0.1:8000/>
- 健康检查：<http://127.0.0.1:8000/api/health>
- API 文档：<http://127.0.0.1:8000/docs>

运行测试：

```powershell
pytest
```

## 开发流程

1. 从最新 `main` 创建 `feature/*` 或 `fix/*` 分支。
2. 完成功能并补充测试。
3. 推送分支并创建 Pull Request。
4. 检查变更和 CI 后合并到受保护的 `main`。
5. 删除已合并分支并同步本地 `main`。

## 当前状态

项目处于基础工程初始化阶段。当前骨架提供应用入口、健康检查和目录职责约定，用户、项目、缺陷等领域功能将在后续迭代中实现。