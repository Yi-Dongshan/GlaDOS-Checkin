# Fork 项目开发指南

## 获取和推送流程

### 1. 获取原始代码
```bash
# 克隆原始仓库
git clone https://github.com/原作者/原仓库名.git
```

### 2. 配置远程仓库
```bash
# 删除原有的 origin
git remote remove origin

# 添加你的仓库作为新的 origin
git remote add origin git@github.com:Yi-Dongshan/glados-checkin.git
```

### 3. 代码修改和提交
```bash
# 查看文件状态
git status

# 添加修改的文件
git add .

# 提交修改
git commit -m "update: 修改说明"

# 首次推送到你的仓库
git push -u origin main
```

## 同步原仓库更新

### 1. 添加原仓库作为上游
```bash
# 添加上游仓库
git remote add upstream https://github.com/原作者/原仓库名.git
```

### 2. 获取和合并更新
```bash
# 获取上游更新
git fetch upstream

# 合并上游更新
git merge upstream/main
```

### 3. 推送到个人仓库
```bash
# 推送更新
git push origin main
```

## 注意事项

1. 开发前确认：
   - 检查原仓库的许可证
   - 在 README.md 中注明代码来源
   - 遵守原作者的开源协议

2. 代码提交：
   - 提交前检查敏感信息
   - 保持代码风格一致
   - 写清晰的提交说明

3. 版本控制：
   - 定期同步原仓库更新
   - 解决可能的合并冲突
   - 保持代码版本最新

## 最佳实践

1. 创建开发分支：
```bash
# 创建并切换到新分支
git checkout -b feature-name
```

2. 分批提交更改：
```bash
# 选择性添加文件
git add 文件1 文件2

# 提交具体更改
git commit -m "feature: 新功能说明"
```

3. 合并到主分支：
```bash
# 切换到主分支
git checkout main

# 合并开发分支
git merge feature-name
```