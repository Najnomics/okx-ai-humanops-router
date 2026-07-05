import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

from .schemas import EscalateWorkProofJob, QuickHumanVote, RequestHumanReview, SubmitReview


BLOCKED_TERMS = {"dox", "steal", "phishing", "malware", "exploit private", "seed phrase"}


def stable_hash(payload: Any) -> str:
    return "0x" + hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def deadline(minutes: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(minutes=minutes)).isoformat()


def safety_check(text: str) -> list[str]:
    lowered = text.lower()
    return [term for term in BLOCKED_TERMS if term in lowered]


def checklist_for(review_type: str, specific_questions: list[str] | None = None) -> list[str]:
    base = {
        "research_qa": ["Required sections present", "Claims supported by sources", "Unsupported claims flagged", "Summary matches brief"],
        "lead_list_qa": ["Required columns present", "Sample rows checked", "Duplicates flagged", "Relevance checked"],
        "listing_qa": ["Value proposition clear", "Tools and pricing clear", "Demo path understandable", "No misleading claims"],
        "general_qa": ["Meets task brief", "Evidence is sufficient", "Output is useful", "Risks are noted"],
    }[review_type]
    return base + (specific_questions or [])


def quote_for(payload: RequestHumanReview) -> dict[str, Any]:
    base = max(2.0, payload.budget_usd)
    urgency_multiplier = 1.5 if payload.deadline_minutes <= 30 else 1.0
    confidentiality_multiplier = 1.25 if payload.confidentiality == "confidential" else 1.0
    quote = round(base * urgency_multiplier * confidentiality_multiplier, 2)
    return {"quote_usd": quote, "estimated_completion_minutes": payload.deadline_minutes, "escrow_required": True}


def create_review_task(payload: RequestHumanReview) -> dict[str, Any]:
    blocked = safety_check(f"{payload.task_brief} {payload.deliverable_text or ''}")
    if blocked:
        return {
            "task_id": f"task_{uuid4().hex[:12]}",
            "status": "rejected",
            "reason": "safety_filter_rejected",
            "blocked_terms": blocked,
            "proof_hash": stable_hash({"blocked_terms": blocked}),
        }
    task_id = f"task_{uuid4().hex[:12]}"
    task = {
        "task_id": task_id,
        "status": "pending_review",
        "review_type": payload.review_type,
        "task_brief": payload.task_brief,
        "deliverable_url": str(payload.deliverable_url) if payload.deliverable_url else None,
        "quote": quote_for(payload),
        "deadline_at": deadline(payload.deadline_minutes),
        "reviewer_assignment": {
            "reviewer_pool": "manual_hackathon_pool",
            "required_skill": payload.review_type,
            "reviewer_count": 1,
        },
        "checklist": checklist_for(payload.review_type),
        "proof_hash": stable_hash(payload.model_dump(mode="json")),
    }
    return task


def quick_vote(payload: QuickHumanVote) -> dict[str, Any]:
    task_id = f"vote_{uuid4().hex[:12]}"
    valid_responses = [item for item in payload.reviewer_responses if item in payload.options]
    if valid_responses:
        counts = Counter(valid_responses)
        top, votes = counts.most_common(1)[0]
        status = "completed" if len(valid_responses) >= payload.reviewer_count else "collecting_votes"
        confidence = round(votes / max(1, len(valid_responses)), 2)
    else:
        top = None
        status = "pending_review"
        confidence = 0
    return {
        "task_id": task_id,
        "status": status,
        "question": payload.question,
        "options": payload.options,
        "reviewer_count": payload.reviewer_count,
        "responses_collected": len(valid_responses),
        "consensus": top,
        "confidence": confidence,
        "deadline_at": deadline(payload.deadline_minutes),
        "proof_hash": stable_hash(payload.model_dump(mode="json")),
    }


def escalate_workproof(payload: EscalateWorkProofJob) -> dict[str, Any]:
    review_payload = RequestHumanReview(
        task_brief=payload.task_brief,
        deliverable_url=payload.deliverable_url,
        review_type="research_qa",
        budget_usd=payload.budget_usd,
        deadline_minutes=60,
    )
    task = create_review_task(review_payload)
    task["workproof_job_id"] = payload.workproof_job_id
    task["escalation_reason"] = payload.reason
    task["checklist"] = checklist_for("research_qa", payload.specific_questions)
    return task


def submit_review(task: dict[str, Any], payload: SubmitReview) -> dict[str, Any]:
    proof = {
        **task,
        "status": "completed",
        "decision": payload.decision,
        "human_review_summary": payload.summary,
        "reviewer_id": payload.reviewer_id,
        "reviewer_confidence": payload.confidence,
        "checklist_results": payload.checklist_results,
        "evidence_items": payload.evidence_items,
        "recommended_action": "accept" if payload.decision == "PASS" else "request_revision" if payload.decision == "NEEDS_REVISION" else "reject",
    }
    proof["proof_hash"] = stable_hash(proof)
    return proof

