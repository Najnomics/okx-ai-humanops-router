# HumanOps Router Demo Script

## 90-Second Walkthrough

1. Open `/docs`.
2. Call `/tools/escalate_workproof_job` with a low-confidence WorkProof job.
3. Show the generated quote, SLA, and reviewer checklist.
4. Call `/tasks/{task_id}/submit_review` as a reviewer.
5. Show the structured proof package with `NEEDS_REVISION`.
6. Call `/tools/quick_human_vote` with three reviewer responses and show consensus.

## X Post Draft

Built HumanOps Router for #OKXAI: a human judgment layer for agents. It turns low-confidence AI outputs into quoted review tasks, reviewer checklists, and proof packages that agents can use before payment release.

