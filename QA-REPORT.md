# Courseware QA Report

**Course:** TGS-2024045795 — Microsoft Copilot for HR
**Courseware version:** 6.3 (27 September 2026)
**Assessment version:** 3.2
**Result:** PASS for local artifact integrity, alignment, and external publication readback.

## Exact artifact hashes

| Artifact | SHA-256 |
|---|---|
| `courseware/Microsoft Copilot for HR-v6.3.pptx` | `b9f7757dbf709c63575519f2e71804fafc761cb4be6e992fe754e75703d1611e` |
| `courseware/Microsoft Copilot for HR-v6.3.pdf` | `28cf50e173e69166eb3af06e1599efabf3eb9d64e1545a0e935a909b465f3d6c` |
| `courseware/LG-Microsoft Copilot for HR.docx` | `aa1fb37cb9056020e2e39a6a1cd263add9193f1ba990001538430ba9e3c0cccb` |
| `courseware/LG-Microsoft Copilot for HR.pdf` | `bad12283db96ba496ddff4587a92e22d42d29a1e924d928ed60874b39a9ffd8d` |
| `courseware/LP-Microsoft Copilot for HR.docx` | `848c518627bca4e00e9223f03f05adc1b61b395ea907e75d974caecc0fdf7721` |
| `courseware/LP-Microsoft Copilot for HR.pdf` | `b3a4edce7c41841a8739e515fbc11cf9c1e4ae2f9e00148e167ae40c74b45b11` |
| `courseware/LEARNER-GUIDE.md` | `f6ba2356a0b2309701dc5d2997f426b422ac3cd58b7c7b157869e9a3632db377` |
| `assessment/WA (SAQ) - Microsoft Copilot for HR - v3.2.docx` | `3bcb94725b1e751b4a70cfc72a89a0103bb94968293dc17ae5311e103c4303c1` |
| `assessment/CS Assessment - Microsoft Copilot for HR - v3.2.docx` | `6ddbe203bde0fe6af6d55314e6ad98fc498e1d7ede088dc4edcc9ebc6a4e04e0` |

## Inventory and checks

- Trainer deck: 202 editable PowerPoint slides plus a 202-page PDF. Cover names the current title, code, version and date; Digital Attendance and Final Assessment are visual layouts.
- Learner Guide: DOCX, PDF and Markdown mirror; 12 lab workflow schematics, 12 Test-it evidence sections, detailed Microsoft workbench paths, Word TOC field and Page X of Y footer.
- Lesson Plan: DOCX and PDF; Word TOC field, Page X of Y footer, 09:30–18:30 daily schedule, and parallel lab-pod/self-paced allocation consistent with the 16 scheduled contact hours. Facilitated reflection intervals are counted as contact time.
- Labs: 12 numbered, self-contained folders with 20 Markdown files, 20 same-basename PDFs, synthetic CSV/XLSX data, diagrams, prompts, controls and test evidence. Agent labs include test-case CSVs.
- Assessment: one WA and one Case Study candidate paper, each with five questions and 60-minute duration; two separate confidential answer keys remain in `assessment/`.
- ZIP integrity of all current PPTX/DOCX files: PASS. Current PDF text contains the course title and code; live current Office content contains no old course title.
- Privacy boundary: answer keys are excluded from learner lab materials and must remain absent from public GitHub and publicly inherited Drive folders.

## Source and visual review

The official course page was checked for the title, code, 2-day/16-hour duration and funding language. Current Microsoft Learn references support Agent Builder, SharePoint knowledge and Copilot Studio agent-flow steps. Visual review of the cover, administration pages, sample evidence views, LG/LP pages and representative lab PDFs found no blank pages or clipped text after reflow.

## Release readback (27 September 2026)

- Google Drive folder `1i6dTEB8l3KnXYagtAckSzMjmv5njJsVE` read back as `TGS-2024045795-Microsoft Copilot for HR`; its hands-on child is `Labs` (`1qC5w8tkw23CrnnoioXFkposW7MViTTKc`). The sync uploaded 83 current lab files and archived 69 superseded files.
- Drive MD5 matched the local trainer PPTX, learner slide PDF, Learner Guide PDF, Lesson Plan PDF, WA paper and Case Study paper. Each of these has an anonymous reader link. Four archived answer keys were checked individually and have no anonymous permissions.
- TMS course `622cc321-b45b-4b13-a0df-91f12aa61587` read back with the exact title `Microsoft Copilot for HR`, code `TGS-2024045795`, and the current Drive file IDs for the seven intended courseware fields. Nested assessment methods enable WA and Case Study, disable Practical Performance, and contain no answer key links.
- A protected before/after edit-data comparison found a `favoriteTrainers` list-to-text serialization defect in the project pusher. It was corrected; that field was restored to its pre-release representation, and a fresh semantic comparison passed for all other non-target fields.
- The public GitHub tree was checked for current PPTX/PDF/DOCX courseware and absence of `assessment/`, `reference/`, `.env`, archived courseware and obsolete `activities/` paths. Remote branch SHA matched the pushed commit.
