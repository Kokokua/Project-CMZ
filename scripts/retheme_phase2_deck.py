import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml

def retheme_presentation():
    project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
    src_pptx = os.path.join(project_root, "finish", "Image_Processing_Presentation_Phase2_Final.backup.pptx")
    out_pptx = os.path.join(project_root, "finish", "Image_Processing_Presentation_Phase2_Final.pptx")
    civet_cutout = os.path.join(project_root, "finish", "civet_cover_cutout.png")

    prs = Presentation(src_pptx)
    print(f"Loaded presentation: {len(prs.slides)} slides, size: {prs.slide_width.inches} x {prs.slide_height.inches}")

    # Color Palette from Phase 1 (22.pptx)
    C_GOLD = RGBColor(229, 169, 60)       # #E5A93C Warm Gold / Mustard
    C_TEAL = RGBColor(27, 73, 88)         # #1B4958 Deep Forest Teal
    C_DARK = RGBColor(34, 34, 34)         # #222222 Body Charcoal
    C_WHITE = RGBColor(255, 255, 255)     # #FFFFFF Pure White
    C_CARD_BG = RGBColor(246, 248, 250)   # Soft Light Card Tint
    C_BORDER = RGBColor(226, 232, 240)    # Soft Slate Border
    C_EMERALD = RGBColor(25, 179, 92)     # #19B35C Zoo Emerald

    # =========================================================================
    # 1. SLIDE 1: Cover Slide Redesign (Matching Phase 1 Zoo Gradient & Teal Card)
    # =========================================================================
    s1 = prs.slides[0]

    # Clear existing shapes on slide 1
    for shp in list(s1.shapes):
        sp = shp._element
        parent = sp.getparent()
        if parent is not None:
            parent.remove(sp)

    # Apply Gradient Background via XML
    bg_xml = """<p:bg xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
      <p:bgPr>
        <a:gradFill rotWithShape="true">
          <a:gsLst>
            <a:gs pos="15000"><a:srgbClr val="082122"><a:alpha val="100000"/></a:srgbClr></a:gs>
            <a:gs pos="40000"><a:srgbClr val="295B53"><a:alpha val="100000"/></a:srgbClr></a:gs>
            <a:gs pos="60000"><a:srgbClr val="19B35C"><a:alpha val="100000"/></a:srgbClr></a:gs>
            <a:gs pos="85000"><a:srgbClr val="FCFF9A"><a:alpha val="100000"/></a:srgbClr></a:gs>
          </a:gsLst>
          <a:lin ang="18900000"/>
        </a:gradFill>
      </p:bgPr>
    </p:bg>"""
    bg_elem = parse_xml(bg_xml)
    s1._element.cSld.insert(0, bg_elem)

    # Add Central Deep Teal Card with White Outline
    card = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.85), Inches(0.75), Inches(11.633), Inches(6.0))
    card.fill.solid()
    card.fill.fore_color.rgb = C_TEAL
    card.line.color.rgb = C_WHITE
    card.line.width = Pt(2.0)

    # Add Civet Cutouts (scaled so text has generous breathing room)
    if os.path.exists(civet_cutout):
        # Top-Left Cutout
        s1.shapes.add_picture(civet_cutout, Inches(0.1), Inches(0.1), Inches(2.4), Inches(2.0))
        # Bottom-Right Cutout
        s1.shapes.add_picture(civet_cutout, Inches(10.7), Inches(5.1), Inches(2.4), Inches(2.0))

    # Add Content inside Central Card (offset to x = 2.6" to avoid top-left civet)
    tb = s1.shapes.add_textbox(Inches(2.6), Inches(1.15), Inches(9.2), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "SMART ZOO MONITORING | CHIANG MAI ZOO × CMU"
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(13.5)
    p0.font.bold = True
    p0.font.color.rgb = C_GOLD

    p1 = tf.add_paragraph()
    p1.text = "ระบบตรวจวัดและจำแนกพฤติกรรมชะมดแผงสันหางดำอัตโนมัติ 24 ชั่วโมง"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(26)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    p1.space_before = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "Automated 24-Hour Multi-Camera Civet Behavior Monitoring System (Phase 2 Outcomes-First)"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(13.5)
    p2.font.bold = True
    p2.font.color.rgb = C_GOLD
    p2.space_before = Pt(4)

    p_div = tf.add_paragraph()
    p_div.text = "─────────────────────────────────────────────────────────────────────────"
    p_div.font.name = "Segoe UI"
    p_div.font.size = Pt(9)
    p_div.font.color.rgb = RGBColor(60, 110, 125)
    p_div.space_before = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "🎯 จุดเปลี่ยนสำคัญจาก Phase 1 สู่ Phase 2 (Key Advancements):"
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = C_GOLD
    p3.space_before = Pt(8)

    p4 = tf.add_paragraph()
    p4.text = "• จากภาพตัดตอนเดี่ยว/ทฤษฎี ➔ สู่การรันจริง 24.0 ชั่วโมงต่อเนื่องบนฟุตเทจ CCTV กรงเลี้ยง 4 ห้องแบบ Synchronized"
    p4.font.name = "Segoe UI"
    p4.font.size = Pt(11)
    p4.font.color.rgb = C_WHITE
    p4.space_before = Pt(5)

    p5 = tf.add_paragraph()
    p5.text = "• จากโมเดล End-to-End ที่เกิด Flicker ➔ สู่ Decoupled Architecture (YOLOv8 ตรวจจับพิกัด + Spatial Handoff FSM)"
    p5.font.name = "Segoe UI"
    p5.font.size = Pt(11)
    p5.font.color.rgb = C_WHITE
    p5.space_before = Pt(4)

    p6 = tf.add_paragraph()
    p6.text = "• ส่งมอบผลลัพธ์เชิงประจักษ์: ตาราง Event Log 30 เหตุการณ์, กราฟสถิติ 24 ชม., และคลิปวิดีโอสาธิตการรันจริง"
    p6.font.name = "Segoe UI"
    p6.font.size = Pt(11)
    p6.font.color.rgb = C_WHITE
    p6.space_before = Pt(4)

    # =========================================================================
    # 2. SLIDES 2-10: Uniform Segoe UI, Palette & Card Harmonization
    # =========================================================================
    for idx in range(1, len(prs.slides)):
        s = prs.slides[idx]
        for shp in s.shapes:
            # Check card shape fill and border
            if shp.shape_type == MSO_SHAPE.ROUNDED_RECTANGLE:
                try:
                    if shp.width.inches > 2.0 and shp.height.inches > 2.0:
                        shp.fill.solid()
                        shp.fill.fore_color.rgb = C_CARD_BG
                        shp.line.color.rgb = C_BORDER
                        shp.line.width = Pt(1.5)
                except Exception:
                    pass

            # Update text runs to Segoe UI and appropriate palette colors
            if shp.has_text_frame:
                tf = shp.text_frame
                # Slide Header check (Shape name == 'TextBox 3' and top < Inches(1.0))
                if shp.name == "TextBox 3" and shp.top.inches < 1.0:
                    if len(tf.paragraphs) >= 1:
                        tf.paragraphs[0].font.name = "Segoe UI"
                        tf.paragraphs[0].font.size = Pt(11)
                        tf.paragraphs[0].font.bold = True
                        tf.paragraphs[0].font.color.rgb = C_GOLD
                    if len(tf.paragraphs) >= 2:
                        tf.paragraphs[1].font.name = "Segoe UI"
                        tf.paragraphs[1].font.size = Pt(22)
                        tf.paragraphs[1].font.bold = True
                        tf.paragraphs[1].font.color.rgb = C_TEAL
                else:
                    # Content card boxes
                    for p_idx, p in enumerate(tf.paragraphs):
                        for r in p.runs:
                            r.font.name = "Segoe UI"
                            if p_idx == 0:
                                # Card title
                                r.font.bold = True
                                if r.font.color and r.font.color.type == 1 and str(r.font.color.rgb) in ["E5A93C", "10B981", "19B35C"]:
                                    pass # preserve gold or emerald accent
                                else:
                                    r.font.color.rgb = C_TEAL
                            else:
                                if not r.font.bold:
                                    r.font.color.rgb = C_DARK

    # =========================================================================
    # 3. SLIDE 10: Update User's GitHub Repo Link (Only TextBox 9)
    # =========================================================================
    s10 = prs.slides[9]
    for shp in s10.shapes:
        if shp.has_text_frame and shp.name == "TextBox 9":
            tf = shp.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            p0.text = "🔗 ลิงก์ซอร์สโค้ดและชุดข้อมูลภาพ (Source & Data)"
            p0.font.name = "Segoe UI"
            p0.font.size = Pt(13)
            p0.font.bold = True
            p0.font.color.rgb = C_GOLD

            p1 = tf.add_paragraph()
            p1.text = "• GitHub Repository:"
            p1.font.name = "Segoe UI"
            p1.font.size = Pt(11)
            p1.font.bold = True
            p1.font.color.rgb = C_TEAL
            p1.space_before = Pt(4)

            p2 = tf.add_paragraph()
            p2.text = "  https://github.com/Kokokua/Project-CMZ.git"
            p2.font.name = "Segoe UI"
            p2.font.size = Pt(11)
            p2.font.bold = True
            p2.font.color.rgb = C_GOLD
            p2.space_before = Pt(2)

            p3 = tf.add_paragraph()
            p3.text = "  (คู่มือการติดตั้ง ใช้งาน และเอกสารการรันระบบฉบับสมบูรณ์ README.md)"
            p3.font.name = "Segoe UI"
            p3.font.size = Pt(10)
            p3.font.color.rgb = C_DARK
            p3.space_before = Pt(2)

            p4 = tf.add_paragraph()
            p4.text = "• Dataset Package (พร้อมส่งมอบ):"
            p4.font.name = "Segoe UI"
            p4.font.size = Pt(11)
            p4.font.bold = True
            p4.font.color.rgb = C_TEAL
            p4.space_before = Pt(8)

            p5 = tf.add_paragraph()
            p5.text = "  finish/civet_yolo_dataset_phase2.zip (95.5 MB)\n" \
                      "  - ครอบคลุมภาพ 227 เฟรม (Train 181, Val 46)\n" \
                      "  - มี Background Negative Images 25% ป้องกัน False Positive 100%"
            p5.font.name = "Segoe UI"
            p5.font.size = Pt(10)
            p5.font.color.rgb = C_DARK
            p5.space_before = Pt(2)

            p6 = tf.add_paragraph()
            p6.text = "• เอกสารวิจัยเชิงเทคนิค:"
            p6.font.name = "Segoe UI"
            p6.font.size = Pt(11)
            p6.font.bold = True
            p6.font.color.rgb = C_TEAL
            p6.space_before = Pt(8)

            p7 = tf.add_paragraph()
            p7.text = "  docs/MODEL_AUDIT_REPORT_YOLOV8N_CIVET.md\n" \
                      "  บันทึกรายงานผลการ Audit อิสระ และการตรวจสอบเชิงลึก 100%"
            p7.font.name = "Segoe UI"
            p7.font.size = Pt(10)
            p7.font.color.rgb = C_DARK
            p7.space_before = Pt(2)

    prs.save(out_pptx)
    print(f"Rethemed presentation successfully saved to: {out_pptx}")

    # Also sync to Desktop folder
    desktop_dest = r"C:\Users\ASUS\Desktop\html knowledge file\Image_Processing_Presentation_Phase2_Final.pptx"
    shutil.copy2(out_pptx, desktop_dest)
    print(f"Synced to Desktop: {desktop_dest}")

if __name__ == "__main__":
    retheme_presentation()
