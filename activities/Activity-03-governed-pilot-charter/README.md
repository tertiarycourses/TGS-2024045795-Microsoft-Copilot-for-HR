# Activity 3: Write the Governed HR AI Pilot Charter

> **Synthetic learning case:** Do not upload live employee or candidate data.

## Scenario

The executive committee will fund only one 90-day HR AI pilot. It expects a clear value case, human controls and an operating owner.

## Learning goal

Convert an opportunity into a testable pilot charter with go/no-go gates.

## Microsoft tools

- Word with Microsoft 365 Copilot
- Excel

## Guardrails

- Synthetic or de-identified pilot data
- Named risk owner
- Kill switch and rollback

## Detailed procedure

1. Select the use case approved in Activity 1 or use the provided leave-agent case.
2. Define the user, outcome, trigger, boundary and non-goals.
3. Map data, knowledge, tools, decisions and human approvals.
4. Ask Copilot to draft a charter from the workbook evidence.
5. Add baseline, target, guardrail and stop metrics.
6. Assign business owner, technical owner, policy owner, approver and support roles.
7. Specify pilot population, test data and feedback route.
8. Run a red-team review and revise the charter.

## Prompt scaffold

> You are supporting the HarbourLight Logistics SG training case. Use only the supplied synthetic evidence. Your task is to convert an opportunity into a testable pilot charter with go/no-go gates. State assumptions; cite record IDs or approved source sections; separate observation from inference; flag missing information; list the human checks and approvals required before use.

## Evidence checklist

- [ ] Pilot charter
- [ ] RACI
- [ ] Metric baseline and gate table
- [ ] Evidence workbook records the input/source, prompt or decision, output, verification, revision and owner.
- [ ] A peer or trainer can reproduce the reasoning from the saved evidence.

## Acceptance criteria

- Synthetic or de-identified pilot data
- Named risk owner
- Kill switch and rollback
- The output is accurate, traceable, usable and explicit about uncertainty.
- Consequential decisions and actions remain with an authorised human.

## Scenario questions

1. Which decision remains human and why?
2. Who can stop the pilot?
3. What would a misleading success metric reward?

## Submission naming

`A03-<YourName>-Evidence.xlsx` plus the listed deliverables.

## Source anchors

- Course source register: `../../SOURCE-COVERAGE.md`
- Microsoft capability boundary: Microsoft 365 Copilot for generative work; Agent Builder or Copilot Studio for agentic work.

## Recommended team roles and timing

- **HR process owner:** confirms that the output solves the stated write the governed hr ai pilot charter outcome and remains consistent with approved policy.
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
