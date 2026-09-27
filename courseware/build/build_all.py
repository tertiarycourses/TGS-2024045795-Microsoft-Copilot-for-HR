#!/usr/bin/env python3
"""Build PPTX, Learner Guide, Lesson Plan, activities and evidence workbooks."""

import csv, json, os, sys, textwrap, re, zipfile, tempfile
from pathlib import Path
from datetime import datetime
from shutil import which
from subprocess import run

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.dml import MSO_THEME_COLOR
from docx import Document
from docx.shared import Inches as DInches, Pt as DPt, RGBColor as DRGB
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

from course_data import META, LEARNING_OUTCOMES, SOURCES, UNITS, ACTIVITIES, SCHEDULE, ROOT, COURSEWARE, ACTIVITIES_DIR

W, H = Inches(13.333), Inches(7.5)
NAVY = RGBColor(12, 35, 64); BLUE = RGBColor(0, 113, 188); CYAN = RGBColor(0, 166, 166)
GREEN = RGBColor(35, 140, 92); ORANGE = RGBColor(238, 126, 32); RED = RGBColor(196, 54, 62)
INK = RGBColor(28, 36, 48); MID = RGBColor(88, 101, 118); PALE = RGBColor(244, 247, 250)
LINE = RGBColor(219, 226, 233); WHITE = RGBColor(255, 255, 255)
ACCENTS = [BLUE, CYAN, GREEN, ORANGE]

MOCK_DATA = {
  1: (["period","forecast_orders","overtime_hours","open_roles","current_analysts","forecast_growth_pct","source_note"],[
      ["2026-Q1",42000,820,4,2,8,"Synthetic operations forecast"],["2026-Q2",46800,1010,5,2,11,"Synthetic operations forecast"],["2026-Q3",53500,1380,7,2,14,"New hub scenario"],["2026-Q4",58100,1520,8,3,9,"New hub scenario"],["2027-Q1",62000,1690,9,3,7,"Planning assumption"]]),
  2: (["role_outcome","essential_skill","trainable_skill","success_measure","legacy_requirement","review_status"],[
      ["Translate hub data into staffing actions","Spreadsheet analysis","Power BI","Weekly plan accepted by operations","Minimum 8 years in logistics","Challenge"],["Improve workforce scheduling","Demand and capacity reasoning","SQL basics","Overtime variance reduced","Must be below age 35","Remove"],["Explain insights to managers","Stakeholder communication","Facilitation","Actions documented and owned","Native English speaker","Remove"],["Maintain trusted reports","Data quality and controls","Workflow automation","No material reporting errors","Degree from selected universities","Challenge"]]),
  3: (["candidate_id","skills_evidence","operations_evidence","analytics_evidence","communication_evidence","missing_or_uncertain"],[
      ["CAND-01","Excel dashboards","Warehouse reporting","Weekly KPI analysis","Stakeholder workshops","No SQL evidence"],["CAND-02","Process mapping","Distribution operations","Power BI portfolio","Training coordination","Outcomes not quantified"],["CAND-03","Inventory analysis","Shift support","SQL basics","Operations improvement briefing","Facilitation evidence limited"],["CAND-04","Customer analytics","Service operations","Excel and trend analysis","Change support","Hub exposure unknown"],["CAND-05","Scheduling","Safety reporting","Capacity analysis","Team facilitation","Dashboard depth unclear"],["CAND-06","Procurement analysis","Supplier operations","Dashboard design","Team coaching","Workforce planning unknown"]]),
  4: (["candidate_id","question_id","job_outcome","evidence_excerpt","panel_score_1_5","panel_note"],[
      ["CAND-01","Q1","Translate data into action","Rebuilt a weekly hub report and documented staffing changes",4,"Verify scale and denominator"],["CAND-01","Q2","Improve scheduling","Used demand peaks to propose shift coverage",4,"Strong job-related example"],["CAND-02","Q1","Translate data into action","Mapped delays and built a Power BI view",4,"Clarify personal contribution"],["CAND-02","Q2","Improve scheduling","Coordinated training around shift constraints",3,"Indirect evidence"],["CAND-03","Q1","Translate data into action","Analysed inventory exceptions using SQL",3,"Good technique; workforce link weak"],["CAND-03","Q2","Improve scheduling","Supported daily roster updates",3,"Outcome not quantified"]]),
  5: (["task_id","journey_stage","task","owner","due_offset_days","system","status"],[
      ["ONB-01","Pre-boarding","Confirm personal details","HR Operations",-7,"HRIS sandbox","Not started"],["ONB-02","Pre-boarding","Order laptop and access","IT Service",-5,"Service desk mock","Not started"],["ONB-03","Day 1","Safety orientation","Safety Lead",0,"Teams","Not started"],["ONB-04","Day 1","Manager welcome and outcomes","Hiring Manager",0,"Teams","Not started"],["ONB-05","Week 1","Role systems training","Process Owner",3,"Learning catalogue","Not started"],["ONB-06","Week 1","Network introductions","Hiring Manager",5,"Teams","Not started"],["ONB-07","Days 8-30","First dashboard practice","Mentor",14,"SharePoint","Not started"],["ONB-08","Days 8-30","New-joiner feedback pulse","HR Partner",25,"Forms mock","Not started"]]),
  6: (["employee_id","role_outcome","evidence_level_1_5","employee_interest","approved_learning","manager_support","consent_status"],[
      ["EMP-101","Demand analysis",3,"Advanced forecasting","Forecasting fundamentals","Weekly practice dataset","Confirmed"],["EMP-101","Stakeholder communication",4,"Facilitation","Facilitation clinic","Shadow hub review","Confirmed"],["EMP-204","Dashboard quality",2,"Power BI","Dashboard design pathway","Peer review time","Confirmed"],["EMP-204","Workforce planning",3,"Scenario modelling","Workforce planning essentials","Monthly coaching","Confirmed"],["EMP-318","Process automation",2,"Power Automate","Workflow foundations","Sandbox access","Pending"],["EMP-318","Data governance",3,"Data stewardship","HR data controls","Data-owner mentoring","Confirmed"]]),
  7: (["source_id","policy_topic","rule_text","effective_date","owner","issue"],[
      ["POL-2025-01","Hybrid work","Up to two remote days with manager agreement","2025-01-01","HR Policy","Current"],["GUIDE-OLD-04","Hybrid work","One remote day after probation","2024-04-01","Unknown","Superseded"],["FAQ-17","Equipment","Employees may take assigned laptop home","2025-06-01","IT Policy","Current"],["EMAIL-09","Equipment","Home equipment needs director approval","2024-11-18","Operations","Unapproved guidance"],["POL-2025-03","Conduct","Confidential data must use approved systems","2025-03-01","Compliance","Current"],["FAQ-22","Exceptions","Contact HR for disability or caregiving adjustment","2025-06-01","HR Policy","Needs clearer route"]]),
  8: (["request_id","employee_id","leave_type","start_date","end_date","balance_days","overlap_flag","approver","request_status"],[
      ["LV-001","EMP-101","Annual","2026-09-14","2026-09-16",8,"No","MGR-12","Draft"],["LV-002","EMP-204","Annual","2026-09-15","2026-09-19",3,"No","MGR-08","Draft"],["LV-003","EMP-318","Medical","2026-09-10","2026-09-10",12,"No","MGR-08","Draft"],["LV-004","EMP-101","Annual","2026-09-14","2026-09-16",8,"Yes","MGR-12","Duplicate test"],["LV-005","EMP-412","Caregiving","2026-10-02","2026-10-03",2,"No","","Missing approver"]]),
  9: (["intent_id","employee_intent","data_class","authentication_required","approved_source","expected_route","risk_note"],[
      ["BEN-01","What outpatient coverage is included?","General","No","Benefits Plan 2026","Answer with citation","Check effective date"],["BEN-02","Am I enrolled in dental coverage?","Personal","Yes","HRIS sandbox","Retrieve status","Least privilege"],["BEN-03","Why was my claim rejected?","Sensitive","Yes","Claims portal mock","Escalate","No final entitlement advice"],["BEN-04","Show my colleague's coverage","Personal","Yes","None","Refuse","Cross-employee data request"],["BEN-05","Which treatment should I choose?","Medical","No","None","Refuse and signpost","No clinical advice"],["BEN-06","Can I change plans after enrolment?","General","No","Benefits Plan 2026","Answer or escalate exception","Clarify qualifying event"]]),
 10: (["team","survey_n","wellbeing_score_1_5","avg_weekly_hours","absence_days_per_fte","manager_support_1_5","data_quality_note"],[
      ["Hub Operations",48,3.1,47,1.8,3.0,"Complete"],["Customer Service",62,3.4,44,1.2,3.6,"Complete"],["Planning",14,2.9,49,2.1,2.8,"Small sample"],["Technology",33,3.8,45,0.9,3.7,"Complete"],["People Team",9,3.2,46,1.5,3.4,"Very small sample"],["Finance",27,3.6,43,1.0,3.5,"One missing survey item"]]),
 11: (["task_id","offboarding_outcome","owner","due_offset_days","approval_required","system","status","failure_test"],[
      ["OFF-01","Confirm exit event and date","HR Partner",-14,"HR Manager","HRIS sandbox","Open","Cancelled exit"],["OFF-02","Agree knowledge transfer","Line Manager",-10,"Employee","SharePoint","Open","Missing handover owner"],["OFF-03","Confirm asset inventory","Facilities",-5,"Facilities Lead","Asset register mock","Open","Missing laptop"],["OFF-04","Calculate final pay","Payroll",-3,"Payroll Lead","Payroll sandbox","Open","Incorrect balance"],["OFF-05","Schedule access removal","IT Security",0,"HR + Manager","Identity sandbox","Open","Early removal"],["OFF-06","Provide benefits continuation information","HR Operations",0,"HR Partner","Benefits plan","Open","Outdated plan"],["OFF-07","Send respectful exit communication","Manager",1,"HR Partner","Outlook","Open","Sensitive reason exposed"],["OFF-08","Close records and retention tasks","Records Owner",7,"Compliance","Records register","Open","Over-retention"]]),
 12: (["solution","baseline_minutes","current_minutes","accuracy_pct","escalation_pct","employee_trust_1_5","open_incidents","owner","recommended_decision"],[
      ["Talent needs Copilot",480,210,92,18,3.8,0,"Workforce Planning Lead","Scale with data-quality gate"],["JD Copilot",180,65,95,12,4.0,0,"Talent Acquisition Lead","Scale"],["Screening evidence",720,260,89,24,3.6,1,"Recruitment Manager","Remediate fairness test"],["Onboarding agent",360,120,91,21,4.1,0,"Employee Experience Lead","Scale"],["Policy agent",300,85,94,16,4.2,0,"Policy Owner","Scale"],["Leave agent",45,12,97,14,4.0,1,"HR Operations Lead","Remediate duplicate control"],["Benefits agent",55,18,90,31,3.7,0,"Benefits Lead","Pilot longer"],["Wellness insights",600,240,86,28,3.2,1,"Wellbeing Lead","Pause privacy review"],["Offboarding agent",420,150,93,19,4.0,0,"HR Operations Lead","Scale with access rehearsal"]])
}

