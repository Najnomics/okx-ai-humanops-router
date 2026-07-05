# HumanOps Router

HumanOps Router lets AI agents escalate work to verified humans when automation is low-confidence, blocked, subjective, or requires judgment.

It routes tasks, collects human review evidence, verifies quality, and returns a structured proof package.

## OKX.AI Genesis Hackathon Fit

- Category: Software Utility / Lifestyle Companion depending on task category
- Service mode: A2A for human work, A2MCP/A2A hybrid for quick votes
- Core value: human judgment fallback for autonomous agents
- Demo target: WorkProof escalates a low-confidence research report and HumanOps returns a review package

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

## Contributor

- eosadolor382@gmail.com

## Status

Hackathon planning repository. Implementation scaffold will add task intake, reviewer portal, proof packages, and WorkProof integration.

