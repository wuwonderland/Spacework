# FounderOS Dev Team Agent v1 Protocol

## Execution contract

For every software task:

1. Read the task specification and repository instructions.
2. Establish acceptance criteria before editing code.
3. Inspect the existing implementation before proposing changes.
4. Create or use an isolated Git branch/worktree.
5. Produce a concise implementation plan.
6. Implement the smallest coherent change.
7. Run deterministic tests and static checks.
8. Record test commands and outcomes.
9. Run adversarial review against the diff and acceptance criteria.
10. Resolve BLOCKER and MAJOR findings.
11. Re-run deterministic checks after fixes.
12. Commit with a descriptive message.
13. Push the branch.
14. Open or update a pull request.
15. Stop before merge unless a human approval policy explicitly authorizes merge.

## Review gates

FAIL when:

- acceptance criteria are missing;
- tests are absent for material behavior;
- deterministic checks fail;
- security-critical findings remain;
- review findings are unresolved;
- an execution result is UNKNOWN and side effects have not been inspected;
- secrets are detected in tracked files;
- the agent claims completion without repository evidence.

## Cost controls

Use the least expensive capable model by default. Escalate only when:

- implementation is blocked;
- architecture is ambiguous;
- security impact is material;
- deterministic tests expose a complex failure;
- adversarial review finds a material issue.

Do not send full repository dumps to an LLM. Provide targeted files, diffs, logs, and relevant test output.

## External review standard

The reviewer must challenge the implementation, not merely summarize it. At minimum inspect:

- correctness;
- regression risk;
- security;
- dependency changes;
- error handling;
- tests;
- performance where material;
- maintainability;
- hidden assumptions.

A reviewer PASS is not a substitute for CI tests.

## Recovery

If a tool stream stalls, a cron run becomes UNKNOWN, or a network operation fails:

1. Persist the failure in `runlogs/`.
2. Inspect Git state and remote branch before retrying.
3. Determine whether side effects happened.
4. Retry idempotently only when safe.
5. Never blindly repeat an external side effect.
