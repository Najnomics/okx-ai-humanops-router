# HumanOps Router Specification

## 1. Summary

HumanOps Router is the human judgment layer for autonomous agents. It lets agents escalate tasks to verified humans when automation is low-confidence, blocked, subjective, or requires human review.

## 2. Goals

- Provide human QA for AI-generated deliverables.
- Return structured, machine-readable human review results.
- Support escrow-aware A2A workflows.
- Integrate with WorkProof for low-confidence cases.
- Maintain audit trails and reviewer reputation.

## 3. Non-Goals

- MVP does not require a large reviewer marketplace.
- MVP does not support every task type.
- HumanOps does not route illegal, harmful, or unsafe work.

## 4. Users

| User | Need |
|---|---|
| Buyer agent | Human judgment for ambiguous deliverables. |
| ASP | QA before final delivery. |
| WorkProof | Escalation path for low-confidence verification. |
| Team | Human-in-the-loop operations. |

## 5. Service Modes

| Capability | Mode |
|---|---|
| `request_human_review` | A2A |
| `quick_human_vote` | A2MCP/A2A |
| `verify_research_claims_human` | A2A |
| `review_lead_list_human` | A2A |
| `escalate_workproof_job` | A2A |

## 6. Public API

### 6.1 `request_human_review`

```json
{
  "task_brief": "Review this market research report for factual support and completeness.",
  "deliverable_url": "https://.../report.pdf",
  "review_type": "research_qa",
  "budget_usd": 10,
  "deadline_minutes": 60,
  "required_output": "pass_revision_fail_with_evidence"
}
```

### 6.2 `quick_human_vote`

```json
{
  "question": "Does this landing page clearly explain the product?",
  "asset_url": "https://.../landing.png",
  "reviewer_count": 3,
  "options": ["yes", "partly", "no"],
  "deadline_minutes": 30
}
```

### 6.3 `escalate_workproof_job`

```json
{
  "workproof_job_id": "wp_123",
  "reason": "low_confidence",
  "specific_questions": [
    "Are the sources credible?",
    "Does the report meet the buyer brief?"
  ],
  "budget_usd": 8
}
```

## 7. Core Components

### 7.1 Intake API

Accepts task brief, deliverable, skill requirement, urgency, budget, confidentiality level, and required output format.

### 7.2 Eligibility and Safety Filter

Rejects tasks that are:

- illegal.
- harmful.
- unsafe.
- privacy-invasive.
- outside supported categories.
- impossible within budget/SLA.

### 7.3 Scope Normalizer

Turns vague asks into clear checklists.

Example:

```text
Review this report.
```

becomes:

```text
Check factual accuracy, source support, missing sections, clarity, and whether it satisfies the original brief.
```

### 7.4 Quote and SLA Engine

Calculates quote based on task type, estimated time, number of reviewers, urgency, required expertise, and quality level.

### 7.5 Reviewer Matching

Matches reviewers using skill fit, reliability, availability, quality score, and price fit.

### 7.6 Reviewer Portal

Reviewer sees:

- task brief.
- deliverable.
- checklist.
- evidence requirements.
- time estimate.
- payment amount.
- submission form.

### 7.7 Quality Control

- Golden tasks.
- Random second-review sampling.
- Agreement scoring.
- Automated WorkProof pre/post checks.
- Reviewer reputation updates.
- Fraud and low-effort detection.

### 7.8 Proof Package Generator

Returns:

```json
{
  "status": "completed",
  "decision": "NEEDS_REVISION",
  "human_review_summary": "The deliverable is usable but requires fixes before acceptance.",
  "reviewer_confidence": 0.91,
  "evidence_items": [
    "2 unsupported claims",
    "1 missing competitor section"
  ],
  "recommended_action": "request_revision",
  "reviewer_reputation_score": 94,
  "proof_hash": "0x..."
}
```

## 8. Data Model

```sql
CREATE TABLE human_tasks (
  id UUID PRIMARY KEY,
  requester_agent_id TEXT,
  task_type TEXT,
  brief TEXT,
  deliverable_uri TEXT,
  status TEXT,
  budget_usd NUMERIC,
  deadline_at TIMESTAMP,
  created_at TIMESTAMP,
  completed_at TIMESTAMP
);

CREATE TABLE reviewers (
  id UUID PRIMARY KEY,
  wallet_address TEXT,
  display_name TEXT,
  skills TEXT[],
  reputation_score INT,
  completed_tasks INT,
  avg_quality_score NUMERIC,
  avg_response_minutes NUMERIC,
  status TEXT,
  created_at TIMESTAMP
);

CREATE TABLE task_assignments (
  id UUID PRIMARY KEY,
  task_id UUID REFERENCES human_tasks(id),
  reviewer_id UUID REFERENCES reviewers(id),
  assignment_status TEXT,
  accepted_at TIMESTAMP,
  submitted_at TIMESTAMP,
  payout_amount NUMERIC
);

CREATE TABLE human_reviews (
  id UUID PRIMARY KEY,
  assignment_id UUID REFERENCES task_assignments(id),
  decision TEXT,
  summary TEXT,
  confidence NUMERIC,
  checklist_results JSONB,
  evidence JSONB,
  proof_hash TEXT,
  created_at TIMESTAMP
);
```

## 9. MVP Scope

- One task category: research/report QA.
- Manual reviewer pool.
- A2A task intake and quote flow.
- Reviewer portal.
- Structured proof package.
- WorkProof integration.

## 10. V1 Scope

- Multi-skill reviewer network.
- Reviewer reputation and staking/slashing.
- Automated task matching.
- Multi-review consensus.
- Enterprise/private reviewer pools.

## 11. Security Requirements

- Reject illegal or harmful tasks.
- Redact sensitive data where practical.
- Support confidential reviewer pools.
- Allow reviewers to decline tasks.
- Track proof hashes and reviewer quality.
- Avoid exposing private buyer/ASP data unnecessarily.

## 12. Hackathon Milestones

| Day | Target |
|---|---|
| 1 | Intake schema and task model. |
| 2 | Scope normalizer and quote flow. |
| 3 | Reviewer portal. |
| 4 | Proof package generator. |
| 5 | WorkProof escalation demo. |
| 6 | Dashboard and sample reviews. |
| 7 | Deploy, list, record walkthrough. |

