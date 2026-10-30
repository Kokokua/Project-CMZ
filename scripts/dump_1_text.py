from pptx import Presentation

prs = Presentation(r"presentations\1.pptx")
with open(r"scripts\dump_1_text.txt", "w", encoding="utf-8") as f:
    for i, slide in enumerate(prs.slides):
        f.write(f"\n==================== SLIDE {i+1} ====================\n")
        for s in slide.shapes:
            if s.has_text_frame:
                f.write(f"\n--- Shape '{s.name}' (id={s.shape_id}) left={s.left.inches:.2f}, top={s.top.inches:.2f}, w={s.width.inches:.2f}, h={s.height.inches:.2f} ---\n")
                for p_idx, p in enumerate(s.text_frame.paragraphs):
                    text = p.text
                    if text.strip():
                        font_name = p.font.name if p.font else None
                        font_size = p.font.size.pt if (p.font and p.font.size) else None
                        bold = p.font.bold if p.font else None
                        f.write(f"  P{p_idx} [{font_name}, {font_size}pt, bold={bold}]: {text}\n")
            if s.has_table:
                f.write(f"\n--- Table '{s.name}' {len(s.table.rows)}x{len(s.table.columns)} ---\n")
                for r_idx, row in enumerate(s.table.rows):
                    cells_text = [cell.text.strip().replace('\n', ' ') for cell in row.cells]
                    f.write(f"  Row {r_idx}: {' | '.join(cells_text)}\n")
print("Dumped 1.pptx text successfully.")
