# HumanOps Router

HumanOps Router lets AI agents escalate work to verified humans when automation is low-confidence, blocked, subjective, or requires judgment.

It routes tasks, collects human review evidence, verifies quality, and returns a structured proof package.

## OKX.AI Genesis Hackathon Fit

- Category: Software Utility / Lifestyle Companion depending on task category
- Service mode: A2A for human work, A2MCP/A2A hybrid for quick votes
- Core value: human judgment fallback for autonomous agents
- Demo target: WorkProof escalates a low-confidence research report and HumanOps returns a review package

Hackathon notes:

- Campaign: OKX.AI Genesis, part of the X Layer Build X series.
- Build goal: create an Agent Service Provider that solves a clear real-world use case.
- Submission flow: list the ASP on OKX.AI, post a short X walkthrough with `#OKXAI`, then submit the project form before the deadline.
- Official context: https://www.okx.com/xlayer/build-x-hackathon

## Problem

Not every agent task can be fully automated. Some deliverables need judgment, factual checking, or subjective QA. Agents need a reliable way to ask humans for help without losing structure, auditability, or payment discipline.

## MVP Tools

### `request_human_review`

Creates a human review task with budget, deadline, deliverable, and desired output format.

### `quick_human_vote`

Routes a small standardized question to one or more reviewers.

### `escalate_workproof_job`

Receives a low-confidence WorkProof job and creates a human QA task.

## Architecture

```text
Agent / WorkProof
  -> HumanOps Intake
  -> Eligibility + Safety Filter
  -> Scope Normalizer
  -> Quote + SLA Engine
  -> Reviewer Matching
  -> Reviewer Portal
  -> Quality Control
  -> Proof Package
```

## Hackathon Demo

1. WorkProof flags a research report as low confidence.
2. HumanOps receives escalation.
3. Reviewer completes a checklist.
4. HumanOps returns `NEEDS_REVISION` with evidence.
5. ASP revises the report.
6. Final WorkProof + HumanOps package returns `PASS`.

## Repository Contents

- `spec.md` - full product and technical specification
- `README.md` - project overview and hackathon framing
- `app/` - FastAPI service implementation
- `tests/` - API tests
- `Dockerfile` - production container
- `okx-ai-listing.md` - marketplace listing draft
- `DEMO_SCRIPT.md` - 90-second walkthrough script

## Run Locally

```bash
uv run uvicorn app.main:app --reload
```

Then open:

- API docs: `http://127.0.0.1:8000/docs`
- MCP-style manifest: `http://127.0.0.1:8000/mcp`
- Demo payloads: `http://127.0.0.1:8000/demo`

## Test

```bash
uv run --extra dev pytest
```

## Production Notes

- Set `HUMANOPS_API_KEY` before exposing paid endpoints.
- Deploy behind HTTPS before OKX.AI registration.
- Use `HUMANOPS_DATA_DIR` for persistent SQLite task storage.
- Live operation requires a real reviewer pool and payout workflow; the MVP provides task routing, quotes, reviewer submission, and proof packages.

## Contributor

- eosadolor382@gmail.com

## Status

Production-shaped MVP: task intake, safety filter, quote/SLA engine, WorkProof escalation, review submission, proof packages, persistence, tests, Dockerfile, listing copy, and demo script are implemented.
