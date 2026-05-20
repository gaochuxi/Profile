import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI
from pydantic import BaseModel


BASE_URL = os.getenv("AI_JUDGE_BASE_URL", "https://api.chatanywhere.tech")
API_KEY = os.getenv("AI_JUDGE_API_KEY")
PORT = int(os.getenv("AI_JUDGE_PORT", "9001"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app = FastAPI(title="AI Smart Court")
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "templates", "static")), name="static")


class CaseRequest(BaseModel):
    case_description: str
    model_type: str


FALLBACK_MODELS = [
    "gpt-5.2",
    "gpt-5.1",
    "gpt-5",
    "gpt-4o",
    "gpt-4.1",
    "deepseek-r1",
    "deepseek-v3",
    "deepseek-v3-2-exp",
    "gpt-4o-mini",
    "gpt-3.5-turbo",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "gpt-5-mini",
    "gpt-5-nano",
]


def get_client() -> OpenAI:
    if not API_KEY:
        raise RuntimeError("AI_JUDGE_API_KEY is not configured.")
    return OpenAI(api_key=API_KEY, base_url=BASE_URL)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/models")
async def get_models():
    try:
        client = get_client()
        models_page = client.models.list()
        model_list = [model.id for model in models_page.data]
        return {"models": model_list or FALLBACK_MODELS}
    except Exception as exc:
        print(f"Failed to fetch remote models, using fallback list: {exc}")
        return {"models": FALLBACK_MODELS}


@app.post("/api/judge")
async def judge_case(item: CaseRequest):
    if not item.case_description or len(item.case_description.strip()) < 5:
        return {"verdict": "案情描述过短，无法进行可靠分析。"}

    try:
        client = get_client()
        response = client.chat.completions.create(
            model=item.model_type,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "你是一名公正、严谨的法律分析助手。请根据用户提供的案件描述进行法律逻辑分析。"
                        "输出结构必须包含：1.【案情核心】一句话概括；"
                        "2.【法律适用】引用相关法理或通用法律原则；"
                        "3.【分析意见】说明关键争点；4.【参考结论】给出明确但非正式的结论。"
                        "必须提醒用户：该内容仅供学习和研究参考，不构成正式法律意见。"
                    ),
                },
                {"role": "user", "content": item.case_description},
            ],
            stream=False,
        )
        return {"verdict": response.choices[0].message.content}
    except Exception as exc:
        print(f"AI judge request failed: {exc}")
        return {"verdict": f"系统暂时无法完成分析：{exc}"}


if __name__ == "__main__":
    print(f"AI Smart Court running at http://0.0.0.0:{PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
