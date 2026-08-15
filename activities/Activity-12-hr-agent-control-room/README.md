# Activity 12: Capstone: Operate the HR Agent Control Room

> **Synthetic learning case:** Do not upload live employee or candidate data.

## Scenario

HarbourLight's pilot portfolio now includes policy, onboarding and leave agents. Leaders must decide whether to scale, remediate or stop each agent.

## Learning goal

Use service, risk, adoption and human-value evidence to make a defensible operating decision.

## Microsoft tools

- Excel
- Teams
- Microsoft 365 Copilot

## Guardrails

- No scale without control thresholds
- Employee feedback included
- Named owner and retirement path

## Detailed procedure

1. Review the synthetic KPI, incident, test and feedback dataset.
2. Validate denominator, target and trend for each metric.
3. Ask Copilot to summarise evidence but require cell references.
4. Identify control failures, unintended outcomes and data gaps.
5. Classify each agent as scale, remediate, pause or retire.
6. Respond to the prompt-injection incident using the provided playbook.
7. Create a 90-day roadmap with decision gates and accountable owners.
8. Present a three-minute executive recommendation and answer peer challenge questions.

## Prompt scaffold

> You are supporting the HarbourLight Logistics SG training case. Use only the supplied synthetic evidence. Your task is to use service, risk, adoption and human-value evidence to make a defensible operating decision. State assumptions; cite record IDs or approved source sections; separate observation from inference; flag missing information; list the human checks and approvals required before use.

## Evidence checklist

- [ ] Agent scorecard
- [ ] Incident response
- [ ] 90-day roadmap and executive recommendation
- [ ] Evidence workbook records the input/source, prompt or decision, output, verification, revision and owner.
- [ ] A peer or trainer can reproduce the reasoning from the saved evidence.

## Acceptance criteria

- No scale without control thresholds
- Employee feedback included
- Named owner and retirement path
- The output is accurate, traceable, usable and explicit about uncertainty.
- Consequential decisions and actions remain with an authorised human.

## Scenario questions

1. Which metric looked good but hid harm?
2. What evidence justifies scale?
3. How will the organisation retire an agent safely?

## Submission naming

`A12-<YourName>-Evidence.xlsx` plus the listed deliverables.

## Source anchors

- Course source register: `../../SOURCE-COVERAGE.md`
- Microsoft capability boundary: Microsoft 365 Copilot for generative work; Agent Builder or Copilot Studio for agentic work.

## Recommended team roles and timing

- **HR process owner:** confirms that the output solves the stated capstone: operate the hr agent control room outcome and remains consistent with approved policy.
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
