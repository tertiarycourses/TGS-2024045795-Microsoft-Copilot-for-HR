# Lab 2: Draft an Inclusive Job Description with Generative AI

> **Synthetic learning case:** Do not upload live employee or candidate data.

## Scenario

Lab 1 established a need for a Workforce Operations Analyst. The old JD is task-heavy, contains copied requirements and does not reflect the outcomes or skills needed at the new hub.

![Lab workflow schematic](workflow.png)

## Learning goal

Use Word Copilot to draft a skills-based, inclusive and approval-ready job description grounded in the approved talent need.

## Microsoft tools

- Word with Microsoft 365 Copilot
- Excel

## Supplied mock data

Use `mock-data.csv` or the **Mock Data** sheet in `Lab-02-Evidence-Workbook.xlsx`. The records are specific to this scenario and carry forward the HarbourLight case.

## Guardrails

- Use job-related criteria only
- Distinguish essential from trainable skills
- Hiring manager and HR approve every requirement

## Detailed procedure

1. Import the approved role outcomes and skills from Lab 1 or use the supplied fallback brief.
2. Identify obsolete, vague or non-job-related requirements in the legacy JD.
3. Prompt Copilot to draft purpose, outcomes, responsibilities and success measures.
4. Separate essential capabilities from skills that can be developed after hiring.
5. Add working conditions, reporting line and realistic candidate information.
6. Run inclusive-language, accessibility and fair-consideration checks.
7. Ask the hiring manager to validate each criterion and remove unsupported requirements.
8. Convert the final JD criteria into the anchored screening rubric for Lab 3.

## Product workbench

1. Sign in with the licensed training account. Use only the supplied synthetic `mock-data.csv` or evidence workbook; do not paste live HR records.
2. Open `Lab-02-Evidence-Workbook.xlsx`, inspect the Mock Data sheet and record the meaning of `role_outcome` and `essential_skill` before prompting.
3. Open Word in the approved Microsoft 365 training account and create a new working document. Open Copilot from the ribbon and attach or reference the approved synthetic brief.
4. Paste the prompt scaffold below. Ask for a structured draft with criterion-to-source citations and a separate UNKNOWN list for unsupported requirements.
5. Track the edits you accept, compare each criterion or question with the source rubric, and ask the HR owner to approve the final version in the evidence workbook.

Microsoft product reference: https://support.microsoft.com/en-us/copilot-word

## Prompt scaffold

> You are supporting the HarbourLight Logistics SG training case. Use only the supplied synthetic evidence. Your task is to use word copilot to draft a skills-based, inclusive and approval-ready job description grounded in the approved talent need. State assumptions; cite record IDs or approved source sections; separate observation from inference; flag missing information; list the human checks and approvals required before use.

## Evidence checklist

- [ ] Role-outcome map
- [ ] Inclusive job description
- [ ] Hiring-manager validation checklist
- [ ] Evidence workbook records the input/source, prompt or decision, output, verification, revision and owner.
- [ ] A peer or trainer can reproduce the reasoning from the saved evidence.

## Acceptance criteria

- Use job-related criteria only
- Distinguish essential from trainable skills
- Hiring manager and HR approve every requirement
- The output is accurate, traceable, usable and explicit about uncertainty.
- Consequential decisions and actions remain with an authorised human.

## Scenario questions

1. Which copied requirement would unnecessarily narrow the talent pool?
2. What must the hiring manager verify rather than delegate to Copilot?
3. How does the JD make later screening contestable?

## Submission naming

`L02-<YourName>-Evidence.xlsx` plus the listed deliverables.

## Source anchors

- Course source register: `../SOURCE-COVERAGE.md`
- Microsoft capability boundary: Microsoft 365 Copilot for generative work; Agent Builder or Copilot Studio for agentic work.

## Recommended team roles and timing

- **HR process owner:** confirms that the output solves the stated draft an inclusive job description with generative ai outcome and remains consistent with approved policy.
- **AI operator or maker:** records the exact prompt, instructions, knowledge sources, tool choices and revisions.
- **Reviewer or approver:** independently checks evidence, permissions, fairness, privacy and any consequential action.
- **Evidence recorder:** keeps the workbook complete enough for another person to reproduce the reasoning.

Allow about 35–50 minutes for the first build, 15 minutes for testing and verification, and 10 minutes for peer challenge and reflection. The trainer may adjust the timing to fit the delivery mode.

## Test-it evidence

Record test ID, input, expected result, actual result, source citation, reviewer and pass/fail in the evidence workbook. For agent labs, use `agent-test-cases.csv` and capture the test conversation or run result before marking a case complete.

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
