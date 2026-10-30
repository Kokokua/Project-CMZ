import pptx
import sys

sys.stdout.reconfigure(encoding='utf-8')
prs = pptx.Presentation(r"D:\CMU\4th\1 st\image processing\project cmz\presentations\22.pptx")
print("Presentation Slide Size:", prs.slide_width.inches, "x", prs.slide_height.inches)

for idx in [0, 1, 8, 11]:
    slide = prs.slides[idx]
    print(f"\n--- SLIDE {idx+1} Details ---")
    print("Shapes count:", len(slide.shapes))
    for s in slide.shapes:
        if s.has_text_frame:
            for p in s.text_frame.paragraphs[:2]:
                font_name = p.font.name
                font_size = p.font.size.pt if p.font.size else "None"
                color = p.font.color.rgb if p.font.color and hasattr(p.font.color, 'rgb') else "None"
                print(f"  Shape {s.name}: text='{p.text[:60]}' font={font_name} size={font_size} color={color}")
        if hasattr(s, 'fill'):
            try:
                if s.fill.type:
                    print(f"  Shape {s.name} fill: {s.fill.fore_color.rgb}")
            except Exception:
                pass
