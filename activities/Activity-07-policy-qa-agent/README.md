# Activity 7: Build an HR Policy Q&A Agent

> **Synthetic learning case:** Do not upload live employee or candidate data.

## Scenario

Employees ask repetitive hybrid-work and benefits questions in Teams. HR needs a reliable self-service front door that cites policy and escalates exceptions.

## Learning goal

Create a bounded policy agent in Agent Builder for Microsoft 365 Copilot and test grounded answers.

## Microsoft tools

- Agent Builder in Microsoft 365 Copilot
- SharePoint
- Teams

## Guardrails

- Cite approved policy
- No personalised entitlement decisions
- Escalate ambiguity and sensitive cases

## Detailed procedure

1. Define the audience, in-scope intents and explicit exclusions.
2. Select the approved synthetic policy knowledge files.
3. Write instructions for citation, effective date, clarification, refusal and escalation.
4. Create the agent in Agent Builder and add the knowledge sources.
5. Add conversation starters for common employee intents.
6. Run normal, ambiguous, outdated-policy and sensitive-personal-case tests.
7. Record answer, citation, pass/fail and corrective action.
8. Share only with the test group after the policy owner approves.

## Prompt scaffold

> You are supporting the HarbourLight Logistics SG training case. Use only the supplied synthetic evidence. Your task is to create a bounded policy agent in agent builder for microsoft 365 copilot and test grounded answers. State assumptions; cite record IDs or approved source sections; separate observation from inference; flag missing information; list the human checks and approvals required before use.

## Evidence checklist

- [ ] Agent purpose and instructions
- [ ] Knowledge map
- [ ] 12-case test report
- [ ] Evidence workbook records the input/source, prompt or decision, output, verification, revision and owner.
- [ ] A peer or trainer can reproduce the reasoning from the saved evidence.

## Acceptance criteria

- Cite approved policy
- No personalised entitlement decisions
- Escalate ambiguity and sensitive cases
- The output is accurate, traceable, usable and explicit about uncertainty.
- Consequential decisions and actions remain with an authorised human.

## Scenario questions

1. What makes an answer grounded rather than merely plausible?
2. When should the agent stop answering?
3. What new operating work does this agent create?

## Submission naming

`A07-<YourName>-Evidence.xlsx` plus the listed deliverables.

## Source anchors

- Course source register: `../../SOURCE-COVERAGE.md`
- Microsoft capability boundary: Microsoft 365 Copilot for generative work; Agent Builder or Copilot Studio for agentic work.

## Recommended team roles and timing

- **HR process owner:** confirms that the output solves the stated build an hr policy q&a agent outcome and remains consistent with approved policy.
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