def blank(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6]); s.background.fill.solid(); s.background.fill.fore_color.rgb = WHITE
    return s

def box(s, x, y, w, h, fill=WHITE, line=LINE, radius=True):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill; sh.line.color.rgb = line
    return sh

def txt(s, x, y, w, h, text, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT, font="Aptos", valign=MSO_ANCHOR.TOP):
    tb=s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf=tb.text_frame; tf.clear(); tf.margin_left=tf.margin_right=Inches(.04); tf.margin_top=tf.margin_bottom=Inches(.02); tf.vertical_anchor=valign
    p=tf.paragraphs[0]; p.alignment=align; r=p.add_run(); r.text=str(text); r.font.name=font; r.font.size=Pt(size); r.font.bold=bold; r.font.color.rgb=color
    return tb

def footer(s, num):
    txt(s,.35,7.12,4.2,.2,f"{META['code']}  |  {META['title']}",8,MID)
    txt(s,4.75,7.12,3.85,.2,"© Tertiary Infotech Academy Pte Ltd",8,MID,align=PP_ALIGN.CENTER)
    txt(s,12.55,7.12,.4,.2,str(num),8,MID,align=PP_ALIGN.RIGHT)

def header(s, title, takeaway=None, accent=BLUE):
    sh=s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(.42), Inches(.36), Inches(.08), Inches(.68)); sh.fill.solid(); sh.fill.fore_color.rgb=accent; sh.line.fill.background()
    # Long activity names must remain one clean line above the subtitle.
    title_size=22 if len(title)>52 else 27
    txt(s,.68,.3,12,.55,title,title_size,NAVY,True)
    if takeaway: txt(s,.7,.94,11.9,.38,takeaway,13,MID)

def add_notes(slide, urls):
    if not urls: return
    try:
        tf=slide.notes_slide.notes_text_frame
        tf.text="[Sources]\n"+"\n".join(urls)
    except Exception:
        pass

def title_slide(prs):
    s=blank(prs)
    hero=COURSEWARE/"assets"/"cover-hero-v1.png"
    # The source hero is composed at 16:9 with negative space on the left.
    # Fill the whole slide at its native aspect ratio; never squeeze it into a portrait crop.
    s.shapes.add_picture(str(hero), Inches(0), Inches(0), width=W, height=H)
    s.shapes.add_picture(str(ROOT/".claude/skills/courseware-build/assets/tertiary-infotech-logo.png"), Inches(5.18), Inches(.38), width=Inches(.43), height=Inches(.43))
    txt(s,5.72,.47,.55,.2,"WSQ",11,BLUE,True)
    txt(s,.62,.52,5.7,.34,"WSQ • HUMAN RESOURCE DIGITALISATION",11,BLUE,True)
    txt(s,.62,1.2,5.8,1.6,META['title'],40,NAVY,True)
    txt(s,.65,2.9,5.35,1.2,"Reduce HR administration with Copilot and governed agents—returning time to faster service, better decisions and strategic people work.",18,INK)
    box(s,.62,4.35,5.2,1.08,PALE,LINE)
    txt(s,.9,4.56,4.7,.28,META['code'],16,BLUE,True)
    tsc_code=META['tsc'].split("(")[-1].rstrip(")")
    txt(s,.9,4.9,4.7,.25,f"{META['duration']}  •  {tsc_code}",10,MID)
    txt(s,.65,6.45,5.8,.22,f"Trainer: {META['trainer']}  |  Version {META['version']}  |  {META['date']}",9,MID)
    txt(s,.65,6.74,5.8,.25,"Tertiary Infotech Academy Pte Ltd  |  UEN 201200696W",10,MID)
    add_notes(s,[SOURCES['course']])
    return s

def simple_admin(prs,title,subtitle,items,accent=BLUE):
    s=blank(prs); header(s,title,subtitle,accent)
    n=len(items); cols=2 if n>=4 else n; cols=max(1,min(cols,3)); rows=(n+cols-1)//cols
    cw=11.9/cols; ch=4.85/rows
    for i,item in enumerate(items):
        r=i//cols; c=i%cols; x=.7+c*cw; y=1.65+r*ch
        box(s,x,y,cw-.25,ch-.25,WHITE,LINE)
        txt(s,x+.25,y+.28,.55,.55,str(i+1).zfill(2),18,accent,True)
        if isinstance(item,(tuple,list)): head,body=item[0],item[1]
        else: head,body=item,""
        txt(s,x+.95,y+.24,cw-1.4,.68,head,16,NAVY,True)
        txt(s,x+.95,y+.92,cw-1.4,ch-1.28,body,12,MID)
    return s

def admin_section(prs):
    s=blank(prs)
    bar=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(.02),Inches(0),Inches(.12),H); bar.fill.solid(); bar.fill.fore_color.rgb=BLUE; bar.line.fill.background()
    sh=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(.72),Inches(2.75),Inches(.09),Inches(1.08)); sh.fill.solid(); sh.fill.fore_color.rgb=GREEN; sh.line.fill.background()
    txt(s,1.0,2.72,3.8,.3,"COURSE ADMINISTRATION",11,BLUE,True)
    txt(s,1.0,3.18,10.6,.75,"Welcome & Housekeeping",32,NAVY,True)
    return s

def bullet_admin(prs,kicker,title,bullets,accent=BLUE):
    s=blank(prs); header(s,title,kicker,accent)
    line=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(.7),Inches(1.37),Inches(11.9),Inches(.02)); line.fill.solid(); line.fill.fore_color.rgb=LINE; line.line.fill.background()
    tf=s.shapes.add_textbox(Inches(1.0),Inches(1.72),Inches(11.2),Inches(4.8)).text_frame
    tf.clear(); tf.margin_left=tf.margin_right=Inches(.05); tf.margin_top=tf.margin_bottom=Inches(.02)
    for i,body in enumerate(bullets):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.text=body; p.level=0; p.font.name="Aptos"; p.font.size=Pt(17); p.font.color.rgb=INK; p.space_after=Pt(12)
        p.text="•  "+p.text
    return s

def digital_attendance(prs):
    s=blank(prs); header(s,"Digital Attendance (Mandatory)","TRAQOM · SSG DIGITAL ATTENDANCE",BLUE)
    for i,(label,caption) in enumerate([("AM","Start of morning session"),("PM","Start of afternoon session"),("ASSESSMENT","Before WA and Case Study")]):
        x=.8+i*4.2; box(s,x,1.85,3.65,2.75,WHITE,LINE)
        txt(s,x+.25,2.12,3.15,.55,label,26,BLUE,True,PP_ALIGN.CENTER)
        txt(s,x+.35,3.02,2.95,.72,caption,17,NAVY,True,PP_ALIGN.CENTER)
        if i<2: txt(s,x+3.72,2.92,.4,.48,"→",24,BLUE,True)
    box(s,1.15,5.18,11.0,.84,PALE,LINE)
    txt(s,1.42,5.4,10.45,.39,"Trainer displays the SSG QR code  →  learner scans and submits each attendance",16,INK,True,PP_ALIGN.CENTER)
    txt(s,1.15,6.38,11.0,.3,"Eligibility check: at least 75% attendance plus a Competent assessment result.",14,RED,True,PP_ALIGN.CENTER)
    return s

def final_assessment_slide(prs):
    s=blank(prs); header(s,"Final Assessment","TWO INSTRUMENTS · INDIVIDUAL · OPEN BOOK",RED)
    for i,(title,code,body) in enumerate([("Written Assessment","K1–K5","Five open-response questions · 60 min"),("Case Study","A1–A5","Five applied questions · 60 min")]):
        x=.86+i*6.25; box(s,x,1.72,5.72,2.5,WHITE,LINE)
        txt(s,x+.32,2.0,5.02,.38,title,21,NAVY,True)
        txt(s,x+.32,2.57,4.95,.36,code,18,RED,True)
        txt(s,x+.32,3.2,5.0,.42,body,14,INK)
    box(s,.86,4.77,11.98,1.13,PALE,LINE)
    txt(s,1.16,5.0,11.4,.73,"Attendance → complete both papers → submit on LMS → sign Assessment Summary Record",17,NAVY,True,PP_ALIGN.CENTER)
    txt(s,1.0,6.37,11.4,.33,"Assessment decisions can be appealed through the published process.",13,MID,False,PP_ALIGN.CENTER)
    return s

def trainer_profile(prs,general=False):
    s=blank(prs); header(s,"About the Trainer","YOUR TRAINER · GENERAL" if general else "YOUR TRAINER",BLUE)
    accent=RGBColor(116,128,142) if general else BLUE
    box(s,.72,1.55,3.25,4.85,PALE,LINE)
    top=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(.72),Inches(1.55),Inches(3.25),Inches(.08)); top.fill.solid(); top.fill.fore_color.rgb=accent; top.line.fill.background()
    av=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(1.62),Inches(1.98),Inches(1.45),Inches(1.45)); av.fill.solid(); av.fill.fore_color.rgb=accent; av.line.fill.background()
    txt(s,1.62,2.46,1.45,.35,"?" if general else "AA",24,WHITE,True,PP_ALIGN.CENTER,valign=MSO_ANCHOR.MIDDLE)
    txt(s,.98,3.72,2.72,.45,"Your Trainer" if general else META['trainer'],19,NAVY,True,PP_ALIGN.CENTER)
    txt(s,1.0,4.23,2.68,.78,"General Trainer template —\nto be completed by the trainer" if general else "Principal Trainer\nTertiary Infotech Academy Pte Ltd",11,MID,False,PP_ALIGN.CENTER)
    rows=[
        ("NAME","____________________________________________"),("TITLE / DESIGNATION","____________________________________________"),("QUALIFICATIONS","____________________________________________"),("AREAS OF EXPERTISE","____________________________________________"),("TRAINING & INDUSTRY EXPERIENCE","____________________________________________"),("CONTACT","____________________________________________")
    ] if general else [
        ("ROLE","Principal Trainer, Tertiary Infotech Academy Pte Ltd"),
        ("BACKGROUND","PhD · 20+ years of industry and training experience in business, technology, analytics and AI."),
        ("DELIVERS","WSQ professional development in AI transformation, data analytics and responsible adoption."),
        ("FOUNDER","Founder and lead instructor at Tertiary Infotech / Tertiary Courses."),
    ]
    x=4.25; y=1.55; h=(4.85-(len(rows)-1)*.11)/len(rows)
    for i,(lab,body) in enumerate(rows):
        yy=y+i*(h+.11); box(s,x,yy,8.35,h,WHITE,LINE)
        stripe=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(yy),Inches(.06),Inches(h)); stripe.fill.solid(); stripe.fill.fore_color.rgb=ACCENTS[i%4] if general else accent; stripe.line.fill.background()
        txt(s,x+.22,yy+.12,2.15,.24,lab,9,ACCENTS[i%4] if general else accent,True)
        txt(s,x+2.45,yy+.10,5.55,h-.16,body,11 if general else 12,NAVY if not general else MID,not general,valign=MSO_ANCHOR.MIDDLE)
    return s

