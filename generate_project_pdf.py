"""
Script to generate a comprehensive, executive-quality PDF report:
'Codebase Evolution Intelligence System - Project Architecture & Interview Guide'
Covers Problem Statement, Solution, Features, Architecture, Tech Stack, and Interview Explanation Guide.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Do not draw headers/footers on cover-like first page top if desired, or draw on all
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "Codebase Evolution Intelligence System - Comprehensive Project & Interview Guide")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 45, letter[0] - 54, 45)

        self.drawString(54, 32, "Confidential - Prepared for Technical Portfolio & Interview Defense")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_str)
        self.restoreState()


def create_project_pdf(output_filename="Codebase_Evolution_Intelligence_System_Guide.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palettes
    c_primary = colors.HexColor("#0f172a")     # Deep Slate
    c_secondary = colors.HexColor("#1e40af")   # Royal Blue
    c_accent = colors.HexColor("#2563eb")      # Electric Blue
    c_dark = colors.HexColor("#1e293b")        # Slate 800
    c_body = colors.HexColor("#334155")        # Slate 700
    c_bg_light = colors.HexColor("#f8fafc")    # Slate 50
    c_bg_box = colors.HexColor("#eff6ff")      # Soft Blue
    c_border = colors.HexColor("#cbd5e1")      # Slate 300
    c_green = colors.HexColor("#059669")       # Emerald
    c_orange = colors.HexColor("#ea580c")      # Orange

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        alignment=0,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        alignment=0,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_secondary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_dark,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_body,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_body,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    callout_text = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark
    )

    qa_q_style = ParagraphStyle(
        'QA_Q',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=c_secondary,
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    qa_a_style = ParagraphStyle(
        'QA_A',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_body,
        spaceAfter=6
    )

    story = []

    # =========================================================================
    # HEADER / COVER TITLE SECTION
    # =========================================================================
    story.append(Paragraph("Codebase Evolution Intelligence System", title_style))
    story.append(Paragraph("Comprehensive Project Specification, Technical Architecture & Interview Defense Guide", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=0, spaceAfter=12))

    # Meta banner table
    meta_data = [
        [
            Paragraph("<b>Domain:</b> Software Engineering Analytics & Mining", body_style),
            Paragraph("<b>Target Stack:</b> Python, MySQL, Streamlit, GitPython, Radon", body_style)
        ],
        [
            Paragraph("<b>Target Audience:</b> Tech Interviewers, Recruiters, Evaluators", body_style),
            Paragraph("<b>Status:</b> Production Ready & End-to-End Verified", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # =========================================================================
    # 1. PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("1. Problem Statement", h1_style))
    p1 = (
        "Modern software engineering repositories accrue thousands of commits, hundreds of modified files, "
        "and multi-author interactions over years of active development. However, <b>Git history remains an unmined "
        "black box</b> for engineering leads and developers. Critical operational questions cannot be answered "
        "using standard Git commands alone:"
    )
    story.append(Paragraph(p1, body_style))

    story.append(Paragraph("• <b>Invisible Technical Debt:</b> Which files undergo erratic modification and code churn without delivering proportional functional value?", bullet_style))
    story.append(Paragraph("• <b>Defect Clustering:</b> Where do defects and bug fixes historically recur across releases?", bullet_style))
    story.append(Paragraph("• <b>Complexity Accumulation:</b> Which files combine complex branching logic with frequent edits, creating high risk for regressions?", bullet_style))
    story.append(Paragraph("• <b>Knowledge Silos & Bus Factor:</b> Is critical domain knowledge concentrated in single authors, and how is code ownership distributed?", bullet_style))
    story.append(Paragraph("• <b>Velocity & Lifecycle Blindness:</b> Is the codebase expanding steadily, or has it entered a phase of high maintenance churn?", bullet_style))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 2. THE SOLUTION
    # =========================================================================
    story.append(Paragraph("2. The Solution", h1_style))
    p2 = (
        "The <b>Codebase Evolution Intelligence System</b> is an automated software repository intelligence "
        "platform. Given any public Git/GitHub URL, the system clones the repository, traverses its complete commit DAG, "
        "computes static McCabe Cyclomatic Complexity using <b>Radon</b>, executes a multi-factor <b>Hotspot Scoring "
        "Algorithm</b>, persists structured records into a relational <b>MySQL</b> database, and delivers high-contrast, "
        "interactive visual analytics through a <b>Streamlit</b> web dashboard."
    )
    story.append(Paragraph(p2, body_style))

    # Solution Callout Box
    sol_box_data = [[
        Paragraph(
            "<b>Core Value Proposition:</b> Transforms raw, chronological Git commits into actionable, multidimensional "
            "engineering insights—enabling proactive refactoring, bug hotspot isolation, and architectural risk mitigation.",
            callout_text
        )
    ]]
    sol_box = Table(sol_box_data, colWidths=[504])
    sol_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_box),
        ('BOX', (0, 0), (-1, -1), 1, c_accent),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(sol_box)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 3. CORE FEATURES & MODULES
    # =========================================================================
    story.append(Paragraph("3. Core Features & Capabilities", h1_style))

    features_table_data = [
        [
            Paragraph("<b>Feature Module</b>", h2_style),
            Paragraph("<b>Technical Functionality & Impact</b>", h2_style)
        ],
        [
            Paragraph("<b>1. Automated Ingestion & Cloning</b>", body_style),
            Paragraph("Autonomous shallow/full cloning of any public Git/GitHub URL via GitPython with real-time percentage progress streaming.", body_style)
        ],
        [
            Paragraph("<b>2. Commit Analytics & Velocity</b>", body_style),
            Paragraph("Parses commit hashes, author metadata, messages, timestamps, files touched, additions (+), and deletions (-). Provides interactive search and date filtering.", body_style)
        ],
        [
            Paragraph("<b>3. File Churn & Inventory</b>", body_style),
            Paragraph("Catalogs all repository files, mapping commit frequency, lines of code (LOC), source lines of code (SLOC), and comments across active and deleted file states.", body_style)
        ],
        [
            Paragraph("<b>4. Radon Code Complexity</b>", body_style),
            Paragraph("Static AST parsing with Radon to measure McCabe Cyclomatic Complexity (CC) and grade Python modules from Rank A (low risk) to Rank F (extreme risk) without arbitrary execution.", body_style)
        ],
        [
            Paragraph("<b>5. Heuristic Bug-Fix Detection</b>", body_style),
            Paragraph("Identifies bug-fixing commits via targeted token heuristics (fix, bug, error, issue, hotfix) and flags them transparently with heuristic attribution.", body_style)
        ],
        [
            Paragraph("<b>6. Multi-Factor Code Hotspots</b>", body_style),
            Paragraph("Composite algorithm combining Change Frequency (40%), Bug Involvement (35%), and Radon Complexity (25%) into a 0–100 score with risk classification and actionable refactoring guidance.", body_style)
        ],
        [
            Paragraph("<b>7. Contributor Intelligence</b>", body_style),
            Paragraph("Computes developer commit rankings, distinct files touched, net code contributions, and commit share percentages to analyze knowledge distribution and bus factor.", body_style)
        ],
        [
            Paragraph("<b>8. Codebase Evolution Visuals</b>", body_style),
            Paragraph("High-contrast Plotly time-series charts for commit velocity, code churn dynamic (+/- lines), net LOC growth curves, bug-fix frequency, and active contributors over time.", body_style)
        ]
    ]

    ft_table = Table(features_table_data, colWidths=[160, 344])
    ft_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(ft_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 4. SYSTEM ARCHITECTURE & WORKING FLOW
    # =========================================================================
    story.append(Paragraph("4. System Architecture & Working Flow", h1_style))

    p4_arch = (
        "The architecture is engineered around a clean, layered pipeline separating external Git ingestion, "
        "static metric computation, relational persistence, and presentation:"
    )
    story.append(Paragraph(p4_arch, body_style))

    arch_steps = [
        [
            Paragraph("<b>Layer</b>", h2_style),
            Paragraph("<b>Component & Execution Responsibility</b>", h2_style)
        ],
        [
            Paragraph("<b>Presentation Layer</b>", body_style),
            Paragraph("<b>Streamlit (Multi-page):</b> Renders 6 analytical views (Overview, Commits, Files, Hotspots, Contributors, Evolution) and interactive Plotly charts styled with high contrast.", body_style)
        ],
        [
            Paragraph("<b>Orchestration Layer</b>", body_style),
            Paragraph("<b>analysis.py:</b> Coordinates pipeline steps, validates URLs, initiates clone jobs, computes hotspot scores, and structures Pandas DataFrames for dashboard consumption.", body_style)
        ],
        [
            Paragraph("<b>Git Ingestion Layer</b>", body_style),
            Paragraph("<b>git_analyzer.py:</b> Interacts with local/remote repos via GitPython. Extracts commit logs, file modification diff stats, developer identities, and HEAD tree blobs.", body_style)
        ],
        [
            Paragraph("<b>Code Metrics Layer</b>", body_style),
            Paragraph("<b>metrics.py:</b> Analyzes Python ASTs via Radon for Cyclomatic Complexity and raw LOC/SLOC. Implements normalized multi-factor hotspot scoring formula.", body_style)
        ],
        [
            Paragraph("<b>Persistence Layer</b>", body_style),
            Paragraph("<b>database.py & models.py:</b> SQLAlchemy ORM connected to MySQL 8.0 via PyMySQL. Handles automated DB creation, pooled sessions, indexes, and cascading deletes.", body_style)
        ]
    ]
    arch_table = Table(arch_steps, colWidths=[140, 364])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>End-to-End Execution Flow:</b>", h2_style))
    story.append(Paragraph("<b>Step 1: URL Input & Validation:</b> The user inputs a public GitHub URL on the Streamlit sidebar. Regex normalizes the URL and extracts repository identity.", bullet_style))
    story.append(Paragraph("<b>Step 2: Autonomous Git Clone / Fetch:</b> GitPython clones the repo into a structured local directory (`./cloned_repos`), streaming percentage progress via a callback.", bullet_style))
    story.append(Paragraph("<b>Step 3: History & Diff Extraction:</b> The engine traverses commits on the active branch, extracting metadata, insertions, deletions, and touched file paths.", bullet_style))
    story.append(Paragraph("<b>Step 4: Radon Complexity Analysis:</b> Active Python files are statically parsed via Radon AST visitors, extracting McCabe Cyclomatic Complexity and rank (A–F).", bullet_style))
    story.append(Paragraph("<b>Step 5: Hotspot Calculation:</b> Each file is scored across normalized change frequency, bug involvement, and complexity.", bullet_style))
    story.append(Paragraph("<b>Step 6: MySQL Relational Persistence:</b> Data is atomically written across 6 relational tables using foreign keys, batch inserts, and cascaded relationships.", bullet_style))
    story.append(Paragraph("<b>Step 7: Dashboard Visualization:</b> Streamlit renders KPIs, search filters, and Plotly charts.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # 5. DATABASE SCHEMA DESIGN
    # =========================================================================
    story.append(Paragraph("5. Relational Database Schema (MySQL 8.0)", h1_style))
    p_schema = (
        "The system persists repository data in a strictly normalized relational schema with 6 tables, "
        "foreign key constraints, and performance indexes:"
    )
    story.append(Paragraph(p_schema, body_style))

    schema_data = [
        [
            Paragraph("<b>Table</b>", h2_style),
            Paragraph("<b>Primary Key & Foreign Keys</b>", h2_style),
            Paragraph("<b>Key Columns & Purpose</b>", h2_style)
        ],
        [
            Paragraph("<b>repositories</b>", body_style),
            Paragraph("PK: <code>id</code>", body_style),
            Paragraph("name, url, default_branch, cloned_path, total_commits, total_files, total_loc, analyzed_at.", body_style)
        ],
        [
            Paragraph("<b>developers</b>", body_style),
            Paragraph("PK: <code>id</code><br/>FK: <code>repository_id</code>", body_style),
            Paragraph("name, email, total_commits, total_lines_added, total_lines_deleted, first_commit_date, last_commit_date.", body_style)
        ],
        [
            Paragraph("<b>commits</b>", body_style),
            Paragraph("PK: <code>id</code><br/>FK: <code>repository_id</code>, <code>developer_id</code>", body_style),
            Paragraph("commit_hash, author_name, author_email, message, commit_date, files_changed, lines_added, lines_deleted, is_bug_fix.", body_style)
        ],
        [
            Paragraph("<b>files</b>", body_style),
            Paragraph("PK: <code>id</code><br/>FK: <code>repository_id</code>", body_style),
            Paragraph("file_path (<code>utf8mb4_bin</code>), file_name, file_extension, current_loc, change_count, lines_added, lines_deleted, bug_fix_count, is_active.", body_style)
        ],
        [
            Paragraph("<b>commit_files</b>", body_style),
            Paragraph("PK: <code>id</code><br/>FK: <code>commit_id</code>, <code>file_id</code>", body_style),
            Paragraph("Associative junction table storing change_type ('M', 'A', 'D'), lines_added, lines_deleted per commit-file touch.", body_style)
        ],
        [
            Paragraph("<b>file_metrics</b>", body_style),
            Paragraph("PK: <code>id</code><br/>FK: <code>file_id</code> (Unique)", body_style),
            Paragraph("loc, sloc, comments, cyclomatic_complexity, complexity_rank ('A'–'F'), hotspot_score, analyzed_at.", body_style)
        ]
    ]

    schema_table = Table(schema_data, colWidths=[90, 160, 254])
    schema_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(schema_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 6. TECHNOLOGY STACK & ARCHITECTURAL RATIONALE
    # =========================================================================
    story.append(Paragraph("6. Technology Stack & Justification", h1_style))

    tech_data = [
        [
            Paragraph("<b>Technology</b>", h2_style),
            Paragraph("<b>Role in System</b>", h2_style),
            Paragraph("<b>Why Chosen Over Alternatives</b>", h2_style)
        ],
        [
            Paragraph("<b>Python 3.12</b>", body_style),
            Paragraph("Core programming language", body_style),
            Paragraph("Rich static analysis ecosystem (AST parsing, Git bindings, data science libraries).", body_style)
        ],
        [
            Paragraph("<b>Streamlit</b>", body_style),
            Paragraph("User interface & dashboard", body_style),
            Paragraph("Rapid interactive multi-page web applications in pure Python without heavy JS frontend overhead.", body_style)
        ],
        [
            Paragraph("<b>MySQL 8.0 & SQLAlchemy</b>", body_style),
            Paragraph("Relational database & ORM", body_style),
            Paragraph("ACID compliance, strict relational constraints (cascading deletes), indexing, connection pooling, and structured querying.", body_style)
        ],
        [
            Paragraph("<b>GitPython</b>", body_style),
            Paragraph("Git repository interface", body_style),
            Paragraph("Direct object-level inspection of Git repositories, commit DAG traversal, tree blobs, and remote progress reporting.", body_style)
        ],
        [
            Paragraph("<b>Radon</b>", body_style),
            Paragraph("Static code complexity engine", body_style),
            Paragraph("Computes McCabe Cyclomatic Complexity by parsing Python ASTs statically—no code execution required.", body_style)
        ],
        [
            Paragraph("<b>Pandas</b>", body_style),
            Paragraph("Data manipulation & aggregation", body_style),
            Paragraph("Vectorized operations, rolling window calculations, and time-series resampling (daily, weekly, monthly).", body_style)
        ],
        [
            Paragraph("<b>Plotly</b>", body_style),
            Paragraph("Data visualization engine", body_style),
            Paragraph("Interactive, publication-quality SVG/WebGL charts (scatter, bars, pies, area curves) with dynamic tooltips.", body_style)
        ]
    ]

    tech_table = Table(tech_data, colWidths=[90, 150, 264])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_bg_light),
        ('BOX', (0, 0), (-1, -1), 0.5, c_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 12))

    # =========================================================================
    # 7. HOW TO EXPLAIN THE PROJECT IN AN INTERVIEW
    # =========================================================================
    story.append(Paragraph("7. How to Explain in a Technical Interview", h1_style))

    p_explain_intro = (
        "When explaining this project to an interviewer, project reviewer, or hiring manager, structure your "
        "response in tiers: start with a high-impact elevator pitch, follow with the architectural workflow, and "
        "then demonstrate mastery over the engineering trade-offs."
    )
    story.append(Paragraph(p_explain_intro, body_style))

    # 30-Second Elevator Pitch Box
    pitch_data = [[
        Paragraph(
            "<b>30-Second Elevator Pitch (Memorize This):</b><br/>"
            "\"I built the <b>Codebase Evolution Intelligence System</b>—a software engineering analytics platform "
            "using Python, MySQL, Streamlit, GitPython, Pandas, Plotly, and Radon. While Git tracks file versions, it doesn't "
            "tell teams which files are accumulating technical debt. My system clones any public repository, mines its commit history, "
            "computes static McCabe Cyclomatic Complexity using Radon, and uses a multi-factor Hotspot algorithm to pinpoint "
            "high-maintenance files that combine frequent edits, recurring bug fixes, and high complexity. All data is persisted in a "
            "relational MySQL schema and visualized through an interactive Streamlit dashboard.\"",
            body_style
        )
    ]]
    pitch_box = Table(pitch_data, colWidths=[504])
    pitch_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_box),
        ('BOX', (0, 0), (-1, -1), 1, c_secondary),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(pitch_box)
    story.append(Spacer(1, 10))

    # 2-Minute Structured Walkthrough
    story.append(Paragraph("<b>2-Minute Comprehensive Walkthrough Structure:</b>", h2_style))
    story.append(Paragraph("<b>1. Hook (Problem):</b> State that raw Git history contains critical patterns that are invisible without automated mining (e.g. churn, bug clustering, code complexity).", bullet_style))
    story.append(Paragraph("<b>2. Architectural Ingestion:</b> Explain that the system accepts a public GitHub URL, uses GitPython to clone it, and parses commit metadata, diff insertions, and deletions.", bullet_style))
    story.append(Paragraph("<b>3. Static Analysis with Radon:</b> Emphasize that you used Radon to parse Python Abstract Syntax Trees (ASTs) to compute McCabe Cyclomatic Complexity without executing arbitrary code.", bullet_style))
    story.append(Paragraph("<b>4. The Hotspot Formula:</b> Explain the multi-factor weighted formula (40% churn, 35% bug fixes, 25% complexity) to separate active configuration files from true architectural risks.", bullet_style))
    story.append(Paragraph("<b>5. Relational Persistence:</b> Describe the 6 MySQL tables, explaining why relational foreign keys and cascading deletes were critical for multi-repo analysis.", bullet_style))
    story.append(Paragraph("<b>6. Business Impact:</b> Conclude by showing how teams use this data for proactive refactoring, reviewing contributor distribution, and monitoring maintenance phases.", bullet_style))
    story.append(Spacer(1, 10))


    story.append(Paragraph("8. Top Interview Questions & Model Answers", h1_style))

    qa_list = [
        (
            "Q1: Why did you design the Code Hotspot score using three specific dimensions?",
            "\"A single metric gives misleading results. A file with high cyclomatic complexity is harmless if developers rarely modify it. Conversely, a file with frequent commits might simply be a documentation or changelog file. A genuine architectural hotspot occurs at the intersection of three factors: high change frequency (40%), frequent bug-fix involvement (35%), and high cyclomatic complexity (25%). By normalizing these metrics across the repository and computing a weighted score from 0 to 100, the system surfaces the files that represent genuine technical debt.\""
        ),
        (
            "Q2: Why did you label Bug-Fix Detection as a 'Heuristic'?",
            "\"In software engineering, commit message keyword detection (searching for words like 'fix', 'bug', 'error', 'hotfix') is an empirical heuristic, not a formal verification technique. Commit messages can have false positives (e.g., 'fixed styling indentation') or false negatives (e.g., 'address edge case in session cache'). Explicitly labeling this feature as a heuristic demonstrates professional software engineering rigor and realistic expectations about static data mining.\""
        ),
        (
            "Q3: How does Radon calculate Cyclomatic Complexity, and why is it safe?",
            "\"Radon computes McCabe Cyclomatic Complexity by statically parsing Python code into an Abstract Syntax Tree (AST) using Python's standard `ast` library. It counts linearly independent paths through the code by calculating decision points (if-statements, for-loops, while-loops, comprehensions, and boolean operations). Because it only inspects the AST grammar nodes without executing the code, it is completely secure and safe against malicious repository code.\""
        ),
        (
            "Q4: How did you solve the case-sensitivity collision issue in MySQL on Windows?",
            "\"In Git, file paths are strictly case-sensitive (e.g., `MANIFEST.in` vs `manifest.in` across commits). By default, MySQL collations like `utf8mb4_unicode_ci` are case-insensitive, which caused duplicate key violations on unique file path constraints. I resolved this by configuring `file_path VARCHAR(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL` on the files table. The binary collation enforces byte-for-byte exact matching, aligning MySQL directly with Git's case-sensitive DAG semantics.\""
        ),
        (
            "Q5: Why did you choose MySQL and SQLAlchemy over MongoDB or SQLite?",
            "\"Git repository history is deeply relational: a repository contains developers and commits; each commit modifies multiple files through a many-to-many relationship (`commit_files`); and files have associated `file_metrics`. A relational schema with foreign key constraints, indexes, and cascading deletes ensures referential integrity. When a repository is deleted or re-analyzed, cascading deletes automatically clean up all associated commits and file metrics. SQLAlchemy connection pooling also ensures connection reuse during high-volume operations.\""
        ),
        (
            "Q6: How does the system handle high-contrast charts across dark and light OS themes?",
            "\"Streamlit applications inherit the user's operating system theme (Light or Dark Mode). Default Plotly charts can cause text labels to wash out against background canvases. I engineered a dedicated styling module (`chart_theme.py`) with `apply_chart_theme()`. It enforces crisp white card canvases (`#ffffff`), explicit deep-slate typography (`#0f172a`), subtle gridlines (`#e2e8f0`), and vibrant color palettes (electric blue, emerald, crimson, amber). This guarantees high visibility regardless of system theme.\""
        ),
        (
            "Q7: What are the engineering limitations, and how would you scale this for enterprise use?",
            "\"Currently, the system clones repositories locally and analyzes commits up to a capped threshold (e.g. 2,500 commits). For enterprise scaling (e.g. repos with 100,000+ commits), I would: 1) Run cloning and parsing as distributed Celery/Redis background worker tasks, 2) Use shallow or blobless Git clones (`--filter=blob:none`) to fetch commit trees without downloading large binary histories, and 3) Implement multi-language complexity parsers (e.g. tree-sitter) for TypeScript, Go, and Java.\""
        )
    ]

    for q, a in qa_list:
        story.append(Paragraph(q, qa_q_style))
        story.append(Paragraph(a, qa_a_style))
        story.append(Spacer(1, 4))

    # =========================================================================
    # 9. SUMMARY & CONCLUSION
    # =========================================================================
    story.append(Spacer(1, 6))
    story.append(Paragraph("9. Key Takeaways for Technical Evaluators", h1_style))
    p_conclusion = (
        "The Codebase Evolution Intelligence System stands out in a technical portfolio because it goes far "
        "beyond simple CRUD operations. It demonstrates end-to-end full-stack engineering proficiency: "
        "low-level version control system inspection (GitPython), AST static code analysis (Radon), relational database design "
        "with connection pooling and cascading integrity (MySQL/SQLAlchemy), multi-dimensional data engineering (Pandas), "
        "and interactive data visualization (Streamlit/Plotly)."
    )
    story.append(Paragraph(p_conclusion, body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    return os.path.abspath(output_filename)


if __name__ == "__main__":
    pdf_path = create_project_pdf()
    print(f"PDF generated successfully at: {pdf_path}")
