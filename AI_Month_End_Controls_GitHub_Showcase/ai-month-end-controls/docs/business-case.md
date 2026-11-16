# Business case and solution ownership

## Problem statement
In a recurring month-end process, Finance has booked expenses and another team has approved supplier invoices. Neither dataset alone answers the two operational questions: what is missing and what has been allocated incorrectly? Manual comparison carries high cognitive load because references, currency and accounting dimensions may differ.

## Target operating model
A trained reviewer provides two files and the review month. A reusable AI Skill applies a written policy for scope, matching, currency, classification and output. The reviewer checks any suggested adjustment against its source, corrects the source journal if necessary, and forwards concise feedback to Finance.

## Human-owned decisions
A responsible analyst remains accountable for (a) whether invoice approval is accurate, (b) whether a matching posting is truly absent, (c) the nature of each expense, (d) whether the account/cost center/project mapping should change, and (e) whether Finance should post anything.

## Solution-design contributions illustrated
- Translate two messy business questions into mutually understandable outcomes.
- Specify data input contracts and date-scope rules.
- Distinguish absent postings from source-quality problems and mapping errors.
- Make uncertainty explicit instead of presenting a confident wrong answer.
- Establish one concise output that stakeholders can reuse each close.
- Build a handover-friendly, explainable workflow with a predictable invocation pattern.

## Why a Skill rather than one long prompt?
The same business rules must be applied repeatedly, by different people, across successive review months. A dedicated Skill encapsulates those rules and output expectations, while lightweight project instructions tell the team what to attach and what prompt to use. The goal is **process consistency and transferability**, not autonomous accounting.

## Outcome evidence in this public repository
The demo proves that a *synthetic fixture* can be processed to produce testable action categories. It does **not** prove any real company's control performance or a production-system deployment. Public numbers should be interpreted exclusively as invented demonstration metrics.
