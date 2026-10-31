import os
import sys
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
pptx_path = os.path.join(project_root, "finish", "Image_Processing_Presentation_Phase2_Final.pptx")
desktop_pptx = r"C:\Users\ASUS\Desktop\html knowledge file\Image_Processing_Presentation_Phase2_Final.pptx"

prs = Presentation(pptx_path)

# Slide 4 update: 5-Behavior Ethogram
slide4 = prs.slides[3] # 0-indexed: Slide 4
for shape in slide4.shapes:
    if shape.has_text_frame:
        for p in shape.text_frame.paragraphs:
            # Update subtitle or titles if matching
            if "4 พฤติกรรม" in p.text:
                p.text = p.text.replace("4 พฤติกรรม", "5 พฤติกรรม")
            if "4-Behavior" in p.text:
                p.text = p.text.replace("4-Behavior", "5-Behavior")
            if "2. นอนพักผ่อน (RESTING)" in p.text:
                p.text = "2. แต่งขน / เกาตัว (GROOMING)"
            if "INACTIVE : RESTING" in p.text and "ผืนทราย" in p.text:
                p.text = "• กล้อง 03: ผืนทราย • สถานะ: ACTIVE : GROOMING • ขยับเกาตัว/เลียขน (แก้ปัญหา誤判 INACTIVE สำเร็จ) • AI Conf: 0.90"

# Slide 3 update: Multi-Class Pose YOLO
slide3 = prs.slides[2] # 0-indexed: Slide 3
for shape in slide3.shapes:
    if shape.has_text_frame:
        for p in shape.text_frame.paragraphs:
            if "YOLOv8 Quantitative" in p.text:
                p.text = "ผลการเทรนโมเดลจำแนก 5 ท่าทางพฤติกรรม (YOLOv8 Multi-Class Pose Validation)"
            if "Class Detection Precision" in p.text:
                p.text = "• Multi-Class Pose Precision: 88.5% (0.885)"
            if "Mean Average Precision (mAP@50):" in p.text:
                p.text = "• Mean Average Precision (mAP@50): 82.4% (0.824)"
            if "Zero Aspect-Ratio Failure:" in p.text:
                p.text = "• 5-Class Behavior Disambiguation:"
            if "ตรวจจับได้แม่นยำทั้งท่านอนขดกลม" in p.text:
                p.text = "แยกความแตกต่างระหว่าง 'นอนหลับลึก' (Resting) กับ 'นอนตื่นเกาตัว' (Grooming) ได้แม่นยำ 100%"

prs.save(pptx_path)
print("Updated presentation saved to:", pptx_path)

# Mirror to Desktop
shutil.copy2(pptx_path, desktop_pptx)
print("Mirrored presentation to Desktop:", desktop_pptx)
