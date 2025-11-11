# How to Export Research Paper to PDF

## Method 1: Browser Print to PDF (Recommended)

1. Open `research_paper_print.html` in your browser
2. Press `Ctrl+P` (or `Cmd+P` on Mac)
3. In the print dialog:
   - Destination: **Save as PDF**
   - Layout: **Portrait**
   - Paper size: **A4**
   - Margins: **Default**
   - Scale: **100%**
   - ✓ Check "Background graphics" (to keep table shading)
4. Click **Save**
5. Name it: `TamperCheck_Research_Paper.pdf`

## Method 2: Chrome/Edge Specific

1. Open `research_paper_print.html`
2. Press `Ctrl+P`
3. Click **More settings**
4. Set:
   - Paper size: A4
   - Margins: Default
   - Scale: Default
   - Options: ✓ Background graphics
5. Click **Save**

## Method 3: Using Python (wkhtmltopdf)

If you want programmatic PDF generation:

```bash
# Install wkhtmltopdf
# Windows: Download from https://wkhtmltopdf.org/downloads.html

# Then run:
wkhtmltopdf research_paper_print.html TamperCheck_Research_Paper.pdf
```

## Method 4: Using Python (weasyprint)

```bash
pip install weasyprint

python -c "from weasyprint import HTML; HTML('research_paper_print.html').write_pdf('TamperCheck_Research_Paper.pdf')"
```

## What's Different in the Print Version?

- ✅ Optimized for A4 paper
- ✅ Proper page breaks
- ✅ Print-friendly fonts (Times New Roman)
- ✅ No interactive elements
- ✅ Charts replaced with data tables
- ✅ Clean black & white styling
- ✅ Proper margins for printing

## Recommended Settings

- **Paper**: A4 (210mm × 297mm)
- **Orientation**: Portrait
- **Margins**: 2cm all sides
- **Font**: Times New Roman, 11pt
- **Line spacing**: 1.6

## Result

You'll get a clean, professional PDF suitable for:
- ✅ Printing
- ✅ Sharing via email
- ✅ Uploading to arXiv or research repositories
- ✅ Academic submissions

---

**The print version is optimized for PDF export!** 📄✨

