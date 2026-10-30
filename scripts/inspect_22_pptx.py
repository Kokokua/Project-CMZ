import pptx
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
pptx_path = r"D:\CMU\4th\1 st\image processing\project cmz\presentations\22.pptx"
prs = pptx.Presentation(pptx_path)

print(f"Presentation: {os.path.basename(pptx_path)}")
print(f"Total Slides: {len(prs.slides)}")
print(f"Slide Dimensions: {prs.slide_width.inches:.2f} x {prs.slide_height.inches:.2f} inches")

for i, slide in enumerate(prs.slides):
    print(f"\n==================== SLIDE {i+1} ====================")
    for shape in slide.shapes:
        if shape.has_text_frame:
            text = shape.text_frame.text.strip().replace('\n', ' ')
            if text:
                print(f"  [TEXT] {text[:120]}")
        elif shape.shape_type == pptx.enum.shapes.MSO_SHAPE.RECTANGLE:
            pass
        elif hasattr(shape, 'image'):
            print(f"  [IMAGE] size={shape.width.inches:.2f}x{shape.height.inches:.2f}")
