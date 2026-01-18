# Agent Skills 仓库

公司 AI 应用开发使用的 Claude Agent Skills 集合。

## 可用 Skills

| Skill | 用途 | 调用方式 | 语言 |
|-------|------|----------|------|
| **creating-agent-skills** ⭐ | **元技能** - 创建其他 Claude Agent Skills 的基础技能 | `/creating-agent-skills` | EN |
| **creating-jtl-shop-5-plugins** | JTL-Shop 5 插件开发 | `/creating-jtl-shop-5-plugins` | DE |
| **creating-jtl-shop-nova-template** | JTL-Shop 5 NOVA 子模板开发 | `/creating-jtl-shop-nova-template` | DE |
| **creating-jtl-wawi-api-apps** | JTL-Wawi REST API 应用注册与集成 | `/creating-jtl-wawi-api-apps` | DE |
| **creating-odoo-18-apps** | Odoo 18 模块/插件开发 | `/creating-odoo-18-apps` | EN |

> ⭐ **元技能说明**：`creating-agent-skills` 是一个特殊的"生产技能的技能"，它定义了如何创建符合规范的新技能，是本仓库所有技能开发的基础。

## JTL 相关 Skills

### creating-jtl-wawi-api-apps

用于 JTL-Wawi REST API 的应用注册和集成开发：

- **完整的 App 注册流程**（3 步骤：POST → 手动确认 → Polling 获取 API-Key）
- **161 个 API Scopes 完整列表**（从官方 OpenAPI v1.2 提取）
- **所有可用端点参考**（customers, salesorders, items, invoices 等）
- **常见错误和社区经验**（Authorization 格式、URL 结构、Scope 选择等）

### creating-jtl-shop-5-plugins

用于 JTL-Shop 5 插件开发：

- info.xml 配置参考
- Bootstrap.php 生命周期钩子
- 插件架构和目录结构
- 常见问题排查

### creating-jtl-shop-nova-template

用于 JTL-Shop 5 NOVA 子模板开发：

- SCSS 变量覆盖
- Smarty 模板块扩展
- 响应式设计模式

## 安装方法

```bash
# 方法 1：复制到个人目录（推荐）
cp -r <skill-name>/ ~/.claude/skills/

# 方法 2：复制到项目目录
cp -r <skill-name>/ .claude/skills/

# 方法 3：链接特定 Skill
ln -s /path/to/Agent-Skills/<skill-name> ~/.claude/skills/<skill-name>
```

## 使用说明

- **手动调用**：输入 `/skill-name`
- **自动触发**：Claude 根据对话内容自动识别
- **查看可用**：输入 `/skills`

## 创建新 Skill

使用元技能 `creating-agent-skills`：

```
/creating-agent-skills 创建一个 [描述] 的 Skill
```

详细规范、最佳实践、常见错误等均在 `creating-agent-skills` 元技能中，无需单独查阅。

## 目录结构

```
Agent-Skills/
├── README.md                           # 本文件
├── CLAUDE.md                           # AI 助手指南
├── best-practices.md                   # Anthropic 官方最佳实践
│
├── creating-agent-skills/              # ⭐ 元技能
├── creating-jtl-shop-5-plugins/        # JTL-Shop 5 插件开发
├── creating-jtl-shop-nova-template/    # JTL-Shop NOVA 模板开发
├── creating-jtl-wawi-api-apps/         # JTL-Wawi API 集成
└── creating-odoo-18-apps/              # Odoo 18 模块开发
```

## 注意事项

- 只安装来自可信来源的 Skills
- 审查 `scripts/` 中的所有代码
- 不要在 Skills 中存储凭据
- JTL 相关 Skills 使用德语（与官方文档一致）

## 许可证

MIT License
