import io
import logging

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_INSTALLED = True
except (ImportError, OSError):
    WEASYPRINT_INSTALLED = False

logger = logging.getLogger('ats_resume_scorer')

def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    if not WEASYPRINT_INSTALLED:
        raise ImportError("WeasyPrint is not installed. PDF generation unavailable.")
        
    documents = []
    
    # Render all 3 HTML strings to WeasyPrint Document objects
    for name, html_str in html_docs.items():
        doc = HTML(string=html_str).render()
        documents.append(doc)
    
    # Merge them into the first document
    first_doc = documents[0]
    for other_doc in documents[1:]:
        for page in other_doc.pages:
            first_doc.pages.append(page)
            
    # Write combined PDF bytes
    pdf_bytes = first_doc.write_pdf()
    return pdf_bytes

def generate_fpdf_report(analysis_data: dict) -> bytes:
    from fpdf import FPDF
    from datetime import datetime
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Font settings
    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(31, 41, 55) # #1F2937
    pdf.cell(0, 15, "ATS Resume Analysis Report", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("helvetica", "I", 10)
    pdf.set_text_color(107, 114, 128) # #6B7280
    date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    pdf.cell(0, 5, f"Report Generated: {date_str}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)
    
    # Executive Summary Card
    score = float(analysis_data.get("ATS_score", analysis_data.get("ats_score", 0)))
    interpretation = analysis_data.get("interpretation", "")
    
    # Draw a colored card background
    # Colors based on score
    if score >= 80:
        bg_r, bg_g, bg_b = 232, 245, 233 # light green
        text_r, text_g, text_b = 46, 125, 50 # dark green
    elif score >= 60:
        bg_r, bg_g, bg_b = 255, 243, 224 # light orange
        text_r, text_g, text_b = 245, 124, 0 # dark orange
    else:
        bg_r, bg_g, bg_b = 255, 235, 238 # light red
        text_r, text_g, text_b = 198, 40, 40 # dark red
        
    pdf.set_fill_color(bg_r, bg_g, bg_b)
    pdf.rect(10, pdf.get_y(), 190, 35, "F")
    
    # Score Text
    pdf.set_y(pdf.get_y() + 5)
    pdf.set_x(15)
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(0, 6, "Overall ATS Score", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_x(15)
    pdf.set_font("helvetica", "B", 24)
    pdf.set_text_color(text_r, text_g, text_b)
    pdf.cell(0, 10, f"{score:.0f} / 100", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_x(15)
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(0, 6, interpretation, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)
    
    # Section: Score Breakdown
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(31, 41, 55)
    pdf.cell(0, 8, "Score Breakdown", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(229, 231, 235)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    cs = analysis_data.get("component_scores", {})
    if hasattr(cs, "__dict__"):
        cs = cs.__dict__
        
    components = [
        ("Formatting", cs.get("formatting", 0), 20),
        ("Keywords & Skills", cs.get("keywords", 0), 25),
        ("Content Quality", cs.get("content", 0), 25),
        ("Skill Validation", cs.get("skill_validation", 0), 15),
        ("ATS Compatibility", cs.get("ats_compatibility", 0), 15),
    ]
    
    pdf.set_font("helvetica", "B", 10)
    pdf.set_text_color(55, 65, 81)
    pdf.cell(90, 8, "Component", border="B")
    pdf.cell(50, 8, "Score Obtained", border="B", align="C")
    pdf.cell(50, 8, "Maximum Score", border="B", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    for label, val, max_val in components:
        pdf.cell(90, 8, label, border="B")
        pdf.cell(50, 8, f"{float(val):.0f}", border="B", align="C")
        pdf.cell(50, 8, f"{max_val}", border="B", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Section: Strengths
    strengths = analysis_data.get("strengths", [])
    if strengths:
        pdf.set_font("helvetica", "B", 14)
        pdf.set_text_color(31, 41, 55)
        pdf.cell(0, 8, "Strengths", new_x="LMARGIN", new_y="NEXT")
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(75, 85, 99)
        for s in strengths:
            pdf.multi_cell(0, 6, f"- {s}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(8)
        
    # Section: Critical Issues
    critical = analysis_data.get("critical_issues") or []
    issues_summary = analysis_data.get("issues_summary") or []
    all_issues = list(set(list(critical) + list(issues_summary)))
    
    if all_issues:
        pdf.set_font("helvetica", "B", 14)
        pdf.set_text_color(198, 40, 40) # red for critical issues
        pdf.cell(0, 8, "Critical Issues to Address", new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(248, 113, 113)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(75, 85, 99)
        for issue in all_issues:
            pdf.multi_cell(0, 6, f"- {issue}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(8)
        
    # Section: Detailed Feedback
    feedback = analysis_data.get("detailed_feedback", [])
    if feedback:
        pdf.set_font("helvetica", "B", 14)
        pdf.set_text_color(31, 41, 55)
        pdf.cell(0, 8, "Detailed Feedback & Suggestions", new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(229, 231, 235)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        
        # Sort feedback by severity if possible
        severity_rank = {"critical": 0, "high": 1, "medium": 2, "moderate": 2, "low": 3}
        try:
            sorted_feedback = sorted(feedback, key=lambda x: severity_rank.get(x.get("severity_level", "low").lower(), 99))
        except Exception:
            sorted_feedback = feedback
            
        for fb in sorted_feedback:
            # Check for page break if drawing detailed feedback
            if pdf.get_y() > 240:
                pdf.add_page()
                
            title = fb.get("issue_title", "Issue")
            severity = fb.get("severity_level", "info").upper()
            impact = fb.get("ats_impact", "")
            explanation = fb.get("explanation", "")
            how_to_fix = fb.get("how_to_fix", "")
            
            # Severity color styling
            if severity in ("CRITICAL", "HIGH"):
                sev_r, sev_g, sev_b = 198, 40, 40
            elif severity in ("MEDIUM", "MODERATE"):
                sev_r, sev_g, sev_b = 245, 124, 0
            else:
                sev_r, sev_g, sev_b = 46, 125, 50
                
            pdf.set_font("helvetica", "B", 11)
            pdf.set_text_color(sev_r, sev_g, sev_b)
            pdf.cell(140, 6, f"{title}")
            
            pdf.set_font("helvetica", "B", 9)
            pdf.cell(50, 6, f"[{severity}]", align="R", new_x="LMARGIN", new_y="NEXT")
            
            pdf.set_font("helvetica", "I", 9)
            pdf.set_text_color(107, 114, 128)
            if impact:
                pdf.cell(0, 5, f"Impact: {impact}", new_x="LMARGIN", new_y="NEXT")
                
            pdf.set_font("helvetica", "", 10)
            pdf.set_text_color(75, 85, 99)
            if explanation:
                pdf.multi_cell(0, 5, f"What's happening: {explanation}", new_x="LMARGIN", new_y="NEXT")
            if how_to_fix:
                pdf.multi_cell(0, 5, f"How to fix: {how_to_fix}", new_x="LMARGIN", new_y="NEXT")
                
            action_items = fb.get("action_items") or []
            if action_items:
                pdf.set_font("helvetica", "B", 9)
                pdf.cell(0, 5, "Action Items:", new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("helvetica", "", 10)
                for item in action_items:
                    pdf.multi_cell(0, 5, f"  - {item}", new_x="LMARGIN", new_y="NEXT")
                    
            example = fb.get("example_improvement", "")
            if example:
                pdf.set_font("helvetica", "B", 9)
                pdf.cell(0, 5, "Example Improvement:", new_x="LMARGIN", new_y="NEXT")
                pdf.set_font("courier", "", 9)
                pdf.set_fill_color(249, 250, 251)
                pdf.multi_cell(0, 5, example, border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
                
            pdf.ln(5)
            
    # Section: Job Description Comparison
    jd_comparison = analysis_data.get("jd_comparison") or analysis_data.get("jd_match_analysis")
    if jd_comparison:
        if hasattr(jd_comparison, "__dict__"):
            jd_comparison = jd_comparison.__dict__
            
        if pdf.get_y() > 220:
            pdf.add_page()
            
        pdf.set_font("helvetica", "B", 14)
        pdf.set_text_color(31, 41, 55)
        pdf.cell(0, 8, "Job Description Match Analysis", new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(229, 231, 235)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        
        match_pct = float(jd_comparison.get("match_percentage", 0))
        semantic = float(jd_comparison.get("semantic_similarity", 0))
        matched = jd_comparison.get("matched_keywords", []) or []
        missing = jd_comparison.get("missing_keywords", []) or []
        gap = jd_comparison.get("skills_gap", []) or []
        
        pdf.set_font("helvetica", "B", 10)
        pdf.set_text_color(55, 65, 81)
        pdf.cell(95, 6, f"Match Percentage: {match_pct:.0f}%")
        pdf.cell(95, 6, f"Semantic Similarity: {semantic * 100:.0f}%", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(0, 6, "Matched Keywords:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(75, 85, 99)
        pdf.multi_cell(0, 5, ", ".join(matched[:20]) if matched else "None", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        
        pdf.set_font("helvetica", "B", 10)
        pdf.set_text_color(198, 40, 40)
        pdf.cell(0, 6, "Missing Keywords:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(75, 85, 99)
        pdf.multi_cell(0, 5, ", ".join(missing[:15]) if missing else "None", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        
        pdf.set_font("helvetica", "B", 10)
        pdf.set_text_color(55, 65, 81)
        pdf.cell(0, 6, "Skills Gap:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(75, 85, 99)
        pdf.multi_cell(0, 5, ", ".join(gap[:10]) if gap else "None", new_x="LMARGIN", new_y="NEXT")
        
    return bytes(pdf.output())
