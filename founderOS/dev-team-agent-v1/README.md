# FounderOS Dev Team Agent v1

## Purpose

Build a reusable AI development team that can take a software task from specification through implementation, testing, adversarial review, and pull request preparation.

This module is intentionally separate from the Japan Real Estate Agent. The Japan RE agent remains a reference implementation for evidence/review architecture.

## Core lifecycle

TASK
→ PLAN
→ IMPLEMENT
→ TEST
→ REVIEW
→ SECURITY REVIEW
→ FIX
→ RE-TEST
→ PR
→ HUMAN APPROVAL

## Operating principles

1. GitHub is the source of truth for code, task state, evidence, and review artifacts.
2. No agent may declare a task complete solely from its own output.
3. Code must pass deterministic tests before final review.
4. Material implementation decisions receive an adversarial review.
5. Failed review findings become structured artifacts and drive a repair cycle.
6. Unknown/interrupted executions are inspected before retrying.
7. Agents must work in isolated branches/worktrees.
8. No automatic merge to the production branch.
9. Secrets never belong in source files, prompts, or commits.
10. Cost-aware model routing is mandatory.

## Suggested model roles

- Hermes: orchestration, terminal, browser, GitHub, task execution.
- Low-cost model: routine coding, extraction, tests, refactors.
- Strong coding/reasoning model: architecture and difficult implementation.
- Independent reviewer: adversarial code review, security/logic challenge.
- GitHub Actions: deterministic CI, tests, linting, security checks.

## Task states

QUEUED
RUNNING
WAITING_TOOL
WAITING_APPROVAL
RETRYING
FAILED
REVIEW_REQUIRED
READY_FOR_PR
READY_FOR_DECISION
COMPLETED
UNKNOWN

UNKNOWN is never automatically retried until Git state and side effects are inspected.

## Required artifacts

- `tasks/` — task specifications and acceptance criteria
- `plans/` — implementation plans
- `changes/` — implementation notes
- `tests/` — test evidence
- `reviews/` — adversarial review findings
- `security/` — security findings
- `runlogs/` — execution failures and recovery records
- `reports/` — final task summaries

## v1 success criteria

A task is not complete until:

- acceptance criteria are explicit;
- implementation is committed on an isolated branch;
- deterministic tests pass;
- review findings are resolved or explicitly accepted by a human;
- a pull request is prepared;
- no untracked secret or credential is present;
- the final status is reproducible from repository artifacts.

## FounderOS integration boundary

FounderOS will orchestrate this module later. This v1 module should remain independently runnable through Hermes + GitHub so it can be validated before being embedded into FounderOS core.
