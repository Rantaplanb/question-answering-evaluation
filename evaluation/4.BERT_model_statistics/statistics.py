from fpdf import FPDF

data = (
    ("First name", "Last name", "Age", "City"),
    ("Jules", "Smith", "34", "San Juan"),
    ("Mary", "Ramos", "45", "Orlando"),
    ("Carlson", "Banks", "19", "Los Angeles"),
    ("Lucas", "Cimon", "31", "Saint-Mahturin-sur-Loire"),
)

pdf = FPDF()
pdf.add_page()
pdf.set_font("Times", size=10)
line_height = pdf.font_size * 2.5
col_width = pdf.epw / 4  # distribute content evenly
for row in data:
    for datum in row:
        pdf.multi_cell(col_width, line_height, datum, border=1,
                new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
    pdf.ln(line_height)
pdf.output('table_with_cells.pdf')