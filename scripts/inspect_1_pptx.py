import os
from pptx import Presentation

pptx_path = r"presentations\1.pptx"
if not os.path.exists(pptx_path):
    print("File not found:", pptx_path)
    exit(1)

prs = Presentation(pptx_path)
print(f"Width: {prs.slide_width.inches:.2f}, Height: {prs.slide_height.inches:.2f}")
print(f"Total slides: {len(prs.slides)}")

with open(r"scripts\inspect_1_output.txt", "w", encoding="utf-8") as out:
    out.write(f"Width: {prs.slide_width.inches:.2f}, Height: {prs.slide_height.inches:.2f}\n")
    out.write(f"Total slides: {len(prs.slides)}\n")
    for i, slide in enumerate(prs.slides):
        out.write(f"\n=== Slide {i+1} ===\n")
        for j, s in enumerate(slide.shapes):
            shape_type = str(s.shape_type)
            text_preview = ""
            if s.has_text_frame:
                text_preview = " | " + " / ".join([p.text.strip() for p in s.text_frame.paragraphs if p.text.strip()])
            out.write(f"  Shape {j}: name='{s.name}', type={shape_type}, left={s.left.inches:.2f}, top={s.top.inches:.2f}, w={s.width.inches:.2f}, h={s.height.inches:.2f}{text_preview}\n")