def ground_rules(prs):
    s=blank(prs); header(s,"Ground Rules","HOUSEKEEPING",BLUE)
    rules=["Set your mobile phone to silent mode.","Participate actively — no question is too small.","Mutual respect: agree to disagree.","One conversation at a time.","Be punctual; return from breaks on time.","Use synthetic data only; protect personal information."]
    for i,body in enumerate(rules):
        x=.72+(i%2)*6.02; y=1.58+(i//2)*1.62; accent=ACCENTS[i%4]
        box(s,x,y,5.7,1.25,WHITE,LINE)
        stripe=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(.08),Inches(1.25)); stripe.fill.solid(); stripe.fill.fore_color.rgb=accent; stripe.line.fill.background()
        av=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x+.28),Inches(y+.37),Inches(.5),Inches(.5)); av.fill.solid(); av.fill.fore_color.rgb=accent; av.line.fill.background()
        txt(s,x+.28,y+.48,.5,.18,i+1,10,WHITE,True,PP_ALIGN.CENTER)
        txt(s,x+1.02,y+.30,4.25,.65,body,13,NAVY,True,valign=MSO_ANCHOR.MIDDLE)
    return s

def lms_slide(prs):
    s=blank(prs); header(s,"Download Course Material","COURSE PORTAL · LMS/TMS",BLUE)
    box(s,.72,1.55,6.25,4.7,PALE,LINE)
    box(s,.98,1.83,5.7,.38,WHITE,LINE); txt(s,1.18,1.92,5.3,.18,"https://lms-tms.tertiaryinfotech.com",9,BLUE,True)
    txt(s,1.02,2.43,5.55,.32,"Microsoft Copilot for HR",15,NAVY,True)
    rows=["Trainer Slides (PDF)  ↓","Learner Guide (PDF)  ↓","Lab Files  ↓","Assessment Submission  ↗"]
    for i,row in enumerate(rows):
        box(s,1.0,2.93+i*.68,5.55,.5,WHITE,LINE); txt(s,1.22,3.06+i*.68,5.1,.2,row,11,NAVY,i==3)
    steps=[("1","Sign in","Use your registered email and OTP or password."),("2","Open your course","Select Microsoft Copilot for HR under My Courses."),("3","Download materials","Keep the slides and Learner Guide for open-book assessment."),("4","Submit work","Upload assessment answers and complete required attendance." )]
    for i,(n,lab,body) in enumerate(steps):
        yy=1.58+i*1.16; accent=ACCENTS[i]
        av=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(7.35),Inches(yy+.1),Inches(.48),Inches(.48)); av.fill.solid(); av.fill.fore_color.rgb=accent; av.line.fill.background()
        txt(s,7.35,yy+.21,.48,.16,n,10,WHITE,True,PP_ALIGN.CENTER)
        txt(s,8.05,yy,4.25,.28,lab,13,NAVY,True); txt(s,8.05,yy+.34,4.25,.55,body,10,MID)
    return s

def workbench_slide(prs):
    s=blank(prs); header(s,"Your HR AI Workbench","COURSE TOOLS · ALL 12 ACTIVITIES",GREEN)
    box(s,.72,1.55,6.25,4.7,PALE,LINE)
    txt(s,1.0,1.88,5.7,.28,"GENERATIVE AI",10,BLUE,True)
    box(s,1.0,2.24,5.55,.78,WHITE,BLUE); txt(s,1.25,2.42,5.05,.35,"Microsoft 365 Copilot",17,NAVY,True)
    txt(s,1.0,3.30,5.7,.28,"AGENTIC AI",10,GREEN,True)
    box(s,1.0,3.66,2.65,1.35,WHITE,GREEN); txt(s,1.2,3.98,2.25,.65,"Agent Builder in\nMicrosoft 365 Copilot",13,NAVY,True,PP_ALIGN.CENTER)
    box(s,3.9,3.66,2.65,1.35,WHITE,GREEN); txt(s,4.1,3.98,2.25,.65,"Microsoft\nCopilot Studio",14,NAVY,True,PP_ALIGN.CENTER)
    txt(s,1.0,5.42,5.55,.38,"Create with Copilot · orchestrate with agents · govern with human review",11,MID,False,PP_ALIGN.CENTER)
    steps=[("1","Use synthetic cases","Start from the supplied activity records."),("2","Create or analyse","Use Microsoft 365 Copilot with approved context."),("3","Build bounded agents","Use Agent Builder or Copilot Studio for governed workflows."),("4","Test and evidence","Save prompts, checks, revisions and human approvals.")]
    for i,(n,lab,body) in enumerate(steps):
        yy=1.58+i*1.16; accent=ACCENTS[i]
        av=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(7.35),Inches(yy+.1),Inches(.48),Inches(.48)); av.fill.solid(); av.fill.fore_color.rgb=accent; av.line.fill.background()
        txt(s,7.35,yy+.21,.48,.16,n,10,WHITE,True,PP_ALIGN.CENTER)
        txt(s,8.05,yy,4.25,.28,lab,13,NAVY,True); txt(s,8.05,yy+.34,4.25,.55,body,10,MID)
    return s

def lesson_plan_slide(prs):
    s=blank(prs); header(s,"Lesson Plan — 2 Days, 9:00am–6:00pm","SCHEDULE",BLUE)
    days=[("DAY 1 · FRAME & GENERATE",["Welcome, pain points and assessment briefing","Unit 1 · From Generative AI to Agentic HR","Labs 1–3 · Talent need, JD and resume screening","Unit 2 · Microsoft 365 Copilot across HR","Labs 4–6 · Interview, onboarding and development"]),("DAY 2 · ORCHESTRATE & GOVERN",["Retrieval practice and Unit 3 · Governed HR agents","Labs 7–9 · Policy, leave and benefits agents","Unit 4 · Responsible adoption and operations","Labs 10–12 · Wellness, offboarding and control room","4:30–6:30pm · WA then Case Study Assessment"])]
    for i,(lab,items) in enumerate(days):
        x=.72+i*6.02; accent=GREEN if i else BLUE; box(s,x,1.6,5.7,4.55,PALE,LINE)
        top=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(1.6),Inches(5.7),Inches(.08)); top.fill.solid(); top.fill.fore_color.rgb=accent; top.line.fill.background()
        txt(s,x+.3,1.88,5.05,.32,lab,13,accent,True)
        for j,item in enumerate(items):
            txt(s,x+.35,2.45+j*.66,.35,.24,"•",13,accent,True); txt(s,x+.72,2.38+j*.66,4.55,.48,item,11,NAVY,j==4)
    return s

def tsc_slide(prs):
    s=blank(prs); header(s,"Skills Framework — Human Resource Digitalisation","WSQ ALIGNMENT",BLUE)
    rows=[("TSC Title / Code",META['tsc']),("Knowledge","Generative AI, agentic AI and HR digitalisation"),("Application","Use-case analysis, feasibility, agent design and responsible controls"),("Evidence","Prompts, outputs, checks, decisions and audit trail")]
    x=.72; y=1.62; widths=[3.0,8.85]
    box(s,x,y,11.85,.55,BLUE,BLUE); txt(s,x+.2,y+.15,2.5,.2,"TSC element",11,WHITE,True); txt(s,x+3.18,y+.15,8.2,.2,"Detail",11,WHITE,True)
    for i,(lab,body) in enumerate(rows):
        yy=y+.62+i*.92; box(s,x,yy,11.85,.76,WHITE if i%2 else PALE,LINE)
        txt(s,x+.2,yy+.22,2.6,.25,lab,11,NAVY,True); txt(s,x+3.18,yy+.18,8.2,.38,body,11,INK)
    txt(s,.85,6.12,11.6,.32,"Every unit, activity and assessment item maps to this TSC through observable evidence.",11,MID,False,PP_ALIGN.CENTER)
    return s

def outcomes_slide(prs):
    s=blank(prs); header(s,"Learning Outcomes","BY THE END OF THIS COURSE",BLUE)
    for i,outcome in enumerate(LEARNING_OUTCOMES):
        y=1.55+i*1.18; accent=ACCENTS[i]
        box(s,.72,y,11.85,.88,WHITE,LINE)
        av=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(.92),Inches(y+.19),Inches(.5),Inches(.5)); av.fill.solid(); av.fill.fore_color.rgb=accent; av.line.fill.background()
        txt(s,.92,y+.30,.5,.16,i+1,10,WHITE,True,PP_ALIGN.CENTER)
        txt(s,1.65,y+.16,.55,.22,f"LO{i+1}",11,accent,True); txt(s,2.35,y+.13,9.75,.52,outcome,12,NAVY,True,valign=MSO_ANCHOR.MIDDLE)
    return s

def assessment_briefing_slide(prs):
    s=blank(prs); header(s,"Briefing for Assessment","READINESS · PRACTICE · CONFIDENTIALITY",RED)
    box(s,.72,1.55,7.15,4.9,PALE,LINE)
    txt(s,1.02,1.88,6.5,.3,"ASSESSMENT READINESS",11,RED,True)
    items=[
        ("01","Know the instruments","Written Assessment and Case Study; 60 minutes each; open book."),
        ("02","Protect the assessment","Work individually. Do not photograph, record, discuss or share assessment content."),
        ("03","Submit complete evidence","Answer every part, protect personal data and follow the assessor's LMS instructions."),
    ]
    for i,(n,lab,body) in enumerate(items):
        y=2.38+i*1.12; box(s,1.0,y,6.55,.9,WHITE,LINE); txt(s,1.25,y+.22,.5,.26,n,12,RED,True); txt(s,1.92,y+.15,2.15,.25,lab,12,NAVY,True); txt(s,4.02,y+.13,3.15,.54,body,10,MID)
    box(s,8.16,1.55,4.42,4.9,WHITE,BLUE)
    txt(s,8.5,1.9,3.72,.28,"PRACTICE EXAM ACCESS",11,BLUE,True)
    txt(s,8.5,2.45,3.55,.75,"Build confidence before assessment",19,NAVY,True)
    box(s,8.5,3.47,3.72,.72,PALE,BLUE)
    txt(s,8.66,3.68,3.4,.27,"exams.tertiaryinfotech.com",12,BLUE,True,PP_ALIGN.CENTER)
    txt(s,8.5,4.58,3.55,1.05,"Use the practice platform only for preparation. The actual WSQ assessment remains on the LMS and follows the assessor's instructions.",11,MID)
    txt(s,8.5,5.83,3.55,.24,"Practice does not replace the official assessment.",10,RED,True,PP_ALIGN.CENTER)
    add_notes(s,[SOURCES['practice_exam']]); return s

