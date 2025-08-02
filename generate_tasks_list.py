#!/usr/bin/env python3
# generate_tasks_list.py

import os
import json
import argparse

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate

# ─────────────────────────────────────────────────────────────────────────────
# Unicode checkbox character
SQUARE_BULLET = "\u2610"

# register DejaVuSans for Unicode checkboxes & filepath
pdfmetrics.registerFont(
    TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
)


def _draw_footer(canvas, doc, output_path):
    canvas.saveState()
    canvas.setFont("DejaVuSans", 8)
    x = doc.leftMargin
    y = 0.5 * inch
    canvas.drawString(x, y, output_path)
    canvas.restoreState()


def main():
    # --- parse CLI ---
    parser = argparse.ArgumentParser(
        description="Generate a PDF task list (daily, weekly, or monthly) from JSON."  # noqa: E501
    )
    parser.add_argument(
        "period",
        choices=["day", "week", "month"],
        help='Use "day" for Daily, "week" for Weekly, or "month" for Monthly Tasks',  # noqa: E501
    )
    args = parser.parse_args()

    # --- pick JSON, PDF name & title ---
    if args.period == "day":
        json_file = "example_daily_tasks.json"
        output_pdf = "Tasks_Daily.pdf"
        title_text = "Daily Tasks"
    elif args.period == "week":
        json_file = "example_weekly_tasks.json"
        output_pdf = "Tasks_Weekly.pdf"
        title_text = "Weekly Tasks"
    else:  # month
        json_file = "example_monthly_tasks.json"
        output_pdf = "Tasks_Monthly.pdf"
        title_text = "Monthly Tasks"

    print(
        f"➡️ Generating {title_text} PDF from `{json_file}` → `{output_pdf}`"  # noqa: E501
    )

    # --- load tasks from JSON ---
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ JSON file not found: {json_file}")
        return

    # --- set up PDF document ---
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    # --- define styles ---
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="Title",
        parent=styles["Title"],
        fontName="DejaVuSans",
        fontSize=28,
        leading=32,
        alignment=1,  # center
        spaceAfter=24,
    )
    category_style = ParagraphStyle(
        name="Category",
        parent=styles["Heading2"],
        spaceAfter=6,
    )
    task_style = ParagraphStyle(
        name="Task",
        parent=styles["Normal"],
        leftIndent=12,
        bulletIndent=0,
        bulletFontName="DejaVuSans",
        bulletFontSize=13,
        spaceAfter=2,
    )

    # --- build the flowables ---
    story = [Paragraph(title_text, title_style)]
    for category, tasks in data.items():
        story.append(Paragraph(category, category_style))
        for task in tasks:
            story.append(Paragraph(task, task_style, bulletText=SQUARE_BULLET))
        story.append(Spacer(1, 12))

    # remove trailing spacer to avoid a blank last page
    if story and isinstance(story[-1], Spacer):
        story.pop()

    # --- generate PDF with footer ---
    abs_path = os.path.abspath(output_pdf)

    def footer_fn(c, d):
        _draw_footer(c, d, abs_path)

    doc.build(story, onFirstPage=footer_fn, onLaterPages=footer_fn)

    print(f"✅ PDF generated: {output_pdf}")


if __name__ == "__main__":
    main()
