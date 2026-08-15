# Activity 11: Design Safe Employee Service and Offboarding

> **Synthetic learning case:** Do not upload live employee or candidate data.

## Scenario

HR wants one conversational front door for benefits, payroll status, employee-relations triage and offboarding tasks.

## Learning goal

Define privacy-aware routing, escalation and least-privilege actions across sensitive HR services.

## Microsoft tools

- Microsoft Copilot Studio
- Teams
- SharePoint
- HRIS sandbox

## Guardrails

- Authenticate personal requests
- No legal or clinical advice
- Separation of duties for access removal

## Detailed procedure

1. Classify the supplied intents by sensitivity, consequence and reversibility.
2. Decide which intents are answer, retrieve, transact or escalate.
3. Map authentication and minimum data for each service.
4. Design response patterns for payroll dispute, wellbeing disclosure and employee-relations complaint.
5. Build the offboarding sequence for confirmation, assets, access and knowledge transfer.
6. Assign maker, approver and verifier roles.
7. Test data leakage, social engineering, urgent safety and incomplete exit scenarios.
8. Record operational owner, retention and incident response.

## Prompt scaffold

> You are supporting the HarbourLight Logistics SG training case. Use only the supplied synthetic evidence. Your task is to define privacy-aware routing, escalation and least-privilege actions across sensitive hr services. State assumptions; cite record IDs or approved source sections; separate observation from inference; flag missing information; list the human checks and approvals required before use.

## Evidence checklist

- [ ] Intent-and-risk catalogue
- [ ] Escalation matrix
- [ ] Offboarding control map
- [ ] Evidence workbook records the input/source, prompt or decision, output, verification, revision and owner.
- [ ] A peer or trainer can reproduce the reasoning from the saved evidence.

## Acceptance criteria

- Authenticate personal requests
- No legal or clinical advice
- Separation of duties for access removal
- The output is accurate, traceable, usable and explicit about uncertainty.
- Consequential decisions and actions remain with an authorised human.

## Scenario questions

1. Why should one front door not mean one permission set?
2. Which disclosure demands an immediate human response?
3. What evidence is needed before access is removed?

## Submission naming

`A11-<YourName>-Evidence.xlsx` plus the listed deliverables.

## Source anchors

- Course source register: `../../SOURCE-COVERAGE.md`
- Microsoft capability boundary: Microsoft 365 Copilot for generative work; Agent Builder or Copilot Studio for agentic work.

## Recommended team roles and timing

- **HR process owner:** confirms that the output solves the stated design safe employee service and offboarding outcome and remains consistent with approved policy.
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
