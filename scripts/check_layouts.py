from pptx import Presentation

prs = Presentation(r"presentations\1.pptx")
print(f"Total layouts in master: {len(prs.slide_layouts)}")
for i, l in enumerate(prs.slide_layouts):
    print(f"Layout {i}: {l.name}")
