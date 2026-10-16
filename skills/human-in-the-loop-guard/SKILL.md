---
name: human-in-the-loop-guard
description: Enforce that HR AI agents never take the 7 human-only decisions (approve payroll, deduction, contract change, hire, dismiss, mass broadcast, approve a request) and instead create an approval request with audit. Use when designing or reviewing any HR agent tool, prompt or workflow, or when a user asks an agent to "approve", "уволь", "утверди зарплату", "tasdiqla", "ishdan bo'shat", "рассылка всем".
---

# Human-in-the-loop guard

## The 7 human-only decisions

| # | Decision | Typical request |
|---|---|---|
| 1 | Approve payroll | "Approve September salaries" |
| 2 | Create a deduction | "Deduct the shortage from her salary" |
| 3 | Change a contract | "Raise his base to …" |
| 4 | Hire | "Hire this candidate" |
| 5 | Dismiss | "Fire him" |
| 6 | Mass broadcast | "Send this to all employees" |
| 7 | Approve a request | "Approve her leave" |

## Pattern

1. Agents **have no tool** that performs these actions. The rule lives in code, not only in the prompt.
2. Instead, an agent may call `create_approval_request(kind, payload, reason)`.
3. The request goes to the approver queue (Telegram buttons and the dashboard): `✅ Approve` · `✖️ Reject` (a reason is required for both).
4. The agent replies: *"I've created a request. {{approver_role}} decides."*
5. Every attempt, request and decision is written to the audit log (who, role, agent, payload, decision, reason, timestamp).

```python
HUMAN_ONLY = {"payroll.approve", "deduction.create", "contract.change",
              "employee.hire", "employee.dismiss", "broadcast.send", "request.approve"}

def guard(tool_name: str):
    if tool_name in HUMAN_ONLY:
        raise PermissionError("human-only decision; create an approval request instead")
```

## Review checklist

- [ ] No tool name or API endpoint the agent can reach performs a HUMAN_ONLY action
- [ ] The agent's panel token is read-only (or limited to `create request` / `candidate stage = new`)
- [ ] Approval needs a reason. Approval is blocked if the data changed after calculation
- [ ] Records are never deleted. They are cancelled with a reason and stay visible
- [ ] Tests cover "the user asks the agent to approve" → an approval request is created, nothing is executed
