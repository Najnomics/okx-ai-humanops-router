from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, get_settings
from .schemas import EscalateWorkProofJob, QuickHumanVote, RequestHumanReview, SubmitReview
from .service import create_review_task, escalate_workproof, quick_vote, submit_review
from .storage import TaskStore

app = FastAPI(title="HumanOps Router", version="0.1.0", description="Human escalation and proof packages for agent workflows.")

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.cors_origins == "*" else [item.strip() for item in settings.cors_origins.split(",")],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
store = TaskStore(settings.data_dir)


def require_api_key(x_api_key: str | None = Header(default=None), config: Settings = Depends(get_settings)) -> None:
    if config.api_key and x_api_key != config.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


def persist(record: dict) -> dict:
    store.upsert(record["task_id"], record["status"], record)
    return record


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "humanops-router", "mode": "A2A"}


@app.get("/mcp")
def mcp_manifest() -> dict:
    return {
        "name": "HumanOps Router",
        "version": "0.1.0",
        "service_mode": "A2A",
        "tools": [
            {"name": "request_human_review", "endpoint": "/tools/request_human_review"},
            {"name": "quick_human_vote", "endpoint": "/tools/quick_human_vote"},
            {"name": "escalate_workproof_job", "endpoint": "/tools/escalate_workproof_job"},
        ],
    }


@app.post("/tools/request_human_review", dependencies=[Depends(require_api_key)])
def tool_request_human_review(payload: RequestHumanReview) -> dict:
    return persist(create_review_task(payload))


@app.post("/tools/quick_human_vote", dependencies=[Depends(require_api_key)])
def tool_quick_human_vote(payload: QuickHumanVote) -> dict:
    return persist(quick_vote(payload))


@app.post("/tools/escalate_workproof_job", dependencies=[Depends(require_api_key)])
def tool_escalate_workproof_job(payload: EscalateWorkProofJob) -> dict:
    return persist(escalate_workproof(payload))


@app.post("/tasks/{task_id}/submit_review", dependencies=[Depends(require_api_key)])
def task_submit_review(task_id: str, payload: SubmitReview) -> dict:
    task = store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    return persist(submit_review(task, payload))


@app.get("/tasks/{task_id}", dependencies=[Depends(require_api_key)])
def get_task(task_id: str) -> dict:
    task = store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    return task


@app.get("/history", dependencies=[Depends(require_api_key)])
def history(limit: int = 50) -> dict:
    return {"items": store.list_recent(limit=limit)}


@app.get("/demo")
def demo() -> dict:
    return {
        "workproof_escalation": {
            "endpoint": "/tools/escalate_workproof_job",
            "payload": {
                "workproof_job_id": "wp_demo_low_confidence",
                "reason": "low_confidence",
                "specific_questions": ["Are the sources credible?", "Does the report meet the buyer brief?"],
                "budget_usd": 8,
            },
        }
    }

