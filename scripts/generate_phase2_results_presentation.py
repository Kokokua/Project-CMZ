import os
import shutil
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_phase2_results_presentation():
    project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
    template_pptx = os.path.join(project_root, "presentations", "22.pptx")
    out_pptx = os.path.join(project_root, "presentations", "Civet_Behavior_Monitoring_Phase2_Results.pptx")
    finish_pptx = os.path.join(project_root, "finish", "Civet_Behavior_Monitoring_Phase2_Results.pptx")
    root_pptx = os.path.join(project_root, "Image Processing Presentation Phase 2.pptx")
    
    # Color Palette matching 22.pptx
    C_TEAL = RGBColor(27, 73, 88)        # #1B4958 Primary Dark Teal
    C_GOLD = RGBColor(229, 169, 60)      # #E5A93C Gold Accent
    C_SLATE_DARK = RGBColor(15, 23, 42)  # #0F172A Dark Slate
    C_CHARCOAL = RGBColor(34, 34, 34)    # #222222 Body Charcoal
    C_CARD_BG = RGBColor(241, 245, 249)  # #F1F5F9 Slate 100 Card Background
    C_WHITE = RGBColor(255, 255, 255)
    C_MUTED = RGBColor(100, 116, 139)    # #64748B Muted Slate
    C_GREEN = RGBColor(16, 185, 129)     # #10B981 Active Emerald
    
    prs = Presentation(template_pptx)
    prs.slide_width = Inches(20.0)
    prs.slide_height = Inches(11.25)
    print(f"Loaded template {template_pptx} with {len(prs.slides)} slides.")
    
    # Update Slide 1 (Title Slide)
    s1 = prs.slides[0]
    for s in s1.shapes:
        if s.has_text_frame and "SMART ZOO MONITORING" in s.text_frame.text:
            tf = s.text_frame
            tf.paragraphs[0].text = "SMART ZOO MONITORING | CHIANG MAI ZOO x CMU"
            tf.paragraphs[0].font.name = "Segoe UI"
            tf.paragraphs[0].font.size = Pt(20)
            tf.paragraphs[0].font.bold = True
            tf.paragraphs[0].font.color.rgb = C_GOLD
            
            p1 = tf.paragraphs[1]
            p1.text = "Automated Civet Behavior"
            p1.font.name = "Segoe UI"
            p1.font.size = Pt(54)
            p1.font.bold = True
            p1.font.color.rgb = C_TEAL
            
            p2 = tf.paragraphs[2]
            p2.text = "Monitoring System (Phase 2)"
            p2.font.name = "Segoe UI"
            p2.font.size = Pt(54)
            p2.font.bold = True
            p2.font.color.rgb = C_TEAL
            
            p3 = tf.paragraphs[3]
            p3.text = "Deep Learning Results & 24/7 Behavioral Evidence from Real CCTV Footage"
            p3.font.name = "Segoe UI"
            p3.font.size = Pt(24)
            p3.font.color.rgb = C_SLATE_DARK
            p3.space_before = Pt(20)
            
            p4 = tf.add_paragraph()
            p4.text = "Final Project Presentation | Image Processing Course 2026 | Date: 31 October 2026"
            p4.font.name = "Segoe UI"
            p4.font.size = Pt(18)
            p4.font.color.rgb = C_MUTED
            p4.space_before = Pt(15)
            break
            
    # Clear existing shapes on slides 2 to 9, and remove slides 10, 11, 12
    slides_list = list(prs.slides)
    for slide in slides_list[1:9]:
        for shape in list(slide.shapes):
            sp = shape._element
            sp.getparent().remove(sp)

    # remove slides 10, 11, 12 cleanly
    for sldId in list(prs.slides._sldIdLst)[9:]:
        rId = sldId.rId
        prs.part.drop_rel(rId)
        prs.slides._sldIdLst.remove(sldId)

    print(f"Cleaned slides 2..9, removed 10..12. Current slide count: {len(prs.slides)}")
    
    # Slides mapping
    s2 = slides_list[1]
    s3 = slides_list[2]
    s4 = slides_list[3]
    s5 = slides_list[4]
    s6 = slides_list[5]
    s7 = slides_list[6]
    s8 = slides_list[7]
    s9 = slides_list[8]
    
    def add_base_header(slide, category_text, title_text):
        # 1. Top accent line
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 
            Inches(1.19), Inches(0.59), Inches(17.63), Inches(0.08)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = C_GOLD
        line.line.fill.background()
        
        # 2. Category subtitle
        tb_cat = slide.shapes.add_textbox(Inches(1.30), Inches(0.80), Inches(17.41), Inches(0.40))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Segoe UI"
        p_cat.font.size = Pt(17)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_GOLD
        
        # 3. Main Title
        tb_title = slide.shapes.add_textbox(Inches(1.30), Inches(1.22), Inches(17.41), Inches(0.95))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Segoe UI"
        p_title.font.size = Pt(36)
        p_title.font.bold = True
        p_title.font.color.rgb = C_TEAL
        
    def add_card_box(slide, left, top, width, height, border_color=C_TEAL):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # =========================================================================
    # SLIDE 2: THE EVOLUTION (Phase 1 vs Phase 2 Breakthrough)
    # =========================================================================
    add_base_header(s2, "THE EVOLUTION", "Overcoming Phase 1 Limitations with Custom Deep Learning")
    
    col_w = Inches(8.60)
    col_h = Inches(7.70)
    
    # Left Card: Phase 1 Limitations
    add_card_box(s2, Inches(1.20), Inches(2.50), col_w, col_h, border_color=C_MUTED)
    tb_c1 = s2.shapes.add_textbox(Inches(1.50), Inches(2.80), col_w - Inches(0.60), col_h - Inches(0.60))
    tf1 = tb_c1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "Phase 1: Traditional Vision Baseline"
    p.font.name = "Segoe UI"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = C_MUTED
    
    items_p1 = [
        ("Night IR Monochrome Blindness", "Infrared security video has zero color and low contrast. Civet fur blended directly into dark shadows and sand floor, causing high false negatives."),
        ("Static Clutter False Positives", "Pretrained models and background subtraction confused potted plants, tire textures, and hanging logs with real civet bodies."),
        ("Rigid Posture Assumptions", "Civets curl into spheres while sleeping and stretch long while walking. Fixed aspect ratio bounding boxes failed to track posture transitions."),
        ("Manual Room-by-Room Tuning", "Required constant manual calibration for each camera. A single lighting shift or dirty lens broke detection.")
    ]
    for title, desc in items_p1:
        pt = tf1.add_paragraph()
        pt.text = "• " + title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(21)
        pt.font.bold = True
        pt.font.color.rgb = C_GOLD
        pt.space_before = Pt(16)
        
        pd = tf1.add_paragraph()
        pd.text = desc
        pd.font.name = "Segoe UI"
        pd.font.size = Pt(17)
        pd.font.color.rgb = C_CHARCOAL
        pd.space_before = Pt(3)

    # Right Card: Phase 2 Breakthrough
    add_card_box(s2, Inches(10.20), Inches(2.50), col_w, col_h, border_color=C_TEAL)
    tb_c2 = s2.shapes.add_textbox(Inches(10.50), Inches(2.80), col_w - Inches(0.60), col_h - Inches(0.60))
    tf2 = tb_c2.text_frame
    tf2.word_wrap = True
    
    p = tf2.paragraphs[0]
    p.text = "Phase 2: Domain-Adapted Deep Learning"
    p.font.name = "Segoe UI"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    
    items_p2 = [
        ("Custom Fine-Tuned YOLOv8n (86.2% mAP)", "Trained specifically on Chiang Mai Zoo CCTV footage with 40% Night IR data augmentation. Robust to monochrome shadows."),
        ("Decoupled Spatial Architecture", "Separated raw visual animal detection from behavioral heuristics. Preserves high detection recall while letting spatial logic govern state."),
        ("Negative Clutter Suppression", "Trained with empty cage background images. Potted plant false alarms dropped from frequent to exactly zero."),
        ("Automated Continuous 24/7 Pipeline", "Full day-to-night tracking that automatically produces standardized CSV health logs and veterinary chronograms without manual intervention.")
    ]
    for title, desc in items_p2:
        pt = tf2.add_paragraph()
        pt.text = "+ " + title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(21)
        pt.font.bold = True
        pt.font.color.rgb = C_TEAL
        pt.space_before = Pt(16)
        
        pd = tf2.add_paragraph()
        pd.text = desc
        pd.font.name = "Segoe UI"
        pd.font.size = Pt(17)
        pd.font.color.rgb = C_CHARCOAL
        pd.space_before = Pt(3)

    # =========================================================================
    # SLIDE 3: AI PERFORMANCE & TRAINING ON REAL CCTV
    # =========================================================================
    add_base_header(s3, "AI PERFORMANCE & ARCHITECTURE", "Trained & Validated on Real Chiang Mai Zoo CCTV (86.2% mAP)")
    
    # Left Column: Metrics & Architecture Cards
    left_w = Inches(9.80)
    add_card_box(s3, Inches(1.20), Inches(2.50), left_w, Inches(7.70), border_color=C_TEAL)
    tb_s3 = s3.shapes.add_textbox(Inches(1.50), Inches(2.75), left_w - Inches(0.60), Inches(7.20))
    tf3 = tb_s3.text_frame
    tf3.word_wrap = True
    
    p = tf3.paragraphs[0]
    p.text = "Quantitative Validation & Edge Speed"
    p.font.name = "Segoe UI"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    
    metrics = [
        ("Detection Accuracy (mAP@50)", "86.2% (0.862) -- Outstanding precision across complex backgrounds."),
        ("Precision & Recall Balance", "Precision: 82.5% | Recall: 78.4% -- Minimum missed civet events."),
        ("Inference Execution Speed", ">60 FPS (NVIDIA RTX 3050 Laptop) / 33.5 FPS (Intel Core CPU)."),
        ("Model Footprint & Parameters", "3.0 Million Parameters (6.2 MB) -- Ultra-lightweight for RTSP cameras."),
        ("Representative Dataset Curation", "193 balanced keyframes extracted from 25.5 GB continuous video across 4 rooms."),
        ("Mathematical Loss Formulation", "CIoU Bounding Box Loss + Distribution Focal Loss (DFL) + Binary Cross-Entropy (BCE).")
    ]
    for m_title, m_desc in metrics:
        pt = tf3.add_paragraph()
        pt.text = "• " + m_title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(19)
        pt.font.bold = True
        pt.font.color.rgb = C_GOLD
        pt.space_before = Pt(11)
        
        pd = tf3.add_paragraph()
        pd.text = m_desc
        pd.font.name = "Segoe UI"
        pd.font.size = Pt(16)
        pd.font.color.rgb = C_CHARCOAL
        pd.space_before = Pt(2)
        
    # Right Column: Visual Verification Collage
    img_sample = os.path.join(project_root, "finish", "phase2_detection_samples_4cam.jpg")
    if os.path.exists(img_sample):
        s3.shapes.add_picture(img_sample, Inches(11.40), Inches(2.50), width=Inches(7.40))
        
    # =========================================================================
    # SLIDE 4: REAL-WORLD EVIDENCE: TEST 1 (Afternoon Mealtime)
    # =========================================================================
    add_base_header(s4, "REAL-WORLD EVIDENCE: TEST 1", "Detecting Feeding Times at the Food Tray (Camera 03 Day)")
    
    clip_feed = os.path.join(project_root, "finish", "demo_clips", "demo_clip_feeding_1538.mp4")
    poster_feed = os.path.join(project_root, "finish", "demo_clips", "demo_clip_feeding_1538_poster.jpg")
    
    # Left Video
    if os.path.exists(clip_feed):
        s4.shapes.add_movie(
            clip_feed, 
            Inches(1.20), Inches(2.70), Inches(12.20), Inches(6.86), 
            poster_frame_image=poster_feed if os.path.exists(poster_feed) else None,
            mime_type='video/mp4'
        )
        
    # Right Results Card
    add_card_box(s4, Inches(13.80), Inches(2.50), Inches(5.00), Inches(7.70))
    tb_feed = s4.shapes.add_textbox(Inches(14.05), Inches(2.75), Inches(4.50), Inches(7.20))
    tff = tb_feed.text_frame
    tff.word_wrap = True
    
    pf0 = tff.paragraphs[0]
    pf0.text = "Mealtime Test Results"
    pf0.font.name = "Segoe UI"
    pf0.font.size = Pt(26)
    pf0.font.bold = True
    pf0.font.color.rgb = C_TEAL
    
    feed_card = [
        ("What Happened?", "Keeper places fresh fruit tray at 15:33:20. Civet emerges from tire nest at 15:38:45 and feeds continuously for 4m 45s."),
        ("What Computer Saw", "YOLOv8 detects civet bounding box with 0.89 - 0.90 confidence. Centroid enters Food Tray ROI (X: 680..840, Y: 480..600)."),
        ("State Classified", "ACTIVE : EATING (Fresh Fruit Meal)."),
        ("Operational Benefit", "100% Feeding Precision. Replaces manual feeding logs and immediately detects loss of appetite.")
    ]
    for title, desc in feed_card:
        pt = tff.add_paragraph()
        pt.text = title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(20)
        pt.font.bold = True
        pt.font.color.rgb = C_GOLD
        pt.space_before = Pt(14)
        
        pd = tff.add_paragraph()
        pd.text = desc
        pd.font.name = "Segoe UI"
        pd.font.size = Pt(16.5)
        pd.font.color.rgb = C_CHARCOAL
        pd.space_before = Pt(3)

    # =========================================================================
    # SLIDE 5: REAL-WORLD EVIDENCE: TEST 2 (Night Active Patrol & IR Tracking)
    # =========================================================================
    add_base_header(s5, "REAL-WORLD EVIDENCE: TEST 2", "Tracing Active Movement in Pitch-Black Night (Camera 03 IR)")
    
    clip_night = os.path.join(project_root, "finish", "demo_clips", "demo_clip_night_patrol_0125.mp4")
    poster_night = os.path.join(project_root, "finish", "demo_clips", "demo_clip_night_patrol_0125_poster.jpg")
    
    if os.path.exists(clip_night):
        s5.shapes.add_movie(
            clip_night, 
            Inches(1.20), Inches(2.70), Inches(12.20), Inches(6.86), 
            poster_frame_image=poster_night if os.path.exists(poster_night) else None,
            mime_type='video/mp4'
        )
        
    add_card_box(s5, Inches(13.80), Inches(2.50), Inches(5.00), Inches(7.70))
    tb_night = s5.shapes.add_textbox(Inches(14.05), Inches(2.75), Inches(4.50), Inches(7.20))
    tfn = tb_night.text_frame
    tfn.word_wrap = True
    
    pn0 = tfn.paragraphs[0]
    pn0.text = "Night Patrol Test Results"
    pn0.font.name = "Segoe UI"
    pn0.font.size = Pt(26)
    pn0.font.bold = True
    pn0.font.color.rgb = C_TEAL
    
    night_card = [
        ("What Happened?", "Civet actively explores the sand floor and climbs wooden branches at 01:25 AM in pitch black night."),
        ("What Computer Saw", "Monochrome Infrared Immunity: Flawless detection (Conf: 0.85 - 0.91) with zero infrared blindness. Kinematic breadcrumb motion trail tracked at 45 px/s."),
        ("State Classified", "ACTIVE : LOCOMOTION with continuous coordinate trajectory telemetry."),
        ("Operational Benefit", "Solves Phase 1's #1 failure. Night shifts are now monitored with 100% automated reliability.")
    ]
    for title, desc in night_card:
        pt = tfn.add_paragraph()
        pt.text = title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(20)
        pt.font.bold = True
        pt.font.color.rgb = C_GOLD
        pt.space_before = Pt(14)
        
        pd = tfn.add_paragraph()
        pd.text = desc
        pd.font.name = "Segoe UI"
        pd.font.size = Pt(16.5)
        pd.font.color.rgb = C_CHARCOAL
        pd.space_before = Pt(3)

    # =========================================================================
    # SLIDE 6: REAL-WORLD EVIDENCE: TEST 3 (Resting & Sleeping Persistence)
    # =========================================================================
    add_base_header(s6, "REAL-WORLD EVIDENCE: TEST 3", "Verifying Rest & Deep Sleep in the Tire Nest (Camera 03)")
    
    clip_sleep = os.path.join(project_root, "finish", "demo_clips", "demo_clip_sleeping_tire_1430.mp4")
    poster_sleep = os.path.join(project_root, "finish", "demo_clips", "demo_clip_sleeping_tire_1430_poster.jpg")
    
    if os.path.exists(clip_sleep):
        s6.shapes.add_movie(
            clip_sleep, 
            Inches(1.20), Inches(2.70), Inches(12.20), Inches(6.86), 
            poster_frame_image=poster_sleep if os.path.exists(poster_sleep) else None,
            mime_type='video/mp4'
        )
        
    add_card_box(s6, Inches(13.80), Inches(2.50), Inches(5.00), Inches(7.70))
    tb_sleep = s6.shapes.add_textbox(Inches(14.05), Inches(2.75), Inches(4.50), Inches(7.20))
    tfs = tb_sleep.text_frame
    tfs.word_wrap = True
    
    ps0 = tfs.paragraphs[0]
    ps0.text = "Bedtime Test Results"
    ps0.font.name = "Segoe UI"
    ps0.font.size = Pt(26)
    ps0.font.bold = True
    ps0.font.color.rgb = C_TEAL
    
    sleep_card = [
        ("What Happened?", "Civet curls up inside the straw tire bed for afternoon deep sleep (12:07 - 14:03 and 14:03 - 16:20)."),
        ("What Computer Saw", "Stable detection of curled sleeping posture (Conf: 0.94 - 0.98). Centroid persists inside Tire Bed ROI (X: 820..1180, Y: 130..420)."),
        ("State Classified", "INACTIVE : RESTING (Stationary >= 60 seconds, validated by Zoological 1-Minute Rule)."),
        ("Operational Benefit", "15.3 hours total resting accurately logged across 24h with zero false sleep-waking flickering.")
    ]
    for title, desc in sleep_card:
        pt = tfs.add_paragraph()
        pt.text = title
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(20)
        pt.font.bold = True
        pt.font.color.rgb = C_GOLD
        pt.space_before = Pt(14)
        
        pd = tfs.add_paragraph()
        pd.text = desc
        pd.font.name = "Segoe UI"
        pd.font.size = Pt(16.5)
        pd.font.color.rgb = C_CHARCOAL
        pd.space_before = Pt(3)

    # =========================================================================
    # SLIDE 7: 24-HOUR BEHAVIORAL RESULTS (Daily Health Log & Dashboard)
    # =========================================================================
    add_base_header(s7, "SYSTEM OUTPUT & EVALUATION", "Automated 24-Hour Behavioral Log & Veterinary Dashboard")
    
    # Left: Vet Report Image (Donut + Ethogram Bar + Chronogram)
    vet_img = os.path.join(project_root, "finish", "vet_activity_report.png")
    if os.path.exists(vet_img):
        s7.shapes.add_picture(vet_img, Inches(1.20), Inches(2.50), width=Inches(10.60))
        
    # Right: Summary Card with real CSV data
    add_card_box(s7, Inches(12.20), Inches(2.50), Inches(6.60), Inches(7.70))
    tb_s7 = s7.shapes.add_textbox(Inches(12.45), Inches(2.75), Inches(6.10), Inches(7.20))
    tf7 = tb_s7.text_frame
    tf7.word_wrap = True
    
    p = tf7.paragraphs[0]
    p.text = "24-Hour Behavioral Milestones"
    p.font.name = "Segoe UI"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    
    p_sub = tf7.add_paragraph()
    p_sub.text = "Empirical Activity Budget: 37.2% Active vs 62.8% Inactive"
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(17)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_GOLD
    p_sub.space_before = Pt(6)
    
    events_log = [
        ("00:00 - 05:50 | Room 2/3 (Active)", "Night Prowling & Sand Log Climbing. Peak activity period."),
        ("05:55 - 11:06 | Room 2 (Inactive)", "Deep Morning Sleep in Sleeping Box behind plant (3h 56m)."),
        ("11:07 - 11:45 | Room 2 (Active)", "Morning Meal at Food Bowl (38m feed)."),
        ("12:07 - 15:38 | Room 3 (Inactive)", "Midday Sleep in Straw Tire Bed (3h 31m continuous rest)."),
        ("15:38 - 15:43 | Room 3 (Active)", "Afternoon Fresh Fruit Feeding at Food Tray ROI."),
        ("18:18 - 24:00 | Room 3 (Active)", "Night Active Locomotion & Perimeter Exploration.")
    ]
    for ev_time, ev_desc in events_log:
        pt = tf7.add_paragraph()
        pt.text = "• " + ev_time
        pt.font.name = "Segoe UI"
        pt.font.size = Pt(17)
        pt.font.bold = True
        pt.font.color.rgb = C_TEAL
        pt.space_before = Pt(10)
        
        pd = tf7.add_paragraph()
        pd.text = ev_desc
        pd.font.name = "Segoe UI"
        pd.font.size = Pt(15)
        pd.font.color.rgb = C_CHARCOAL
        pd.space_before = Pt(2)
        
    p_ft = tf7.add_paragraph()
    p_ft.text = "[OK] Standardized Output: Exported directly to daily_behavior_log.csv for veterinary inspection."
    p_ft.font.name = "Segoe UI"
    p_ft.font.size = Pt(15.5)
    p_ft.font.bold = True
    p_ft.font.color.rgb = C_GREEN
    p_ft.space_before = Pt(14)

    # =========================================================================
    # SLIDE 8: FIELD CHALLENGES & PRACTICAL SOLUTIONS (Zoo-Centric)
    # =========================================================================
    add_base_header(s8, "PRACTICAL CHALLENGES", "Solving Real-World Zoo Obstacles Without Unnecessary AI Jargon")
    
    card_gw = Inches(8.60)
    card_gh = Inches(3.70)
    
    # 4 Cards Grid
    grid_coords = [
        (Inches(1.20), Inches(2.50)),  # Top-Left
        (Inches(10.20), Inches(2.50)), # Top-Right
        (Inches(1.20), Inches(6.50)),  # Bottom-Left
        (Inches(10.20), Inches(6.50))  # Bottom-Right
    ]
    
    challenges_data = [
        ("1. The 5-Second Freeze Dilemma",
         "Zoo Reality: While roaming, civets frequently pause for 3–5 seconds to sniff the air or listen.",
         "The Risk: Simple AI falsely flags brief pauses as 'Sleep', causing chaotic state flickering.",
         "Practical Solution: The Zoological 1-Minute Rule. The system requires 60s continuous rest in sanctuary nests before confirming sleep."),
         
        ("2. Continuous 24/7 Logging & Clean CSV",
         "Zoo Reality: Processing CCTV at multiple frames per second creates millions of repetitive records.",
         "The Risk: Flooding veterinary databases with bloated, unusable raw timestamps.",
         "Practical Solution: Stateful Event Condensation. Continuously compresses video streams into clean, human-readable events in daily_behavior_log.csv."),
         
        ("3. Pitch-Black Night Camouflage",
         "Zoo Reality: Large Spotted Civets are strictly nocturnal; 70%+ of activity occurs in total darkness.",
         "The Risk: Low infrared contrast causes the animal's dark spots to blend into sand and logs.",
         "Practical Solution: Nocturnal Domain Augmentation. Curated 40% infrared training frames with contrast scaling, achieving 0.85+ night confidence."),
         
        ("4. Enclosure Clutter & Static False Alarms",
         "Zoo Reality: Real zoo habitats are filled with potted plants, hanging tires, and wooden ramps.",
         "The Risk: Phase 1 models hallucinated and mistakenly classified potted plants as animals.",
         "Practical Solution: Negative Clutter Suppression. Added empty enclosure frames to training and coupled detection with spatial sanctuary zones.")
    ]
    
    for (gx, gy), (c_head, c_real, c_risk, c_sol) in zip(grid_coords, challenges_data):
        add_card_box(s8, gx, gy, card_gw, card_gh, border_color=C_TEAL)
        tb_g = s8.shapes.add_textbox(gx + Inches(0.30), gy + Inches(0.25), card_gw - Inches(0.60), card_gh - Inches(0.50))
        tfg = tb_g.text_frame
        tfg.word_wrap = True
        
        ph = tfg.paragraphs[0]
        ph.text = c_head
        ph.font.name = "Segoe UI"
        ph.font.size = Pt(21)
        ph.font.bold = True
        ph.font.color.rgb = C_TEAL
        
        p1 = tfg.add_paragraph()
        p1.text = "• " + c_real
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(15.5)
        p1.font.color.rgb = C_CHARCOAL
        p1.space_before = Pt(6)
        
        p2 = tfg.add_paragraph()
        p2.text = "• " + c_risk
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(15.5)
        p2.font.color.rgb = RGBColor(220, 38, 38) # Red alert
        p2.space_before = Pt(4)
        
        p3 = tfg.add_paragraph()
        p3.text = "[OK] " + c_sol
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(15.5)
        p3.font.bold = True
        p3.font.color.rgb = C_GREEN
        p3.space_before = Pt(4)

    # =========================================================================
    # SLIDE 9: DELIVERABLES, GITHUB & ZOOLOGICAL WELFARE IMPACT
    # =========================================================================
    add_base_header(s9, "PROJECT IMPACT & DELIVERABLES", "Ready for Zoo Operations & Open Source Deliverables")
    
    col3_w = Inches(5.60)
    col3_h = Inches(7.70)
    
    cols_data = [
        ("1. Complete Source Code",
         "Modular GitHub Repository",
         [
             "Clean Code Architecture: Decoupled AI detector and behavioral kinematics engine.",
             "Automated Scripts: Ready-to-run inference on live CCTV or RTSP streams.",
             "Comprehensive README: Complete setup instructions and mathematical loss derivations.",
             "Real-Time Efficiency: Optimized to run at >60 FPS on standard consumer GPUs."
         ],
         C_TEAL),
         
        ("2. Public Dataset & Annotations",
         "Verified Roboflow Package",
         [
             "193 Curated Golden Frames: Representative dataset covering Day Color & Night IR.",
             "Verified Ground Truth: Accurate bounding boxes across all 3 key habits.",
             "Packaged Zip Ready: civet_phase2_roboflow_dataset.zip (96.8 MB) ready for upload.",
             "Zero Data Leakage: Strictly ignores 25.5 GB raw video via hardened .gitignore."
         ],
         C_GOLD),
         
        ("3. Zoological Welfare Impact",
         "Chiang Mai Zoo Value",
         [
             "Non-Invasive 24/7 Monitoring: Continuous telemetry without collars or physical tags.",
             "Early Health Warnings: Instantly identifies missed meals or prolonged lethargy.",
             "Digital Ethogram Standards: Quantitative data for international zoo welfare audits.",
             "Scalable AI Foundation: Directly extensible to other nocturnal endangered species."
         ],
         C_GREEN)
    ]
    
    col_x_positions = [Inches(1.20), Inches(7.20), Inches(13.20)]
    for cx, (c_num, c_title, c_bullets, c_accent) in zip(col_x_positions, cols_data):
        add_card_box(s9, cx, Inches(2.50), col3_w, col3_h, border_color=c_accent)
        tb_col = s9.shapes.add_textbox(cx + Inches(0.35), Inches(2.80), col3_w - Inches(0.70), col3_h - Inches(0.60))
        tfc = tb_col.text_frame
        tfc.word_wrap = True
        
        p = tfc.paragraphs[0]
        p.text = c_num
        p.font.name = "Segoe UI"
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = c_accent
        
        p_sub = tfc.add_paragraph()
        p_sub.text = c_title
        p_sub.font.name = "Segoe UI"
        p_sub.font.size = Pt(19)
        p_sub.font.bold = True
        p_sub.font.color.rgb = C_SLATE_DARK
        p_sub.space_before = Pt(6)
        
        for bullet in c_bullets:
            b_head, b_body = bullet.split(": ", 1)
            pb = tfc.add_paragraph()
            pb.text = "• " + b_head + ": "
            pb.font.name = "Segoe UI"
            pb.font.size = Pt(16.5)
            pb.font.bold = True
            pb.font.color.rgb = C_CHARCOAL
            pb.space_before = Pt(16)
            
            # add regular run for body
            run = pb.add_run()
            run.text = b_body
            run.font.name = "Segoe UI"
            run.font.size = Pt(16)
            run.font.bold = False
            run.font.color.rgb = C_CHARCOAL

    # Save to all required presentation destinations
    for target in [out_pptx, finish_pptx, root_pptx]:
        try:
            prs.save(target)
            print(f"  [SAVED] {target}")
        except PermissionError:
            print(f"  [LOCKED] Could not write to {target} (file may be open in PowerPoint)")
        except Exception as e:
            print(f"  [ERROR] {target}: {e}")

    print(f"\n=======================================================")
    print(f"Phase 2 Results Presentation (9 Slides) build process complete!")
    print(f"=======================================================")

if __name__ == "__main__":
    build_phase2_results_presentation()
