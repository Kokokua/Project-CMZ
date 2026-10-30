from pptx import Presentation

prs = Presentation(r"presentations\1.pptx")
print("Slide master count:", len(prs.slide_masters))
slide = prs.slides[1] # Slide 2
print("Slide 2 shapes count:", len(slide.shapes))
for s in slide.shapes:
    print(f"Shape: {s.name}, type: {s.shape_type}")
    if s.has_text_frame:
        for p in s.text_frame.paragraphs:
            if p.text.strip():
                print(f"  P: '{p.text[:60]}' | font: {p.font.name}, size: {p.font.size.pt if p.font.size else None}, color: {p.font.color.rgb if p.font.color and p.font.color.type == 1 else 'other'}")