def course_outline_slide(prs):
    s=blank(prs); header(s,"Course Outline — Four Learning Units","THE JOURNEY",BLUE)
    for i,u in enumerate(UNITS):
        x=.72+(i%2)*6.02; y=1.58+(i//2)*2.32; accent=ACCENTS[i]
        box(s,x,y,5.7,1.92,PALE,LINE)
        top=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(5.7),Inches(.08)); top.fill.solid(); top.fill.fore_color.rgb=accent; top.line.fill.background()
        txt(s,x+.28,y+.24,.55,.34,str(i+1).zfill(2),16,accent,True)
        txt(s,x+1.0,y+.20,4.35,.58,u['title'],16,NAVY,True)
        txt(s,x+1.0,y+.90,4.35,.62,u['subtitle'],11,MID)
    return s

def assessment_flow_slide(prs):
    s=blank(prs); header(s,"Assessment Flow","ON ASSESSMENT DAY",BLUE)
    stages=["TRAQOM survey\non the LMS","Assessment digital\nattendance","Sit WA then\nCase Study","Submit answers\non the LMS","Sign Assessment\nSummary Record"]
    for i,body in enumerate(stages):
        x=.72+i*2.43; box(s,x,1.72,2.05,3.55,PALE,LINE)
        top=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(1.72),Inches(2.05),Inches(.08)); top.fill.solid(); top.fill.fore_color.rgb=BLUE; top.line.fill.background()
        av=s.shapes.add_shape(MSO_SHAPE.OVAL,Inches(x+.72),Inches(2.18),Inches(.62),Inches(.62)); av.fill.solid(); av.fill.fore_color.rgb=BLUE; av.line.fill.background()
        txt(s,x+.72,2.35,.62,.18,i+1,12,WHITE,True,PP_ALIGN.CENTER)
        txt(s,x+.18,3.25,1.69,1.1,body,13,NAVY,True,PP_ALIGN.CENTER,valign=MSO_ANCHOR.MIDDLE)
        if i<4: txt(s,x+2.08,3.05,.34,.4,"▶",18,BLUE,True,PP_ALIGN.CENTER)
    return s

def section_slide(prs,unit):
    s=blank(prs)
    accent=ACCENTS[(unit['id']-1)%4]
    txt(s,.7,.72,2,.35,f"LEARNING UNIT {unit['id']}",13,accent,True)
    txt(s,.7,1.55,11.5,1.2,unit['title'],38,NAVY,True)
    txt(s,.72,3.0,10.8,.55,unit['subtitle'],20,MID)
    # lifecycle ribbon
    labels=["FRAME","GENERATE","ORCHESTRATE","GOVERN"]
    for i,l in enumerate(labels):
        fill=accent if i==unit['id']-1 else PALE; col=WHITE if i==unit['id']-1 else MID
        box(s,.72+i*2.95,4.55,2.65,.72,fill,fill)
        txt(s,.82+i*2.95,4.75,2.45,.25,l,11,col,True,PP_ALIGN.CENTER)
    txt(s,.72,6.25,10.8,.28,"Concepts → evidence → activity → reflection",12,MID)
    return s

