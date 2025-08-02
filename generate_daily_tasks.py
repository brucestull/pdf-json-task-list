#!/usr/bin/env python3
# generate_daily_tasks.py
import os
import json

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate

# ─────────────────────────────────────────────────────────────────────────────
FILE_NAME = "Daily_Tasks.pdf"
JSON_INPUT_FILE = "example_daily_tasks.json"
PAGE_TITLE = "Daily Tasks"
SQUARE_BULLET = "\u2610"

# register a Unicode font for checkbox & filepath
pdfmetrics.registerFont(
    TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
)


def _draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DejaVuSans", 8)
    path = os.path.abspath(FILE_NAME)
    x = doc.leftMargin
    y = 0.5 * inch
    canvas.drawString(x, y, path)
    canvas.restoreState()


def main():
    # load tasks
    with open(JSON_INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # set up the PDF
    doc = SimpleDocTemplate(
        FILE_NAME,
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    # styles
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
        name="Category", parent=styles["Heading2"], spaceAfter=6
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

    # build the story
    story = [Paragraph(PAGE_TITLE, title_style)]
    for category, tasks in data.items():
        story.append(Paragraph(category, category_style))
        for task in tasks:
            story.append(Paragraph(task, task_style, bulletText=SQUARE_BULLET))
        story.append(Spacer(1, 12))

    # remove the final spacer so no blank page
    if story and isinstance(story[-1], Spacer):
        story.pop()

    # generate PDF with footer callbacks
    doc.build(story, onFirstPage=_draw_footer, onLaterPages=_draw_footer)

    print(f"✅ PDF generated: {FILE_NAME}")


if __name__ == "__main__":
    main()
