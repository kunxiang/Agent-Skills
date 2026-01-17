# Agent Skills 仓库

公司 AI 应用开发使用的 Claude Agent Skills 集合。

## 目录

- [可用 Skills](#可用-skills)
- [安装方法](#安装方法)
- [使用说明](#使用说明)
- [创建新 Skill](#创建新-skill)
- [注意事项](#注意事项)

---

## 可用 Skills

### 1. skill-creator

**用途**：创建符合规范的 Claude Agent Skills

**功能**：
- 指导完整的 Skill 创建流程
- 提供最佳实践和设计模式
- 包含验证清单和常见错误
- 自动使用 WebSearch 研究目标领域

**调用方式**：`/skill-creator` 或让 Claude 自动识别

---

### 2. jtl-nova-template

**用途**：JTL-Shop 5 NOVA 模板开发

**功能**：
- Child-Template 创建和配置
- SCSS/CSS 变量自定义
- Smarty 模板块继承
- 参数化产品目录（DigiKey 风格）
- 产品筛选和对比
- CSV/Excel 导出

**调用方式**：`/jtl-nova-template` 或提及 JTL-Shop 相关开发

---

## 安装方法

### 方法 1：个人目录（推荐）

```bash
# 复制到个人 Skills 目录
cp -r <skill-name>/ ~/.claude/skills/
```

适用于所有项目，优先级高。

### 方法 2：项目目录

```bash
# 复制到项目 Skills 目录
cp -r <skill-name>/ .claude/skills/
```

仅在当前项目中生效，适合团队共享。

### 方法 3：直接克隆仓库

```bash
# 克隆到个人目录
git clone <repo-url> ~/.claude/skills/Agent-Skills

# 或链接特定 Skill
ln -s /path/to/Agent-Skills/skill-creator ~/.claude/skills/skill-creator
```

---

## 使用说明

### 基本用法

1. **手动调用**：在 Claude Code 中输入 `/skill-name`
2. **自动触发**：Claude 根据对话内容自动识别并调用

### 查看可用 Skills

```bash
# 在 Claude Code 中
/skills
```

### Skill 目录结构

```
skill-name/
├── SKILL.md              # 核心指令（必需，< 500 行）
├── references/           # 详细文档（按需加载，消耗 token）
├── scripts/              # 可执行脚本（直接运行，不消耗 token）
└── assets/               # 静态资源（路径引用，不消耗 token）
```

---

## 创建新 Skill

### 推荐流程

1. **研究阶段**：使用 WebSearch 收集目标领域信息
   - 官方文档、论坛讨论、博客文章
   - 注意：德语软件（JTL、SAP）用德语搜索

2. **调用 skill-creator**：
   ```
   /skill-creator 创建一个 [描述] 的 Skill
   ```

3. **验证规范**：
   - SKILL.md < 500 行
   - description 使用第三人称
   - 包含触发关键词

### 快速模板

```yaml
---
name: my-skill
description: "执行 X 操作并生成 Y。用于：(1) 场景A，(2) 场景B。关键词：keyword1, keyword2。"
---

# Skill 标题

## Quick Start
[最小示例]

## 核心指令
[步骤说明]

## 参考
- 详细文档：[references/详情.md](references/详情.md)
```

---

## 注意事项

### 规范要求

| 项目 | 要求 |
|------|------|
| SKILL.md 行数 | **< 500 行** |
| name 格式 | 小写、字母数字、连字符，最多 64 字符 |
| description 长度 | 最多 1024 字符 |
| description 人称 | **第三人称**（"处理文件" 而非 "我处理文件"） |
| 禁用词 | name 中不能包含 "anthropic"、"claude" |

### 最佳实践

1. **简洁优先**：只添加 Claude 不知道的内容
2. **渐进式披露**：核心内容在 SKILL.md，详细内容在 references/
3. **WebSearch 优于 WebFetch**：WebFetch 常返回 403
4. **语言策略**：德语软件用德语搜索，中国平台用中文搜索

### 常见错误

- SKILL.md 超过 500 行
- description 使用第一/第二人称
- 把 "何时使用" 放在 body 而非 description
- references 嵌套超过一层
- 包含时间敏感信息

### 安全提醒

- 只安装来自可信来源的 Skills
- 审查 scripts/ 中的所有代码
- 不要在 Skills 中存储凭据
- 使用 `allowed-tools` 限制工具权限

---

## 贡献指南

1. Fork 本仓库
2. 创建新分支：`git checkout -b feature/new-skill`
3. 使用 `skill-creator` 创建新 Skill
4. 验证符合规范
5. 提交 PR

---

## 许可证

MIT License
