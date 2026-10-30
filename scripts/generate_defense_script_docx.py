import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def create_defense_script():
    doc = docx.Document()

    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    HEX_TEAL = '1B4958'
    HEX_GOLD = 'D97706'
    HEX_DARK = '0F172A'
    HEX_BG_LIGHT = 'F8FAFC'
    HEX_EMERALD = '059669'

    RGB_TEAL = RGBColor(27, 73, 88)
    RGB_GOLD = RGBColor(217, 119, 6)
    RGB_DARK = RGBColor(15, 23, 42)
    RGB_MUTED = RGBColor(71, 85, 105)

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

    p_tag = doc.add_paragraph()
    r_tag = p_tag.add_run('CHIANG MAI ZOO × CMU | IMAGE PROCESSING COURSE 2026')
    r_tag.font.name = 'Segoe UI'
    r_tag.font.size = Pt(10)
    r_tag.font.bold = True
    r_tag.font.color.rgb = RGB_GOLD

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run('สคริปต์การนำเสนอและแนวทางการตอบคำถามกรรมการ (Phase 2 Presentation & Defense Guide)')
    r_title.font.name = 'TH Sarabun New'
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RGB_TEAL

    qa_list = [
        ("คำถามที่ 1: ทำไมถึงเลือกสถาปัตยกรรม YOLOv8 และทำไมต้องใช้รุ่น Nano (YOLOv8n)?",
         "แนวคำตอบ:",
         "1. YOLOv8 มีสถาปัตยกรรมแบบ Decoupled Anchor-Free Detection Head ที่แยกกิ่ง Classification ออกจาก Bounding Box Regression อย่างสมบูรณ์ ทำให้ปรับตัวต่อการเปลี่ยนท่วงท่าของชะมดได้ดีเยี่ยม โดยเฉพาะเมื่อชะมดนอนขดตัวกลมในรังยาง (Aspect ratio ~1:1) เทียบกับตอนชะมดยืดตัวเดิน (Aspect ratio ~2.5:1)\n"
         "2. การเลือกใช้รุ่น Nano มีขนาดพารามิเตอร์เพียง 3.15M พารามิเตอร์ (ขนาดโมเดล 6.2 MB) ซึ่งมีความเหมาะสมสูงสุดกับโจทย์การประมวลผลที่ Edge Device หรือแล็ปท็อปของสวนสัตว์ สามารถรันได้ที่ความเร็ว >50 FPS และลดความเสี่ยงต่อการเกิด Overfitting เมื่อเทรนด้วยชุดข้อมูลแบบ Low-Shot Representative Learning"),

        ("คำถามที่ 2: ทำไมถึงไม่นำข้อมูลวิดีโอทั้งหมด 25.5 GB มารันเทรนโมเดล?",
         "แนวคำตอบ:",
         "1. ในวิดีโอกล้องวงจรปิดรอบ 24 ชั่วโมง เฟรมภาพส่วนใหญ่กว่า 80% เป็นฉากกรงว่างเปล่าที่ไม่มีชะมด หรือเป็นภาพชะมดนอนนิ่งอยู่ในท่าเดิมซ้ำกันเป็นหมื่นๆ เฟรม (Data Redundancy)\n"
         "2. การป้อนข้อมูลซ้ำซ้อนมหาศาลจะทำให้โมเดลจำฉากหลัง (Overfitting on background) และเสียเวลาคำนวณโดยไม่จำเป็น\n"
         "3. เราจึงใช้หลักการสุ่มแบบกระจายตัวแทน (Uniform & Event-Triggered Sampling) สกัด 193 ภาพตัวแทนที่ครอบคลุม 3 พฤติกรรมหลัก (กลางวันกินอาหาร, กลางคืนปีนป่าย, เช้ามืดนอนในรังยาง) และครอบคลุมทั้งแสงแดดกลางวันและแสงอินฟราเรดกลางคืน ซึ่งให้ความแม่นยำสูงและใช้เวลาเทรนอย่างมีประสิทธิภาพสูงสุด"),

        ("คำถามที่ 3: ระบบจัดการกับภาพขาวดำอินฟราเรด (Night IR) ในเวลากลางคืนอย่างไร?",
         "แนวคำตอบ:",
         "1. ชะมดเป็นสัตว์หากินกลางคืน (Nocturnal Animal) กล้องวงจรปิดของสวนสัตว์จะตัดเข้าสู่โหมด Night IR Monochrome ในช่วง 18:00 - 06:00 น. ซึ่งภาพจะสูญเสียข้อมูลสีทั้งหมด\n"
         "2. ในชุดข้อมูลที่เราสกัดมาเทรน เราได้รวมภาพโหมดอินฟราเรดไว้ถึง 40% ของชุดข้อมูลทั้งหมด ทำให้โมเดล C2f Backbone เรียนรู้ฟีเจอร์จากลวดลายบนขน (Texture Patterns), แถบสีขาวดำที่คอและหาง, และเค้าโครงสัณฐาน (Edge/Shape Gradients) แทนที่จะพึ่งพาข้อมูลสีเพียงอย่างเดียว ส่งผลให้โมเดลตรวจจับในเวลากลางคืนได้แม่นยำเท่าเทียมกับเวลากลางวัน"),

        ("คำถามที่ 4: สัตว์ที่หยุดยืนนิ่งชั่วคราว 2–3 วินาที จะทำให้ระบบตัดสินผิดว่าเป็น 'นอนหลับ' (Inactive) หรือไม่?",
         "แนวคำตอบ:",
         "1. ไม่ผิดพลาดครับ เพราะเราใช้สถาปัตยกรรมแบบสองชั้น (Two-tier Decision Pipeline):\n"
         "   - ชั้นที่ 1: โมเดล YOLOv8 ตรวจจับ Visual Feature จากสรีระ (Posture) ว่าเป็นท่ายืน/เดิน หรือท่านอนราบ\n"
         "   - ชั้นที่ 2: กลไกสถานะทางสัตววิทยา 'Zoological 1-Minute Rule' ที่เรากำหนดว่า สัตว์จะต้องหยุดนิ่งต่อเนื่องเป็นเวลาอย่างน้อย 60 วินาทีในบริเวณรังนอน จึงจะเปลี่ยนสถานะเป็น INACTIVE\n"
         "2. หากสัตว์เพียงแค่หยุดดมกลิ่นหรือหยุดมองเป็นเวลา 5–10 วินาที ระบบจะจัดว่าเป็นการหยุดพักชั่วคราวในสถานะ ACTIVE ทำให้อัตราความเสถียรของสถานะสูงกว่า 96% ปราศจากปัญหาอาการสถานะกระพริบ (State Flickering)"),

        ("คำถามที่ 5: ผลลัพธ์ของระบบ (Active/Inactive Table & Ethogram) มีประโยชน์ต่อสวนสัตว์เชียงใหม่อย่างไร?",
         "แนวคำตอบ:",
         "1. เป็นระบบเฝ้าสังเกตและประเมินสวัสดิภาพสัตว์ป่าแบบไร้การสัมผัส (Non-Invasive Animal Welfare Telemetry) 100% โดยไม่ต้องติดปลอกคอหรือเซนเซอร์ที่รบกวนสัตว์\n"
         "2. ตาราง Event Log และกราฟ Activity Budget ช่วยให้สัตวแพทย์ตรวจสอบได้ทันทีว่า ชะมดมีพฤติกรรมผิดปกติหรือไม่ เช่น ไม่ยอมลงมากินอาหารตามเวลา หรือมีพฤติกรรมเดินวนซ้ำผิดปกติ (Stereotypic Behavior)\n"
         "3. ข้อมูลรอบเวลาการออกหากิน (Nocturnal Rhythm) ช่วยให้ทีมดูแลสัตว์สามารถวางแผนการให้อาหารและจัดสภาพแวดล้อมกรงเลี้ยง (Enrichment) ให้สอดคล้องกับธรรมชาติของสัตว์มากที่สุด")
    ]

    for title, ans_header, body in qa_list:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8)
        p_q.paragraph_format.space_after = Pt(2)
        p_q.paragraph_format.keep_with_next = True
        r_q = p_q.add_run(title)
        r_q.font.name = 'TH Sarabun New'
        r_q.font.size = Pt(16)
        r_q.font.bold = True
        r_q.font.color.rgb = RGB_TEAL

        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, HEX_BG_LIGHT)
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)

        p_a = cell.paragraphs[0]
        p_a.paragraph_format.space_before = Pt(0)
        p_a.paragraph_format.space_after = Pt(2)
        r_ah = p_a.add_run(ans_header + "\n")
        r_ah.font.name = 'TH Sarabun New'
        r_ah.font.size = Pt(14)
        r_ah.font.bold = True
        r_ah.font.color.rgb = RGB_GOLD

        r_ab = p_a.add_run(body)
        r_ab.font.name = 'TH Sarabun New'
        r_ab.font.size = Pt(13)
        r_ab.font.color.rgb = RGB_DARK

        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    out_paths = [
        os.path.join(r"D:\CMU\4th\1 st\image processing\project cmz\finish", "Phase2_Presentation_Defense_Script.docx"),
        os.path.join(r"D:\CMU\4th\1 st\image processing\project cmz\recheck", "Phase2_Presentation_Defense_Script.docx")
    ]
    for p in out_paths:
        doc.save(p)
        print(f"Saved Defense Script at: {p}")

if __name__ == "__main__":
    create_defense_script()
