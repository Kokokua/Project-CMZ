import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os

def create_script_docx():
    doc = Document()
    
    # Page setup
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Styles
    C_TEAL = RGBColor(27, 73, 88)
    C_GOLD = RGBColor(229, 169, 60)
    C_DARK = RGBColor(15, 23, 42)
    C_MUTED = RGBColor(100, 116, 139)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cat = p_title.add_run("CHIANG MAI ZOO × CHIANG MAI UNIVERSITY | IMAGE PROCESSING 2026\n")
    r_cat.font.name = "Segoe UI"
    r_cat.font.size = Pt(11)
    r_cat.font.bold = True
    r_cat.font.color.rgb = C_GOLD

    r_main = p_title.add_run("Phase 2 Presentation & Defense Script (9 Slides)\n")
    r_main.font.name = "Segoe UI"
    r_main.font.size = Pt(22)
    r_main.font.bold = True
    r_main.font.color.rgb = C_TEAL

    r_sub = p_title.add_run("Deep Learning Results, Real CCTV Video Evidence & Practical Zoo Solutions\n")
    r_sub.font.name = "Segoe UI"
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = C_MUTED

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_line = p_line.add_run("―" * 55)
    r_line.font.color.rgb = C_GOLD

    slides_script = [
        ("Slide 1: Cover / Title Slide",
         "SMART ZOO MONITORING: Automated Civet Behavior Monitoring System (Phase 2)",
         "แนะนำตัวและเปิดประเด็นเข้าสู่งาน Phase 2",
         "Good afternoon Ajarn and committee members. Today, our team presents Phase 2 of the Automated Civet Behavior Monitoring System for Chiang Mai Zoo. While Phase 1 explored traditional computer vision heuristics, Phase 2 cuts straight to the core: deploying a custom, domain-adapted YOLOv8 deep learning model directly onto real 24-hour zoo security camera footage. Today, we will present our 86.2% mAP detection results, live video evidence of feeding, nocturnal locomotion, and resting, as well as our automated 24-hour behavioral health logs.",
         "สวัสดีครับอาจารย์และคณะกรรมการ วันนี้กลุ่มของพวกเราขอนำเสนอความคืบหน้าของโครงการใน Phase 2 ซึ่งในเฟสนี้เรามุ่งเน้นที่ 'ผลลัพธ์จริงจากการประยุกต์ใช้โมเดล Deep Learning' โดยตรง เราได้แก้ปัญหาข้อจำกัดของเฟสแรกด้วยการเทรน YOLOv8 เฉพาะทางบนภาพกล้องวงจรปิดจริงของสวนสัตว์เชียงใหม่ ได้ค่าความแม่นยำ mAP สูงถึง 86.2% พร้อมนำเสนอหลักฐานคลิปวิดีโอผลลัพธ์ทั้ง 3 พฤติกรรม และตารางบันทึกพฤติกรรม 24 ชั่วโมงแบบอัตโนมัติครับ"),

        ("Slide 2: The Evolution (Phase 1 vs Phase 2)",
         "Overcoming Phase 1 Limitations with Custom Deep Learning",
         "เปรียบเทียบจุดเปลี่ยนสำคัญจาก Phase 1 สู่ Phase 2",
         "In Phase 1, our traditional vision baseline suffered from four major bottlenecks: severe blindness in black-and-white night infrared video, frequent false alarms from static potted plants, inability to handle changing civet sleeping postures, and fragile manual calibration. In Phase 2, we completely solved these by training a domain-adapted YOLOv8n model with empty-enclosure negative samples and 40% infrared night data. This decoupled our visual detection from behavioral logic, eliminating false alarms and achieving continuous 24/7 reliability.",
         "ในสไลด์นี้เปรียบเทียบให้เห็นจุดเปลี่ยนสำคัญครับ ใน Phase 1 วิธีดั้งเดิมติดปัญหาใหญ่ 4 ข้อ คือ มองไม่เห็นชะมดในโหมดอินฟราเรดกลางคืน, มักตรวจจับกระถางต้นไม้ผิดพลาดเป็นสัตว์, ไม่ยืดหยุ่นต่อท่วงท่านอนขดกลม, และต้องตั้งค่าแสงใหม่ตลอดเวลา ใน Phase 2 เราจึงเปลี่ยนมาใช้โมเดล Deep Learning ที่เทรนด้วยข้อมูลสวนสัตว์โดยตรง มีการใส่ภาพกรงเปล่าเพื่อตัด False Positive และเพิ่มภาพอินฟราเรดกลางคืน ทำให้ระบบมีความทนทานและพร้อมรันได้ตลอด 24 ชั่วโมงครับ"),

        ("Slide 3: AI Performance & Architecture",
         "Trained & Validated on Real Chiang Mai Zoo CCTV (86.2% mAP)",
         "ชี้แจงตัวเลขผลการเทรนและประสิทธิภาพเชิงปริมาณ",
         "Our custom YOLOv8 Nano model achieves an overall mAP@50 of 86.2%, with a Precision of 82.5% and Recall of 78.4%. The model was trained using 193 representative keyframes curated across all four CCTV cameras, optimized via CIoU box regression, Distribution Focal Loss, and BCE classification loss. Most importantly for real-world deployment, the model has only 3.0 million parameters (6.2 MB) and executes at over 60 FPS on a laptop GPU and 33.5 FPS on a standard CPU, making it perfectly suited for edge camera hardware.",
         "ด้านประสิทธิภาพเชิงปริมาณ โมเดลของเราทำค่า mAP@50 ได้สูงถึง 86.2% โดยมี Precision 82.5% และ Recall 78.4% จากการคัดเลือกภาพตัวแทนทองคำ 193 ภาพครอบคลุมทั้ง 4 กล้อง ที่สำคัญคือโมเดลมีขนาดกะทัดรัดมากเพียง 6.2 MB (3.0 ล้านพารามิเตอร์) สามารถประมวลผลได้เร็วเกิน 60 FPS บนการ์ดจอโน้ตบุ๊ก และ 33.5 FPS บน CPU ทั่วไป จึงพร้อมนำไปติดตั้งบนกล้อง IP Camera หรือ Edge Box ของสวนสัตว์ได้ทันทีครับ"),

        ("Slide 4: Real-World Evidence: Test 1",
         "Detecting Feeding Times at the Food Tray (Camera 03 Day)",
         "บรรยายผลลัพธ์คลิปวิดีโอการกินอาหารมื้อบ่าย",
         "This video demonstrates our system detecting the civet's afternoon fruit feeding in Camera 03. At 15:33, zoo keepers placed the fresh fruit tray. At 15:38, the civet emerged and fed continuously for 4 minutes and 45 seconds. The computer tracks the civet with 0.89 to 0.90 confidence, detects its centroid entering the Food Tray ROI, and accurately logs the state as ACTIVE: EATING. This completely replaces manual clipboard feeding logs and provides immediate alerts if an animal skips a meal.",
         "คลิปที่ 1 แสดงผลลัพธ์จริงในพฤติกรรมการกินอาหารมื้อบ่ายครับ เจ้าหน้าที่วางถาดผลไม้เวลา 15:33 น. และชะมดออกมากินเวลา 15:38 น. ต่อเนื่องเป็นเวลา 4 นาที 45 วินาที โมเดลตรวจจับ Bounding Box ได้อย่างแม่นยำด้วย Confidence 0.89-0.90 และเมื่อจุดกึ่งกลางเข้าสู่ Food Tray ROI ระบบจะบันทึกสถานะเป็น ACTIVE : EATING ทันที ช่วยให้สัตวแพทย์ทราบเวลาและปริมาณการกินอาหารโดยไม่ต้องมานั่งเฝ้ากล้องครับ"),

        ("Slide 5: Real-World Evidence: Test 2",
         "Tracing Active Movement in Pitch-Black Night (Camera 03 IR)",
         "บรรยายผลลัพธ์คลิปวิดีโอการเดินลาดตระเวนกลางคืน",
         "This clip proves that our model has conquered Phase 1's biggest limitation: total nocturnal blindness. Here at 01:25 AM in pitch-black night, the civet actively roams the sand floor and climbs logs. Despite monochrome infrared lighting, YOLOv8 maintains solid detection at 0.85 to 0.91 confidence. Furthermore, our kinematics engine traces a real-time breadcrumb motion path at an average speed of 45 pixels per second, logging the state as ACTIVE: LOCOMOTION with zero false negatives.",
         "คลิปที่ 2 เป็นหลักฐานสำคัญที่พิสูจน์ว่าเราแก้จุดอ่อนของ Phase 1 ได้สำเร็จครับ ในเวลา 01:25 น. ซึ่งมืดสนิทและกล้องเป็นโหมดอินฟราเรดขาวดำ ชะมดออกเดินสำรวจพื้นทรายและปีนขอนไม้ โมเดลยังคงตรวจจับได้เสถียรที่ Confidence 0.85-0.91 พร้อมวาดเส้นทางเดิน (Breadcrumb Trail) และคำนวณความเร็วเฉลี่ย 45 px/s เพื่อยืนยันสถานะ ACTIVE : LOCOMOTION ได้อย่างสมบูรณ์แบบโดยไม่หลุดโฟกัสเลยครับ"),

        ("Slide 6: Real-World Evidence: Test 3",
         "Verifying Rest & Deep Sleep in the Tire Nest (Camera 03)",
         "บรรยายผลลัพธ์คลิปวิดีโอการนอนพักผ่อนในรังยางรถยนต์",
         "This third clip validates resting behavior inside the straw tire bed. During midday, the civet curled up inside the elevated tire nest for deep sleep. The model continuously recognizes the curled resting posture with 0.94 to 0.98 confidence. Because the animal remains stationary inside the Tire Nest ROI for greater than 60 seconds, our Zoological 1-Minute Rule confirms the state as INACTIVE: RESTING, contributing to a total of 15.3 hours of verified rest over 24 hours.",
         "คลิปที่ 3 แสดงการตรวจจับการนอนพักผ่อนในยางรถยนต์รองฟางครับ ชะมดนอนขดตัวหลับลึกในช่วงกลางวัน โมเดลตรวจจับท่านอนได้อย่างต่อเนื่องที่ Confidence 0.94-0.98 และเมื่อจุดศูนย์กลางอยู่นิ่งใน Tire Bed ROI เกินกว่า 60 วินาที ระบบจะใช้กฎทางสัตววิทยา 1 นาที (1-Minute Rule) ยืนยันสถานะเป็น INACTIVE : RESTING อย่างแม่นยำ ตัดปัญหาสถานะกระพริบเมื่อสัตว์หยุดนิ่งชั่วคราวครับ"),

        ("Slide 7: 24-Hour Behavioral Results",
         "Automated 24-Hour Behavioral Log & Veterinary Dashboard",
         "นำเสนอแดชบอร์ดสัตวแพทย์และโครงสร้างข้อมูลตาราง CSV",
         "Here is our primary clinical deliverable: the full 24-hour behavioral analysis of April 5th, 2026. On the left, our veterinary dashboard reveals a natural nocturnal activity budget: 37.2% Active (8.9 hours) versus 62.8% Inactive (15.1 hours), with detailed breakdowns of resting, locomotion, eating, and room transit. On the right, the continuous video is aggregated into our standardized daily_behavior_log.csv, providing exact timestamps, enclosure zones, and confidence scores ready for clinical zoo records.",
         "สไลด์นี้คือผลลัพธ์หลักที่ส่งมอบให้ทางสวนสัตว์ครับ เป็นแดชบอร์ดวิเคราะห์พฤติกรรมตลอด 24 ชั่วโมงของวันที่ 5 เมษายน แผนภูมิด้านซ้ายสะท้อนธรรมชาติของสัตว์หากินกลางคืนอย่างชัดเจน คือ Active 37.2% (8.9 ชม.) และ Inactive 62.8% (15.1 ชม.) พร้อมแจกแจงเวลารายพฤติกรรม ส่วนตารางด้านขวาคือไฟล์ daily_behavior_log.csv ที่รวบรวมทุกเหตุการณ์พร้อมระบุพิกัดห้อง เวลาเริ่ม-สิ้นสุด และค่าความเชื่อมั่นอย่างเป็นระบบครับ"),

        ("Slide 8: Practical Challenges Encountered",
         "Solving Real-World Zoo Obstacles Without Unnecessary AI Jargon",
         "อธิบายปัญหาหน้างานจริง 4 ข้อและวิธีแก้ที่เน้นการใช้งานจริง",
         "Rather than focusing on abstract theoretical hurdles, we tackled four concrete zoo challenges: First, the 5-second freeze problem, where animals briefly pause during walks; we solved this with the Zoological 1-Minute Rule to eliminate state flickering. Second, raw video creates millions of redundant frame logs; we solved this with stateful event condensation into clean CSVs. Third, dark night camouflage was solved by nocturnal domain augmentation. Fourth, potted plants and enclosure clutter were suppressed by training on empty enclosure backgrounds.",
         "ในการทำงานจริง เราเผชิญปัญหาหน้างานสำคัญ 4 ประเด็นและแก้ไขได้สำเร็จ: 1) ปัญหาสัตว์หยุดยืนนิ่ง 3-5 วินาทีขณะเดิน ซึ่ง AI ทั่วไปจะเข้าใจผิดว่านอน เราแก้ด้วยกฎ 1-Minute Rule รอให้นิ่งครบ 60 วินาทีในจุดนอนก่อนเปลี่ยนสถานะ 2) ปัญหาข้อมูลล้นเกินจากการรันหลายสิบเฟรมต่อวินาที เราแก้ด้วยการบีบอัดเป็น Event สรุปช่วงเวลาลง CSV 3) ปัญหาสัตว์กลืนไปกับความมืด แก้ด้วยการ Augment ภาพอินฟราเรด และ 4) ปัญหากระถางต้นไม้หลอน แก้ด้วยการใส่ภาพกรงเปล่าเป็นตัวอย่างเชิงลบครับ"),

        ("Slide 9: Deliverables & Zoo Welfare Impact",
         "Ready for Zoo Operations & Open Source Deliverables",
         "สรุปการส่งมอบงาน ซอร์สโค้ด และคุณค่าต่อสวัสดิภาพสัตว์ป่า",
         "In conclusion, Phase 2 delivers a production-ready solution: 1) A clean, modular GitHub repository with full inference code running at over 60 FPS; 2) A curated 193-frame Roboflow dataset package with verified annotations; and 3) Genuine veterinary impact at Chiang Mai Zoo, enabling continuous, non-invasive welfare monitoring, early sickness alerts, and a scalable computer vision pipeline ready for other nocturnal wildlife. Thank you, and we welcome your questions.",
         "สรุปการส่งมอบงานใน Phase 2 กลุ่มของเรามีความพร้อมสมบูรณ์ครบ 100%: 1) ซอร์สโค้ดสะอาดบน GitHub ที่แยกส่วนตรวจจับและตรรกะพฤติกรรมชัดเจน รันได้เกิน 60 FPS 2) ชุดข้อมูลตัวแทน 193 ภาพพร้อม Bounding Box ที่บีบอัดพร้อมอัปโหลดขึ้น Roboflow และ 3) คุณค่าที่จับต้องได้ต่อสวนสัตว์เชียงใหม่ ในการเฝ้าระวังสวัสดิภาพสัตว์ตลอด 24 ชั่วโมงโดยไม่รบกวนสัตว์ และพร้อมขยายผลสู่สัตว์ป่าชนิดอื่นในสวนสัตว์ต่อไปครับ ขอขอบคุณครับ")
    ]

    for s_idx, (s_num, s_title, s_intent, s_en, s_th) in enumerate(slides_script):
        # Header Box
        h_table = doc.add_table(rows=1, cols=1)
        h_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        h_cell = h_table.cell(0, 0)
        h_cell.width = Inches(6.8)
        
        # Shading
        shading = parse_xml(r'<w:shd {} w:fill="1B4958"/>'.format(nsdecls('w')))
        h_cell._tc.get_or_add_tcPr().append(shading)
        
        hp = h_cell.paragraphs[0]
        hr1 = hp.add_run(f"■ {s_num}: {s_title}\n")
        hr1.font.name = "Segoe UI"
        hr1.font.size = Pt(13)
        hr1.font.bold = True
        hr1.font.color.rgb = RGBColor(255, 255, 255)
        
        hr2 = hp.add_run(f"เป้าหมายสไลด์: {s_intent}")
        hr2.font.name = "Segoe UI"
        hr2.font.size = Pt(10.5)
        hr2.font.color.rgb = C_GOLD

        # Script Content Table
        s_table = doc.add_table(rows=2, cols=1)
        s_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # English Row
        c_en = s_table.cell(0, 0)
        c_en.width = Inches(6.8)
        shd_en = parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w')))
        c_en._tc.get_or_add_tcPr().append(shd_en)
        pe = c_en.paragraphs[0]
        re_label = pe.add_run("🎙️ English Speaking Script (Conversational & Punchy):\n")
        re_label.font.name = "Segoe UI"
        re_label.font.size = Pt(11)
        re_label.font.bold = True
        re_label.font.color.rgb = C_TEAL
        
        re_body = pe.add_run(f'"{s_en}"')
        re_body.font.name = "Segoe UI"
        re_body.font.size = Pt(10.5)
        re_body.font.italic = True
        re_body.font.color.rgb = C_DARK

        # Thai Row
        c_th = s_table.cell(1, 0)
        c_th.width = Inches(6.8)
        shd_th = parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w')))
        c_th._tc.get_or_add_tcPr().append(shd_th)
        pt = c_th.paragraphs[0]
        rt_label = pt.add_run("🇹🇭 บทพูดภาษาไทย (สำหรับซ้อมพรีเซนต์หน้าชั้นเรียน):\n")
        rt_label.font.name = "Segoe UI"
        rt_label.font.size = Pt(11)
        rt_label.font.bold = True
        rt_label.font.color.rgb = RGBColor(180, 83, 9) # Amber 700
        
        rt_body = pt.add_run(f'"{s_th}"')
        rt_body.font.name = "Segoe UI"
        rt_body.font.size = Pt(10.5)
        rt_body.font.color.rgb = C_DARK

        doc.add_paragraph() # Spacing

    out_docx = os.path.join(r"D:\CMU\4th\1 st\image processing\project cmz\finish", "Phase2_Results_Presentation_Script_EN_TH.docx")
    doc.save(out_docx)
    print(f"Successfully generated defense script docx at: {out_docx}")

if __name__ == "__main__":
    create_script_docx()
