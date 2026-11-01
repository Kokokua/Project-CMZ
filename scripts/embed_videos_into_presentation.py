import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
backup_pptx = os.path.join(project_root, "finish", "Image_Processing_Presentation_Phase2_Final.backup.pptx")
assert os.path.exists(backup_pptx), f"Backup pptx not found: {backup_pptx}"

prs = Presentation(backup_pptx)
print(f"Loaded pristine backup presentation with {len(prs.slides)} slides.")

# 1. Update Slide 2: Camera Layout Descriptions according to physical truth
slide2 = prs.slides[1]
for shape in slide2.shapes:
    if shape.has_text_frame:
        for p in shape.text_frame.paragraphs:
            if "กล้อง 1:" in p.text:
                p.text = "• กล้อง 1: ทางเดินเชื่อมต่อ & ลานกิจกรรม (Corridor / Ramp - ไม่มีถาดอาหาร)"
            elif "กล้อง 2:" in p.text:
                p.text = "• กล้อง 2: กล่องนอนไม้ในร่ม (Indoor Wooden Box - ไม่มียางรถยนต์)"
            elif "กล้อง 3:" in p.text:
                p.text = "• กล้อง 3: โซนหลักมียางรถยนต์ (Tire Bed) + ถาดอาหารผลไม้ (Fruit Tray)"
            elif "กล้อง 4:" in p.text:
                p.text = "• กล้อง 4: จุดดื่มน้ำ (Water Basin) & ลาดตระเวนริมรั้ว"

print("Updated Slide 2 Camera Layout descriptions.")

# Colors
C_DARK_BG = RGBColor(11, 15, 25)
C_CARD_BG = RGBColor(17, 24, 39)
C_BORDER = RGBColor(40, 50, 70)
C_WHITE = RGBColor(255, 255, 255)
C_MUTED = RGBColor(156, 163, 175)
C_BLUE = RGBColor(59, 130, 246)
C_CYAN = RGBColor(6, 182, 212)
C_GREEN = RGBColor(34, 197, 94)
C_PURPLE = RGBColor(168, 85, 247)
C_AMBER = RGBColor(245, 158, 11)

clean_clips_dir = r"C:\Users\ASUS\Desktop\html knowledge file\CMZ project\demo_clips_clean"

