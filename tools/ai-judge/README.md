# AI Smart Court

一个用于法律学习和研究展示的 AI 辅助分析工具。

## 安全配置

不要把 API Key 写进代码或提交到 GitHub。请用环境变量：

```bash
export AI_JUDGE_API_KEY="你的 API Key"
export AI_JUDGE_BASE_URL="https://api.chatanywhere.tech"
export AI_JUDGE_PORT="9001"
```

## 本地运行

```bash
cd tools/ai-judge
python3 -m pip install -r requirements.txt
python3 app.py
```

然后打开：

```text
http://localhost:9001
```

## 说明

AI 输出仅供学习、研究和原型展示参考，不构成正式法律意见。
