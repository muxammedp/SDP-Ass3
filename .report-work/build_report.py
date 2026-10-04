from pathlib import Path
import sys
from html import escape

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".report-work" / "python"))

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Preformatted
from reportlab.lib.utils import ImageReader

NAVY = colors.HexColor("#173B56")
TEAL = colors.HexColor("#117B83")
INK = colors.HexColor("#253B49")
MUTED = colors.HexColor("#526776")
PALE = colors.HexColor("#F0F5F8")
BASE = "423467d70f88646b802b9eb139b2db4efc1c2ec2"
EXTENSION = "be88bfaeeb7be8418ab0b2cd7ef11996e0e0555a"
BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14, textColor=INK)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8.5, leading=11)
CODE = ParagraphStyle("code", fontName="Courier", fontSize=8.2, leading=10.7, textColor=INK)


def paragraph(text, x, top, width, style=BODY):
    item = Paragraph(text, style)
    _, height = item.wrap(width, 1000)
    item.drawOn(pdf, x, top - height)
    return top - height - 8


def heading(text, top, x=42):
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x, top - 12, text)
    return top - 22


def codebox(text, top, width, x=42):
    item = Preformatted(text, CODE)
    _, height = item.wrap(width - 20, 1000)
    pdf.setFillColor(PALE)
    pdf.roundRect(x, top - height - 16, width, height + 16, 5, fill=1, stroke=0)
    item.drawOn(pdf, x + 10, top - height - 8)
    return top - height - 20


def start_page(number, title, size=A4):
    pdf.setPageSize(size)
    width, height = size
    pdf.setFillColor(TEAL)
    pdf.rect(0, height - 9, width, 9, fill=1, stroke=0)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(42, height - 34, "ASTANA IT UNIVERSITY  /  SOFTWARE DESIGN PATTERNS")
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 21)
    pdf.drawString(42, height - 67, title)
    pdf.setStrokeColor(colors.HexColor("#D6E2E9"))
    pdf.line(42, 38, width - 42, 38)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 8)
    pdf.drawString(42, 24, "Assignment 3 | Bridge Pattern - Topic A: Drawing")
    pdf.drawRightString(width - 42, 24, f"4 October 2026  |  {number} / 3")
    return height - 89


def excerpt(path, start, end):
    lines = (ROOT / path).read_text(encoding="utf-8").splitlines()[start - 1:end]
    nonempty = [len(line) - len(line.lstrip()) for line in lines if line.strip()]
    indent = min(nonempty) if nonempty else 0
    return "\n".join(line[indent:] for line in lines)


pdf = canvas.Canvas(str(ROOT / "report.pdf"), pagesize=A4, pageCompression=1)
pdf.setAuthor("Zhuman Mukhammed, SE-2522")
pdf.setTitle("Assignment 3 | Bridge Pattern - Topic A: Drawing")
pdf.setSubject("Bridge implementation, UML, code quality and reproducible demonstration")
width = A4[0] - 84
y = start_page(1, "Assignment 3 | Bridge Pattern")
y = paragraph("School of Software Engineering<br/>ShP-2216 Software Design Patterns | 2026-2027 | Yerassyl Bekenov<br/><b>Topic A - Drawing</b>", 42, y, width)
y = paragraph("<b>Student:</b> Zhuman Mukhammed | <b>Group:</b> SE-2522<br/><b>Repository:</b> <link href='https://github.com/muxammedp/SDP-Ass3' color='#117B83'>https://github.com/muxammedp/SDP-Ass3</link>", 42, y, width, SMALL)
y = heading("Two independently varying dimensions", y - 3)
y = paragraph("The abstraction hierarchy contains Shape, Circle and Square. It owns each shape's ID and geometry: a radius of 2 for the sample Circle and a side of 3 for the sample Square. The implementation hierarchy contains Renderer and three rendering styles. Each style returns its own text description while preserving the supplied geometry.", 42, y, width)
y = paragraph("Shape stores a Renderer interface reference supplied by the client. Circle.execute() selects renderCircle(radius); Square.execute() selects renderSquare(side). Neither abstraction knows which concrete renderer performs the operation. Composition makes the six combinations possible without six combination subclasses. This is the separation described by Bridge [1].", 42, y, width)
y = heading("Runtime replacement: T5", y)
y = codebox(excerpt("src/Main.java", 51, 57), y, width)
y = paragraph("The original reference, ID and radius are saved before this excerpt. The == expression proves identity; the getter comparisons prove preserved domain data. Only the private renderer reference changes. The demo also compares both real execute() results with independent expected strings.", 42, y, width)
y = paragraph("<b>Observed:</b> sameObject=true; stateUnchanged=true; ID circle-switch -&gt; circle-switch; radius 2 -&gt; 2.<br/><b>Before:</b> VECTOR circle radius=2<br/><b>After:</b> RASTER circle radius=2", 42, y, width, SMALL)
y = heading("Reproduction and evidence", y)
y = codebox('javac --release 17 -encoding UTF-8 -d out "@sources.txt"\njava -cp out Main --demo', y, width)
y = paragraph("The captured program output in demo-output.txt runs T1-T7 in order and ends with <b>SUMMARY: 7/7 PASS</b>. T1-T4 cover both shapes with both initial renderers; T5 checks runtime replacement; T6-T7 cover the ASCII extension. Comparisons determine the labels, and counters determine the summary. Failures print the expected value and cause exit status 1.", 42, y, width, SMALL)
y = paragraph(f"<b>Base commit:</b> {BASE}<br/><b>I3 source commit:</b> {EXTENSION}<br/><b>Packaged submission commit:</b> recorded exactly in SUBMISSION.txt at the ZIP root. The packaged Java sources are unchanged from the I3 source commit.", 42, y, width, SMALL)
assert y > 46, f"Page 1 overflow: {y}"
pdf.showPage()

