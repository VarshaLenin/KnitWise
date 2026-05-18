from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_pattern_pdf(file_path: str, data: dict, meta: dict) -> bool:
    try:
        doc = SimpleDocTemplate(
            file_path, 
            pagesize=letter,
            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
        )
        story = []
        
        styles = getSampleStyleSheet()
        
        # Custom Accent Styling Definitions
        title_style = ParagraphStyle(
            'DocTitle', parent=styles['Heading1'], fontSize=24, leading=28, 
            textColor=colors.HexColor("#2C3E50"), spaceAfter=15
        )
        section_style = ParagraphStyle(
            'SecTitle', parent=styles['Heading2'], fontSize=14, leading=18, 
            textColor=colors.HexColor("#16A085"), spaceBefore=12, spaceAfter=6
        )
        body_style = ParagraphStyle(
            'Body', parent=styles['Normal'], fontSize=10, leading=14, 
            textColor=colors.HexColor("#34495E")
        )
        warn_style = ParagraphStyle(
            'Warning', parent=styles['Normal'], fontSize=10, leading=14, 
            textColor=colors.HexColor("#C0392B"), backColor=colors.HexColor("#FADBD8"),
            borderPadding=8, spaceBefore=10, spaceAfter=10
        )

        # 1. Header Frame
        story.append(Paragraph("🧶 AI Generated Crochet Pattern", title_style))
        story.append(Spacer(1, 10))
        
        # 2. Quality Alert Flagging
        if data.get("image_quality") == "low" or data.get("warning"):
            warn_text = f"<b>⚠️ ALERT:</b> {data.get('warning', 'Low image structural feedback data resolved. Approximation engine rendering standard blocks.')}"
            story.append(Paragraph(warn_text, warn_style))
            story.append(Spacer(1, 5))

        # 3. Dynamic Metadata Properties Table Layout
        meta_data = [
            [Paragraph("<b>Target Type:</b>", body_style), Paragraph(meta['item_type'].capitalize(), body_style),
             Paragraph("<b>Estimated Difficulty:</b>", body_style), Paragraph(data.get('difficulty', 'N/A').capitalize(), body_style)],
            [Paragraph("<b>Yarn Metric:</b>", body_style), Paragraph(meta['yarn_size'], body_style),
             Paragraph("<b>Hook Dimension:</b>", body_style), Paragraph(meta['hook_size'], body_style)]
        ]
        t = Table(meta_data, colWidths=[100, 160, 120, 150])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9F9")),
            ('PADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#BDC3C7")),
        ]))
        story.append(t)
        story.append(Spacer(1, 15))

        # 4. Summary Frame
        story.append(Paragraph("Pattern Summary", section_style))
        story.append(Paragraph(data.get("summary", "No structural overview provided."), body_style))
        story.append(Spacer(1, 10))

        # 5. Detected Motif Blocks
        motifs = data.get("motifs", [])
        if motifs:
            story.append(Paragraph("Identified Motifs & Features", section_style))
            story.append(Paragraph(", ".join(motifs), body_style))
            story.append(Spacer(1, 10))

       # 6. Primary Stitch Script Instructions Loop
        story.append(Paragraph("Stitch Instructions", section_style))
        stitch_pattern = data.get("stitch_pattern", {})
        
        # Safely extract the rounds list layer
        rounds = []
        if isinstance(stitch_pattern, dict):
            rounds = stitch_pattern.get("rounds", [])
        elif isinstance(stitch_pattern, list):
            rounds = stitch_pattern

        if rounds and isinstance(rounds, list):
            for step in rounds:
                # SAFE CHECK: Convert step to string if the API sent it as a dict/object
                if isinstance(step, dict):
                    # Fallback to extract text from common keys, or drop to raw string dump
                    step_str = step.get("instruction") or step.get("text") or step.get("step") or str(step)
                else:
                    step_str = str(step)

                # Now it's safe to run string methods like .lower()
                step_text = f"<b>• {step_str}</b>" if not step_str.lower().startswith("round") else f"<b>{step_str}</b>"
                story.append(Paragraph(step_text, body_style))
                story.append(Spacer(1, 4))
        else:
            story.append(Paragraph("No explicit directional layers discovered.", body_style))
        story.append(Spacer(1, 10))

        # 7. Color Allocation Strategy Guide
        colors_list = data.get("color_changes", [])
        if colors_list:
            story.append(Paragraph("Color Guide & Chronology", section_style))
            for item in colors_list:
                story.append(Paragraph(f"• {item}", body_style))
                story.append(Spacer(1, 3))
            story.append(Spacer(1, 10))

        # 8. Structural Appendix Notes
        notes = data.get("notes")
        if notes:
            story.append(Paragraph("Designer Construction Notes", section_style))
            story.append(Paragraph(notes, body_style))

        # Document compilation action
        doc.build(story)
        return True
    except Exception as e:
        print(f"PDF Compiler Error: {e}")
        return False