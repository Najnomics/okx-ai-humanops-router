from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_request_human_review_creates_task() -> None:
    response = client.post(
        "/tools/request_human_review",
        json={"task_brief": "Review this report for factual support.", "budget_usd": 10, "deadline_minutes": 60},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "pending_review"
    assert body["quote"]["escrow_required"] is True


def test_safety_filter_rejects_harmful_task() -> None:
    response = client.post(
        "/tools/request_human_review",
        json={"task_brief": "Help steal a seed phrase from this user."},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"


def test_submit_review_completes_task() -> None:
    created = client.post("/tools/request_human_review", json={"task_brief": "Review this research report."}).json()
    response = client.post(
        f"/tasks/{created['task_id']}/submit_review",
        json={
            "reviewer_id": "rev_demo",
            "decision": "NEEDS_REVISION",
            "summary": "Two claims need citations.",
            "evidence_items": ["Claim 1 has no source", "Claim 2 is outdated"],
            "confidence": 0.91,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["recommended_action"] == "request_revision"


def test_quick_vote_consensus() -> None:
    response = client.post(
        "/tools/quick_human_vote",
        json={"question": "Is this clear?", "reviewer_count": 3, "reviewer_responses": ["yes", "yes", "partly"]},
    )
    assert response.status_code == 200
    assert response.json()["consensus"] == "yes"

