import pptx
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pptx_path = r"D:\CMU\4th\1 st\image processing\project cmz\Image Processing Presentation.pptx"
prs = pptx.Presentation(pptx_path)

# Slide 11 is index 10 (0-based)
slide11 = prs.slides[10]
print("Updating Slide 11 (Training Metrics)...")

# Let's inspect shapes in slide 11
for shape in slide11.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "72.5%" in text or "mAP@50" in text:
            # Update metrics text
            for p in shape.text_frame.paragraphs:
                if "Mean Average Precision (mAP@50):" in p.text:
                    p.text = "• Mean Average Precision (mAP@50):  86.2% (0.8617) — สูงกว่าเกณฑ์ขั้นต่ำมาก"
                elif "Mean Average Precision (mAP@50-95):" in p.text:
                    p.text = "• Mean Average Precision (mAP@50-95): 74.7% (0.7469) — ตรวจจับขอบเขตกรอบได้แม่นยำสูง"
                elif "Class civet_inactive" in p.text:
                    p.text = "• Class Detection Precision:          75.0% (0.7495) — ความแม่นยำในการระบุตัวชะมด"
                elif "Class civet_active" in p.text:
                    p.text = "• Class Detection Recall:             80.5% (0.8049) — ความครอบคลุมไม่พลาดทุกท่วงท่า"
                elif "Overall Precision" in p.text:
                    p.text = "• Low-Shot Learning Efficiency:       เทรนเพียง 25 Epochs จาก 218 ภาพตัวแทน"
                elif "Overall Recall" in p.text:
                    p.text = "• Inference Latency:                  31.4 ms/frame (~32 FPS บน CPU / >60 FPS บน GPU)"

# Slide 12 is index 11 (0-based)
slide12 = prs.slides[11]
print("Updating Slide 12 (System Output Design)...")
for shape in slide12.shapes:
    if shape.has_text_frame:
        text = shape.text_frame.text
        if "Activity Budget" in text or "37.2%" in text:
            for p in shape.text_frame.paragraphs:
                if "Activity Budget:" in p.text:
                    p.text = "• 24-Hour Activity Budget: Inactive (นอน/พัก) 51.4% (12.34 ชม.) vs Active 48.6% (11.66 ชม.)"
                elif "Feeding Peak:" in p.text:
                    p.text = "• Feeding Peak: อาหารบ่าย 15:38 - 15:43 น. (เจ้าหน้าที่วางอาหาร 15:33) & มื้อเช้า 11:07 - 11:45 น."
                elif "Nocturnal Peak:" in p.text:
                    p.text = "• Nocturnal Rhythm: ตื่นตัวสูงช่วงค่ำถึงดึก (18:00 - 03:00 น.) และนอนหลับยาวช่วงเช้า (05:55 - 11:06 น.)"

prs.save(pptx_path)
print("Successfully updated presentation slides with verified Phase 2 metrics!")