page_size = landscape(A4)
y = start_page(2, "UML class diagram", page_size)
diagram = ImageReader(str(ROOT / "docs" / "bridge.png"))
image_width, image_height = diagram.getSize()
max_width = page_size[0] - 84
max_height = y - 108
scale = min(max_width / image_width, max_height / image_height)
draw_width, draw_height = image_width * scale, image_height * scale
pdf.drawImage(diagram, (page_size[0] - draw_width) / 2, y - draw_height,
              width=draw_width, height=draw_height, mask="auto")
y = y - draw_height - 14
y = paragraph("<b>Reading the diagram:</b> solid hollow triangles show inheritance; dashed hollow triangles show interface implementation. The open diamond and arrow represent Shape holding exactly one Renderer; a renderer may be shared by several shapes. Dotted arrows show the client's creation/use dependencies. '+' is public, '#' protected, '-' private. The diagram shows the methods relevant to the Bridge and demo; constructors of concrete classes and Main's output helpers are omitted.", 42, y, max_width, SMALL)
y = paragraph("<b>Delegated call:</b> Main constructs Circle with VectorRenderer -&gt; Circle.execute() -&gt; Shape.getRenderer() -&gt; Renderer.renderCircle(2) -&gt; VectorRenderer returns the result. Source: docs/bridge.puml, rendered with PlantUML.", 42, y, max_width, SMALL)
assert y > 44, f"Page 2 overflow: {y}"
pdf.showPage()

y = start_page(3, "Code quality and extension")
examples = [
    ("1. Separate responsibilities", "src/drawing/Circle.java", 19, 21,
     "Circle selects the shape operation and passes its geometry. The renderer owns the presentation, so style changes stay outside Circle."),
    ("2. Meaningful names", "src/drawing/Renderer.java", 3, 6,
     "renderCircle, radius, renderSquare and side identify the shape and the exact measurement at the contract boundary."),
    ("3. Small, focused methods", "src/drawing/Shape.java", 22, 24,
     "setImplementation has one job: validate and replace the renderer reference. It does not reconstruct the shape or modify its data."),
    ("4. Avoid duplicated workflow", "src/Main.java", 72, 74,
     "One helper compares each ordinary result and forwards it to record(), which centralizes counters, labels and failure output."),
    ("5. Encapsulate state", "src/drawing/Circle.java", 3, 4,
     "The private final radius is assigned in the constructor and exposed only by a getter. Shape uses the same approach for its ID."),
]
for title, path, start, end, benefit in examples:
    y = heading(title, y)
    y = paragraph(f"{path}:{start}-{end}", 42, y + 3, width, SMALL)
    y = codebox(excerpt(path, start, end), y + 4, width)
    y = paragraph(benefit, 42, y + 4, width, SMALL)

y = heading("Independent extension, trade-off and intent", y)
y = paragraph("The working I1/I2 version was committed first. The next commit added AsciiRenderer and updated Main for T6-T7; sources.txt and documentation were also updated. extension.diff proves that Shape, Circle, Square, Renderer, VectorRenderer and RasterRenderer stayed unchanged. Existing code calls the same Renderer contract.", 42, y, width, SMALL)
y = paragraph("The cost is more classes and indirection for a small simulation. Adding a new shape-specific primitive, such as renderTriangle, would also require changes to the interface and every renderer. Bridge separates planned dimensions so implementations can vary under a stable contract [1]. Adapter instead makes an incompatible existing API usable by translating calls [2]; no such legacy API is present here.", 42, y, width, SMALL)
y = heading("References and authorship", y)
y = paragraph('[1] Refactoring.Guru, <i>Bridge</i>. <link href="https://refactoring.guru/design-patterns/bridge" color="#117B83">refactoring.guru/design-patterns/bridge</link><br/>[2] Refactoring.Guru, <i>Adapter</i>. <link href="https://refactoring.guru/design-patterns/adapter" color="#117B83">refactoring.guru/design-patterns/adapter</link><br/>[3] Astana IT University, <i>Assignment 3 | Bridge Pattern</i>, ShP-2216, 2026-2027, user-provided brief. Web references consulted 4 October 2026.<br/>Prepared with AI assistance. Review and adapt the work under the course rules and be able to explain every submitted method.', 42, y, width, SMALL)
assert y > 44, f"Page 3 overflow: {y}"
pdf.save()
print("Created report.pdf (3 pages)")
