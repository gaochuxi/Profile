# Chuxi Gao Profile

一个适合部署到 GitHub Pages 的个人学术主页，包含 English / 简体中文 / 繁體中文三语切换。

## 内容

- 个人主页：`index.html`
- 三语切换：`script.js`
- 视觉样式：`styles.css`
- 工具项目：`tools/ai-judge`

## AI Smart Court

`tools/ai-judge` 是一个 FastAPI + Vue 的 AI 智慧法庭原型。运行前请设置 API Key 环境变量，不要把密钥写入代码：

```bash
export AI_JUDGE_API_KEY="你的 API Key"
cd tools/ai-judge
python3 -m pip install -r requirements.txt
python3 app.py
```

访问 `http://localhost:9001`。

## 本地预览

直接在浏览器打开 `index.html` 即可预览，也可以使用任意静态服务器运行。

## 部署到 GitHub Pages

1. 将代码推送到 `main` 分支。
2. 打开仓库 Settings。
3. 进入 Pages。
4. Source 选择 `Deploy from a branch`，Branch 选择 `main` 和 `/root`。
