# Git 和 GitHub 操作指南

## 初始配置

### 1. SSH 密钥配置
```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "你的邮箱@example.com"

# 查看公钥内容
type C:\Users\你的用户名\.ssh\id_ed25519.pub
```
然后将公钥添加到 GitHub 的 SSH Keys 中。

### 2. 测试 SSH 连接
```bash
ssh -T git@github.com
```

## 基本操作流程

### 1. 初始化仓库
```bash
# 初始化 Git 仓库
git init

# 添加远程仓库
git remote add origin git@github.com:用户名/仓库名.git
```

### 2. 添加 .gitignore
创建 `.gitignore` 文件，添加需要忽略的文件和目录：
```plaintext
# 配置文件
config.py

# 日志文件
log/
*.log

# Python
__pycache__/
venv/
```

### 3. 日常代码提交
```bash
# 查看文件状态
git status

# 查看具体修改
git diff

# 添加修改文件
git add .

# 提交修改
git commit -m "update: 更新说明"

# 推送到远程仓库
git push
```

## 常见问题处理

### 1. 敏感信息意外上传
如果不小心上传了敏感文件：
```bash
# 从 Git 历史中删除文件
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch 敏感文件路径" --prune-empty --tag-name-filter cat -- --all

# 强制推送更改
git push origin --force --all
```

### 2. 更改远程仓库地址
```bash
# 删除原有远程仓库
git remote remove origin

# 添加新的远程仓库
git remote add origin 新仓库地址

# 验证远程仓库
git remote -v
```

## 注意事项

1. 提交前务必检查：
   - 使用 `git status` 查看将要提交的文件
   - 使用 `git diff` 查看具体修改内容
   - 确保敏感信息已在 `.gitignore` 中

2. 安全建议：
   - 定期更新 SSH 密钥
   - 不要上传配置文件，使用示例配置文件代替
   - 发现敏感信息泄露及时处理

3. 常用命令退出方式：
   - `git diff` 和 `git log`: 按 `q` 退出
   - vim 编辑器: 按 `Esc` 后输入 `:q` 或 `:wq`

## 最佳实践

1. 提交前预览：
```bash
git add -n .  # 预览要添加的文件
```

2. 分批提交：
```bash
git add 文件1 文件2  # 选择性添加文件
git commit -m "update: 具体更新内容"
```

3. 保护敏感信息：
   - 使用 `config.example.py` 作为配置文件模板
   - 实际配置文件使用 `config.py` 并加入 `.gitignore`