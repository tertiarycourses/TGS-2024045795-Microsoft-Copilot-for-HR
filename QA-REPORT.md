# Courseware QA Report

Course: **TGS-2024045795 — Agentic AI for HR**  
Courseware version: **6.0**  
Assessment version: **3.0**  
QA date: **16 August 2026**  
Result: **PASS — ready for controlled publication**

## Build inventory

| Artifact | Result |
|---|---:|
| Trainer deck | 105 slides, 16:9, PPTX + PDF |
| Learner Guide | 28 pages, DOCX + PDF |
| Lesson Plan | 7 pages, DOCX + PDF |
| Activity folders | 12 individual folders |
| Detailed activity Markdown | 12 files, 679–712 words each |
| Evidence workbooks | 12 XLSX files with Brief, Inputs, Evidence Log and Audit/Score sheets |
| Agent test-case sets | Activities 7, 8, 9 and 11 |
| Synthetic resumes | Six fictional resumes in Activity 4 |
| Assessment papers | Written Assessment + Case Study Assessment, DOCX + PDF |
| Confidential answer keys | Two separate DOCX + PDF files |

## Automated and visual checks

- PowerPoint package validation: **PASS**.
- DOCX package validation for Learner Guide, Lesson Plan and both candidate papers: **PASS**.
- Full-deck contact-sheet review across all 105 slides: **PASS; no clipping or overflow observed**.
- Learner Guide, Lesson Plan and assessment render review: **PASS after correcting a trailing source page and footer version**.
- Slide count within the 100–150 target: **PASS**.
- No click-by-click or step-by-step instructions in the deck: **PASS**.
- Detailed procedures, prompts, evidence requirements, acceptance criteria and scenario questions in the Learner Guide/activity Markdown: **PASS**.
- Canonical learner folder is `activities/`; no learner-facing `labs/` folder: **PASS**.
- Activity workbooks contain no spreadsheet error tokens: **PASS**.
- Candidate assessment papers contain five open-response questions each and do not contain confidential answer content: **PASS**.
- Answer keys are separate and visibly marked confidential: **PASS**.

## Alignment

| Course requirement | Evidence |
|---|---|
| Microsoft 365 Copilot for generative AI | Unit 2; Activities 1–6, 10 and 12 |
| Agent Builder / Copilot Studio for agentic AI | Unit 3; Activities 7–9 and 11–12 |
| Recruitment and resume screening | Activities 2 and 4; assessment A2 |
| HR policy | Activities 5 and 7; assessment A4 |
| Onboarding | Activities 6 and 8 |
| Leave application | Activity 9; assessment A3 |
| Broader HR lifecycle | Performance, learning, mobility, engagement, benefits, payroll, employee relations, offboarding and operations |
| Responsible adoption | Unit 4 and controls embedded in every activity |

## Assessment lineage

The old Written Assessment v2, Case Study Assessment v1 and Assessment Plan v4.0 were retrieved from the user-specified Drive courseware folder into the private `reference/tms/` folder. The revised instruments preserve the current five-question K1–K5 and A1–A5 structure and the 60-minute duration for each instrument, while updating the content to the new Copilot/agentic-AI curriculum.

## Publication boundary

Candidate papers may be shared by link. Answer keys must remain trainer-only and are excluded from GitHub. The public GitHub release excludes `.env`, `assessment/`, `reference/`, build sources, generated artwork sources and QA renders.

