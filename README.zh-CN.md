# ⚡ LayaLog — 智能日志可观测性与 AI 语义诊断系统

<p align="center">
  <strong>将海量原始服务器日志转化为结构化 AI 诊断、故障根因分析以及实时可观测性指标。</strong>
</p>

<p align="center">
  <a href="README.md"><strong>🇺🇸 English</strong></a> •
  <a href="README.pt-BR.md"><strong>🇧🇷 Português</strong></a> •
  <a href="README.zh-CN.md"><strong>🇨🇳 简体中文</strong></a>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white" alt="Python 3.9+" /></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white" alt="FastAPI" /></a>
  <a href="https://github.com/typesafe-ai/laya"><img src="https://img.shields.io/badge/Laya%20AI-System%20One-7928CA?logo=openai&logoColor=white" alt="Laya AI" /></a>
  <a href="https://driverjs.com/"><img src="https://img.shields.io/badge/Driver.js-交互式指南-FF5722?logo=javascript&logoColor=white" alt="Driver.js" /></a>
  <a href="https://playwright.dev/"><img src="https://img.shields.io/badge/Playwright-E2E%E6%B5%8B%E8%AF%95%E5%85%A8%E9%80%9A%E8%BF%87-2EAD33?logo=playwright&logoColor=white" alt="Playwright" /></a>
  <a href="https://docs.pytest.org/"><img src="https://img.shields.io/badge/Pytest-100%25%20%E9%80%9A%E8%BF%87-brightgreen?logo=pytest&logoColor=white" alt="Pytest" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
</p>

---

## 📖 项目概述

**LayaLog** 是一款专为工程开发与 SRE 运维团队打造的高性能智能日志分析与可观测性系统。摆脱在数百兆文本日志中执行耗时且繁琐的 `grep` 检索，LayaLog 融合了以下核心优势：

