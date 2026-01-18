# Claude Skills Configuration

此目录包含 Claude Code 的本地配置和技能。

## 📚 已安装的 Skills

### creating-agent-skills (Meta-skill)

这是一个特殊的 "meta-skill"，用于创建其他 Claude Agent Skills。

**用途**：
- 创建新的 skills
- 将文档/工作流转换为 skills
- 重构现有 skills
- 学习 skill 开发最佳实践

**使用方法**：
```
/creating-agent-skills
```

**为什么需要这个 skill？**

在 Agent-Skills 仓库中开发新 skills 时，使用这个 meta-skill 可以：
1. 确保新 skill 符合规范（< 500 行，正确的 frontmatter）
2. 自动应用最佳实践（progressive disclosure, 第三人称描述）
3. 生成标准的目录结构（SKILL.md, references/, assets/, scripts/）
4. 验证 skill 质量

## 📁 目录结构

```
.claude/
├── skills/
│   └── creating-agent-skills -> ../../creating-agent-skills
└── README.md (此文件)
```

符号链接指向仓库中的实际 skill 目录，这样可以：
- 避免重复文件
- 确保使用最新版本
- 方便在本仓库中使用 meta-skill

## 🔧 配置说明

当在 Agent-Skills 仓库中工作时，Claude Code 会：
1. 自动加载 `.claude/skills/` 下的所有 skills
2. 允许通过 `/creating-agent-skills` 命令调用
3. 使用 meta-skill 的规范创建新 skills

## 💡 开发流程

1. **创建新 skill**：
   ```
   /creating-agent-skills
   ```
   然后描述你想创建的 skill

2. **验证 skill**：
   Meta-skill 会自动检查：
   - SKILL.md 是否 < 500 行
   - Frontmatter 是否正确
   - 描述是否使用第三人称
   - 文件结构是否规范

3. **测试 skill**：
   创建后，可以直接在项目中测试新 skill

## 📝 注意事项

- 这个配置是为了在 Agent-Skills 仓库内部开发使用
- 其他项目使用 skills 时，应该从这个仓库复制或链接需要的 skills
- Meta-skill 是所有 skill 开发的基础，应该保持最新

## 🔗 相关文档

- [Skill 规范](../creating-agent-skills/references/specification.md)
- [最佳实践](../creating-agent-skills/references/best-practices.md)
- [常见错误](../creating-agent-skills/references/common-mistakes.md)