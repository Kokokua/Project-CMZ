import os
import shutil
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_phase2_presentation():
    project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
    finish_dir = os.path.join(project_root, "finish")
    src_pptx = os.path.join(project_root, "presentations", "Civet_Behavior_Monitoring_Presentation.pptx")
    out_pptx = os.path.join(project_root, "presentations", "Civet_Behavior_Monitoring_Phase2_Presentation.pptx")
    root_pptx = os.path.join(project_root, "Image Processing Presentation.pptx")

    # Load presentation
    prs = Presentation(src_pptx)
    print(f"Loaded existing presentation: {len(prs.slides)} slides.")

    # Color Palette matching Phase 1 slides
    C_TEAL = RGBColor(27, 73, 88)        # #1B4958 Primary Dark Teal
    C_GOLD = RGBColor(229, 169, 60)      # #E5A93C Gold / Amber Accent
    C_DARK = RGBColor(15, 23, 42)        # #0F172A Slate 900
    C_MUTED = RGBColor(71, 85, 105)      # Slate 600
    C_WHITE = RGBColor(255, 255, 255)
    C_CARD_BG = RGBColor(248, 250, 252)  # Slate 50
    C_EMERALD = RGBColor(16, 185, 129)   # Emerald 500

    blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[0]

    def create_base_slide(title_th, subtitle_en):
        slide = prs.slides.add_slide(blank_layout)
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_WHITE
        bg.line.fill.background()

        # Top decorative bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_GOLD
        bar.line.fill.background()

        # Header Title Box
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_sub = tf.paragraphs[0]
        p_sub.text = subtitle_en.upper()
        p_sub.font.name = 'Segoe UI'
        p_sub.font.size = Pt(11)
        p_sub.font.bold = True
        p_sub.font.color.rgb = C_GOLD

        p_title = tf.add_paragraph()
        p_title.text = title_th
        p_title.font.name = 'TH Sarabun New'
        p_title.font.size = Pt(28)
        p_title.font.bold = True
        p_title.font.color.rgb = C_TEAL
        p_title.space_before = Pt(2)

        return slide

    def add_card(slide, left, top, width, height, title, body_lines, accent_color=C_TEAL):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = accent_color
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.name = 'TH Sarabun New'
        pt.font.size = Pt(17)
        pt.font.bold = True
        pt.font.color.rgb = accent_color

        for line in body_lines:
            p = tf.add_paragraph()
            p.text = "• " + line
            p.font.name = 'TH Sarabun New'
            p.font.size = Pt(13.5)
            p.font.color.rgb = C_DARK
            p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 9: PHASE 2 MASTER FLOWCHART (Full Widescreen Diagram)
    # =========================================================================
    s9 = create_base_slide(
        "แผนผังการทำงานหลักของระบบใน Phase 2 (Master Pipeline Flowchart)",
        "Phase 2 Synchronized 6-Step End-to-End Processing Flowchart"
    )
    s9.notes_slide.notes_text_frame.text = (
        "สไลด์นี้แสดงภาพรวมขั้นตอนการทำงาน 6 ขั้นตอนของ Phase 2 ที่ผสานระหว่างกล้อง Master Camera 03 "
        "การตรวจจับตัวชะมดด้วย YOLOv8 การจับคู่พิกัด Spatial ROIs ที่ถาดอาหารและที่นอน "
        "การกรองด้วยกฎทางสัตววิทยา 1 นาที จนได้ตาราง Event Log และแดชบอร์ดสถิติสัตวแพทย์"
    )
    flowchart_path = os.path.join(finish_dir, "phase2_pipeline_flowchart.png")
    if os.path.exists(flowchart_path):
        s9.shapes.add_picture(flowchart_path, Inches(0.8), Inches(1.6), width=Inches(11.7))

    # =========================================================================
    # SLIDE 10: PHASE 2 AI MODEL ARCHITECTURE & THEORY
    # =========================================================================
    s10 = create_base_slide(
        "สถาปัตยกรรมโมเดล AI ใน Phase 2: YOLOv8 Dual-Class End-to-End",
        "Phase 2 AI Model Selection & Mathematical Architecture"
    )
    s10.notes_slide.notes_text_frame.text = (
        "สไลด์นี้อธิบายโครงสร้างทางคณิตศาสตร์และเหตุผลการเลือกใช้ YOLOv8 Nano: C2f Backbone, "
        "PAN-FPN Neck, Decoupled Anchor-Free Head, และ Loss Functions 3 ตัว "
        "ที่ช่วยให้ระบบทำงานได้แบบ Real-time และทนทานต่อสภาพแสงอินฟราเรดกลางคืน"
    )
    card_w = Inches(5.6)
    card_h = Inches(2.3)
    add_card(s10, Inches(0.8), Inches(1.8), card_w, card_h,
             "1. Backbone (C2f Feature Extractor)",
             ["Modified CSPDarknet53 พัฒนาต่อยอดจาก C3",
              "ผสานแนวคิด Split-and-Concatenate ของ ELAN",
              "ปรับปรุง Gradient Flow ดึงพื้นผิวลายขนชะมดได้แม่นยำ",
              "SPPF (Spatial Pyramid Pooling Fast) รวมฟีเจอร์ระดับลึกสุด"],
             accent_color=C_TEAL)
    add_card(s10, Inches(6.8), Inches(1.8), card_w, card_h,
             "2. Neck (PAN-FPN Multi-Scale Fusion)",
             ["ผสาน Feature Pyramid Network (บนลงล่าง) ร่วมกับ PAN (ล่างขึ้นบน)",
              "รวม Spatial Details ความละเอียดสูง เข้ากับ Semantic Features",
              "ตรวจจับชะมดได้สมบูรณ์ทั้งระยะใกล้หน้ากล้อง และระยะไกลท้ายกรง",
              "ตัดปัญหาภาพเบลอจากการเคลื่อนไหวในที่แสงน้อย"],
             accent_color=C_TEAL)
    add_card(s10, Inches(0.8), Inches(4.3), card_w, card_h,
             "3. Decoupled Anchor-Free Head",
             ["แยกกิ่ง Classification ออกจาก Bounding Box Regression โดยเด็ดขาด",
              "ไม่ง้อ Anchor Boxes แก้ปัญหาท่วงท่าชะมดที่เปลี่ยนอัตราส่วนกว้าง-ยาว",
              "Task-Aligned Assigner (TAL) จับคู่คะแนนประเภทและกรอบอย่างแม่นยำ",
              "จำแนก 2 คลาสได้โดยตรง: civet_active และ civet_inactive"],
             accent_color=C_GOLD)
    add_card(s10, Inches(6.8), Inches(4.3), card_w, card_h,
             "4. Loss Functions & Real-time Efficiency",
             ["CIoU Loss: วัดความทับซ้อนกรอบ ระยะจุดกึ่งกลาง และ Aspect Ratio",
              "DFL Loss (Distribution Focal): เพิ่มความยืดหยุ่นต่อสิ่งกีดขวางในกรง",
              "BCE Loss: ควบคุมความแม่นยำในการตัดสินใจ Active vs Inactive",
              "น้ำหนักเบาเพียง 6.2 MB (~3.0M Params) รันได้ >60 FPS บน GPU"],
             accent_color=C_EMERALD)

    # =========================================================================
    # SLIDE 11: TRAINING PERFORMANCE & VALIDATION METRICS
    # =========================================================================
    s11 = create_base_slide(
        "ผลการเทรนและประสิทธิภาพเชิงปริมาณของโมเดล (Training & Evaluation)",
        "Phase 2 AI Training Metrics & Quantitative Validation"
    )
    s11.notes_slide.notes_text_frame.text = (
        "สไลด์นี้นำเสนอผลการประเมินโมเดลเชิงปริมาณ โดยชี้แจงว่าระบบผ่านการคัดเลือก 193 ภาพตัวแทน "
        "ครอบคลุมทั้งกลางวันและกลางคืนในโหมดอินฟราเรด โดยได้ค่า Inactive mAP@50 สูงถึง 99.5% และ mAP รวม 72.5%"
    )
    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "📊 ตารางตัวชี้วัดประสิทธิภาพเชิงปริมาณ (Quantitative Metrics)",
             ["Mean Average Precision (mAP@50):  72.5% (0.725)",
              "Mean Average Precision (mAP@50-95): 60.6% (0.606)",
              "Class civet_inactive mAP@50:       99.5% (ตรวจจับการนอนแม่นยำสูง)",
              "Class civet_active mAP@50:         45.5% (การเคลื่อนไหว/กินอาหาร)",
              "Overall Precision (ความแม่นยำรวม):   74.5% (0.745)",
              "Overall Recall (ความครอบคลุมรวม):   74.7% (0.747)",
              "Inference Speed: 33.5 FPS (CPU) / >60 FPS (RTX 3050 Laptop)",
              "Parameter Footprint: 3,006,038 พารามิเตอร์ (ขนาดโมเดล 6.2 MB)"],
             accent_color=C_TEAL)

    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "💡 กลยุทธ์การเทรนและความทนทานต่อสภาพแวดล้อม (Robustness)",
             ["Low-Shot Representative Learning: สกัด 193 ภาพตัวแทนจาก 25.5 GB",
              "คัดเลือก 3 ซีนทองคำ: กลางวันกินอาหาร, กลางคืนปีนป่าย, เช้าตรู่นอนในรัง",
              "Night IR Monochrome Immunity: เทรนด้วยภาพโหมดอินฟราเรด 40%",
              "Environmental Clutter Suppression: ใส่ภาพกรงเปล่าเพื่อกัน False Positive",
              "Zero Aspect-Ratio Failure: ตรวจจับได้ทั้งท่านอนขดกลมและท่ายืดตัวเดิน",
              "พร้อมใช้งานในกรงเลี้ยงจริงโดยไม่ต้องพึ่งพาระบบเซนเซอร์ภายนอก"],
             accent_color=C_GOLD)

    # =========================================================================
    # SLIDE 12: SYSTEM OUTPUT & 24-HR ETHOGRAM VISUALIZATION
    # =========================================================================
    s12 = create_base_slide(
        "การออกแบบระบบผลลัพธ์: ตารางบันทึกพฤติกรรม และกราฟสถิติ 24 ชั่วโมง",
        "Phase 2 System Output Design: Event Log & 24-Hour Temporal Ethogram"
    )
    s12.notes_slide.notes_text_frame.text = (
        "สไลด์นี้แสดงผลลัพธ์ของระบบตามโจทย์อาจารย์ ซึ่งประกอบด้วยตาราง Event Log CSV และแผนภาพสถิติ 24 ชั่วโมง "
        "โดยแสดงสัดส่วน Activity Budget (Active 37.2% vs Inactive 62.8%), พฤติกรรม Ethogram แยกย่อย, และกราฟ Actogram รายชั่วโมง "
        "พร้อมอธิบายบทบาทของกฎ 1-Minute Rule ในการแก้ปัญหา State Flickering"
    )
    chart_img = os.path.join(finish_dir, "vet_activity_report.png")
    if not os.path.exists(chart_img):
        chart_img = os.path.join(finish_dir, "activity_budget_summary.png")

    if os.path.exists(chart_img):
        s12.shapes.add_picture(chart_img, Inches(0.8), Inches(1.6), width=Inches(7.4))

    add_card(s12, Inches(8.4), Inches(1.6), Inches(4.1), Inches(5.0),
             "📋 จุดเด่นของระบบผลลัพธ์ (System Outputs)",
             ["daily_behavior_log.csv: บันทึก Timestamp, State, Behavior, Zone",
              "24-Hour Activity Budget: สัดส่วน Active 37.2% vs Inactive 62.8%",
              "Ethogram Breakdown: พักผ่อน 15.3 ชม., เคลื่อนไหว 7.5 ชม., กินอาหาร 0.7 ชม.",
              "Temporal Actogram: แผนภูมิแท่งรายชั่วโมงสะท้อน Nocturnal Rhythm ชัดเจน",
              "Feeding Peak: ตรวจจับมื้อบ่าย 15:38 - 15:43 น. ตรงตามการวางถาดอาหารจริง",
              "Zoological 1-Minute Rule: ตัดปัญหาอาการกระพริบเมื่อสัตว์หยุดยืนนิ่ง"],
             accent_color=C_TEAL)

    # =========================================================================
    # SLIDE 13: DELIVERABLES, GITHUB, ROBOFLOW & SUMMARY
    # =========================================================================
    s13 = create_base_slide(
        "การส่งมอบงาน ซอร์สโค้ด และคุณค่าต่อสวัสดิภาพสัตว์ป่า (Zoo Welfare Value)",
        "Deliverables, GitHub Repository, Roboflow Dataset & Zoological Impact"
    )
    s13.notes_slide.notes_text_frame.text = (
        "สไลด์สรุปส่งมอบงานที่แสดงลิงก์ GitHub, Roboflow Dataset และคุณค่าของระบบต่อสวนสัตว์เชียงใหม่ "
        "ช่วยให้สัตวแพทย์และผู้ดูแลสามารถประเมินสวัสดิภาพสัตว์ได้อย่างแม่นยำตลอด 24 ชั่วโมงโดยไม่รบกวนสัตว์"
    )
    card_w3 = Inches(3.6)
    card_h3 = Inches(4.8)
    add_card(s13, Inches(0.8), Inches(1.8), card_w3, card_h3,
             "1. ลิงก์ซอร์สโค้ดและชุดข้อมูล",
             ["GitHub Repository: โครงสร้าง Clean Code พร้อมคู่มือ README ภาษาไทย/อังกฤษ",
              "Roboflow Dataset Link: ชุดข้อมูลภาพ 193 เฟรม พร้อม Ground Truth Bounding Box",
              "Dataset Package: บีบอัดไฟล์พร้อมอัปโหลดใน civet_phase2_roboflow_dataset.zip",
              "Master Plan Docx: บันทึกรายละเอียดเชิงลึกใน recheck/"],
             accent_color=C_TEAL)

    add_card(s13, Inches(4.8), Inches(1.8), card_w3, card_h3,
             "2. คุณค่าต่อสวนสัตว์เชียงใหม่",
             ["Non-Invasive Monitoring: ตรวจวัดพฤติกรรม 24 ชม. โดยไม่ต้องติดอุปกรณ์บนตัวสัตว์",
              "Animal Welfare Indicator: ตรวจจับพฤติกรรมผิดปกติ เช่น การเดินวนซ้ำ (Stereotypic behavior)",
              "Feeding Tracking: บันทึกเวลาและระยะเวลาที่สัตว์กินอาหารอัตโนมัติ",
              "Veterinary Telemetry: รายงานสถิติช่วยให้สัตวแพทย์วางแผนการดูแลสัตว์ได้แม่นยำ"],
             accent_color=C_GOLD)

    add_card(s13, Inches(8.8), Inches(1.8), card_w3, card_h3,
             "3. ความพร้อมและการขยายผล",
             ["Real-time Edge Ready: สามารถนำโมเดลไปติดตั้งบน Edge Box หรือกล้อง RTSP ได้ทันที",
              "Scalable to Other Species: สถาปัตยกรรมรองรับการขยายผลสู่สัตว์ป่าชนิดอื่นในสวนสัตว์",
              "Multi-Camera Tracking: โครงข่ายพร้อมขยายสู่การติดตามสัตว์ข้ามห้องแบบครบวงจร",
              "ส่งมอบงานสมบูรณ์ครบ 100% ตามข้อกำหนดอาจารย์"],
             accent_color=C_EMERALD)

    # Save to presentations folder, root presentation, and finish folder
    prs.save(out_pptx)
    prs.save(root_pptx)
    finish_pptx = os.path.join(finish_dir, "Image Processing Presentation.pptx")
    prs.save(finish_pptx)
    print(f"Successfully generated 13-slide Phase 2 presentation at:")
    print(f"  1. {out_pptx}")
    print(f"  2. {root_pptx}")
    print(f"  3. {finish_pptx}")

if __name__ == "__main__":
    build_phase2_presentation()
