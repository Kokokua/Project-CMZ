from pptx import Presentation

prs = Presentation(r"presentations\1.pptx")
for i, slide in enumerate(prs.slides):
    print(f"\n--- Slide {i+1} ---")
    for s in slide.shapes:
        if s.shape_type == 6: # Group
            print(f"Group: '{s.name}' with {len(s.shapes)} subshapes:")
            for sub in s.shapes:
                print(f"    Sub: '{sub.name}', type={sub.shape_type}")
                if sub.shape_type == 13: # Picture
                    print(f"      Picture size: {sub.width.inches:.2f} x {sub.height.inches:.2f}")
                if sub.has_text_frame:
                    print(f"      Text: {sub.text_frame.text[:40]}")
        elif s.shape_type == 13:
            print(f"Picture: '{s.name}' size={s.width.inches:.2f} x {s.height.inches:.2f}")