def concept_slide(prs,concept,index,accent):
    s=blank(prs); header(s,concept['title'],concept['takeaway'],accent)
    mode=concept.get('layout',index%4)
    pts=concept['points']
    if mode==0:
        # four stage horizontal pathway
        for i,p in enumerate(pts):
            x=.65+i*3.1
            box(s,x,2.1,2.65,2.65,WHITE,LINE)
            txt(s,x+.22,2.35,.52,.52,str(i+1),21,accent,True,PP_ALIGN.CENTER)
            txt(s,x+.25,3.18,2.15,1.15,p,15,NAVY,True,PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
            if i<3:
                txt(s,x+2.67,3.12,.4,.4,"→",24,accent,True,PP_ALIGN.CENTER)
        txt(s,.9,5.55,11.5,.45,"Design question  •  What evidence would make this safe enough for HR work?",15,MID,False,PP_ALIGN.CENTER)
    elif mode==1:
        # 2x2 quadrant
        labels=[("01",pts[0]),("02",pts[1]),("03",pts[2]),("04",pts[3])]
        for i,(n,p) in enumerate(labels):
            x=.8+(i%2)*6.05; y=1.7+(i//2)*2.35
            box(s,x,y,5.65,1.9,WHITE,LINE)
            txt(s,x+.28,y+.25,.6,.3,n,13,accent,True)
            txt(s,x+1.0,y+.35,4.25,1.05,p,18,NAVY,True,valign=MSO_ANCHOR.MIDDLE)
    elif mode==2:
        # orbit-like central idea
        box(s,4.55,2.45,4.25,1.5,PALE,accent)
        txt(s,4.8,2.72,3.75,.9,concept['takeaway'],16,NAVY,True,PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        coords=[(.7,1.65),(9.35,1.65),(.7,4.45),(9.35,4.45)]
        for i,p in enumerate(pts):
            x,y=coords[i]; box(s,x,y,3.25,1.22,WHITE,LINE); txt(s,x+.22,y+.25,2.82,.7,p,14,INK,True,PP_ALIGN.CENTER,valign=MSO_ANCHOR.MIDDLE)
    else:
        # decision bands
        for i,p in enumerate(pts):
            y=1.62+i*1.18
            box(s,1.0,y,11.25,.88,PALE if i%2==0 else WHITE,LINE)
            txt(s,1.25,y+.2,.55,.36,str(i+1),15,accent,True)
            txt(s,1.95,y+.18,9.8,.42,p,17,NAVY,True)
        txt(s,1.0,6.5,11.2,.3,"Human accountability remains visible at every layer.",13,MID,False,PP_ALIGN.CENTER)
    add_notes(s,concept.get('sources',[])); return s

def lab_evidence_slides(prs, a, accent):
    """Seven editable, case-specific evidence views for each learner lab."""
    slides=[]
    headers, rows = MOCK_DATA[a['num']]
    n=a['num']
    def base(title, subtitle):
        slide=blank(prs); header(slide,f"Lab {n:02d} | {title}",subtitle,accent)
        slides.append(slide)
        return slide
    # 1. Source schema and provenance
    s=base("Source fields", "Read the supplied synthetic CSV before asking Copilot to reason over it.")
    txt(s,.75,1.48,11.8,.36,f"mock-data.csv  •  {len(rows)} records  •  {len(headers)} fields",14,NAVY,True)
    for i,key in enumerate(headers):
        col=i%4; row=i//4; x=.75+col*3.12; y=2.05+row*1.04
        box(s,x,y,2.84,.83,WHITE,LINE)
        txt(s,x+.16,y+.14,2.52,.5,key.replace('_',' '),12,INK,True,valign=MSO_ANCHOR.MIDDLE)
    txt(s,.8,6.38,11.8,.4,"Source boundary  →  Synthetic records only; verify row IDs and field meaning before output.",14,accent,True)
    # 2. Actual source records
    s=base("Evidence sample", "Compare the output against real rows in the supplied lab data.")
    shown=headers[:4]
    if len(headers)>4: shown.append(headers[-1])
    colw=12.0/len(shown)
    for i,key in enumerate(shown):
        x=.7+i*colw; box(s,x,1.65,colw-.08,.6,accent,accent,False)
        txt(s,x+.12,1.78,colw-.32,.37,key.replace('_',' '),11,WHITE,True)
    for j,record in enumerate(rows[:3]):
        y=2.35+j*1.04
        for i,key in enumerate(shown):
            x=.7+i*colw; value=str(record[headers.index(key)])
            box(s,x,y,colw-.08,.94,PALE if j%2==0 else WHITE,LINE,False)
            txt(s,x+.1,y+.12,colw-.28,.68,value[:46],10,INK)
    txt(s,.8,6.18,11.8,.5,"Evidence check  →  Point to the source row and column before accepting a summary or recommendation.",14,NAVY,True)
    # 3. Case-specific prompt contract
    s=base("Prompt contract", "Use named fields, a bounded task and a verifiable output shape.")
    cards=[("ROLE",f"Act as an HR analyst for the synthetic {a['title'].lower()} case."),
           ("SOURCE",f"Use only mock-data.csv; cite {headers[0]} and {headers[min(1,len(headers)-1)]} for each claim."),
           ("TASK",a['outcome']),
           ("OUTPUT","Return a table: source record | observation | uncertainty | recommendation | human check."),
           ("STOP RULE","Write UNKNOWN when evidence is missing. Do not take a consequential HR action.")]
    for i,(label,body) in enumerate(cards):
        y=1.48+i*1.01; box(s,.8,y,11.7,.87,WHITE,LINE)
        txt(s,1.0,y+.16,1.45,.35,label,11,accent,True)
        txt(s,2.55,y+.12,9.65,.58,body,12,INK)
    # 4. Control flow with accountable hand-offs
    s=base("Controlled workflow", "The agent or Copilot prepares evidence; an authorised person controls the decision.")
    stages=[("INPUT",headers[0].replace('_',' ')),("ANALYSE",a['tools'][0]),("VERIFY",a['controls'][0]),("APPROVE","HR process owner"),("RECORD",a['deliverables'][0])]
    for i,(label,body) in enumerate(stages):
        x=.65+i*2.55; box(s,x,2.05,2.25,2.5,WHITE,LINE)
        txt(s,x+.15,2.3,1.95,.34,label,12,accent,True,PP_ALIGN.CENTER)
        txt(s,x+.18,3.0,1.9,1.1,body[:75],14,NAVY,True,PP_ALIGN.CENTER,valign=MSO_ANCHOR.MIDDLE)
        if i<4: txt(s,x+2.26,3.0,.25,.4,"→",20,accent,True)
    txt(s,.9,5.52,11.5,.75,"Audit trail: source ID → prompt/instructions → output → verification → approval → final status",16,INK,True,PP_ALIGN.CENTER)
    # 5. Verification matrix
    s=base("Verification matrix", "A claim passes only when the source, control and reviewer agree.")
    checks=[("Source",f"Match {headers[0]} to the CSV row", "Row exists"),
            ("Meaning",f"Interpret {headers[min(1,len(headers)-1)]} using the scenario brief", "No invented fact"),
            ("Control",a['controls'][0],"Human check recorded"),
            ("Boundary",a['controls'][-1],"Escalate exception")]
    for i,(label,rule,expected) in enumerate(checks):
        y=1.55+i*1.2; box(s,.8,y,11.7,1.04,WHITE,LINE)
        txt(s,1.0,y+.18,1.4,.4,label,12,accent,True)
        txt(s,2.45,y+.16,6.8,.58,rule[:95],13,INK)
        txt(s,9.55,y+.16,2.65,.58,expected,11,GREEN,True)
    # 6. Exception and regression tests
    s=base("Exception tests", "Test normal and failure paths before a learner marks the solution ready.")
    cases=[("Normal",str(rows[0][0]),"Grounded result with source ID"),
           ("Missing",str(headers[-1]),"Clarify or mark UNKNOWN"),
           ("Unauthorised","Cross-employee request","Refuse and escalate"),
           ("Failure","Tool/connector unavailable","No false success; retain audit"),
           ("Duplicate","Same request twice","One action or safe rejection")]
    for i,(kind,stimulus,expected) in enumerate(cases):
        y=1.45+i*.96; box(s,.72,y,11.85,.79,PALE if i%2==0 else WHITE,LINE,False)
        txt(s,.95,y+.18,1.45,.31,kind,12,accent,True)
        txt(s,2.55,y+.13,4.1,.45,stimulus[:48],12,INK)
        txt(s,6.9,y+.13,5.35,.45,expected,12,NAVY,True)
    txt(s,.85,6.45,11.7,.25,"Pass only with recorded actual result, reviewer and evidence reference.",12,RED,True)
    # 7. Evidence artifact and acceptance gate
    s=base("Evidence package", "Submit a traceable artifact, not a polished output alone.")
    for i,artifact in enumerate(a['deliverables']):
        y=1.7+i*1.08; box(s,.85,y,7.7,.88,WHITE,LINE)
        txt(s,1.1,y+.19,7.2,.47,artifact[:105],14,NAVY,True)
    box(s,8.8,1.7,3.55,3.65,PALE,LINE)
    txt(s,9.1,1.98,2.9,.34,"RELEASE GATE",12,accent,True)
    txt(s,9.1,2.56,2.9,2.48,"Source linked\nUncertainty stated\nHuman owner named\nFailure case tested",15,INK)
    txt(s,.85,6.25,11.6,.4,f"Save in Lab-{n:02d}-Evidence-Workbook.xlsx  •  include prompt, output, checks and revision.",14,accent,True)
    for slide in slides: add_notes(slide,[META['github']+f"/tree/master/labs/Lab-{n:02d}-{a['slug']}"])
    return slides

def activity_slides(prs,a,accent):
    slides=[]
    s=blank(prs); header(s,f"Lab {a['num']}: {a['title']}",a['outcome'],accent)
    box(s,.7,1.55,7.25,2.05,PALE,LINE); txt(s,.98,1.82,1.4,.28,"CASE",11,accent,True); txt(s,.98,2.25,6.65,1.05,a['scenario'],15,NAVY,True)
    box(s,8.2,1.55,4.4,2.05,WHITE,LINE); txt(s,8.48,1.82,1.5,.28,"TOOLS",11,accent,True)
    txt(s,8.48,2.22,3.75,1.1,"\n".join("• "+x for x in a['tools']),13,INK)
    for i,(lab,vals) in enumerate([("OUTPUTS",a['deliverables']),("GUARDRAILS",a['controls'])]):
        x=.7+i*6.0; box(s,x,4.05,5.72,1.78,WHITE,LINE); txt(s,x+.28,4.32,1.6,.26,lab,11,accent,True); txt(s,x+.28,4.75,5.1,.75,"\n".join("• "+v for v in vals),12,INK)
    txt(s,.7,6.46,11.8,.35,"Detailed procedure, prompts and evidence checklist: Learner Guide + lab folder",12,MID,False,PP_ALIGN.CENTER)
    slides.append(s)
    s=blank(prs); header(s,f"Lab {a['num']} success map","Show your reasoning—not only a polished output.",accent)
    stages=[("INPUT","Use the supplied synthetic case and approved sources"),("DECISION","State assumptions, criteria and the human owner"),("EVIDENCE","Save prompts, output, checks, revisions and approvals"),("QUALITY","Pass the acceptance criteria and answer reflection questions")]
    for i,(lab,body) in enumerate(stages):
        x=.72+i*3.05; box(s,x,1.7,2.72,3.65,WHITE,LINE); txt(s,x+.22,2.0,2.25,.28,lab,12,accent,True,PP_ALIGN.CENTER); txt(s,x+.26,2.72,2.15,1.55,body,15,NAVY,True,PP_ALIGN.CENTER,valign=MSO_ANCHOR.MIDDLE); txt(s,x+.45,4.72,1.78,.3,"✓ reviewable",11,GREEN,True,PP_ALIGN.CENTER)
    txt(s,.8,6.25,11.7,.45,"Stop if the agent or Copilot output cannot be traced, corrected or safely escalated.",15,RED,True,PP_ALIGN.CENTER)
    slides.append(s)
    return slides

def chart_slide(prs):
    s=blank(prs); header(s,"A balanced HR AI scorecard","Speed is useful only when quality, trust and control remain healthy.",GREEN)
    data=ChartData(); data.categories=["Cycle time","Accuracy","Adoption","Trust","Control"]
    data.add_series("Baseline",(42,72,35,68,64)); data.add_series("Pilot target",(70,90,65,80,92))
    ch=s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(.85), Inches(1.7), Inches(7.3), Inches(4.55), data).chart
    ch.has_legend=True; ch.legend.position=XL_LEGEND_POSITION.BOTTOM; ch.value_axis.maximum_scale=100; ch.value_axis.minimum_scale=0; ch.has_title=False
    ch.series[0].format.fill.solid(); ch.series[0].format.fill.fore_color.rgb=RGBColor(172,184,196)
    ch.series[1].format.fill.solid(); ch.series[1].format.fill.fore_color.rgb=GREEN
    box(s,8.55,1.7,3.9,4.55,PALE,LINE)
    txt(s,8.88,2.0,3.2,.35,"READ TOGETHER",12,GREEN,True)
    txt(s,8.88,2.55,3.15,2.75,"A lower cycle time cannot compensate for weak evidence, falling trust or missing approvals. Pair one value metric with at least one quality and one risk guardrail.",18,NAVY,True,valign=MSO_ANCHOR.MIDDLE)
    add_notes(s,[SOURCES['mckinsey'],SOURCES['gartner']]); return s

def build_ppt():
    prs=Presentation(); prs.slide_width=W; prs.slide_height=H
    title_slide(prs)
    # Front administration follows the approved SPC deck sequence and component style.
    admin_section(prs)
    digital_attendance(prs)
    trainer_profile(prs,True)
    trainer_profile(prs,False)
    bullet_admin(prs,"ICE-BREAKER","Let's Know Each Other",[
        "Your name and organisation or HR role.",
        "Your experience with Microsoft 365 Copilot, Copilot Studio or HR automation, if any.",
        "One HR process you would like to improve with generative or agentic AI.",
    ],BLUE)
    ground_rules(prs)
    lms_slide(prs)
    workbench_slide(prs)
    lesson_plan_slide(prs)
    tsc_slide(prs)
    outcomes_slide(prs)
    course_outline_slide(prs)
    assessment_briefing_slide(prs)
    final_assessment_slide(prs)
    assessment_flow_slide(prs)

    slide_map={"admin":{"start":1,"end":len(prs.slides)},"units":{},"activities":{}}
    for unit in UNITS:
        start=len(prs.slides)+1; section_slide(prs,unit); accent=ACCENTS[unit['id']-1]
        for i,concept in enumerate(unit['concepts']): concept_slide(prs,concept,i,accent)
        acts=[a for a in ACTIVITIES if a['unit']==unit['id']]
        for a in acts:
            astart=len(prs.slides)+1
            lab_evidence_slides(prs,a,accent)
            for s in activity_slides(prs,a,accent): add_notes(s,[META['github']+f"/tree/master/labs/Lab-{a['num']:02d}-{a['slug']}"])
            slide_map['activities'][str(a['num'])]={'start':astart,'end':len(prs.slides),'title':a['title']}
        # unit integration
        simple_admin(prs,f"Unit {unit['id']} integration","Connect concept, evidence and action",[("Key decision",unit['subtitle']),("Evidence","What would make the recommendation reviewable?"),("Human role","Who remains accountable?"),("Next move","What will you test or change?")],accent)
        slide_map['units'][str(unit['id'])]={'start':start,'end':len(prs.slides),'title':unit['title']}
    chart_slide(prs)
    simple_admin(prs,"HR lifecycle coverage","One operating system, many employee moments",[("Attract","Workforce planning, job design, recruitment and selection"),("Join","Onboarding, access, policy and manager connection"),("Grow","Performance, learning, mobility and engagement"),("Serve","Leave, benefits, payroll and employee relations"),("Exit","Offboarding, access, assets and knowledge transfer"),("Operate","Metrics, incidents, governance and retirement")],BLUE)
    simple_admin(prs,"The responsible-agent operating loop","Agents remain a managed organisational capability",[("1. Observe","Service, quality, adoption and risk signals"),("2. Review","Human owner inspects evidence and exceptions"),("3. Improve","Update knowledge, instructions, tools or process"),("4. Validate","Regression, fairness, security and user testing"),("5. Decide","Scale, remediate, pause or retire")],GREEN)
    simple_admin(prs,"Your 90-day pathway","Move through evidence gates",[("Days 1–30","Baseline • use-case boundary • privacy/risk review • prototype"),("Days 31–60","Test • human controls • user feedback • operating design"),("Days 61–90","Measured pilot • incident rehearsal • scale decision • handover")],ORANGE)
    simple_admin(prs,"Key takeaways","Use AI to return HR capacity to people and strategy",[("Reduce administration","Remove repetitive search, drafting, rekeying and follow-up."),("Improve productivity","Deliver faster, more consistent and evidence-led HR services."),("Elevate HR value","Redirect saved time to workforce strategy, coaching and employee care."),("Govern the change","Keep evidence, human authority, privacy and fairness visible.")],NAVY)
    simple_admin(prs,"Assessment reminder","Demonstrate your own competence",[("Written Assessment","60 minutes • K1–K5"),("Case Study Assessment","60 minutes • A1–A5"),("Before submission","Answer every part • check evidence • protect confidentiality")],RED)
    assessment_flow_slide(prs)
    digital_attendance(prs)
    simple_admin(prs,"Thank you","Design HR AI that gives people better service and humans better judgement",[("Course",META['title']),("Code",META['code']),("Resources","LMS/TMS course portal")],NAVY)
    for i,s in enumerate(prs.slides,1): footer(s,i)
    out=COURSEWARE/f"{META['title']}-v{META['version']}.pptx"; prs.save(out); normalize_pptx(out)
    slide_map['total_slides']=len(prs.slides); slide_map['version']=META['version']; slide_map['generated']=datetime.now().isoformat()
    (COURSEWARE/"slide_map.json").write_text(json.dumps(slide_map,indent=2),encoding="utf-8")
    return out,slide_map

def _rewrite_zip(path, transform):
    fd,tmp=tempfile.mkstemp(suffix=path.suffix); os.close(fd)
    try:
        with zipfile.ZipFile(path,'r') as src, zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as dst:
            for item in src.infolist():
                data=src.read(item.filename)
                data=transform(item.filename,data)
                dst.writestr(item,data)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def normalize_pptx(path):
    """Normalise python-pptx signed chart IDs to valid unsigned OOXML IDs."""
    def tr(name,data):
        if name.startswith('ppt/charts/') and name.endswith('.xml'):
            s=data.decode('utf-8')
            def repl(m):
                v=int(m.group(2)); return m.group(1)+str(v+2**32 if v<0 else v)+m.group(3)
            s=re.sub(r'(<c:(?:axId|crossAx) val=")(-?\d+)(")',repl,s)
            return s.encode('utf-8')
        return data
    _rewrite_zip(Path(path),tr)

def normalize_docx(path):
    """Supply required OOXML attributes omitted by some python-docx defaults."""
    def tr(name,data):
        if name=='word/settings.xml':
            s=data.decode('utf-8')
            s=re.sub(r'<w:zoom w:val="([^"]+)"\s*/>',r'<w:zoom w:val="\1" w:percent="100"/>',s)
            return s.encode('utf-8')
        return data
    _rewrite_zip(Path(path),tr)

def set_doc_margins(doc):
    for sec in doc.sections:
        sec.top_margin=DInches(.65); sec.bottom_margin=DInches(.65); sec.left_margin=DInches(.75); sec.right_margin=DInches(.75)

def style_doc(doc):
    styles=doc.styles
    styles['Normal'].font.name='Arial'; styles['Normal'].font.size=DPt(11); styles['Normal'].paragraph_format.space_after=DPt(5)
    for nm,size,col in [('Title',28,'0C2340'),('Heading 1',20,'0C2340'),('Heading 2',15,'0071BC'),('Heading 3',12,'00A6A6')]:
        st=styles[nm]; st.font.name='Arial'; st.font.size=DPt(size); st.font.bold=True; st.font.color.rgb=DRGB.from_string(col)
    set_doc_margins(doc)

def shade(cell,fill):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:fill'),fill); tcPr.append(shd)

def header_footer(doc,label):
    for sec in doc.sections:
        p=sec.header.paragraphs[0]; p.text=f"Tertiary Infotech Academy  |  {META['code']}  |  {META['title']}"; p.style=doc.styles['Normal']; p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p=sec.footer.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run(f"© Tertiary Infotech Academy Pte Ltd • {label} • Version {META['version']} • Page ")
        fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); p._p.append(fld)
        p.add_run(' of ')
        total=OxmlElement('w:fldSimple'); total.set(qn('w:instr'),'NUMPAGES'); p._p.append(total)

def cover_doc(doc,label):
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(ROOT/".claude/skills/courseware-build/assets/tertiary-infotech-logo.png"),width=DInches(.65))
    p.add_run("\nTERTIARY INFOTECH ACADEMY • WSQ\n").bold=True
    p.add_run("\n"+label.upper()+"\n").bold=True
    r=p.add_run("\n"+META['title']); r.bold=True; r.font.size=DPt(28); r.font.color.rgb=DRGB(12,35,64)
    p.add_run(f"\n\nCourse Code: {META['code']}\n{META['duration']}\n{META['tsc']}\nUEN 201200696W\n\nVersion {META['version']} • {META['date']}")
    doc.add_page_break()

