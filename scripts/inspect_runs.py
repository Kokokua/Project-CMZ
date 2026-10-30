from pptx import Presentation

prs = Presentation(r"presentations\1.pptx")
with open(r"scripts\inspect_runs.txt", "w", encoding="utf-8") as out:
    for i, slide in enumerate(prs.slides):
        out.write(f"\n==================== SLIDE {i+1} ====================\n")
        for s in slide.shapes:
            if s.has_text_frame:
                out.write(f"\n--- Shape: '{s.name}' ---\n")
                for p_idx, p in enumerate(s.text_frame.paragraphs):
                    runs_info = []
                    for r in p.runs:
                        font_size = r.font.size.pt if r.font.size else "None"
                        font_bold = r.font.bold
                        font_color = r.font.color.rgb if (r.font.color and r.font.color.type == 1) else "theme/None"
                        runs_info.append(f"['{r.text}' | {r.font.name} | {font_size}pt | bold={font_bold} | col={font_color}]")
                    out.write(f"  P{p_idx} (align={p.alignment}): {' + '.join(runs_info)}\n")
print("Done inspecting runs.")