1. **智能特征聚类（Smart Clustering）**：在 AI 推理前对时间戳、UUID、IP 及堆栈特征进行密码学规范化聚合，将重复异常归纳为唯一事件，减少超过 98% 的大语言模型推理调用。
2. **Laya AI（System One 决策引擎）**：提供类型化语义评估（`Choice`、`Score`、`Noul`），精准判定故障根本原因、严重级别（低、中、严重）并输出即时可行的修复建议。
3. **Quiet UI 与主从视图（Master-Detail）**：秉持低干扰、高信息密度的专业可观测性界面设计风格。
4. **虚拟化流式浏览器（60 FPS）**：采用分块异步虚拟滚动引擎，流畅加载并翻阅数百万行日志，零浏览器内存暴涨，支持全文关键词即时高亮。
5. **交互式新手引导（[Driver.js](https://driverjs.com/)）**：原生无缝集成的步骤式产品漫游指南，支持多语言动态响应。
6. **全功能多语言体系（i18n）**：支持英文（`en`）、巴西葡萄牙语（`pt-br`）与简体中文（`cn`）三语秒级无刷新即时切换。

---

## 📸 界面截图

### 1. 严重性配置与 AI 校准工作台
针对不同技术栈（*Web应用、Keycloak认证、支付网关、数据库、事件驱动消息队列*）自定义或克隆 AI 语义判定标准，实现精准定级。

<p align="center">
  <img src="docs/assets/02-perfis-gravidade.png" alt="严重性配置窗口" width="100%" style="border-radius: 8px; border: 1px solid #CBD5E1;" />
</p>

### 2. 高性能虚拟化日志浏览器
配备等宽代码字体（*JetBrains Mono*）、行号精准直达跳转与搜索关键词毫秒级同步高亮。

<p align="center">
  <img src="docs/assets/03-explorador-logs.png" alt="虚拟化日志流查看器" width="100%" style="border-radius: 8px; border: 1px solid #CBD5E1;" />
</p>

---

## 🎯 7 种原生预置 Laya AI 严重性配置

LayaLog 内置 7 种针对典型生产架构深度调优的评估基准：

| 架构类型 | 业务重心 | 严重级别触发条件 (3分 - Critical) |
| :--- | :--- | :--- |
| **Web 应用 / 单体架构** | REST API、MVC、HTTP 状态流 | 大面积 5xx 级联故障、数据库不可达、核心交易阻断 |
| **Keycloak / IAM / OAuth2** | 单点登录、Realm域、LDAP、JWT校验 | Realm 锁死、Keycloak 数据库连接池耗尽、令牌伪造风险 |
| **支付网关与清结算** | 资金流转、信用卡、实时支付接口 | 订单交易丢失、收单机构超时、幂等性校验失效 |
| **微服务 / 事件驱动架构** | Kafka、RabbitMQ、gRPC 服务间通信 | 死信队列溢出、脑裂状态、消费者组卡死停滞 |
| **异步任务与后台队列** | Celery、Redis、批处理进程 | 执行流死锁、Worker 内存溢出（OOM）、计费批处理中断 |
| **数据库与存储系统** | Postgres、MySQL、Redis、S3 | 连接池饱和耗尽、锁等待超时、物理数据损坏 |
| **边缘网关与基础设施** | Nginx、Traefik、Envoy、DNS 解析 | 全部上游集群宕机、SSL 证书失效、网关连接数饱和 |

---

## 🚀 核心特性

- **⚡ NDJSON 渐进式流传输**：支持实时进度展示与随时通过 `AbortController` 中断分析。
- **🎯 动态配置管理**：随时根据业务需求调整语义判定规则，支持一键克隆系统内置配置。
- **🧭 交互式产品引导**：基于 [Driver.js](https://driverjs.com/) 深度打造，引导用户快速上手关键功能。
- **🌐 三语国际化支持**：英文、葡萄牙语与简体中文全界面无缝即时切换。
- **📊 实时运行指标看板（KPIs）**：自动汇总总行数、分类异常频次、高危致命错误数与不可用影响率。
- **📝 一键导出 Markdown 报告**：自动生成结构完备的故障复盘技术报告，适配 Jira 与 GitHub。
- **💾 SQLite 轻量持久化**：零配置本地数据库存储，支持历史秒级回放与一键永久彻底清理。

---

## 🛠️ 快速安装与启动

### 环境要求
- Python 3.9 或更高版本
- 现代浏览器（Chrome、Firefox、Safari、Edge）

### 1. 克隆仓库并配置运行环境

```bash
# 克隆项目仓库
git clone https://github.com/gugaucb/layalog.git
cd layalog

# 创建 Python 虚拟环境
python3 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # macOS / Linux
# 或: .venv\Scripts\activate  # Windows

# 安装项目依赖包
pip install -r requirements.txt
pip install -e .
```

### 2. 启动服务

```bash
python run.py
```

在浏览器中访问系统：**[http://localhost:8100](http://localhost:8100)**

---

## 🧪 自动化测试套件

项目拥有完整的单元测试与基于 **Playwright** 的自动化浏览器端到端（E2E）测试：

```bash
# 运行后端单元与集成测试套件
pytest

# 运行 Playwright 浏览器端到端自动化测试
python scripts/run_e2e_tests.py

# 详细模式输出
pytest -v
```

---

## 🔌 REST API 接口定义

| 请求方式 | 接口路由 | 功能说明 |
| :--- | :--- | :--- |
| `POST` | `/api/analyze-stream` | NDJSON 流式上传并实时执行 AI 分类诊断 |
| `POST` | `/api/analyze` | 同步汇总分析日志文件 |
| `GET` | `/api/analyses` | 获取已保存的历史分析列表 |
| `GET` | `/api/analyses/{id}` | 获取单次分析的完整详情数据 |
| `GET` | `/api/analyses/{id}/lines` | 虚拟化流浏览器按需分页获取原始日志分块 |
| `GET` | `/api/analyses/{id}/export-md` | 导出并下载 Markdown 格式诊断报告 |
| `DELETE`| `/api/analyses/{id}` | 彻底删除历史记录并从磁盘清理日志文件 |
| `GET` | `/api/profiles` | 获取所有可用严重性校准配置 |
| `POST` | `/api/profiles` | 新建自定义严重性配置 |
| `PUT` | `/api/profiles/{id}` | 更新指定的自定义配置 |
| `DELETE`| `/api/profiles/{id}` | 删除指定的自定义配置 |
| `POST` | `/api/profiles/{id}/clone` | 复制已有配置为新的可编辑副本 |

---

## 📁 项目目录结构

```
layalog/
├── layalog/
│   ├── app.py              # FastAPI 核心服务、REST 路由与静态 SPA 挂载
│   ├── classifier.py       # Laya AI System One 语义分类诊断引擎
│   ├── database.py         # SQLite 本地持久化与快照审计
│   ├── exporter.py         # Markdown 格式执行诊断报告生成器
│   ├── models.py           # Pydantic 数据模型与校验
│   ├── parser.py           # 日志结构解析与密码学特征聚类
│   ├── profiles.py         # 7 种原生预置配置与 CRUD 管理
│   └── static/             # 前端单页面应用 (SPA)
│       ├── css/v2.css      # Quiet UI 设计系统与 Driver.js 样式定制
│       ├── js/i18n.js      # 多语言翻译词典 (EN, PT-BR, CN)
│       ├── js/tour.js      # 基于 Driver.js 的交互式操作向导
│       ├── js/v2-app.js    # 应用控制器与响应式状态管理
│       ├── js/v2-log-viewer.js # 60 FPS 虚拟滚动日志引擎
│       └── index.html      # 响应式 HTML5 入口页面
├── tests/                  # Pytest 测试套件
│   ├── e2e/                # Playwright 浏览器自动化端到端测试
├── docs/                   # 架构决策记录 (ADR) 与图片资源
├── pyproject.toml          # Python 包配置
├── requirements.txt        # 核心依赖清单
└── run.py                  # 服务启动入口脚本 (端口 8100)
```

---

## 🤝 开源贡献

非常欢迎来自开源社区的任何反馈与贡献！

1. Fork 本项目仓库 (`git checkout -b feature/my-cool-feature`)
2. 提交代码更改 (`git commit -m "feat: add some amazing feature"`)
3. 确保所有自动化测试均顺利通过 (`pytest && python scripts/run_e2e_tests.py`)
4. 推送分支到您的仓库 (`git push origin feature/my-cool-feature`)
5. 提交清晰详细的 Pull Request

---

## 📄 开源许可证

本项目基于 **MIT License** 开放源码。详情请参阅 [`LICENSE`](LICENSE) 文件。
