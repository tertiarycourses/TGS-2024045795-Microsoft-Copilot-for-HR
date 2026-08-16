# Activity 6: Create a Personalised Talent Development Journey

> **Synthetic learning case:** Do not upload live employee or candidate data.

## Scenario

After onboarding, the new analyst and two existing employees need different development pathways. HR currently assembles courses manually and managers lack a consistent skills-conversation structure.

## Learning goal

Use Copilot and a bounded development agent to identify evidence-based skill gaps, prepare learning options and automate routine follow-up.

## Microsoft tools

- Microsoft 365 Copilot in Word and Teams
- Agent Builder in Microsoft 365 Copilot
- Excel

## Supplied mock data

Use `mock-data.csv` or the **Mock Data** sheet in `Activity-06-Evidence-Workbook.xlsx`. The records are specific to this scenario and carry forward the HarbourLight case.

## Guardrails

- Employee can correct the skills record
- No deterministic potential ranking
- Manager and employee choose the final plan

## Detailed procedure

1. Review the role outcomes, employee aspirations and synthetic performance evidence.
2. Separate observed capability, self-reported interest and unsupported inference.
3. Ask Copilot to map evidenced gaps to approved learning and stretch options.
4. Draft a 90-day plan with milestones, practice and manager support.
5. Create a bounded Agent Builder agent over approved learning resources.
6. Add instructions for explainable recommendations, consent and escalation.
7. Test irrelevant, inaccessible and sensitive development requests.
8. Record employee corrections, manager approval and follow-up reminders.

## Prompt scaffold

> You are supporting the HarbourLight Logistics SG training case. Use only the supplied synthetic evidence. Your task is to use copilot and a bounded development agent to identify evidence-based skill gaps, prepare learning options and automate routine follow-up. State assumptions; cite record IDs or approved source sections; separate observation from inference; flag missing information; list the human checks and approvals required before use.

## Evidence checklist

- [ ] Skills evidence summary
- [ ] 90-day development plan
- [ ] Development-agent instructions and tests
- [ ] Evidence workbook records the input/source, prompt or decision, output, verification, revision and owner.
- [ ] A peer or trainer can reproduce the reasoning from the saved evidence.

## Acceptance criteria

- Employee can correct the skills record
- No deterministic potential ranking
- Manager and employee choose the final plan
- The output is accurate, traceable, usable and explicit about uncertainty.
- Consequential decisions and actions remain with an authorised human.

## Scenario questions

1. How can the employee challenge the skills profile?
2. What would make a recommendation explainable?
3. Which development decision should never be automated?

## Submission naming

`A06-<YourName>-Evidence.xlsx` plus the listed deliverables.

## Source anchors

- Course source register: `../../SOURCE-COVERAGE.md`
- Microsoft capability boundary: Microsoft 365 Copilot for generative work; Agent Builder or Copilot Studio for agentic work.

## Recommended team roles and timing

- **HR process owner:** confirms that the output solves the stated create a personalised talent development journey outcome and remains consistent with approved policy.
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
