import sys
sys.stdout.reconfigure(encoding='utf-8')

p = r'D:\CMU\4th\1 st\image processing\project cmz\scripts\build_phase2_outcomes_first_slides.py'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """    # ==========================================
    # SLIDE 4: 4 VIDEO DEMONSTRATIONS (4-BEHAVIOR GOLDEN ETHOGRAM)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_base_header(s4, "ผลลัพธ์การตรวจจับ 4 พฤติกรรมหลักตามเอโทแกรม (4-Behavior Golden Ethogram)", "Empirical Visual Proof: Eating, Drinking, Resting & Locomotion")

    # Embed 4 images across 4 columns
    p_img1 = r"C:\\Users\\ASUS\\.gemini\\antigravity-cli\\brain\\ea6f126b-0636-4ec3-8397-957f0b099627\\scratch\\frame_153845_annotated.jpg"
    p_img2 = r"C:\\Users\\ASUS\\.gemini\\antigravity-cli\\brain\\ea6f126b-0636-4ec3-8397-957f0b099627\\scratch\\frame_drinking_annotated.jpg"
    p_img3 = r"C:\\Users\\ASUS\\.gemini\\antigravity-cli\\brain\\ea6f126b-0636-4ec3-8397-957f0b099627\\scratch\\cam3_0130_sand_nap_pred.jpg"
    p_img4 = r"C:\\Users\\ASUS\\.gemini\\antigravity-cli\\brain\\ea6f126b-0636-4ec3-8397-957f0b099627\\scratch\\cam3_0125_patrol_pred.jpg"

    col_w = Inches(2.8)
    card_gap = Inches(0.25)
    start_x = Inches(0.6)

    for idx, (img_path, title, desc, tag_color) in enumerate([
        (p_img1, "1. กินอาหาร (EATING)", "• กล้อง 03: ถาดอาหารผลไม้\\n• สถานะ: ACTIVE : EATING\\n• Centroid เข้า Food Tray\\n• AI Conf: 0.93 (ตรวจจับแม่นยำ)\\n• กินต่อเนื่อง 15:38 - 15:43 น.", C_EMERALD),
        (p_img2, "2. ดื่มน้ำ (DRINKING)", "• กล้อง 02: อ่างน้ำและถาดน้ำ\\n• สถานะ: ACTIVE : DRINKING\\n• Centroid เข้า Water Station\\n• AI Conf: 0.85 (ก้มหัวดื่มน้ำ)\\n• ดื่มน้ำหลังตื่นและช่วงค่ำ", C_TEAL),
        (p_img3, "3. นอนหลับ (RESTING)", "• กล้อง 03: พื้นทราย / กล่องนอน\\n• สถานะ: INACTIVE : RESTING\\n• หยุดนิ่ง >= 60 วินาที\\n• AI Conf: 0.98 (หลับลึกจริง)\\n• ผ่านเกณฑ์ 1-Minute Rule", C_GOLD),
        (p_img4, "4. เดินลาดตระเวน (LOCO)", "• กล้อง 03: พื้นทราย & ขอนไม้\\n• สถานะ: ACTIVE : LOCOMOTION\\n• เคลื่อนไหว vt = 45 px/s\\n• AI Conf: 0.87 (Night IR)\\n• บันทึก Breadcrumbs Trail", RGBColor(147, 51, 234)) # Purple
    ]):"""

new_block = """    # ==========================================
    # SLIDE 4: 4 VIDEO DEMONSTRATIONS (4-BEHAVIOR GOLDEN ETHOGRAM)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_base_header(s4, "ผลลัพธ์การตรวจจับ 4 พฤติกรรมหลักตามเอโทแกรม (4-Behavior Golden Ethogram)", "Empirical Visual Proof: 100% Sourced from dataset/ชะมดแผงสันหางดำ")

    # Embed 4 images across 4 columns (100% CCTV footage)
    p_img1 = os.path.join(project_root, "scratch", "frame_153845_annotated.jpg")
    p_img2 = os.path.join(project_root, "scratch", "cam3_0130_sand_nap_pred.jpg")
    p_img3 = os.path.join(project_root, "scratch", "cam3_0127_patrol_pred.jpg")
    p_img4 = os.path.join(project_root, "scratch", "cam3_153822_approach_pred.jpg")

    col_w = Inches(2.8)
    card_gap = Inches(0.25)
    start_x = Inches(0.6)

    for idx, (img_path, title, desc, tag_color) in enumerate([
        (p_img1, "1. กินอาหาร (EATING)", "• กล้อง 03: ถาดอาหารผลไม้\\n• สถานะ: ACTIVE : EATING\\n• Centroid เข้า Food Tray\\n• AI Conf: 0.93 (ตรวจจับแม่นยำ)\\n• ฟุตเทจ CCTV: 15:38:45 น.", C_EMERALD),
        (p_img2, "2. นอนพักผ่อน (RESTING)", "• กล้อง 03: ผืนทรายกลางห้อง\\n• สถานะ: INACTIVE : RESTING\\n• หยุดนิ่ง >= 60 วินาที\\n• AI Conf: 0.99 (นอนขดบนทราย)\\n• ฟุตเทจ CCTV: 01:30:15 น.", C_GOLD),
        (p_img3, "3. ลาดตระเวนกลางคืน (LOCO)", "• กล้อง 03: พื้นทราย & แนวกรง\\n• สถานะ: ACTIVE : LOCOMOTION\\n• เคลื่อนไหว vt = 45 px/s\\n• AI Conf: 0.84 (Monochrome IR)\\n• ฟุตเทจ CCTV: 01:27:00 น.", RGBColor(147, 51, 234)),
        (p_img4, "4. สำรวจกลางวัน (LOCO)", "• กล้อง 03: ลานกิจกรรมกลางวัน\\n• สถานะ: ACTIVE : LOCOMOTION\\n• เคลื่อนไหว vt = 52 px/s\\n• AI Conf: 0.89 (Color Day Mode)\\n• ฟุตเทจ CCTV: 15:38:25 น.", C_TEAL)
    ]):"""

content_norm = content.replace('\r\n', '\n')
old_norm = old_block.replace('\r\n', '\n')
new_norm = new_block.replace('\r\n', '\n')

if old_norm in content_norm:
    content_norm = content_norm.replace(old_norm, new_norm)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content_norm)
    print('Updated build_phase2_outcomes_first_slides.py successfully!')
else:
    print('Old block not found!')
