from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib import colors


def create_pattern_pdf(file_path: str, data: dict, meta: dict) -> bool:

    try:

        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        story = []

        styles = getSampleStyleSheet()

        # =========================
        # Custom Styles
        # =========================

        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#2C3E50"),
            spaceAfter=15
        )

        section_style = ParagraphStyle(
            'SecTitle',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#16A085"),
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#34495E")
        )

        warn_style = ParagraphStyle(
            'Warning',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#C0392B"),
            backColor=colors.HexColor("#FADBD8"),
            borderPadding=8,
            spaceBefore=10,
            spaceAfter=10
        )

        # =========================
        # Title
        # =========================

        story.append(
            Paragraph(
                "🧶 AI Generated Crochet Pattern",
                title_style
            )
        )

        story.append(Spacer(1, 10))

        # =========================
        # Warning Banner
        # =========================

        if data.get("image_quality") == "low" or data.get("warning"):

            warn_text = (
                f"<b>⚠️ ALERT:</b> "
                f"{data.get('warning', 'Low image clarity detected.')}"
            )

            story.append(
                Paragraph(warn_text, warn_style)
            )

            story.append(Spacer(1, 5))

        # =========================
        # Metadata Table
        # =========================

        meta_data = [
            [
                Paragraph("<b>Target Type:</b>", body_style),
                Paragraph(meta['item_type'].capitalize(), body_style),

                Paragraph("<b>Difficulty:</b>", body_style),
                Paragraph(data.get('difficulty', 'N/A').capitalize(), body_style)
            ],
            [
                Paragraph("<b>Yarn:</b>", body_style),
                Paragraph(meta['yarn_size'], body_style),

                Paragraph("<b>Hook Size:</b>", body_style),
                Paragraph(meta['hook_size'], body_style)
            ]
        ]

        table = Table(
            meta_data,
            colWidths=[100, 160, 120, 150]
        )

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8F9F9")),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#BDC3C7")),
        ]))

        story.append(table)

        story.append(Spacer(1, 15))

        # =========================
        # Summary
        # =========================

        story.append(
            Paragraph("Pattern Summary", section_style)
        )

        story.append(
            Paragraph(
                data.get(
                    "summary",
                    "No summary available."
                ),
                body_style
            )
        )

        story.append(Spacer(1, 10))

        # =========================
        # Motifs
        # =========================

        motifs = data.get("motifs", [])

        if motifs:

            story.append(
                Paragraph(
                    "Identified Motifs & Features",
                    section_style
                )
            )

            story.append(
                Paragraph(", ".join(motifs), body_style)
            )

            story.append(Spacer(1, 10))

        # =========================
        # Instructions
        # =========================

        story.append(
            Paragraph(
                "Stitch Instructions",
                section_style
            )
        )

        stitch_pattern = data.get("stitch_pattern", {})

        rounds = []

        if isinstance(stitch_pattern, dict):
            rounds = stitch_pattern.get("rounds", [])

        elif isinstance(stitch_pattern, list):
            rounds = stitch_pattern

        shape_type = data.get(
            "detected_shape",
            ""
        ).lower()

        step_label = (
            "Row"
            if shape_type == "rows"
            else "Round"
        )

        if rounds and isinstance(rounds, list):

            for step in rounds:

                if isinstance(step, dict):

                    round_num = step.get(
                        "round_number",
                        ""
                    )

                    instructions = step.get(
                        "instructions",
                        ""
                    )

                    total_stitches = step.get(
                        "total_stitches",
                        ""
                    )

                    stitches_per_side = step.get(
                        "stitches_per_side",
                        ""
                    )

                    step_text = (
                        f"<b>{step_label} "
                        f"{round_num}:</b> "
                        f"{instructions}"
                    )

                    if (
                        stitches_per_side
                        and stitches_per_side > 0
                    ):

                        step_text += (
                            f"<br/><font color='#7F8C8D'>"
                            f"Stitches Per Side: "
                            f"{stitches_per_side}"
                            f"</font>"
                        )

                    if total_stitches:

                        step_text += (
                            f"<br/><font color='#16A085'>"
                            f"<b>Total Stitches:</b> "
                            f"{total_stitches}"
                            f"</font>"
                        )

                else:
                    step_text = str(step)

                story.append(
                    Paragraph(step_text, body_style)
                )

                story.append(Spacer(1, 8))

        else:

            story.append(
                Paragraph(
                    "No stitch instructions generated.",
                    body_style
                )
            )

        story.append(Spacer(1, 10))

        # =========================
        # Color Changes
        # =========================

        colors_list = data.get("color_changes", [])

        if colors_list:

            story.append(
                Paragraph(
                    "Color Guide & Chronology",
                    section_style
                )
            )

            for item in colors_list:

                story.append(
                    Paragraph(
                        f"• {item}",
                        body_style
                    )
                )

                story.append(Spacer(1, 3))

            story.append(Spacer(1, 10))

        # =========================
        # Notes
        # =========================

        notes = data.get("notes")

        if notes:

            story.append(
                Paragraph(
                    "Designer Construction Notes",
                    section_style
                )
            )

            story.append(
                Paragraph(notes, body_style)
            )

        # =========================
        # Build PDF
        # =========================

        doc.build(story)

        return True

    except Exception as e:

        print(f"PDF Compiler Error: {e}")

        return False
