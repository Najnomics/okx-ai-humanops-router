from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


Decision = Literal["PASS", "NEEDS_REVISION", "FAIL"]


class RequestHumanReview(BaseModel):
    task_brief: str
    deliverable_url: HttpUrl | None = None
    deliverable_text: str | None = None
    review_type: Literal["research_qa", "lead_list_qa", "listing_qa", "general_qa"] = "research_qa"
    budget_usd: float = 10
    deadline_minutes: int = 60
    required_output: str = "pass_revision_fail_with_evidence"
    confidentiality: Literal["standard", "confidential"] = "standard"


class QuickHumanVote(BaseModel):
    question: str
    asset_url: HttpUrl | None = None
    reviewer_count: int = 3
    options: list[str] = Field(default_factory=lambda: ["yes", "partly", "no"])
    deadline_minutes: int = 30
    reviewer_responses: list[str] = Field(default_factory=list)


class EscalateWorkProofJob(BaseModel):
    workproof_job_id: str
    reason: str = "low_confidence"
    specific_questions: list[str] = Field(default_factory=list)
    budget_usd: float = 8
    task_brief: str = "Review the WorkProof job and decide whether the deliverable meets the buyer brief."
    deliverable_url: HttpUrl | None = None


class SubmitReview(BaseModel):
    reviewer_id: str
    decision: Decision
    summary: str
    checklist_results: list[dict[str, str]] = Field(default_factory=list)
    evidence_items: list[str] = Field(default_factory=list)
    confidence: float = 0.9