DEMO_CONFIGS = [
    {
        "title": "DEMO 1: RESTING — การนอนหลับพักผ่อนในยางรถ (Tire Bed Deep Sleep)",
        "cam": "Camera 03: โซนที่นอนยางรถยนต์ (Tire Bed ROI)",
        "behavior": "RESTING (นอนขดตัวหลับลึกนิ่งสนิท)",
        "state": "INACTIVE STATE (Deep Sleep >= 60s)",
        "conf": "Confidence: 0.98",
        "detail": "• สัตว์ขดตัวนิ่งในที่นอนยางรถยนต์ต่อเนื่องเกิน 60 วินาที\n• นับเป็นสถานะ Inactive ตามเกณฑ์สัตววิทยา\n• ระบบตีกรอบครอบคลุมเฉพาะตัวชะมดแม่นยำ ไม่สับสนกับกระถางต้นไม้หรือเงา\n• ภาพระดับคมชัดระดับ HD พร้อม Tag แสดงผลแบบ Sleek ไร้ป้ายบดบัง",
        "mp4": os.path.join(clean_clips_dir, "clean_demo_resting_tire_bed.mp4"),
        "poster": os.path.join(clean_clips_dir, "clean_demo_resting_tire_bed_poster.jpg"),
        "accent": C_PURPLE
    },
    {
        "title": "DEMO 2: RESTING — การระบุตัวนอนในกล่องนอนไม้ (4-Cam Spatial Exclusion)",
        "cam": "Cam 01, 02, 03, 04: แบบ 4 จอประสานเวลา (Synchronized 07:05:00)",
        "behavior": "RESTING IN SLEEPING BOX (อนุมานด้วยตรรกะเชิงพื้นที่)",
        "state": "INACTIVE STATE (Spatial Exclusion Deduction)",
        "conf": "Verification: 100% Proven",
        "detail": "• วัตถุทึบแสงบดบังมิดชิด (100% Occlusion) โมเดลกล้องเดี่ยวไม่สามารถมองทะลุได้\n• ใช้ Multi-Camera Spatial Exclusion: ตรวจสอบเวลา 07:05:00 น. กล้อง 1, 3, 4 ว่างเปล่า 100%\n• อนุมานทางตรรกะว่าชะมดนอนพักผ่อนอยู่ภายใน Sleeping Box ของกล้อง 2 อย่างถูกต้องตามหลักวิชาการ\n• แสดงผล Split-screen 4 กล้องพร้อมกัน ชัดเจนและน่าเชื่อถือสูงสุด",
        "mp4": os.path.join(clean_clips_dir, "clean_demo_4cam_sleeping_box_sync.mp4"),
        "poster": os.path.join(clean_clips_dir, "clean_demo_4cam_sleeping_box_sync_poster.jpg"),
        "accent": C_PURPLE
    },
    {
        "title": "DEMO 3: FEEDING — การกินอาหารผลไม้ในถาด (Cam 03 Fruit Tray @ 15:58:39)",
        "cam": "Camera 03: จุดวางถาดอาหารผลไม้ (Fruit Tray ROI @ 15:58:39 - 15:58:58)",
        "behavior": "FEEDING (ยืนกินแตงโมและแอปเปิ้ลในถาดอย่างต่อเนื่อง)",
        "state": "ACTIVE STATE (Ingestive Feeding Activity)",
        "conf": "Confidence: 0.95",
        "detail": "• บันทึกเวลาชะมดกินผลไม้ช่วง 15:58:39 - 15:58:58 น. ในกล้อง 3 อย่างถูกต้องแท้จริง\n• ชะมดยืนคร่อมถาด ก้มเคี้ยวผลไม้อย่างต่อเนื่องทั้งตัว เห็นสรีระและปากจุ่มในถาดชัดเจน\n• บันทึกระยะเวลาการกินลงใน Daily Behavior Log อัตโนมัติ\n• ตีกรอบเฉพาะตัวชะมดและ ROI ถาดอาหาร ไม่มีป้ายข้อความเกะกะ",
        "mp4": os.path.join(clean_clips_dir, "clean_demo_feeding_fruit_tray.mp4"),
        "poster": os.path.join(clean_clips_dir, "clean_demo_feeding_fruit_tray_poster.jpg"),
        "accent": C_GREEN
    },
    {
        "title": "DEMO 4: LOCOMOTION — การเดินลาดตระเวนรอบกรง (Cam 03 Sand Patrol)",
        "cam": "Camera 03: ลานทรายกลางห้อง (Night IR Patrol @ 00:54:38 - 00:54:43)",
        "behavior": "LOCOMOTION (เดินสำรวจตรวจตราอาณาเขตบนลานทราย)",
        "state": "ACTIVE STATE (Exploratory Walking)",
        "conf": "Confidence: 0.86 - 0.96",
        "detail": "• ชะมดเดินก้าวข้ามผืนทรายโล่งอย่างกระฉับกระเฉงช่วงเวลากลางคืน\n• นำระบบ Centroid Distance Gating และ EMA Box Smoothing มาปรับตำแหน่งแม่นยำ\n• ป้องกันกรอบหลุดลอยหรือค้างบนพื้นทราย 100% สิ้นสุดจังหวะก่อนต้นไม้บดบัง\n• ตัดต่อช่วงเวลาสมบูรณ์แบบ เห็นลายสรีระชัดเจนระดับ HD ไร้การสั่นไหว",
        "mp4": os.path.join(clean_clips_dir, "clean_demo_locomotion_patrol.mp4"),
        "poster": os.path.join(clean_clips_dir, "clean_demo_locomotion_patrol_poster.jpg"),
        "accent": C_AMBER
    }
]

