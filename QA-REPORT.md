# Courseware QA Report

Course: **TGS-2024045795 — Agentic AI for HR**  
Courseware version: **6.2**  
Assessment version: **3.1**  
QA date: **16 August 2026**  
Result: **PASS — ready for controlled publication**

## Build inventory

| Artifact | Result |
|---|---:|
| Trainer deck | 118 slides, 16:9, PPTX + PDF |
| Learner Guide | 31 pages, DOCX + PDF |
| Lesson Plan | 7 pages, DOCX + PDF |
| Activity folders | 12 individual folders |
| Learner-facing Markdown/PDF | 19 Markdown files rendered to 19 same-basename PDFs |
| Evidence workbooks | 12 XLSX files with Brief, Mock Data, Evidence Log and Audit/Score sheets |
| Scenario-specific mock data | 12 CSV files mirrored in the 12 workbooks |
| Agent test-case sets | Activities 5–9 and 11–12 |
| Synthetic resumes | Six fictional resumes in Activity 3, each in Markdown + PDF |
| Assessment papers | Written Assessment + Case Study Assessment, DOCX |
| Confidential answer keys | Two separate trainer-only DOCX files |

## Automated and visual checks

- PowerPoint package validation: **PASS**.
- DOCX package validation for Learner Guide, Lesson Plan and both candidate papers: **PASS**.
- Full-deck contact-sheet review across all 118 slides: **PASS after replacing the repeated admin-card template, correcting course-outline distortion, restoring the cover image aspect ratio, repairing long activity headers and shortening an overflowing case-vignette slide**.
- Front administration follows the approved SPC pattern: **PASS** — attendance, two trainer profiles, ice-breaker, ground rules, LMS, workbench, lesson plan, TSC, outcomes, outline and assessment pages use purpose-specific layouts.
- Learning Agreements slide removed and no trainer identity appears on the Digital Attendance slides: **PASS**.
- Deloitte and ebook extensions in opening concepts, operating model, implementation patterns and case vignettes: **PASS**.
- Learner Guide, Lesson Plan, activity guides and supplied-resume PDF render review: **PASS**.
- Learner Guide Markdown mirror generated from the same concepts, activities and slide map as the DOCX/PDF: **PASS**.
- Slide count within the 100–150 target: **PASS**.
- No click-by-click or step-by-step instructions in the deck: **PASS**.
- Detailed procedures, prompts, evidence requirements, acceptance criteria and scenario questions in the Learner Guide/activity Markdown: **PASS**.
- Canonical learner folder is `activities/`; no learner-facing `labs/` folder: **PASS**.
- Every activity has a detailed learner PDF, scenario-specific CSV and matching workbook Mock Data sheet: **PASS**.
- Activity workbooks contain six formulas each and no spreadsheet error tokens after LibreOffice recalculation: **PASS**.
- Candidate assessment papers contain five open-response questions each, preserve the WA + Case Study instrument types, and do not contain confidential answer content: **PASS**.
- Assessment structural verifier: **PASS** — cover-only page 1, candidate instructions and grading on page 2, content from page 3, LMS link present and answer keys separated.
- Case Study traceability: **PASS** — A1 maps Activities 5–9/11; A2 Activity 3; A3 Activity 8; A4 Activity 7; A5 Activity 12.
- Answer keys are separate and visibly marked confidential: **PASS**.

## Alignment

| Course requirement | Evidence |
|---|---|
| Central value message | Opening HR pain and strategic-case slides; facilitator prompts; closing takeaways; every activity debrief |
| Microsoft 365 Copilot for generative AI | Unit 2; Activities 1–4, 6–7, 10 and 12 |
| Agent Builder / Copilot Studio for agentic AI | Unit 3; Activities 5–9 and 11; portfolio governance in 12 |
| Talent needs and job description | Activities 1–2 |
| Resume screening and interviewing | Activities 3–4; assessment A2 |
| Onboarding and talent development | Activities 5–6 |
| HR policy | Activity 7; assessment A4 |
| Leave and benefits | Activities 8–9; assessment A3 |
| Wellness and offboarding | Activities 10–11 |
| Full-spectrum HR operations | Activity 12 control-room capstone |
| Responsible adoption | Unit 4 and controls embedded in every activity |

## Assessment lineage

The old Written Assessment v2, Case Study Assessment v1 and Assessment Plan v4.0 were retrieved from the user-specified Drive courseware folder into the private `reference/tms/` folder. Version 3.1 preserves the five-question K1–K5 and A1–A5 structure and the 60-minute duration for each instrument, while explicitly tracing case-study application to the revised lifecycle activities.

## Publication boundary

Candidate papers may be shared by link. Answer keys must remain trainer-only and are excluded from GitHub. The public GitHub release excludes `.env`, `assessment/`, `reference/`, build sources, generated artwork sources and QA renders.
