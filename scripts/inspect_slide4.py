from pptx import Presentation

prs = Presentation(r"presentations\1.pptx")
slide4 = prs.slides[3] # Slide 4
for s in slide4.shapes:
    print(f"Shape: {s.name}, type: {s.shape_type}, left: {s.left.inches:.2f}, top: {s.top.inches:.2f}, w: {s.width.inches:.2f}, h: {s.height.inches:.2f}")
    if s.shape_type == 6: # Group
        for sub in s.shapes:
            print(f"   Sub: {sub.name}, type: {sub.shape_type}, fill: {sub.fill.type if hasattr(sub, 'fill') else None}")
