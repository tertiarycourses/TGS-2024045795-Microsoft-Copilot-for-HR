# Activity 8: Design an Onboarding Coordination Agent

> **Synthetic learning case:** Do not upload live employee or candidate data.

## Scenario

New joiners miss equipment, access and manager check-ins because work is spread across email, service tickets and spreadsheets.

## Learning goal

Design a Copilot Studio agent that coordinates onboarding while retaining accountable task owners.

## Microsoft tools

- Microsoft Copilot Studio
- Teams
- SharePoint
- Power Automate or agent flows

## Guardrails

- Least-privilege connectors
- No invented commitments
- Human owner confirms every completion

## Detailed procedure

1. Map the onboarding trigger, milestones, systems and owners.
2. Define what the agent may answer, recommend and execute.
3. Create the Copilot Studio agent purpose and instructions.
4. Add approved knowledge and a new-joiner profile input.
5. Design tools for task creation, reminder and status retrieval.
6. Add human confirmation before closing an access or equipment task.
7. Test normal joiner, missing manager, late equipment and confidential-question scenarios.
8. Review analytics and hand the pilot to named owners.

## Prompt scaffold

> You are supporting the HarbourLight Logistics SG training case. Use only the supplied synthetic evidence. Your task is to design a copilot studio agent that coordinates onboarding while retaining accountable task owners. State assumptions; cite record IDs or approved source sections; separate observation from inference; flag missing information; list the human checks and approvals required before use.

## Evidence checklist

- [ ] Conversation map
- [ ] Tool and approval design
- [ ] Test evidence
- [ ] Evidence workbook records the input/source, prompt or decision, output, verification, revision and owner.
- [ ] A peer or trainer can reproduce the reasoning from the saved evidence.

## Acceptance criteria

- Least-privilege connectors
- No invented commitments
- Human owner confirms every completion
- The output is accurate, traceable, usable and explicit about uncertainty.
- Consequential decisions and actions remain with an authorised human.

## Scenario questions

1. Which step is orchestration rather than content generation?
2. Where could duplicate actions occur?
3. What evidence proves the joiner—not only the workflow—was ready?

## Submission naming

`A08-<YourName>-Evidence.xlsx` plus the listed deliverables.

## Source anchors

- Course source register: `../../SOURCE-COVERAGE.md`
- Microsoft capability boundary: Microsoft 365 Copilot for generative work; Agent Builder or Copilot Studio for agentic work.

## Recommended team roles and timing

- **HR process owner:** confirms that the output solves the stated design an onboarding coordination agent outcome and remains consistent with approved policy.
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
