# Activity 10: Prepare a Fair Performance and Learning Conversation

> **Synthetic learning case:** Do not upload live employee or candidate data.

## Scenario

A manager has fragmented notes, goals and service metrics for two employees and wants Copilot to draft development conversations.

## Learning goal

Use Copilot to organise evidence, distinguish observation from inference and prepare human-led coaching.

## Microsoft tools

- Word and Teams with Microsoft 365 Copilot
- Excel

## Guardrails

- No personality inference
- Employee can correct evidence
- Manager owns the conversation and rating

## Detailed procedure

1. Review the synthetic goals, evidence and contextual notes.
2. Label each item as observation, result, feedback, context or unsupported inference.
3. Ask Copilot to summarise evidence by agreed goal and cite the source.
4. Challenge the summary for recency and confirmation bias.
5. Draft coaching questions that invite the employee's perspective.
6. Map agreed gaps to learning and stretch options.
7. Record employee corrections and final human judgement.
8. Check that the plan supports development rather than surveillance.

## Prompt scaffold

> You are supporting the HarbourLight Logistics SG training case. Use only the supplied synthetic evidence. Your task is to use copilot to organise evidence, distinguish observation from inference and prepare human-led coaching. State assumptions; cite record IDs or approved source sections; separate observation from inference; flag missing information; list the human checks and approvals required before use.

## Evidence checklist

- [ ] Evidence summary
- [ ] Coaching questions
- [ ] Learning plan
- [ ] Evidence workbook records the input/source, prompt or decision, output, verification, revision and owner.
- [ ] A peer or trainer can reproduce the reasoning from the saved evidence.

## Acceptance criteria

- No personality inference
- Employee can correct evidence
- Manager owns the conversation and rating
- The output is accurate, traceable, usable and explicit about uncertainty.
- Consequential decisions and actions remain with an authorised human.

## Scenario questions

1. Which evidence is relevant but not sufficient?
2. How can the employee contest the summary?
3. What should Copilot never infer from tone or activity data?

## Submission naming

`A10-<YourName>-Evidence.xlsx` plus the listed deliverables.

## Source anchors

- Course source register: `../../SOURCE-COVERAGE.md`
- Microsoft capability boundary: Microsoft 365 Copilot for generative work; Agent Builder or Copilot Studio for agentic work.

## Recommended team roles and timing

- **HR process owner:** confirms that the output solves the stated prepare a fair performance and learning conversation outcome and remains consistent with approved policy.
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
