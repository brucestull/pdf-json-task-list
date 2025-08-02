# PDF-JSON Task List Generator

Generate a styled PDF “Daily Tasks” checklist from a simple JSON file.  
This repo currently supports a **daily** tasks list; future updates will add weekly and monthly lists.

---

## Table of Contents

- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [File Structure](#file-structure)  
- [Usage](#usage)  
- [daily_tasks.json Format](#daily_tasksjson-format)  
- [Script Overview](#script-overview)  
- [Glossary of Imports & Key Methods](#glossary-of-imports--key-methods)  
- [License](#license)  

---

## Prerequisites

- Python 3.7+  
- [pipenv](https://pipenv.pypa.io/) (or use `pip` + virtualenv)  

---

## Installation

1. Clone this repo:
    ```bash
    git clone https://github.com/yourusername/pdf-json-task-list.git
    cd pdf-json-task-list
    ```

2. Install dependencies with pipenv:

    ```bash
    pipenv install
    ```

    Or with plain pip:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

---

## File Structure

```bash
.
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── daily_tasks.json       # Your task categories & items
└── generate_daily_tasks.py  # Script to build the PDF
```

---

## Usage

1. Edit **daily\_tasks.json** to tweak categories or tasks.
2. Run the generator:

    ```bash
    pipenv run python generate_daily_tasks.py
    ```
3. The script produces **Tinys\_Daily\_Tasks.pdf** in the same folder, with:

    * A centered title
    * Checkbox-style bullets
    * Your full file path in the footer of each page

---

## daily\_tasks.json Format

A simple object where each key is a category (emoji OK!) and each value is an array of task strings. Example:

```json
{
    "🛏️ Personal Care": [
        "Make your bed",
        "Brush teeth & floss",
        "Shower or wash face"
    ],
    "🥗 Nutrition & Health": [
        "Drink a full glass of water",
        "Prepare balanced meals"
    ]
}
```

---

## Script Overview

**generate\_daily\_tasks.py** does the following:

1. **Loads** `daily_tasks.json`.
2. **Registers** a Unicode font (`DejaVuSans`) so that checkboxes and file paths render correctly.
3. Defines `_draw_footer()`, which ReportLab calls on each page to stamp the absolute PDF path in the bottom margin.
4. Builds a list of **flowables**:
    * A large, centered title
    * For each category: a heading + checkbox-style `Paragraph` items
    * Spacers for vertical gaps
5. **Removes** any trailing spacer (to avoid a blank “third” page).
6. Calls `doc.build(...)` with `onFirstPage` and `onLaterPages` pointing to `_draw_footer`, generating the final PDF.

---

## Glossary of Imports & Key Methods

### Imports

| Import                                     | Purpose                                                                     |
| ------------------------------------------ | --------------------------------------------------------------------------- |
| `os`                                       | File-system utilities; used to compute `os.path.abspath(FILE_NAME)`.        |
| `json`                                     | Parse the JSON tasks file.                                                  |
| `reportlab.lib.pagesizes.letter`           | Standard US letter page size.                                               |
| `reportlab.lib.units.inch`                 | Converts inches to points for positioning.                                  |
| `reportlab.pdfbase.pdfmetrics`             | ReportLab’s font registry API.                                              |
| `reportlab.pdfbase.ttfonts.TTFont`         | Load and register TrueType fonts (e.g. DejaVuSans).                         |
| `reportlab.platypus.SimpleDocTemplate`     | High-level PDF builder taking a list of “flowables.”                        |
| `reportlab.platypus.Paragraph`             | Text block element with styling and optional bullet.                        |
| `reportlab.platypus.Spacer`                | Vertical blank space between flowables.                                     |
| `reportlab.lib.styles.getSampleStyleSheet` | Provides a collection of base styles (`Title`, `Heading2`, `Normal`, etc.). |
| `reportlab.lib.styles.ParagraphStyle`      | Customize fonts, sizes, alignment, spacing for `Paragraph`.                 |

### Key Methods & Commands

| Method / Command                                                        | What It Does                                                                                  |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `pdfmetrics.registerFont(TTFont(...))`                                  | Makes the specified TTF font available for drawing text and bullets in the PDF.               |
| `_draw_footer(canvas, doc)`                                             | Called on each page to draw `os.path.abspath(FILE_NAME)` in 8 pt DejaVuSans at bottom margin. |
| `Paragraph(text, style, bulletText=…)`                                  | Creates a rich text element; `bulletText` renders the checkbox character before the text.     |
| `Spacer(width, height)`                                                 | Inserts vertical space; helps control page layout.                                            |
| `if story and isinstance(story[-1], Spacer): story.pop()`               | Removes any trailing spacer to prevent an extra blank page.                                   |
| `doc.build(story, onFirstPage=_draw_footer, onLaterPages=_draw_footer)` | Renders all flowables to PDF, invoking the footer callback on every page.                     |

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

- [Table of Contents](#table-of-contents)
