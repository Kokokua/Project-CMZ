import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def create_phase2_plan_document():
    doc = docx.Document()

    # Configure Margins (0.75 inch)
    for s in doc.sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Color Palette
    HEX_TEAL = '1B4958'       # Primary Corporate Teal
    HEX_GOLD = 'D97706'       # Accent Amber / Gold
    HEX_DARK = '0F172A'       # Slate 900
    HEX_MUTED = '475569'      # Slate 600
    HEX_BG_LIGHT = 'F8FAFC'   # Slate 50
    HEX_BORDER = 'CBD5E1'     # Slate 300
    HEX_EMERALD = '059669'    # Emerald 600
    HEX_ROSE = 'E11D48'       # Rose 600

    RGB_TEAL = RGBColor(27, 73, 88)
    RGB_GOLD = RGBColor(217, 119, 6)
    RGB_DARK = RGBColor(15, 23, 42)
    RGB_MUTED = RGBColor(71, 85, 105)
    RGB_EMERALD = RGBColor(5, 150, 105)

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), fill_hex)
        tcPr.append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def add_header_tag(text, subtext=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(text.upper())
        r.font.name = 'Segoe UI'
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGB_GOLD
        if subtext:
            p2 = doc.add_paragraph()
            p2.paragraph_format.space_before = Pt(0)
            p2.paragraph_format.space_after = Pt(4)
            r2 = p2.add_run(subtext)
            r2.font.name = 'TH Sarabun New'
            r2.font.size = Pt(12)
            r2.font.color.rgb = RGB_MUTED

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(20)
        r.font.bold = True
        r.font.color.rgb = RGB_TEAL
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGB_DARK
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGB_GOLD
        return p

    def add_body(text, bold_prefix="", italic_note=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = 'TH Sarabun New'
            rb.font.size = Pt(14)
            rb.font.bold = True
            rb.font.color.rgb = RGB_DARK
        r = p.add_run(text)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(14)
        r.font.color.rgb = RGB_DARK
        if italic_note:
            ri = p.add_run(italic_note)
            ri.font.name = 'TH Sarabun New'
            ri.font.size = Pt(13)
            ri.font.italic = True
            ri.font.color.rgb = RGB_MUTED
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = 'TH Sarabun New'
            rb.font.size = Pt(14)
            rb.font.bold = True
            rb.font.color.rgb = RGB_DARK
        r = p.add_run(text)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(14)
        r.font.color.rgb = RGB_DARK
        return p

    def add_callout(title, body, border_color='1B4958', bg_color='F8FAFC'):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, bg_color)
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

        # Left border only
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        left = OxmlElement('w:left')
        left.set(qn('w:val'), 'single')
        left.set(qn('w:sz'), '24')
        left.set(qn('w:space'), '0')
        left.set(qn('w:color'), border_color)
        tcBorders.append(left)

        for side in ['top', 'bottom', 'right']:
            b = OxmlElement(f'w:{side}')
            b.set(qn('w:val'), 'none')
            tcBorders.append(b)
        tcPr.append(tcBorders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        rt = p.add_run(title)
        rt.font.name = 'TH Sarabun New'
        rt.font.size = Pt(14.5)
        rt.font.bold = True
        rt.font.color.rgb = RGB_TEAL if border_color == '1B4958' else RGB_GOLD

        pb = cell.add_paragraph()
        pb.paragraph_format.space_before = Pt(2)
        pb.paragraph_format.space_after = Pt(0)
        rb = pb.add_run(body)
        rb.font.name = 'TH Sarabun New'
        rb.font.size = Pt(13.5)
        rb.font.color.rgb = RGB_DARK

        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    # ==================== DOCUMENT COVER / HEADER ====================
    add_header_tag("CHIANG MAI ZOO × CHIANG MAI UNIVERSITY | IMAGE PROCESSING 2026", "โครงการระบบเฝ้าสังเกตและวิเคราะห์พฤติกรรมชะมดแผงสันหางดำอัตโนมัติ")

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("แผนกลยุทธ์การดำเนินงาน Phase 2 และรายงานการตรวจสอบสถานะระบบ\n(Phase 2 Master Plan & Current System Audit)")
    r_title.font.name = 'TH Sarabun New'
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = RGB_TEAL

    add_callout("⏱️ สรุปกรอบเวลาและกำหนดการส่งมอบงานสำคัญ (Deadlines & Presentations)",
                "• กำหนดส่งมอบงาน (Submission Deadline): วันเสาร์ที่ 31 ตุลาคม 2569 เวลา 12:00 น. (เที่ยงวัน)\n"
                "• กำหนดวันนำเสนอผลงาน (Final Presentation): วันที่ 31 ต.ค. – 3 พ.ย. 2569 (ช่วงเวลา 15:00 – 18:00 น.)\n"
                "• ขอบเขตงาน Phase 2: คัดเลือกวิดีโอตัวแทนจาก Google Drive, เทรนโมเดล AI, อธิบายสถาปัตยกรรมเชิงลึก, ออกแบบตาราง Active/Inactive และ Visualization, ส่งมอบลิงก์ GitHub & Roboflow Annotation",
                border_color='D97706', bg_color='FFFBEB')

    # ==================== ส่วนที่ 1: AUDIT & GAP ANALYSIS ====================
    add_h1("ส่วนที่ 1: รายงานการตรวจสอบระบบปัจจุบัน และสิ่งที่ต้องปรับปรุงก่อนตอนนี้ (Audit & Gap Analysis)")

    add_body("จากการตรวจสอบโค้ดและผลลัพธ์ใน Phase 1 ที่ผ่านมา พบว่าระบบสามารถพิสูจน์แนวคิด (Proof of Concept) ได้เป็นอย่างดีบนชุดข้อมูลคลิปสั้น 22 คลิป แต่เมื่อเข้าสู่ Phase 2 ที่ต้องประมวลผลวิดีโอกล้องวงจรปิดรอบ 24 ชั่วโมงต่อเนื่องจาก 4 มุมกล้อง (Camera 1 – 4 รวม 25.5 GB) ระบบมีจุดที่ต้องปรับปรุงและยกระดับอย่างเร่งด่วนตามข้อกำหนดของอาจารย์ ดังตารางเปรียบเทียบต่อไปนี้:")

    # Table: Gap Analysis
    table_gap = doc.add_table(rows=6, cols=3)
    table_gap.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["มิติการประเมิน", "สถานะปัจจุบัน (Phase 1 Baseline)", "สิ่งที่ต้องปรับปรุงเร่งด่วนใน Phase 2"]
    widths = [Inches(1.8), Inches(2.5), Inches(2.7)]

    # Header Row
    for idx, name in enumerate(headers):
        cell = table_gap.cell(0, idx)
        cell.width = widths[idx]
        set_cell_background(cell, HEX_TEAL)
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        r = p.add_run(name)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    gaps_data = [
        ("1. การเลือกและเทรนโมเดล AI\n(AI Model & Training)",
         "ใช้ OpenCV MOG2 และนำโมเดล COCO Pretrained YOLOv8n มาทดสอบ Zero-shot ซึ่งจำแนกชะมดเป็น 'cat', 'dog' หรือ 'bear' โดยยังไม่ได้เทรนบนข้อมูลชะมดจริง",
         "ต้องสกัดเฟรมจาก CCTV กล้อง 1–4 ทำ Annotation สองคลาส (civet_active, civet_inactive) และ Fine-tune น้ำหนักโมเดล YOLOv8n ให้จำแนกพฤติกรรมได้โดยตรง"),
        ("2. ขอบเขตข้อมูลนำเข้า\n(Input Data Scope)",
         "ใช้คลิปสั้นที่ถูกตัดมาเฉพาะช่วงเกิดเหตุการณ์ 22 คลิป (คลิปละ 3–10 วินาที) ซึ่งตัดต่อแยกพฤติกรรมมาแล้ว",
         "ต้องคัดเลือกคลิปตัวแทนที่ดีที่สุดจากไฟล์วิดีโอยาว 24 ชม. (Camera 1–4) จัดการความหลากหลายของสภาพแสง (Day/Night IR) และมุมมองสิ่งกีดขวาง"),
        ("3. รูปแบบผลลัพธ์ระบบ\n(System Output Format)",
         "แยกสคริปต์ทำงาน 3 สคริปต์เดี่ยว (locomotion, eating, resting) ส่งผลลัพธ์เป็นภาพนิ่งแยกกัน",
         "ต้องรวมศูนย์เป็น Pipeline เดียวที่ส่งออกตาราง Active & Inactive Event Log (CSV) และสร้างกราฟสถิติ Activity Budget ประจำวัน"),
        ("4. การจัดการ Noise และแสง\n(Robustness & Noise)",
         "ใช้ Background Subtraction ซึ่งอ่อนไหวต่อแสงแดดสะท้อน ใบไม้ไหว และการเปลี่ยนโหมดอินฟราเรดของกล้อง",
         "สถาปัตยกรรม Deep Features (YOLOv8) ทนทานต่อแสงเงา ผสาน Zoological 1-Minute Rule ป้องกัน State Flickering"),
        ("5. ลิงก์ซอร์สโค้ดและชุดข้อมูล\n(Deliverables & Links)",
         "โค้ดอยู่ใน Local Workspace ไม่มีลิงก์สาธารณะและชุดข้อมูลที่ผ่านการ Label กำกับ",
         "จัดระเบียบ GitHub Repository ที่มี README ชัดเจน และสร้างโปรเจกต์ Annotation บน Roboflow เพื่อแนบลิงก์ส่งอาจารย์")
    ]

    for row_idx, row_content in enumerate(gaps_data, start=1):
        bg = HEX_BG_LIGHT if row_idx % 2 == 1 else 'FFFFFF'
        for col_idx, text in enumerate(row_content):
            cell = table_gap.cell(row_idx, col_idx)
            cell.width = widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.name = 'TH Sarabun New'
            r.font.size = Pt(12.5)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGB_TEAL
            elif col_idx == 2:
                r.font.bold = True
                r.font.color.rgb = RGB_DARK
            else:
                r.font.color.rgb = RGB_MUTED

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 4 Urgent bottlenecks
    add_h2("4 ปัญหาคอขวดที่ต้องแก้ไขทันทีก่อนเริ่มเทรนโมเดล")
    add_bullet("โมเดล Pretrained ทั่วไปจำแนกสัตว์ป่าผิดพลาด: ", "ปัญหาที่ 1: ")
    add_body("โมเดล COCO ไม่เคยเห็น 'ชะมดแผงสันหางดำ' (Large Indian Civet - Viverra zibetha) จึงมองเห็นเป็นสุนัขหรือแมว และไม่สามารถรู้ได้ว่าสัตว์กำลังนอนหลับหรือกำลังเดินหาอาหาร การ Fine-tune จึงเป็นเรื่องจำเป็นอย่างยิ่ง")

    add_bullet("การเปลี่ยนผ่านโหมดภาพกลางวันและอินฟราเรด (Daylight vs. Night IR): ", "ปัญหาที่ 2: ")
    add_body("กล้องวงจรปิดของสวนสัตว์เชียงใหม่จะสลับเป็นภาพขาวดำอินฟราเรด (IR Monochrome) ในช่วง 18:00 – 06:00 น. หากเทรนโมเดลด้วยภาพกลางวันอย่างเดียว โมเดลจะไม่สามารถตรวจจับในเวลากลางคืนได้ จึงต้องคัดเลือกภาพที่มีทั้งสองสภาวะแสง")

    add_bullet("ปรากฏการณ์สถานะกระพริบ (State Flickering): ", "ปัญหาที่ 3: ")
    add_body("ในธรรมชาติ ชะมดที่กำลังเดินหรือตื่นตัว อาจหยุดยืนนิ่งเป็นเวลา 2–3 วินาทีเพื่อดมกลิ่น หากระบบตัดสิน Active/Inactive จากภาพเฟรมเดี่ยว จะเกิดอาการสถานะกระพริบสลับไปมา จำเป็นต้องใช้กฎการหน่วงเวลา 1 นาที (1-Minute Zoological Smoothing) มากำกับ")

    add_bullet("ข้อจำกัดด้านเวลา (~14 ชั่วโมงก่อนเที่ยงวัน 31 ต.ค.): ", "ปัญหาที่ 4: ")
    add_body("ไม่สามารถรันการประมวลผลทั้ง 25.5 GB ได้ทันเวลาแน่นอน กลยุทธ์ที่ถูกต้องคือการคัดเลือกคลิปตัวแทนพฤติกรรมทองคำ (Representative Golden Clips) สกัดเฟรม 150–200 ภาพ แล้ว Fine-tune แบบ Low-Shot Learning ซึ่งจะใช้เวลาไม่เกิน 15 นาที")

    # ==================== ส่วนที่ 2: DATA SELECTION ====================
    add_h1("ส่วนที่ 2: กลยุทธ์การคัดเลือกข้อมูลที่เหมาะสมที่สุดจาก Google Drive (Representative Data Selection)")

    add_body("อาจารย์ระบุชัดเจนว่า: 'no need to run all data, just select the most suitable one' จากชุดข้อมูล Google Drive ซึ่งมีขนาด 25.5 GB (31 ไฟล์วิดีโอ) จาก Camera 1 – 4 เราได้วิเคราะห์และคัดเลือก 3 วิดีโอตัวแทนพฤติกรรมหลัก ที่มีความสมบูรณ์เชิงสัตววิทยาสูงสุด ดังนี้:")

    # Table of Golden Clips
    table_clips = doc.add_table(rows=4, cols=4)
    table_clips.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_headers = ["ซีนพฤติกรรม", "ไฟล์วิดีโอตัวแทนที่เลือก", "ช่วงเวลา / ความยาว", "เหตุผลความเหมาะสมทางเทคนิค"]
    c_widths = [Inches(1.5), Inches(2.2), Inches(1.5), Inches(2.0)]

    for idx, name in enumerate(c_headers):
        cell = table_clips.cell(0, idx)
        cell.width = c_widths[idx]
        set_cell_background(cell, HEX_TEAL)
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(name)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    clips_data = [
        ("ซีนที่ 1: Active / Feeding\n(การกินอาหาร & เดินสำรวจ)",
         "Camera 4:\nA04_11.07-12.40_dur_1h33m.mp4",
         "11:07 – 12:40 น.\n(กลางวัน / 1 ชม. 33 นาที)",
         "ชะมดลงมากินอาหารในถาดอาหารอย่างชัดเจน มีทั้งพฤติกรรมก้มกินอาหาร (Feeding) และเดินวนรอบถาด แสงแดดสว่าง คมชัดสูง"),
        ("ซีนที่ 2: Active / Locomotion\n(การออกหากินกลางคืน)",
         "Camera 3:\nA03_00.00-06.56_dur_6h56m.mp4",
         "00:00 – 02:00 น.\n(กลางคืน IR / คัด 1 ชม.)",
         "ชะมดตื่นออกหากิน ปีนป่ายโครงสร้างไม้และวิ่งข้ามห้อง เหมาะอย่างยิ่งสำหรับการทดสอบระบบในโหมด Night IR"),
        ("ซีนที่ 3: Inactive / Resting\n(การนอนหลับพักผ่อน)",
         "Camera 1 & Camera 3:\nA01_06.13-09.48_dur_3h35m.mp4",
         "06:13 – 09:48 น.\n(เช้าตรู่ / 3 ชม. 35 นาที)",
         "ชะมดนอนขดตัวนิ่งในรังยางรถยนต์ (Tire Bed) และบนแท่นไม้ เป็นตัวแทน Inactive ที่สมบูรณ์แบบเพื่อทดสอบเกณฑ์ 1-Minute Rule")
    ]

    for row_idx, row_content in enumerate(clips_data, start=1):
        bg = HEX_BG_LIGHT if row_idx % 2 == 1 else 'FFFFFF'
        for col_idx, text in enumerate(row_content):
            cell = table_clips.cell(row_idx, col_idx)
            cell.width = c_widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.name = 'TH Sarabun New'
            r.font.size = Pt(12)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGB_GOLD
            else:
                r.font.color.rgb = RGB_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_body("กระบวนการสกัดเฟรม (Frame Extraction Pipeline):", bold_prefix="ขั้นตอนการจัดเตรียมข้อมูล: ")
    add_bullet("สกัดภาพ 150 – 200 เฟรมจากคลิปตัวแทนทั้ง 3 โดยใช้อัตราการสุ่มแบบกระจายสม่ำเสมอ (Uniform Sampling) ผสมกับการสุ่มเน้นช่วงเกิดพฤติกรรม (Event-Triggered Sampling)")
    add_bullet("จัดเก็บเฟรมภาพที่มีความหลากหลายของมุมกล้อง (Cam 1, 3, 4) และสภาวะแสง (กลางวัน 60% และอินฟราเรดกลางคืน 40%) เพื่อให้โมเดลมี Generalization สูง")
    add_bullet("ใช้ระบบตรวจจับและรูปภาพที่สกัดไว้แล้วบางส่วนใน pic/inspections/cam1_cam4_presence เพื่อประหยัดเวลาและเริ่มกระบวนการ Labeling ได้ทันที")

    # ==================== ส่วนที่ 3: MODEL SELECTION ====================
    add_h1("ส่วนที่ 3: การเลือกและอธิบายโมเดล AI ในเชิงลึก (AI Model Selection & Architecture Explanation)")

    add_body("สำหรับ Phase 2 เราเลือกสถาปัตยกรรม YOLOv8 Nano (YOLOv8n) ในการทำ Transfer Learning & Fine-Tuning เพื่อจำแนกสถานะพฤติกรรมแบบ End-to-End โดยมีรายละเอียดทางเทคนิคและเหตุผลสนับสนุนเชิงวิชาการ ดังนี้:")

    add_h2("1. สถาปัตยกรรมเครือข่ายของ YOLOv8 (Architectural Breakdown)")
    add_bullet("Backbone (Modified CSPDarknet53 + C2f): ", "1.1 โครงข่ายหลัก: ")
    add_body("โครงสร้างกระดูกสันหลังใช้โมดูล C2f (Cross-Stage Partial with 2 Convolutions) ซึ่งพัฒนาต่อยอดจากโมดูล C3 ใน YOLOv5 โดย C2f รวมเอาแนวคิด Split-and-Concatenate ของ ELAN เข้ามา ช่วยให้การไหลเวียนของเกรเดียนต์ (Gradient Flow) ในการคำนวณ Backpropagation มีความต่อเนื่องสูง สามารถจับลวดลายขน รูปร่างลำตัว และใบหน้าของชะมดได้ละเอียดแม้ภาพจะเบลอจากการเคลื่อนไหว พร้อมทั้งโมดูล SPPF (Spatial Pyramid Pooling Fast) เพื่อดึงคุณลักษณะที่ Multi-scale ที่ระดับชั้นลึกสุด")

    add_bullet("Neck (PAN-FPN Feature Fusion): ", "1.2 คอเครือข่าย: ")
    add_body("ใช้โครงสร้างผสมผสานระหว่าง Feature Pyramid Network (FPN) จากบนลงล่าง และ Path Aggregation Network (PAN) จากล่างขึ้นบน ทำให้ Features ระดับต่ำที่มีข้อมูลพิกัดแม่นยำ (Spatial Resolution) ผสานเข้ากับ Features ระดับสูงที่มีข้อมูลความหมายเชิงลึก (Semantic Features) ช่วยให้ระบบตรวจจับชะมดได้ทั้งเมื่ออยู่ใกล้หน้ากล้อง (กล้อง 4 ถาดอาหาร) และเมื่ออยู่ไกลท้ายกรง (กล้อง 1 ขอนไม้)")

    add_bullet("Head (Decoupled Anchor-Free Detection Head): ", "1.3 ส่วนหัวการตรวจจับ: ")
    add_body("YOLOv8 เปลี่ยนจาก Anchor-based ในอดีตมาเป็น Anchor-free Head อย่างสมบูรณ์ โดยแยกกิ่งการจำแนกประเภท (Classification Branch) และกิ่งการทำนายกรอบพิกัด (Bounding Box Regression Branch) ออกจากกันอย่างเด็ดขาด ข้อดีคือช่วยลดปัญหาเมื่อชะมดนอนขดตัวซึ่งมีอัตราส่วนกรอบ (Aspect Ratio) เป็นรูปไข่หรือวงกลม เทียบกับตอนชะมดยืดตัวเดินซึ่งเป็นสี่เหลี่ยมผืนผ้าแนวนอน")

    add_bullet("Loss Functions (ฟังก์ชันการสูญเสียร่วม 3 ตัว): ", "1.4 ฟังก์ชันวัดการสูญเสีย: ")
    add_body("สูตรคำนวณการสูญเสียรวมของระบบประกอบด้วย 3 ส่วนหลัก:\n"
             "• Complete IoU Loss (L_CIoU): วัดความทับซ้อนของ Bounding Box โดยคำนึงถึงระยะห่างจุดกึ่งกลางและอัตราส่วนกว้าง-ยาว\n"
             "• Distribution Focal Loss (L_DFL): ช่วยให้ขอบเขตพิกัดมีความยืดหยุ่นต่อสิ่งกีดขวาง เช่น ขอบกรงหรือกิ่งไม้\n"
             "• Binary Cross-Entropy Loss (L_BCE): คำนวณความคลาดเคลื่อนในการจำแนกคลาส (civet_active vs civet_inactive)")

    add_h2("2. เหตุผลที่เลือก YOLOv8 เหนือโมเดลทางเลือกอื่น (Model Justification)")

    # Comparison Table
    table_models = doc.add_table(rows=5, cols=4)
    table_models.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_headers = ["สถาปัตยกรรมโมเดล", "ความเร็วประมวลผล (FPS)", "ขนาดโมเดล / Params", "ความเหมาะสมกับงานเฝ้าระวังชะมด"]
    m_widths = [Inches(1.8), Inches(1.5), Inches(1.6), Inches(2.3)]

    for idx, name in enumerate(m_headers):
        cell = table_models.cell(0, idx)
        cell.width = m_widths[idx]
        set_cell_background(cell, HEX_TEAL)
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(name)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    models_data = [
        ("YOLOv8 Nano (เลือกใช้)\n(Ultralytics)", "45 – 65 FPS\n(Real-time สูง)", "3.2M Params\n(6.2 MB)", "เหมาะสมสูงสุด: น้ำหนักเบา เทรนไว ใช้ GPU แล็ปท็อปหรือ CPU ได้สบาย ทนต่อแสง IR และจำแนกได้ในตัว"),
        ("Faster R-CNN\n(Two-Stage)", "8 – 15 FPS\n(ไม่เรียลไทม์)", "41.5M Params\n(160 MB)", "ข้อจำกัด: หนักเกินไป ประมวลผลช้า กิน VRAM สูง และเสี่ยงต่อการเกิด Overfitting เมื่อข้อมูลมีจำกัด"),
        ("SSD-MobileNetV3\n(Single-Stage)", "30 – 40 FPS\n(Real-time)", "4.8M Params\n(19 MB)", "ข้อจำกัด: ยังเป็น Anchor-based พลาดง่ายเมื่อชะมดขดตัวนอน และความแม่นยำในแสงน้อยต่ำกว่า YOLOv8"),
        ("Vision Transformer\n(RT-DETR)", "18 – 25 FPS\n(ปานกลาง)", "32.0M Params\n(125 MB)", "ข้อจำกัด: ต้องการชุดข้อมูลขนาดใหญ่มากในการ Pretrain หากเทรนบน Low-shot dataset ประสิทธิภาพจะไม่เสถียร")
    ]

    for row_idx, row_content in enumerate(models_data, start=1):
        bg = HEX_BG_LIGHT if row_idx % 2 == 1 else 'FFFFFF'
        for col_idx, text in enumerate(row_content):
            cell = table_models.cell(row_idx, col_idx)
            cell.width = m_widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.name = 'TH Sarabun New'
            r.font.size = Pt(12)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGB_TEAL if "เลือกใช้" in text else RGB_DARK
            elif col_idx == 3 and "เหมาะสมสูงสุด" in text:
                r.font.bold = True
                r.font.color.rgb = RGB_EMERALD
            else:
                r.font.color.rgb = RGB_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ==================== ส่วนที่ 4: OUTPUT DESIGN & EVALUATION ====================
    add_h1("ส่วนที่ 4: การออกแบบระบบผลลัพธ์และการประเมินผล (System Output Design & Evaluation)")

    add_body("ตามข้อกำหนด 'Design and evaluate the output of the system (active and inactive table or any visualization)' เราได้ออกแบบโครงสร้างระบบส่งมอบผลลัพธ์เป็น 3 ระดับที่สอดคล้องกับมาตรฐานทางสัตววิทยาและวิทยาการคอมพิวเตอร์ ดังนี้:")

    add_h2("1. ตารางบันทึกเหตุการณ์พฤติกรรม (Active / Inactive Event Log Table Schema)")
    add_body("ระบบจะส่งออกผลการวิเคราะห์พฤติกรรมเป็นตารางบันทึกแบบเรียลไทม์ (บันทึกลงไฟล์ CSV และ DataFrame) โดยมีโครงสร้างคอลัมน์มาตรฐานดังนี้:")

    # Table Schema
    table_schema = doc.add_table(rows=7, cols=3)
    table_schema.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["ชื่อคอลัมน์ (Column Name)", "ประเภทข้อมูล", "คำอธิบายความหมายทางสัตววิทยาและเทคนิค"]
    s_widths = [Inches(2.2), Inches(1.3), Inches(3.7)]

    for idx, name in enumerate(s_headers):
        cell = table_schema.cell(0, idx)
        cell.width = s_widths[idx]
        set_cell_background(cell, HEX_TEAL)
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(name)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    schema_data = [
        ("timestamp", "DATETIME", "วันเวลาที่ตรวจพบเหตุการณ์ตามเวลาจริงของกล้องวงจรปิด (เช่น 2026-04-05 11:15:30)"),
        ("camera_id", "STRING", "รหัสระบุตำแหน่งกล้องในกรงเลี้ยง (Camera 1, Camera 2, Camera 3, Camera 4)"),
        ("behavior_state", "ENUM", "สถานะหลักตามโจทย์อาจารย์: 'ACTIVE' (ตื่น/เคลื่อนไหว) หรือ 'INACTIVE' (นอน/พักผ่อน)"),
        ("sub_behavior", "STRING", "พฤติกรรมย่อยที่ระบุได้: 'Locomotion' (เดิน), 'Feeding' (กิน), 'Resting' (นอนในรัง)"),
        ("confidence_score", "FLOAT [0.0-1.0]", "ระดับความเชื่อมั่นของโมเดล YOLOv8 ในการทำนายสถานะนั้นๆ"),
        ("duration_seconds", "FLOAT", "ระยะเวลาที่ดำรงพฤติกรรมต่อเนื่อง (Persistent Duration) ผ่านการกรอง 1-Minute Rule")
    ]

    for row_idx, row_content in enumerate(schema_data, start=1):
        bg = HEX_BG_LIGHT if row_idx % 2 == 1 else 'FFFFFF'
        for col_idx, text in enumerate(row_content):
            cell = table_schema.cell(row_idx, col_idx)
            cell.width = s_widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.name = 'TH Sarabun New'
            r.font.size = Pt(12)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGB_TEAL
            else:
                r.font.color.rgb = RGB_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_h2("2. การสร้างภาพสรุปผลเชิงสถิติ (Visualizations)")
    add_bullet("2.1 กราฟสัดส่วนการใช้เวลาประจำวัน (24-Hour Activity Budget Donut Chart): ", "แผนภาพที่ 1: ")
    add_body("แสดงสัดส่วนร้อยละของเวลาที่ชะมดใช้ในการ Active (เดิน/กิน/สำรวจ) เปรียบเทียบกับ Inactive (นอนหลับในรังยาง/นอนบนขอนไม้) ซึ่งเป็นดัชนีสำคัญที่สุดในการประเมินสวัสดิภาพสัตว์ (Animal Welfare Assessment)")

    add_bullet("2.2 กราฟพฤติกรรมเชิงเวลา (Temporal Ethogram / 24-hr Actogram): ", "แผนภาพที่ 2: ")
    add_body("แผนภูมิแท่งรายชั่วโมง (Stacked Bar Chart 00:00 – 23:00) แสดงจำนวนนาทีที่เป็น Active และ Inactive ในแต่ละชั่วโมง ช่วยให้สัตวแพทย์และผู้ดูแลสัตว์เห็นรอบการออกหากินกลางคืน (Nocturnal Rhythm) ได้อย่างชัดเจน")

    add_bullet("2.3 วิดีโอและภาพเฟรมตัวอย่างพร้อม Telemetry Overlay: ", "แผนภาพที่ 3: ")
    add_body("เฟรมภาพวิดีโอที่ตีกรอบ Bounding Box รอบตัวชะมด พร้อมแท็กระบุสถานะสีเขียว [ACTIVE] หรือสีส้ม [INACTIVE] แสดงค่า Confidence และแถบข้อมูลสถานะ (Status Banner) ด้านบน")

    add_h2("3. ระเบียบวิธีและตัวชี้วัดการประเมินผล (Evaluation Framework)")
    add_body("การประเมินความสำเร็จของระบบจะแบ่งเป็น 2 มิติที่เข้มข้น:")
    add_bullet("การประเมินทาง Computer Vision (AI Metrics): ", "มิติด้านเทคนิค: ")
    add_body("• Precision (ความแม่นยำในการระบุพฤติกรรม ไม่ให้มี False Positive)\n"
             "• Recall (ความสามารถในการตรวจจับชะมด ไม่หลุดหายแม้ในมุมมืด)\n"
             "• mAP@0.5 (Mean Average Precision ที่ IoU threshold 0.50)\n"
             "• Confusion Matrix (ตารางแสดงการทำนายสับสนระหว่าง Active vs Inactive)")

    add_bullet("การประเมินทางสัตววิทยา (Zoological Validation): ", "มิติด้านชีววิทยา: ")
    add_body("ทดสอบความสอดคล้องกับเกณฑ์ 1-Minute Rule โดยการหยุดนิ่งสั้นๆ ไม่เกิน 60 วินาทีต้องไม่ถูกจัดเป็น Inactive เพื่อรักษาความถูกต้องตามพฤติกรรมสัตว์จริง")

    # ==================== ส่วนที่ 5: DELIVERABLES ====================
    add_h1("ส่วนที่ 5: การจัดเตรียม Source Code และ Annotation Deliverables (GitHub & Roboflow)")

    add_body("ตามข้อกำหนด 'Provide the github/annotation link of your source code' เราได้จัดเตรียมโครงสร้างการส่งมอบงานให้พร้อมสำหรับการตรวจสอบของอาจารย์:")

    add_h2("1. โครงสร้าง GitHub Repository")
    add_body("โปรเจกต์ได้รับการจัดหมวดหมู่ไฟล์ให้ได้มาตรฐานงานวิจัย พร้อมไฟล์ README.md อธิบายขั้นตอนการทำงานอย่างเป็นระบบ:")
    add_bullet("docs/ : บันทึกข้อกำหนดเชิงเทคนิค แผนงาน Phase 2 และสคริปต์สไลด์")
    add_bullet("dataset/ : ชุดข้อมูลวิดีโอ CCTV และไฟล์ json แมปเวลาและกล้อง")
    add_bullet("models/ : ไฟล์น้ำหนักโมเดลที่ผ่านการเทรน (best.pt) และไฟล์คอนฟิก yaml")
    add_bullet("scripts/ : สคริปต์การสกัดเฟรม, การเทรนโมเดล, และการสร้างกราฟ Active/Inactive")
    add_bullet("presentations/ : สไลด์นำเสนอ Phase 2 (PPTX) และเอกสารสรุป")

    add_h2("2. การจัดทำและส่งมอบลิงก์ Annotation บน Roboflow")
    add_body("เพื่อให้อาจารย์สามารถตรวจสอบการทำ Ground Truth และ Bounding Box ได้อย่างโปร่งใส:\n"
             "• อัปโหลดภาพตัวแทน 150 เฟรมขึ้นสู่ Roboflow Universe (Public Project)\n"
             "• กำกับ Label ชัดเจน 2 คลาส: 'civet_active' และ 'civet_inactive'\n"
             "• ส่งออกชุดข้อมูลในฟอร์แมต 'YOLOv8' เพื่อนำมาใช้เทรนและแนบลิงก์ชุดข้อมูลในรายงานส่งงาน")

    # ==================== ส่วนที่ 6: ROADMAP & PRESENTATION ====================
    add_h1("ส่วนที่ 6: แผนงานนับถอยหลังรายชั่วโมง (Hour-by-Hour Roadmap สู่เส้นตาย 12:00 น.)")

    add_body("เหลือเวลาอีกประมาณ 14 ชั่วโมงก่อนกำหนดส่งงานในวันเสาร์ที่ 31 ตุลาคม 2569 เวลา 12:00 น. ตารางการทำงานนับถอยหลังนี้ถูกออกแบบเพื่อให้ส่งงานได้สมบูรณ์และทันเวลา 100%:")

    # Table Roadmap
    table_road = doc.add_table(rows=8, cols=3)
    table_road.alignment = WD_TABLE_ALIGNMENT.CENTER
    r_headers = ["ช่วงเวลา (Time Window)", "ภารกิจหลักที่ต้องดำเนินงาน (Milestone Tasks)", "ผลลัพธ์ที่ได้ (Deliverables)"]
    r_widths = [Inches(1.8), Inches(3.2), Inches(2.2)]

    for idx, name in enumerate(r_headers):
        cell = table_road.cell(0, idx)
        cell.width = r_widths[idx]
        set_cell_background(cell, HEX_TEAL)
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(name)
        r.font.name = 'TH Sarabun New'
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    roadmap_data = [
        ("22:00 – 23:00 น.\n(คืนวันที่ 30 ต.ค.)", "อนุมัติแผนงาน Phase 2 และสร้างเอกสาร Audit ลงโฟลเดอร์ recheck/", "ไฟล์ Word ฉบับสมบูรณ์ใน recheck/ และ Implementation Plan"),
        ("23:00 – 01:00 น.\n(คืนวันที่ 30 ต.ค.)", "คัดเลือกเฟรม 150 ภาพ และจัดทำ Annotation 2 คลาส (Roboflow)", "ชุดข้อมูล YOLO Dataset พร้อม data.yaml และ Roboflow Link"),
        ("01:00 – 02:30 น.\n(เช้ามืด 31 ต.ค.)", "เทรนโมเดล YOLOv8n (30 Epochs) ด้วย GPU RTX 3050 / CPU", "ไฟล์น้ำหนักโมเดล best.pt, กราฟ Loss และ Confusion Matrix"),
        ("02:30 – 04:30 น.\n(เช้ามืด 31 ต.ค.)", "รัน Pipeline สร้างตาราง Active/Inactive CSV และกราฟสรุปสถิติ", "civet_activity_event_log.csv และกราฟ Activity Budget PNG"),
        ("04:30 – 08:30 น.\n(เช้า 31 ต.ค.)", "ช่วงเวลาสำรอง / พักผ่อน (Buffer Time)", "ตรวจสอบผลลัพธ์การรัน และเตรียมสไลด์นำเสนอ"),
        ("08:30 – 11:30 น.\n(เช้า 31 ต.ค.)", "อัปเดตสไลด์ PowerPoint สำหรับการนำเสนอ และเตรียมลิงก์ส่งงาน", "ไฟล์ PPTX Phase 2 ฉบับสมบูรณ์ พร้อมบทพูดนำเสนอ"),
        ("11:30 – 12:00 น.\n(31 ต.ค. DEADLINE)", "ตรวจสอบความถูกต้องขั้นสุดท้าย และส่งมอบงานตามฟอร์มอาจารย์", "ส่งมอบงานครบถ้วนก่อนเที่ยงวัน 31 ต.ค. 100%")
    ]

    for row_idx, row_content in enumerate(roadmap_data, start=1):
        bg = HEX_BG_LIGHT if row_idx % 2 == 1 else 'FFFFFF'
        for col_idx, text in enumerate(row_content):
            cell = table_road.cell(row_idx, col_idx)
            cell.width = r_widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(text)
            r.font.name = 'TH Sarabun New'
            r.font.size = Pt(12)
            if col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGB_TEAL
            elif "DEADLINE" in text:
                r.font.bold = True
                r.font.color.rgb = RGBColor(225, 29, 72)
            else:
                r.font.color.rgb = RGB_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2("การเตรียมตัวนำเสนอผลงาน (Final Presentation Defense: 31 ต.ค. – 3 พ.ย.)")
    add_body("สำหรับช่วงเวลานำเสนอผลงาน (15:00 – 18:00 น.) แนวคำถามสำคัญที่คาดว่าอาจารย์จะซักถามและแนวทางคำตอบที่เตรียมไว้:")
    add_bullet("แนวคำตอบ: ", "คำถามที่ 1: ทำไมถึงไม่เทรนข้อมูลทั้งหมด 25 GB? ")
    add_body("การเทรนวิดีโอวงจรปิดที่มีเฟรมซ้ำซ้อน (Redundant Frames) ในห้องว่างจะทำให้โมเดลเกิด Overfitting ต่อฉากหลัง การคัดเลือก Representative Frames ที่มีความหลากหลายของพฤติกรรม แสง Day/Night และมุมกล้อง ให้ผลลัพธ์ mAP ที่สูงกว่าและใช้เวลาเทรนได้อย่างคุ้มค่าสูงสุด")

    add_bullet("แนวคำตอบ: ", "คำถามที่ 2: ระบบแยกแยะระหว่าง 'สัตว์ยืนนิ่งชั่วคราว' กับ 'สัตว์นอนหลับ' อย่างไร? ")
    add_body("ระบบใช้การผสานรวมระหว่าง Visual Feature จากโมเดล YOLOv8 (ท่วงท่านอนราบ/ขดตัว) ร่วมกับตรรกะทางสัตววิทยา '1-Minute Inactivity Rule' หากสัตว์หยุดเคลื่อนไหวแต่น้อยกว่า 60 วินาที ระบบจะยังคงสถานะ Active ไว้ เพื่อไม่ให้เกิด State Flickering")

    # Output file path
    out_dir = r"D:\CMU\4th\1 st\image processing\project cmz\recheck"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "Phase2_Master_Plan_and_Current_Audit.docx")
    doc.save(out_path)
    print(f"Successfully generated Word document at: {out_path}")

if __name__ == "__main__":
    create_phase2_plan_document()
