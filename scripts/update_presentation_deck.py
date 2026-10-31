import sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'D:\CMU\4th\1 st\image processing\project cmz\scripts\build_phase2_outcomes_first_slides.py'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

target_marker = "    # ==========================================\n    # SLIDE 5: 24-HOUR BEHAVIORAL EVENT LOG (CSV TABLE)\n    # =========================================="

new_slide_code = '''    # ==========================================
    # SLIDE 5: MULTI-CAMERA SPATIAL HANDOFF & SHELTER SLEEP
    # ==========================================
    s5_multi = prs.slides.add_slide(blank_layout)
    add_base_header(s5_multi, "การสลับกล้องติดตามข้ามห้อง & การตรวจจับการนอนในที่หลบภัย (Multi-Camera Spatial Handoff & Shelter Sleep)", "Autonomous Multi-Camera Orchestration & Synchronized FSM")

    p_handoff_img = os.path.join(project_root, "finish", "demo_clips", "demo_clip_multi_camera_handoff_with_live_csv_poster.jpg")
    p_shelter_img = os.path.join(project_root, "finish", "demo_clips", "demo_clip_shelter_sleep_sync_poster.jpg")

    # Card 1: Multi-Cam Handoff + Live CSV (Left)
    card1 = s5_multi.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_CARD_BG
    card1.line.color.rgb = C_BORDER

    if os.path.exists(p_handoff_img):
        s5_multi.shapes.add_picture(p_handoff_img, Inches(0.95), Inches(1.65), Inches(5.3), Inches(2.35))

    tb1 = s5_multi.shapes.add_textbox(Inches(0.95), Inches(4.1), Inches(5.3), Inches(2.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "1. สลับกล้องอัตโนมัติ & พิมพ์บันทึก CSV สด (Multi-Cam Handoff)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GOLD

    p2 = tf1.add_paragraph()
    p2.text = "• Side-by-Side Dual View: ติดตามชะมดตื่นนอนห้อง 2 ➔ เดินลง Ramp ➔ สลับเข้าห้อง 3\\n• Auto-Director Switcher: สลับหน้าจออัตโนมัติเมื่อตรวจพบการเดินข้ามประตู (Doorway)\\n• Live Typewriter CSV Stream: หน้าจอด้านขวาจำลองการพิมพ์ event ทีละตัวอักษร\\n• Real-Time Edge Logging: บันทึกข้อมูลลง daily_behavior_log.csv ต่อเนื่องไร้ดีเลย์"
    p2.font.name = 'Segoe UI'
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_DARK
    p2.space_before = Pt(4)

    # Card 2: Shelter Sleeping & 4-Cam Sync (Right)
    card2 = s5_multi.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    card2.fill.solid()
    card2.fill.fore_color.rgb = C_CARD_BG
    card2.line.color.rgb = C_BORDER

    if os.path.exists(p_shelter_img):
        s5_multi.shapes.add_picture(p_shelter_img, Inches(6.95), Inches(1.65), Inches(5.4), Inches(2.35))

    tb2 = s5_multi.shapes.add_textbox(Inches(6.95), Inches(4.1), Inches(5.4), Inches(2.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "2. การนอนในที่หลบภัย & ตรวจสอบ 4 กล้องพร้อมกัน (Shelter Sleep Sync)"
    p.font.name = 'Segoe UI'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    p2 = tf2.add_paragraph()
    p2.text = "• กล้อง 3 เห็นชัดเจน 100%: บันทึกจังหวะชะมดเดินมุ่งหน้าเข้าสู่ประตูกล่องนอนห้อง 2\\n• กล้อง 2 บันทึกการมุดเข้าที่หลบภัย: ก้าวขึ้น Ramp และมุดเข้าไปนอนในกล่องนอนมืด\\n• Synchronized 4-Cam Verification: ตรวจสอบเวลา 05:00 น. พบห้อง 1, 3, 4 ว่างเปล่า\\n• Zoological FSM Logic: เมื่อห้องอื่นไม่มีตัว ยืนยันสถานะ RESTING ในที่หลบภัยแม่นยำ"
    p2.font.name = 'Segoe UI'
    p2.font.size = Pt(10)
    p2.font.color.rgb = C_DARK
    p2.space_before = Pt(4)

    # ==========================================
    # SLIDE 6: 24-HOUR BEHAVIORAL EVENT LOG (CSV TABLE)
    # =========================================='''

content_norm = content.replace('\r\n', '\n')
if target_marker in content_norm:
    content_norm = content_norm.replace(target_marker, new_slide_code)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content_norm)
    print("Successfully added Multi-Camera & Shelter Sleep Slide to build_phase2_outcomes_first_slides.py!")
else:
    print("Target marker not found!")
