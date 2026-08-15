# Activity 9: Build a Leave Request Agent and Approval Flow

> **Synthetic learning case:** Do not upload live employee or candidate data.

## Scenario

Employees submit leave through messages that HR rekeys into a tracker. Errors occur around balance, overlapping dates and manager approvals.

## Learning goal

Design a Copilot Studio agent plus deterministic flow for eligibility, approval, update and notification.

## Microsoft tools

- Microsoft Copilot Studio
- Agent flows or Power Automate
- Teams
- Excel or HRIS sandbox

## Guardrails

- Confirm before submission
- Manager approves exceptions
- Idempotency prevents duplicates

## Detailed procedure

1. Review the synthetic leave policy, balances and requests.
2. Define required inputs and validation messages.
3. Design the conversation to clarify dates, leave type and coverage.
4. Create a deterministic flow for balance check, overlap check and approval routing.
5. Add a confirmation step before the agent calls the flow.
6. Write successful, rejected and failed outcomes to the audit log.
7. Test insufficient balance, duplicate request, missing approver and connector failure.
8. Review access permissions and the employee-facing explanation.

## Prompt scaffold

> You are supporting the HarbourLight Logistics SG training case. Use only the supplied synthetic evidence. Your task is to design a copilot studio agent plus deterministic flow for eligibility, approval, update and notification. State assumptions; cite record IDs or approved source sections; separate observation from inference; flag missing information; list the human checks and approvals required before use.

## Evidence checklist

- [ ] Agent instructions
- [ ] Flow design
- [ ] Approval matrix
- [ ] Audit log and test report
- [ ] Evidence workbook records the input/source, prompt or decision, output, verification, revision and owner.
- [ ] A peer or trainer can reproduce the reasoning from the saved evidence.

## Acceptance criteria

- Confirm before submission
- Manager approves exceptions
- Idempotency prevents duplicates
- The output is accurate, traceable, usable and explicit about uncertainty.
- Consequential decisions and actions remain with an authorised human.

## Scenario questions

1. Which rule belongs in the flow rather than the language model?
2. How will a duplicate submission be detected?
3. Who resolves a disputed balance?

## Submission naming

`A09-<YourName>-Evidence.xlsx` plus the listed deliverables.

## Source anchors

- Course source register: `../../SOURCE-COVERAGE.md`
- Microsoft capability boundary: Microsoft 365 Copilot for generative work; Agent Builder or Copilot Studio for agentic work.

## Recommended team roles and timing

- **HR process owner:** confirms that the output solves the stated build a leave request agent and approval flow outcome and remains consistent with approved policy.
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