def version_control(doc):
    doc.add_heading("Document Version Control",1)
    table(doc,["Version","Date","Summary"],[
        ("6.0","16 August 2026","Initial redesigned courseware package"),
        ("6.1","16 August 2026","SPC-aligned administration pages and visual repairs"),
        ("6.2","16 August 2026","Expanded research, full HR lifecycle activities, mock data and learner PDFs"),
        (META['version'],META['date'],"Renamed Microsoft Copilot for HR; converted activities to numbered labs and aligned the assessment"),
    ])
    doc.add_paragraph("Version numbers apply to this generated courseware release; assessment instruments retain their separately controlled version.")

def table(doc,headers,rows,widths=None):
    t=doc.add_table(rows=1,cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.style='Table Grid'
    for i,h in enumerate(headers):
        c=t.rows[0].cells[i]; c.text=str(h); shade(c,'0C2340')
        for r in c.paragraphs[0].runs: r.font.color.rgb=DRGB(255,255,255); r.bold=True
    for row in rows:
        cells=t.add_row().cells
        for i,v in enumerate(row): cells[i].text=str(v); cells[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    return t

def lab_visual(a, folder):
    """Generate an honest editable-source workflow schematic for the lab pack."""
    canvas=Image.new("RGB",(1600,380),(247,250,253)); draw=ImageDraw.Draw(canvas)
    try:
        font=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf",24)
        small=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf",17)
    except OSError:
        font=ImageFont.load_default(); small=font
    headers=MOCK_DATA[a['num']][0]
    nodes=[("SOURCE",headers[0]),("COPILOT",a['tools'][0]),("CONTROL",a['controls'][0]),("HUMAN", "HR process owner"),("EVIDENCE",a['deliverables'][0])]
    for i,(label,detail) in enumerate(nodes):
        x=25+i*315; y=55
        draw.rounded_rectangle((x,y,x+270,y+245),radius=24,fill=(255,255,255),outline=(37,97,160),width=3)
        draw.rounded_rectangle((x+15,y+15,x+255,y+68),radius=13,fill=(18,66,121))
        draw.text((x+28,y+27),label,font=font,fill=(255,255,255))
        words=detail.split(); rows=[]; line=''
        for word in words:
            test=(line+' '+word).strip()
            if len(test)>24 and line: rows.append(line); line=word
            else: line=test
        if line: rows.append(line)
        for j,line in enumerate(rows[:4]): draw.text((x+22,y+93+j*29),line,font=small,fill=(25,44,67))
        if i<4: draw.text((x+278,y+130),'→',font=font,fill=(37,97,160))
    draw.text((35,330),"Synthetic source → grounded output → control check → accountable approval → saved evidence",font=small,fill=(35,88,112))
    canvas.save(folder/'workflow.png')

def lab_workbench(a):
    """Current Microsoft workbench paths with a synthetic-data fallback."""
    n=a['num']; fields=MOCK_DATA[n][0]
    common=[
        "Sign in with the licensed training account. Use only the supplied synthetic `mock-data.csv` or evidence workbook; do not paste live HR records.",
        f"Open `Lab-{n:02d}-Evidence-Workbook.xlsx`, inspect the Mock Data sheet and record the meaning of `{fields[0]}` and `{fields[min(1,len(fields)-1)]}` before prompting.",
    ]
    if n in (1,3,10,12):
        steps=common+[
            "Save a working copy of the workbook in the approved OneDrive or SharePoint training location. In Excel, make the source range a named Table with headers, then open Copilot from the ribbon.",
            f"Ask Copilot to use the named table and cite `{fields[0]}` for each finding. Request an output table with evidence, uncertainty and an HR reviewer action.",
            "Compare at least three claims with the original CSV rows. Write corrections and the exact prompt in the Evidence Log; do not treat a Copilot chart or summary as a final decision.",
        ]
        url="https://support.microsoft.com/en-us/copilot-excel"
    elif n in (2,4):
        steps=common+[
            "Open Word in the approved Microsoft 365 training account and create a new working document. Open Copilot from the ribbon and attach or reference the approved synthetic brief.",
            "Paste the prompt scaffold below. Ask for a structured draft with criterion-to-source citations and a separate UNKNOWN list for unsupported requirements.",
            "Track the edits you accept, compare each criterion or question with the source rubric, and ask the HR owner to approve the final version in the evidence workbook.",
        ]
        url="https://support.microsoft.com/en-us/copilot-word"
    elif n in (6,7):
        steps=common+[
            "Open Microsoft 365 Copilot in a desktop browser. In the left pane choose New agent; use Describe or Configure to enter a purpose, audience and bounded instructions.",
            "On Configure, add only approved training knowledge from SharePoint or OneDrive. Record the exact source title, owner, effective date and access boundary.",
            "Create the agent, open it in Copilot and test one normal, one ambiguous, one outdated or unsupported, and one unauthorised request. Save the actual replies and citations.",
            "If a reply lacks a citation or exceeds scope, revise the instructions or knowledge set and rerun the same test ID before sharing the agent.",
        ]
        url="https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-templates-overview"
    else:
        steps=common+[
            "Open Copilot Studio in the approved training environment. Under Agents create a draft agent; set a clear name, purpose, instructions, authentication and escalation boundary.",
            "Add only approved synthetic knowledge. If the scenario needs a transaction, create a deterministic flow from Workflows > New agent flow with typed inputs, validation, an approval gate and a status output.",
            "For an agent-callable flow use a When an agent calls the flow trigger and Respond to the agent action. Add the published flow as a tool to the draft agent and map each input explicitly.",
            "Use the agent Test pane with `agent-test-cases.csv`. Record the test ID, input, expected result, actual reply or tool trace, permission result, reviewer and pass/fail.",
            "Do not publish the agent to a broad channel during class. A trainer may allow a private test after all normal, exception, duplicate and connector-failure cases pass.",
        ]
        url="https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-overview"
    return steps,url

def build_learner_guide(slide_map):
    d=Document(); style_doc(d); header_footer(d,"Learner Guide"); cover_doc(d,"Learner Guide")
    version_control(d)
    d.add_heading("Contents",1)
    toc=d.add_paragraph()
    toc_field=OxmlElement('w:fldSimple'); toc_field.set(qn('w:instr'),'TOC \\o "1-2" \\h \\z \\u'); toc._p.append(toc_field)
    d.add_heading("How to use this guide",1); d.add_paragraph("The slide deck explains concepts visually. This Learner Guide contains the detailed activity procedures, prompts, evidence requirements and questions. All cases and records are synthetic for learning; do not substitute live employee data.")
    d.add_heading("Course information",1); table(d,["Field","Detail"],[("Course",META['title']),("Course code",META['code']),("Duration",META['duration']),("TSC",META['tsc']),("Trainer",META['trainer'])])
    d.add_heading("Learning outcomes",1)
    for i,x in enumerate(LEARNING_OUTCOMES,1): d.add_paragraph(f"LO{i}. {x}",style='List Number')
    d.add_heading("The course message",1)
    table(d,["Use AI to","Operational effect","Value released"],[
        ("Reduce administrative work","Automate repetitive search, drafting, rekeying, routing, reminders and status updates","More time for complex employee needs"),
        ("Improve productivity and efficiency","Shorten cycle time while improving consistency, traceability and service access","More reliable HR delivery at scale"),
        ("Focus HR on strategic value","Return capacity to workforce planning, coaching, culture, organisation design and employee care","A stronger connection between the people agenda and business outcomes"),
    ])
    d.add_paragraph("The objective is not to remove human accountability. Copilot accelerates knowledge work; bounded agents coordinate approved work; authorised HR professionals remain responsible for consequential decisions and human conversations.")
    d.add_heading("Platform model",1)
    table(d,["Need","Preferred Microsoft capability","Human role"],[
        ("Draft, summarise, compare or analyse","Microsoft 365 Copilot in Word, Excel, Outlook, Teams","Provide context, verify evidence and approve output"),
        ("Focused team Q&A over approved knowledge","Agent Builder in Microsoft 365 Copilot","Curate knowledge, test and manage sharing"),
        ("Multi-step workflow across systems","Microsoft Copilot Studio with tools/agent flows","Approve consequential actions and operate controls"),
    ])
    d.add_heading("Reference case vignettes",1)
    d.add_paragraph("The user-supplied ebook presents four unnamed implementation vignettes. They are included as secondary-source discussion cases; the reported organisations are not independently identified in the reference.")
    for heading,body in [
        ("Technology — recruitment","AI-assisted screening and candidate chat reportedly shortened the hiring cycle by 30% while supporting diversity-oriented process improvements."),
        ("Retail — engagement and retention","Feedback and sentiment analysis informed targeted interventions associated with a reported 20% reduction in turnover."),
        ("Financial services — talent development","Predictive talent evidence supported succession planning, leadership-pipeline decisions and personalised development."),
        ("Healthcare — performance and coaching","More timely performance evidence enabled earlier coaching and more consistent reviews."),
    ]:
        d.add_heading(heading,2); d.add_paragraph(body)
    d.add_paragraph("Discussion: What administrative work was reduced? What evidence suggests productivity or service improvement? Which strategic HR activity became more possible? What safeguards and verification would be required before applying the pattern?")
    d.add_heading("Contents and slide alignment",1)
    table(d,["Unit","Coverage","Slides"],[(u['id'],u['title'],f"{slide_map['units'][str(u['id'])]['start']}–{slide_map['units'][str(u['id'])]['end']}") for u in UNITS])
    for unit in UNITS:
        d.add_heading(f"Learning Unit {unit['id']}: {unit['title']}",1); d.add_paragraph(unit['subtitle'])
        d.add_heading("Concept notes",2)
        for con in unit['concepts']:
            d.add_heading(con['title'],3); d.add_paragraph(con['takeaway'])
            for p in con['points']: d.add_paragraph(p,style='List Bullet')
            d.add_paragraph("Sources: "+"; ".join(con['sources']))
        for a in [x for x in ACTIVITIES if x['unit']==unit['id']]:
            d.add_heading(f"Lab {a['num']}: {a['title']}",2)
            d.add_heading("Scenario",3); d.add_paragraph(a['scenario'])
            d.add_picture(str(ACTIVITIES_DIR/f"Lab-{a['num']:02d}-{a['slug']}"/"workflow.png"),width=DInches(6.3))
            d.add_paragraph("Workflow schematic: synthetic source → Copilot/agent → control → human approval → evidence.")
            d.add_heading("Learning goal",3); d.add_paragraph(a['outcome'])
            d.add_heading("Tools",3); d.add_paragraph("; ".join(a['tools']))
            d.add_heading("Procedure",3)
            for i,st in enumerate(a['steps'],1): d.add_paragraph(f"{i}. {st}")
            d.add_heading("Test-it evidence",3)
            d.add_paragraph("Record test ID, input, expected result, actual result, citation, reviewer and pass/fail. For agents, use the supplied test-case CSV and save the conversation or flow trace.")
            d.add_heading("Product workbench",3)
            workbench,url=lab_workbench(a)
            for i,step in enumerate(workbench,1): d.add_paragraph(f"{i}. {step}")
            d.add_paragraph("Microsoft product reference: "+url)
            d.add_heading("Prompt scaffold",3)
            d.add_paragraph(f"You are supporting the {META['title']} case. Use only the supplied synthetic evidence. Task: {a['outcome']} State assumptions, cite the evidence used, distinguish observation from inference, identify uncertainty, and list the human checks required before use.")
            d.add_heading("Evidence to submit",3)
            for x in a['deliverables']: d.add_paragraph(x,style='List Bullet')
            d.add_heading("Acceptance criteria",3)
            for x in a['controls']: d.add_paragraph(x,style='List Bullet')
            d.add_paragraph("The submission is complete when the workbook evidence log contains the input/source, prompt or design decision, output, verification, revision and named human owner.")
            d.add_heading("Scenario questions",3)
            for q in a['questions']: d.add_paragraph(q,style='List Number')
    d.add_heading("Responsible HR AI checklist",1)
    for x in ["Purpose and scope are explicit.","Only necessary and authorised data are used.","Job-related evidence and fair criteria are documented.","Sources, uncertainty and limitations are visible.","Consequential decisions have an authorised human approver.","Agent identity, permissions, tools and destinations use least privilege.","Normal, edge, adversarial and failure cases are tested.","Logs, incidents, feedback, change and retirement have owners."]:
        d.add_paragraph("☐ "+x)
    d.add_heading("Source register",1)
    d.add_paragraph("The complete reviewed source register, access status and cross-artifact coverage matrix are maintained in SOURCE-COVERAGE.md alongside the courseware. Key authoritative anchors include Microsoft product/adoption guidance, Singapore PDPC's Model AI Governance Framework and Singapore MOM's Fair Consideration Framework.")
    out=COURSEWARE/f"LG-{META['title']}.docx"; d.save(out); normalize_docx(out); return out

def build_learner_guide_markdown(slide_map):
    lines=[f"# {META['title']} — Learner Guide","",f"Course code: {META['code']}  ",f"Version: {META['version']}  ",f"Duration: {META['duration']}","","## Course message","","Use AI to reduce administrative work, improve productivity and efficiency, and return HR capacity to workforce strategy, coaching, organisation design and employee care. Human professionals remain accountable for consequential decisions and conversations.","","## Platform model","","- **Microsoft 365 Copilot:** human-directed drafting, summarisation, comparison and analysis.","- **Agent Builder in Microsoft 365 Copilot:** focused team Q&A over approved knowledge.","- **Microsoft Copilot Studio:** bounded agents, tools, flows, channels and lifecycle operations.","","## Reference case vignettes","","The supplied ebook presents four unnamed secondary-source cases: recruitment screening and candidate chat; retail engagement and retention; financial-services talent development; and healthcare performance coaching. Treat the reported outcomes as discussion evidence, not independently verified company identities.",""]
    for unit in UNITS:
        sm=slide_map['units'][str(unit['id'])]
        lines += [f"## Learning Unit {unit['id']}: {unit['title']}","",f"Slides {sm['start']}–{sm['end']} · {unit['subtitle']}",""]
        for con in unit['concepts']:
            lines += [f"### {con['title']}","",con['takeaway'],""]+[f"- {p}" for p in con['points']]+["",f"Sources: {'; '.join(con['sources'])}",""]
        for a in [x for x in ACTIVITIES if x['unit']==unit['id']]:
            am=slide_map['activities'][str(a['num'])]
            lines += [f"### Lab {a['num']}: {a['title']}","",f"Slides {am['start']}–{am['end']}","","Scenario: "+a['scenario'],"","Learning goal: "+a['outcome'],"","Tools: "+"; ".join(a['tools']),"","Detailed procedure:",""]+[f"{i}. {step}" for i,step in enumerate(a['steps'],1)]+["","Evidence to submit:",""]+[f"- {x}" for x in a['deliverables']]+["","Guardrails:",""]+[f"- {x}" for x in a['controls']]+["","Scenario questions:",""]+[f"{i}. {q}" for i,q in enumerate(a['questions'],1)]+["",f"Full learner pack: `../labs/Lab-{a['num']:02d}-{a['slug']}/README.pdf`",""]
    lines += ["## Responsible HR AI checklist","","- Purpose and scope are explicit.","- Only necessary and authorised data are used.","- Evidence, uncertainty and limitations are visible.","- Consequential decisions have an authorised human approver.","- Normal, edge, adversarial and failure cases are tested.","- Logs, incidents, feedback, changes and retirement have owners.",""]
    out=COURSEWARE/"LEARNER-GUIDE.md"; out.write_text("\n".join(lines)+"\n",encoding="utf-8"); return out

def build_lesson_plan(slide_map):
    d=Document(); style_doc(d); header_footer(d,"Lesson Plan"); cover_doc(d,"Lesson Plan")
    version_control(d)
    d.add_heading("Contents",1)
    toc=d.add_paragraph()
    toc_field=OxmlElement('w:fldSimple'); toc_field.set(qn('w:instr'),'TOC \\o "1-2" \\h \\z \\u'); toc._p.append(toc_field)
    d.add_heading("Course and delivery overview",1)
    table(d,["Field","Detail"],[("Course",META['title']),("Code",META['code']),("Duration","2 days, 09:30–18:30 daily; 16 scheduled contact hours excluding lunch, including two facilitated 15-minute reflection intervals per day"),("Mode","Facilitated classroom or synchronous virtual delivery"),("Assessment","Written Assessment, 60 minutes; Case Study Assessment, 60 minutes")])
    d.add_heading("Learning outcomes and evidence",1)
    for i,x in enumerate(LEARNING_OUTCOMES,1): d.add_paragraph(f"LO{i}: {x}")
    d.add_paragraph("Labs 1–3, 4–6 and 7–9 are parallel team pods: each learner completes one lab in class and shares the result with peers; the other two are self-paced. Labs 10–11 are self-paced extensions. Lab 12 is a 45-minute in-class decision sprint using supplied evidence; full build and regression testing continue after class. The individual WA and Case Study remain 60 minutes each.")
    d.add_heading("Facilitation principles",1)
    for x in ["Open with the current HR pain points and return throughout to the three-part value message: less administration, higher productivity and more strategic HR capacity.","Use the slides for visual explanation; use the Learner Guide for procedures.","Demonstrate only with synthetic records and approved tenant content.","Ask learners to state evidence, uncertainty and human ownership.","Do not coach or disclose answers during individual assessment."]:
        d.add_paragraph(x,style='List Bullet')
    for day in [1,2]:
        d.add_page_break(); d.add_heading(f"Day {day} schedule",1)
        rows=[]
        for _,start,end,topic,method,align in [r for r in SCHEDULE if r[0]==day]:
            if align.startswith("Unit "):
                uid=align[-1]; sm=slide_map['units'][uid]; align=f"Slides {sm['start']}–{sm['end']}"
            elif align.startswith("Labs"):
                nums=[]
                rng=align.replace('Labs ','').split('–'); nums=range(int(rng[0]),int(rng[-1])+1)
                align="; ".join(f"L{n}: {slide_map['activities'][str(n)]['start']}–{slide_map['activities'][str(n)]['end']}" for n in nums)
            rows.append((f"{start}–{end}",topic,method,align))
        table(d,["Time","Topic/activity","Method","Slide/evidence alignment"],rows)
        d.add_heading("Trainer notes",2)
        if day==1:
            d.add_paragraph("Begin with fragmented requests, repeated rekeying, slow responses and weak traceability. Establish the continuum from deterministic automation to Copilot-assisted work and bounded agency. Use Labs 1–6 as one talent journey from demand through development. At every debrief, ask what administration was removed, what productivity improved and what strategic or human work received the returned capacity.")
        else:
            d.add_paragraph("Use Labs 7–9 as parallel employee-service pods and Lab 12 as a short control-room decision sprint; Labs 10–11 are self-paced extensions. Use the employee-service and exit journey. Keep agent building anchored to purpose, knowledge, tools, boundaries and tests. Rehearse failure and escalation, and distinguish time genuinely returned from new monitoring work. Before assessment, clarify logistics and permitted resources without revealing model responses.")
    d.add_page_break(); d.add_heading("Lab facilitation and debrief",1)
    for a in ACTIVITIES:
        d.add_heading(f"Lab {a['num']}: {a['title']}",2)
        d.add_paragraph(f"Purpose: {a['outcome']}")
        d.add_paragraph("Observe for: " + "; ".join(a['controls']))
        d.add_paragraph("Debrief: " + " | ".join(a['questions']))
        d.add_paragraph(f"Slides: {slide_map['activities'][str(a['num'])]['start']}–{slide_map['activities'][str(a['num'])]['end']}")
    out=COURSEWARE/f"LP-{META['title']}.docx"; d.save(out); normalize_docx(out); return out

def build_workbook(a,folder):
    wb=Workbook(); ws=wb.active; ws.title="Brief"
    rows=[("Lab",f"{a['num']}: {a['title']}"),("Scenario",a['scenario']),("Outcome",a['outcome']),("Data notice","All data are synthetic. Do not add live employee personal data."),("Tools","; ".join(a['tools']))]
    for r in rows: ws.append(r)
    inp=wb.create_sheet("Mock Data")
    headers, mock_rows=MOCK_DATA[a['num']]
    inp.append(headers)
    for row in mock_rows: inp.append(row)
    ev=wb.create_sheet("Evidence Log"); ev.append(["Step","Input/source","Prompt or design decision","AI/output summary","Human verification","Revision/action","Owner","Status"])
    for i,st in enumerate(a['steps'],1): ev.append([i,st,"","","","","Learner","Not started"])
    audit=wb.create_sheet("Audit and Score")
    audit.append(["Criterion","Weight","Evidence score (0-5)","Weighted result","Notes"])
    crit=[("Outcome fit",25),("Evidence traceability",25),("Human control",20),("Privacy/fairness/security",20),("Usability",10)]
    for i,(c,w) in enumerate(crit,2): audit.append([c,w,"",f'=IF(C{i}="","",B{i}*C{i}/5)',""])
    audit.append(["Total",100,"",f"=SUM(D2:D{len(crit)+1})",""])
    for wsx in wb.worksheets:
        wsx.freeze_panes="A2"; wsx.sheet_view.showGridLines=False
        for cell in wsx[1]: cell.font=Font(name="Arial",bold=True,color="FFFFFF"); cell.fill=PatternFill("solid",fgColor="0C2340"); cell.alignment=Alignment(wrap_text=True,vertical="center")
        for row in wsx.iter_rows(min_row=2):
            for cell in row: cell.font=Font(name="Arial",size=10); cell.alignment=Alignment(wrap_text=True,vertical="top")
        for col in range(1,wsx.max_column+1): wsx.column_dimensions[get_column_letter(col)].width=min(42,max(13,max(len(str(wsx.cell(r,col).value or "")) for r in range(1,wsx.max_row+1))*.85))
        wsx.auto_filter.ref=wsx.dimensions
    out=folder/f"Lab-{a['num']:02d}-Evidence-Workbook.xlsx"; wb.save(out); return out

def build_activities():
    ACTIVITIES_DIR.mkdir(parents=True,exist_ok=True)
    index=[f"# {META['title']} — Labs","",f"Course code: {META['code']}","","The 12 labs form one coherent HarbourLight Logistics SG journey from talent demand to safe offboarding and portfolio governance.","","Every folder is self-contained and includes the detailed learner procedure in Markdown and PDF, scenario-specific mock data in CSV and Excel, and evidence requirements. All cases and records are synthetic.",""]
    for a in ACTIVITIES:
        folder=ACTIVITIES_DIR/f"Lab-{a['num']:02d}-{a['slug']}"; folder.mkdir(parents=True,exist_ok=True); lab_visual(a,folder)
        body=[f"# Lab {a['num']}: {a['title']}","","> **Synthetic learning case:** Do not upload live employee or candidate data.","","## Scenario","",a['scenario'],"","![Lab workflow schematic](workflow.png)","","## Learning goal","",a['outcome'],"","## Microsoft tools",""]
        body += [f"- {x}" for x in a['tools']]
        body += ["","## Supplied mock data","",f"Use `mock-data.csv` or the **Mock Data** sheet in `Lab-{a['num']:02d}-Evidence-Workbook.xlsx`. The records are specific to this scenario and carry forward the HarbourLight case.","","## Guardrails",""]+[f"- {x}" for x in a['controls']]
        body += ["","## Detailed procedure",""]+[f"{i}. {x}" for i,x in enumerate(a['steps'],1)]
        body += ["","## Product workbench","" ]
        workbench,url=lab_workbench(a)
        body += [f"{i}. {step}" for i,step in enumerate(workbench,1)] + ["",f"Microsoft product reference: {url}","","## Prompt scaffold","",f"> You are supporting the HarbourLight Logistics SG training case. Use only the supplied synthetic evidence. Your task is to {a['outcome'].lower()} State assumptions; cite record IDs or approved source sections; separate observation from inference; flag missing information; list the human checks and approvals required before use.","","## Evidence checklist",""]
        body += [f"- [ ] {x}" for x in a['deliverables']]
        body += ["- [ ] Evidence workbook records the input/source, prompt or decision, output, verification, revision and owner.","- [ ] A peer or trainer can reproduce the reasoning from the saved evidence.","","## Acceptance criteria",""]+[f"- {x}" for x in a['controls']]
        body += ["- The output is accurate, traceable, usable and explicit about uncertainty.","- Consequential decisions and actions remain with an authorised human.","","## Scenario questions",""]+[f"{i}. {q}" for i,q in enumerate(a['questions'],1)]
        body += ["","## Submission naming","",f"`L{a['num']:02d}-<YourName>-Evidence.xlsx` plus the listed deliverables.","","## Source anchors","",f"- Course source register: `../SOURCE-COVERAGE.md`",f"- Microsoft capability boundary: Microsoft 365 Copilot for generative work; Agent Builder or Copilot Studio for agentic work."]
        body += ["","## Recommended team roles and timing","",f"- **HR process owner:** confirms that the output solves the stated {a['title'].lower()} outcome and remains consistent with approved policy.","- **AI operator or maker:** records the exact prompt, instructions, knowledge sources, tool choices and revisions.","- **Reviewer or approver:** independently checks evidence, permissions, fairness, privacy and any consequential action.","- **Evidence recorder:** keeps the workbook complete enough for another person to reproduce the reasoning.","", "Allow about 35–50 minutes for the first build, 15 minutes for testing and verification, and 10 minutes for peer challenge and reflection. The trainer may adjust the timing to fit the delivery mode.","","## Test-it evidence","","Record test ID, input, expected result, actual result, source citation, reviewer and pass/fail in the evidence workbook. For agent labs, use `agent-test-cases.csv` and capture the test conversation or run result before marking a case complete.","","## Verification method","","1. Compare every factual statement or extracted item with the supplied source record.","2. Mark missing information as unknown; do not convert absence into a negative assumption.","3. Check that personal data, tool access and sharing are limited to the stated purpose.","4. Test one normal case, one ambiguous case, one out-of-scope case and one failure or exception.","5. Ask a peer to challenge the decision, then record whether you accepted or rejected the challenge and why.","6. Confirm the named human owner can correct, stop or reverse the work before submission.","","## Troubleshooting and recovery","","- If Copilot invents evidence, narrow the prompt to named files, tables or record IDs and request citations.","- If an agent answers outside scope, strengthen instructions, remove inappropriate knowledge or tools, and add an explicit escalation response.","- If a flow fails or repeats an action, do not report success. Preserve the error, check the audit record, use a unique request key, and route the case to the human owner.","- If the output is polished but cannot be traced to evidence, treat it as incomplete and rebuild the evidence chain."]
        (folder/"README.md").write_text("\n".join(body)+"\n",encoding="utf-8")
        headers, mock_rows=MOCK_DATA[a['num']]
        with (folder/"mock-data.csv").open("w",newline="",encoding="utf-8") as f:
            writer=csv.writer(f); writer.writerow(headers); writer.writerows(mock_rows)
        build_workbook(a,folder)
        # specialised test cases for agent activities
        if a['num'] in (5,6,7,8,9,11,12):
            cases=["Normal request","Ambiguous request","Out-of-scope personal decision","Prompt injection attempt","Unauthorised data request","Connector failure","Duplicate action","Human escalation"]
            lines=["test_id,intent,expected_behavior,actual_result,pass_fail,evidence"]+[f"TC-{i:02d},{c},Clarify or act only within approved bounds,,," for i,c in enumerate(cases,1)]
            (folder/"agent-test-cases.csv").write_text("\n".join(lines)+"\n",encoding="utf-8")
        if a['num']==3:
            rd=folder/"synthetic-resumes"; rd.mkdir(exist_ok=True)
            names=[("Alex Tan","warehouse reporting, Excel dashboards, stakeholder workshops"),("Jamie Lim","process mapping, Power BI, training coordination"),("Morgan Lee","inventory analysis, SQL basics, operations improvement"),("Riley Ong","customer service analytics, Excel, change support"),("Casey Goh","workforce scheduling, safety reporting, facilitation"),("Taylor Koh","procurement analysis, dashboard design, team coaching")]
            for i,(name,skills) in enumerate(names,1):
                (rd/f"Resume-{i:02d}.md").write_text(f"# Synthetic Resume {i:02d}\n\nCandidate: {name}\n\nProfile: Operations professional with experience in {skills}.\n\nEvidence:\n- Led a synthetic improvement project with documented outcomes.\n- Prepared weekly operational reports for cross-functional stakeholders.\n- Completed relevant digital skills learning.\n\nThis record is fictional and created solely for training.\n",encoding="utf-8")
        index.append(f"- [Lab {a['num']}: {a['title']}](Lab-{a['num']:02d}-{a['slug']}/README.md)")
    (ACTIVITIES_DIR/"README.md").write_text("\n".join(index)+"\n",encoding="utf-8")

def convert_pdf(paths):
    soffice=which("soffice") or which("libreoffice")
    if not soffice: return []
    done=[]
    for p in paths:
        r=run([soffice,"--headless","--convert-to","pdf","--outdir",str(p.parent),str(p)],capture_output=True,text=True)
        if r.returncode==0: done.append(p.with_suffix('.pdf'))
    return done

def main():
    COURSEWARE.mkdir(parents=True,exist_ok=True); build_activities()
    ppt,sm=build_ppt(); lg=build_learner_guide(sm); lp=build_lesson_plan(sm)
    lg_md=build_learner_guide_markdown(sm)
    pdfs=convert_pdf([ppt,lg,lp])
    print(json.dumps({"ppt":str(ppt),"slides":sm['total_slides'],"lg":str(lg),"lg_md":str(lg_md),"lp":str(lp),"pdfs":[str(x) for x in pdfs],"activities":len(ACTIVITIES)},indent=2))

if __name__=="__main__": main()
