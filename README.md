# PDF-JSON Task List Generator

Generate a styled PDF checklist for **Daily**, **Weekly**, or **Monthly** tasks from simple JSON files.  

---

## Table of Contents

- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [File Structure](#file-structure)  
- [Usage](#usage)  
- [JSON Format](#json-format)  
- [Script Overview](#script-overview)  
- [Glossary of Imports & Key Methods](#glossary-of-imports--key-methods)  
- [License](#license)  

---

## Prerequisites

- **Python 3.12+**  
- [pipenv](https://pipenv.pypa.io/) (or `pip` + `virtualenv`)  

---

## Installation

1. **Clone** this repository:
        ```bash
        git clone https://github.com/yourusername/pdf-json-task-list.git
        cd pdf-json-task-list
        ```

2. **Install** dependencies:

    ```bash
    pipenv install
    ```

    or, if you prefer `pip`:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install reportlab
    ```

---

## File Structure

```bash
.
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── example_daily_tasks.json
├── example_weekly_tasks.json
├── example_monthly_tasks.json
└── generate_tasks_list.py
```

* **example\_\*.json** — Your task definitions (one file per period).
* **generate\_tasks\_list.py** — CLI script that reads JSON → produces PDF.

---

## Usage

Run the generator with one argument: `day`, `week`, or `month`.

```bash
# Daily checklist
./generate_tasks_list.py day
# → generates Tasks_Daily.pdf

# Weekly checklist
./generate_tasks_list.py week
# → generates Tasks_Weekly.pdf

# Monthly checklist
./generate_tasks_list.py month
# → generates Tasks_Monthly.pdf
```

Your PDF will include:

* A centered title (`Daily Tasks` / `Weekly Tasks` / `Monthly Tasks`)
* Checkbox-style bullets
* The PDF’s absolute file path in the footer of each page

---

## JSON Format

Each **example\_\*.json** file is a JSON object whose keys are **categories** and whose values are **arrays of task strings**. Emojis in category names are allowed!

```json
{
    "🛏️ Personal Care": [
        "Make your bed",
        "Brush teeth & floss",
        "Shower or wash face"
    ],
        "💻 Digital Organization": [
        "Zero-inbox: clear/archive/respond to new emails",
        "Review notifications (Slack, Teams, etc.)"
        ]
}
```

---

## Script Overview

**generate\_tasks\_list.py** performs the following steps:

1. **Parse** the CLI argument (`day`/`week`/`month`).
2. **Select** the matching JSON input file, PDF output filename, and title text.
3. **Load** the JSON tasks into memory.
4. **Register** the DejaVuSans font so both checkboxes and Unicode file-paths render correctly.
5. **Define** paragraph styles for title, categories, and task items (with checkbox bullets).
6. **Build** a list of “flowables” (ReportLab objects):

    * Title paragraph
    * Category headings + task paragraphs
    * Spacers for vertical gaps
7. **Strip** any trailing spacer to avoid a blank final page.
8. **Render** the PDF via `doc.build(...)`, passing a footer callback that stamps the file’s absolute path on each page.

---

## Glossary of Imports & Key Methods

### Imports

| Import                                     | Purpose                                                     |
| ------------------------------------------ | ----------------------------------------------------------- |
| `os`                                       | File-system utilities (e.g. `os.path.abspath`).             |
| `json`                                     | Load & parse the JSON task files.                           |
| `argparse`                                 | Parse the `day`/`week`/`month` CLI argument.                |
| `reportlab.lib.pagesizes.letter`           | Standard US Letter page size.                               |
| `reportlab.lib.units.inch`                 | Inch-to-points conversion for positioning.                  |
| `reportlab.pdfbase.pdfmetrics`             | ReportLab font registry API.                                |
| `reportlab.pdfbase.ttfonts.TTFont`         | Load & register TrueType fonts (DejaVuSans).                |
| `reportlab.platypus.SimpleDocTemplate`     | High-level PDF builder that takes a list of “flowables.”    |
| `reportlab.platypus.Paragraph`             | Styled text blocks, with optional bullets.                  |
| `reportlab.platypus.Spacer`                | Blank vertical space to separate sections.                  |
| `reportlab.lib.styles.getSampleStyleSheet` | Provides base styles (`Title`, `Heading2`, `Normal`).       |
| `reportlab.lib.styles.ParagraphStyle`      | Customize fonts, sizes, alignment, spacing for `Paragraph`. |

### Key Methods & Commands

| Method / Command                                          | Description                                                                          |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `pdfmetrics.registerFont(TTFont(...))`                    | Registers a TTF font so ReportLab can render Unicode (checkboxes & file paths).      |
| `_draw_footer(canvas, doc, path)`                         | Callback that draws the PDF’s absolute path in 8 pt DejaVuSans at the bottom margin. |
| `Paragraph(text, style, bulletText=SQUARE_BULLET)`        | Creates a text block; `bulletText` injects the checkbox glyph before each task line. |
| `Spacer(width, height)`                                   | Inserts vertical space (in points).                                                  |
| `if story and isinstance(story[-1], Spacer): story.pop()` | Removes a trailing spacer to prevent a blank last page.                              |
| `doc.build(flowables, onFirstPage=…, onLaterPages=…)`     | Renders all flowables into a PDF, calling the footer callback on every page.         |

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

- [Table of Contents](#table-of-contents)
