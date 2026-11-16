# Business case — from manual review to a transferable workflow

[Back to the LedgerSignal overview](../README.md)

## 1. The situation

In many businesses, one team approves supplier invoices while Finance maintains the records of what has been booked. Both sources describe part of the same activity, but they are not automatically aligned.

At month-end, a reviewer needs to spot expenses that may be missing, amounts that do not match, and charges that may have been assigned to the wrong team, project, or account. Reviewing those differences manually requires familiarity with dates, invoice references, currencies, and how the business actually operates.

The challenge is not merely that spreadsheets are inconvenient. It is that **repeatable decisions are hidden inside one person's manual review process**.

## 2. The opportunity

The guiding question was:

> Could we make this monthly check faster and easier to hand over, while preserving the reviewer's judgment on uncertain financial items?

The desired outcome was a practical workflow, not an autonomous accounting system: a colleague should be able to provide the right inputs, follow the same decision logic, and receive a clear list of issues to confirm.

## 3. The solution approach

The work was organized around five design choices:

1. **Two clear inputs:** an invoice-approval record and a Finance expense record, both provided by the user.
2. **A defined review period:** avoid mixing prior months, late approvals, and current activity indiscriminately.
3. **A small number of useful outcomes:** potential missing expense, possible incorrect allocation, needs verification, and information only.
4. **Human validation before action:** a flagged item is a question to investigate, not proof that an accounting entry must be made.
5. **Predictable outputs:** a short written summary, a structured workbook, and a draft response suitable for the next stakeholder discussion.

A reusable **Claude Skill** stores the workflow instructions so the process does not depend on repeatedly writing a long prompt. Separate project instructions explain how team members start a new review, which files to attach, and what to check before sending feedback.

## 4. My role and ownership

This was a business-led solution-design initiative, involving more than building an AI instruction file.

- **Process analysis:** identified the recurring manual workload and the decisions hidden within it.
- **Requirements and control design:** defined what the review should compare, how exceptions should be grouped, and when the correct result is 'check first'.
- **AI-enabled implementation:** designed and iterated the Skill, reviewed results, and improved instructions based on observed issues.
- **Quality assurance:** tested edge cases and challenged unsupported recommendations, including situations where the source approval record might itself be wrong.
- **Rollout and enablement:** created accessible project instructions, shared the workflow with users, and supported hands-on onboarding, training, and QA.
- **Operational handover:** reduced reliance on the creator's memory by making expectations and review steps explicit.

Technical implementation mattered, but the central contribution was **turning business understanding into a process that others could use**.

## 5. What changed

| Dimension | Previous approach | Designed approach |
|---|---|---|
| Execution | Manual cross-checking and ad hoc investigation | Guided monthly review of two supplied files |
| Consistency | Dependent on reviewer knowledge | Written rules, cutoff logic, and repeatable output |
| Visibility | Mismatches require individual investigation | Findings grouped by what a human should do next |
| Quality | Greater risk of treating every difference as an error | Explicit 'check first' and information-only routes |
| Communication | Findings summarized manually | Structured review workbook and response draft |
| Continuity | Knowledge held by an individual | Project instructions, onboarding, and handover |

### Measured review-time improvement

The recurring monthly review took approximately **2–3 hours before** and **20–50 minutes after** introducing the Skill, including human validation. Comparing the midpoints of these observed ranges (150 minutes versus 35 minutes) yields an approximate **76.7% (~77%) reduction in review time**.

This is a midpoint-based calculation from measured operating ranges, rather than an average calculated from individual runs. It is separate from the fictional financial results in the public demo.

## 6. Why human review stays central

Neither input should be assumed to be perfect. An approved invoice may contain a typing error; Finance may have booked the same economic cost using a different reference; a cross-team posting may be legitimate; and a missing amount may be impossible to convert reliably without further evidence.

The workflow is designed to **surface questions and separate levels of certainty**, not to post entries or make authoritative accounting decisions. A trained reviewer checks the source and confirms any suggested action with Finance.

## 7. What the public project actually proves

LedgerSignal is an **independently authored public reconstruction** using invented vendors, invoice numbers, accounts, cost centers, amounts, and scenarios. It is not a release of an employer's files or proprietary Skill.

- The [example inputs](../demo/inputs/) show what a controlled sample review looks like.
- The [reference code](../src/reconcile_demo.py) produces deterministic findings from the fictional CSV data.
- The [tests](../tests/) verify 14 specific scenarios in that reference engine.
- The [example Claude Skill](../skills/month-end-expense-review/SKILL.md) illustrates the AI-assisted workflow approach, but has not been separately proven to reproduce the Python output in every Claude runtime.

See [validation details](validation.md) and [control design](control-design.md) for deeper technical notes.

## 8. Broader relevance

The same solution-design pattern is useful beyond financial close: **understand two sources, define an operating policy, surface exceptions, and keep people responsible for decisions**. The transferable skills are process discovery, decision design, AI enablement, validation, and adoption—not expertise in a single accounting system.
