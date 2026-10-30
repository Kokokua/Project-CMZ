from pptx import Presentation

prs = Presentation(r"presentations\1.pptx")
print(f"Slide width: {prs.slide_width.inches}, height: {prs.slide_height.inches}")

for i, slide in enumerate(prs.slides):
    bg = slide.background
    fill = bg.fill
    print(f"Slide {i+1} background fill type: {fill.type if fill else 'None'}")