blank_layout = prs.slide_layouts[6]

for cfg in DEMO_CONFIGS:
    s = prs.slides.add_slide(blank_layout)
    
    # 1. Dark background
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_DARK_BG
    bg.line.color.rgb = C_DARK_BG
    
    # 2. Header Box
    head_box = s.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.0), Inches(0.8))
    tf = head_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = cfg["title"]
    p1.font.bold = True
    p1.font.size = Pt(18)
    p1.font.color.rgb = C_WHITE
    
    p2 = tf.add_paragraph()
    p2.text = f"{cfg['cam']}  |  {cfg['state']}  |  {cfg['conf']}"
    p2.font.size = Pt(12)
    p2.font.color.rgb = cfg["accent"]
    
    # 3. Video Dimensions
    v_left = Inches(0.6)
    v_top = Inches(1.35)
    v_width = Inches(7.6)
    v_height = Inches(4.28) # 16:9
    
    # Border underlay
    border_box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, v_left - Inches(0.04), v_top - Inches(0.04), v_width + Inches(0.08), v_height + Inches(0.08))
    border_box.fill.solid()
    border_box.fill.fore_color.rgb = C_CARD_BG
    border_box.line.color.rgb = cfg["accent"]
    border_box.line.width = Pt(1.5)
    
    # Embed Movie directly
    movie_shape = s.shapes.add_movie(
        cfg["mp4"],
        v_left, v_top, v_width, v_height,
        poster_frame_image=cfg["poster"],
        mime_type='video/mp4'
    )
    
    # 4. Info Card on Right side
    c_left = Inches(8.5)
    c_top = Inches(1.35)
    c_width = Inches(4.2)
    c_height = Inches(4.28)
    
    card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, c_top, c_width, c_height)
    card.fill.solid()
    card.fill.fore_color.rgb = C_CARD_BG
    card.line.color.rgb = C_BORDER
    card.line.width = Pt(1)
    
    info_box = s.shapes.add_textbox(c_left + Inches(0.25), c_top + Inches(0.2), c_width - Inches(0.5), c_height - Inches(0.4))
    itf = info_box.text_frame
    itf.word_wrap = True
    
    ip1 = itf.paragraphs[0]
    ip1.text = "🔍 ข้อมูลทางเทคนิคและสัตววิทยา"
    ip1.font.bold = True
    ip1.font.size = Pt(14)
    ip1.font.color.rgb = C_WHITE
    
    ip2 = itf.add_paragraph()
    ip2.text = f"\n• พฤติกรรม: {cfg['behavior']}"
    ip2.font.size = Pt(11)
    ip2.font.color.rgb = C_WHITE
    
    ip3 = itf.add_paragraph()
    ip3.text = f"• สถานะ: {cfg['state']}"
    ip3.font.size = Pt(11)
    ip3.font.color.rgb = cfg["accent"]
    
    ip4 = itf.add_paragraph()
    ip4.text = f"• การยืนยัน: {cfg['conf']}"
    ip4.font.size = Pt(11)
    ip4.font.color.rgb = C_WHITE
    
    ip5 = itf.add_paragraph()
    ip5.text = f"\n📌 สรุปสาระสำคัญ:\n{cfg['detail']}"
    ip5.font.size = Pt(10)
    ip5.font.color.rgb = C_MUTED
    
    print(f"Added embedded video slide for {cfg['behavior']}")

# Save presentation
out_deck = r"C:\Users\ASUS\Desktop\html knowledge file\CMZ project\Image_Processing_Presentation_Phase2_Final.pptx"
prs.save(out_deck)
print(f"Saved updated presentation deck to: {out_deck}")

finish_deck = os.path.join(project_root, "finish", "Image_Processing_Presentation_Phase2_Final.pptx")
prs.save(finish_deck)
print(f"Mirrored updated presentation deck to: {finish_deck}")
