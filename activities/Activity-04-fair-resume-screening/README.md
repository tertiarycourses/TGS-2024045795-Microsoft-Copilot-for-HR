# Activity 4: Build a Fair Resume Evidence Matrix

> **Synthetic learning case:** Do not upload live employee or candidate data.

## Scenario

HarbourLight received six synthetic applications for the Workforce Operations Analyst role. The hiring manager wants a fast shortlist without an opaque score.

## Learning goal

Use Microsoft 365 Copilot to extract job-related evidence and prepare a human-reviewed shortlist.

## Microsoft tools

- Excel with Microsoft 365 Copilot
- Word

## Guardrails

- Synthetic resumes only
- Protected attributes excluded
- AI cannot reject candidates

## Detailed procedure

1. Read the approved job outcomes and anchored rubric.
2. Review the six synthetic resumes without adding criteria.
3. Prompt Copilot to extract verbatim evidence for each criterion and mark gaps as unknown.
4. Check every extracted item against the source resume.
5. Calculate rubric totals using workbook formulas; do not let Copilot invent a score.
6. Review for proxy variables and inconsistent evidence standards.
7. Record human shortlist decisions and reasons separately from the AI extraction.
8. Draft candidate next-step messages without disclosing other candidates' information.

## Prompt scaffold

> You are supporting the HarbourLight Logistics SG training case. Use only the supplied synthetic evidence. Your task is to use microsoft 365 copilot to extract job-related evidence and prepare a human-reviewed shortlist. State assumptions; cite record IDs or approved source sections; separate observation from inference; flag missing information; list the human checks and approvals required before use.

## Evidence checklist

- [ ] Evidence matrix
- [ ] Uncertainty log
- [ ] Human shortlist rationale
- [ ] Evidence workbook records the input/source, prompt or decision, output, verification, revision and owner.
- [ ] A peer or trainer can reproduce the reasoning from the saved evidence.

## Acceptance criteria

- Synthetic resumes only
- Protected attributes excluded
- AI cannot reject candidates
- The output is accurate, traceable, usable and explicit about uncertainty.
- Consequential decisions and actions remain with an authorised human.

## Scenario questions

1. Where did missing evidence risk becoming a negative assumption?
2. What would make this screening process contestable?
3. Which errors matter most: false inclusion or false exclusion?

## Submission naming

`A04-<YourName>-Evidence.xlsx` plus the listed deliverables.

## Source anchors

- Course source register: `../../SOURCE-COVERAGE.md`
- Microsoft capability boundary: Microsoft 365 Copilot for generative work; Agent Builder or Copilot Studio for agentic work.

## Recommended team roles and timing

- **HR process owner:** confirms that the output solves the stated build a fair resume evidence matrix outcome and remains consistent with approved policy.
- **AI operator or maker:** records the exact prompt, instructions, knowledge sources, tool choices and revisions.
- **Reviewer or approver:** independently checks evidence, permissions, fairness, privacy and any consequential action.
- **Evidence recorder:** keeps the workbook complete enough for another person to reproduce the reasoning.

Allow about 35–50 minutes for the first build, 15 minutes for testing and verification, and 10 minutes for peer challenge and reflection. The trainer may adjust the timing to fit the delivery mode.

## Verification method

1. Compare every factual statement or extracted item with the supplied source record.
2. Mark missing information as unknown; do not convert absence into a negative assumption.
3. Check that personal data, tool access and sharing are limited to the stated purpose.
4. Test one normal case, one ambiguous case, one out-of-scope case and one failure or exception.
5. Ask a peer to challenge the decision, then record whether you accepted or rejected the challenge and why.
6. Confirm the named human owner can correct, stop or reverse the work before submission.

## Troubleshooting and recovery

- If Copilot invents evidence, narrow the prompt to named files, tables or record IDs and request citations.
- If an agent answers outside scope, strengthen instructions, remove inappropriate knowledge or tools, and add an explicit escalation response.
- If a flow fails or repeats an action, do not report success. Preserve the error, check the audit record, use a unique request key, and route the case to the human owner.
- If the output is polished but cannot be traced to evidence, treat it as incomplete and rebuild the evidence chain.
