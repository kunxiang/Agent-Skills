# Agent Skills 仓库

公司 AI 应用开发使用的 Claude Agent Skills 集合。

## 可用 Skills

| Skill | 用途 | 调用方式 |
|-------|------|----------|
| **creating-agent-skills** ⭐ | **元技能** - 创建其他 Claude Agent Skills 的基础技能 | `/creating-agent-skills` |
| **jtl-nova-template** | JTL-Shop 5 NOVA 模板开发 | `/jtl-nova-template` |

> ⭐ **元技能说明**：`creating-agent-skills` 是一个特殊的"生产技能的技能"，它定义了如何创建符合规范的新技能，是本仓库所有技能开发的基础。

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

## 注意事项

- 只安装来自可信来源的 Skills
- 审查 `scripts/` 中的所有代码
- 不要在 Skills 中存储凭据

## 许可证

MIT License
