import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_pptx = os.path.join(project_root, "presentations", "Civet_Behavior_Monitoring_Presentation_EN.pptx")
    
    # Image asset paths
    flowchart_img = os.path.join(project_root, "pic", "flowcharts", "pipeline_flowchart_en.png")
    locomotion_img = os.path.join(project_root, "pic", "tracking_results", "locomotion_tracking_result.png")
    eating_img = os.path.join(project_root, "pic", "tracking_results", "eating_tracking_result.png")
    resting_img = os.path.join(project_root, "pic", "tracking_results", "resting_tracking_result.png")
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Color Palette
    C_BG = RGBColor(15, 23, 42)         # #0F172A Deep Navy
    C_CARD = RGBColor(30, 41, 59)       # #1E293B Dark Slate Card
    C_CARD_ALT = RGBColor(24, 33, 47)   # Darker card
    C_BORDER = RGBColor(51, 65, 85)     # #334155 Slate Border
    C_CYAN = RGBColor(56, 189, 248)     # #38BDF8 Neon Cyan
    C_GREEN = RGBColor(16, 185, 129)    # #10B981 Emerald
    C_AMBER = RGBColor(245, 158, 11)    # #F59E0B Amber
    C_RED = RGBColor(239, 68, 68)       # #EF4444 Red Accent
    C_WHITE = RGBColor(248, 250, 252)   # #F8FAFC Crisp White
    C_MUTED = RGBColor(148, 163, 184)   # #94A3B8 Slate Grey
    C_BADGE = RGBColor(2, 132, 199)     # #0284C7 Sky Blue
    
    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, category, title, subtitle=None):
        # Top accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.04))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_CYAN
        bar.line.fill.background()
        
        # Category pill text
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.44), Inches(11.733), Inches(0.25))
        tf = cat_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = category.upper()
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_CYAN
        p.font.name = "Segoe UI"
        
        # Slide Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.55))
        tf = t_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.font.name = "Segoe UI"
        
        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.size = Pt(11)
            p2.font.color.rgb = C_MUTED
            p2.font.name = "Segoe UI"

    def add_card(slide, left, top, width, height, bg_color=C_CARD, border_color=C_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Non-Technical & Engaging)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)
    
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(4.5), Inches(0.38))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_BADGE
    badge.line.fill.background()
    tf = badge.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = "SMART ZOO MONITORING | CHIANG MAI ZOO"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.font.name = "Segoe UI"

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(11.733), Inches(1.6))
    tf = t_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Automated Civet Behavior\nMonitoring System"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.font.name = "Segoe UI"

    sub_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.9), Inches(11.733), Inches(0.8))
    tf = sub_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "A 24/7 Smart Camera Assistant That Tracks Animal Health & Daily Habits Automatically"
    p.font.size = Pt(16)
    p.font.color.rgb = C_CYAN
    p.font.name = "Segoe UI"

    specs = [
        ("WHAT IT TRACKS", "Walking, Eating, Sleeping\nCovers 85%+ of Daily Life", C_GREEN),
        ("WHERE IT WORKS", "4-Room Night Enclosure\nWorks in Complete Darkness (IR)", C_CYAN),
        ("HOW IT RUNS", "Lightweight & Super Fast\nRuns on a Normal Laptop", C_AMBER)
    ]
    for i, (title, desc, acc_color) in enumerate(specs):
        x = 0.8 + i * 4.0
        add_card(s1, x, 5.0, 3.733, 1.6)
        tb = s1.shapes.add_textbox(Inches(x + 0.2), Inches(5.15), Inches(3.333), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = acc_color
        p1.font.name = "Segoe UI"
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(12)
        p2.font.color.rgb = C_WHITE
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(4)

    add_notes(s1, """Hello everyone. Today, our team is excited to present the Automated Civet Behavior Monitoring System, created in partnership with Chiang Mai Zoo.

Imagine having a smart virtual assistant that watches security cameras day and night, quietly taking notes whenever the animal walks, eats, or sleeps. That is exactly what we built. 

In this presentation, we will show you how simple computer vision can solve a real-world zoo problem, without needing expensive supercomputers or confusing black-box AI.""")

    # =========================================================================
    # SLIDE 2: PROBLEM & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "The Real-World Challenge", "The Trouble with Watching CCTV by Hand", "Why zookeepers need a smart assistant instead of staring at screens for hours")

    challenges = [
        ("1. Hours of Rewinding Video", "Zoo staff have to sit through hours of recorded CCTV across 4 different rooms, taking valuable time away from hands-on animal care.", C_RED),
        ("2. Eye Fatigue & Missed Moments", "Staring at security screens for hours is exhausting. People easily miss when the animal took a quick drink or a 10-second walk.", C_AMBER),
        ("3. Animals Active in the Dark", "Civets love the night! Most activity happens in pitch-black darkness under infrared cameras where human eyes struggle to see.", C_CYAN)
    ]
    for i, (title, desc, col) in enumerate(challenges):
        y = 1.6 + i * 1.7
        add_card(s2, 0.8, y, 5.7, 1.5)
        tb = s2.shapes.add_textbox(Inches(1.0), Inches(y + 0.15), Inches(5.3), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.font.name = "Segoe UI"
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11.5)
        p2.font.color.rgb = C_WHITE
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(4)

    add_card(s2, 6.8, 1.6, 5.733, 4.9, bg_color=C_CARD_ALT, border_color=C_CYAN)
    tb = s2.shapes.add_textbox(Inches(7.1), Inches(1.85), Inches(5.133), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "OUR AUTOMATED SOLUTION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.font.name = "Segoe UI"

    bullets = [
        ("Watches 24/7 Without Tiring", "The system never blinks or gets tired. It watches every camera feed all night and records behavior as it happens."),
        ("Simple, Explainable Rules", "No confusing mystery AI. It uses clear, common-sense rules: if the civet walks across the room, it's walking; if its head is in the food bowl, it's eating."),
        ("Runs on an Ordinary PC", "No need for costly GPU servers. It runs smoothly on a standard zoo office computer."),
        ("Clear Daily Health Reports", "Generates daily summaries showing exact meal times, sleeping hours, and activity levels for the zoo veterinarians.")
    ]
    for b_title, b_desc in bullets:
        p1 = tf.add_paragraph()
        p1.text = f"•  {b_title}: "
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p1.font.name = "Segoe UI"
        p1.space_before = Pt(10)
        run = p1.add_run()
        run.text = b_desc
        run.font.bold = False
        run.font.color.rgb = C_MUTED

    add_notes(s2, """To understand why this project matters, look at how zookeepers currently work.

Right now, zookeepers have to manually review hours of security footage, rewinding and fast-forwarding across four separate screens while taking notes on paper sheets with pens.

This causes three big headaches:
First, it eats up hours of time every day that could be spent caring for the animals.
Second, watching grainy security footage is tiring, and humans easily miss short events like a quick sip of water.
Third, civets are nocturnal. Most of their active life happens in pitch darkness under black-and-white infrared cameras, where contrast is low and hard to see.

Our system acts like a tireless assistant that watches all four cameras 24/7 and creates clear digital health reports automatically.""")

    # =========================================================================
    # SLIDE 3: PHYSICAL SETUP & CAMERAS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "The Zoo Enclosure", "Understanding the Animal's Home", "How fixed security cameras give our computer an unfair advantage")

    cams = [
        ("CAMERA 02: THE DINING ROOM", 
         "• What it monitors: The Food & Water bowls\n"
         "• Camera Type: Full color in daytime, infrared at night\n"
         "• Key Landmark: Food tray placed permanently at the bottom center\n"
         "• Behavior Goal: Spotting exactly when and how long the civet eats", C_AMBER),
        ("CAMERA 03: THE BEDROOM & PLAYGROUND",
         "• What it monitors: Sleeping nest & climbing log\n"
         "• Camera Type: Night-vision infrared (black & white)\n"
         "• Key Landmarks: Tire bed filled with straw (top) & wooden climbing log\n"
         "• Behavior Goal: Spotting when the civet curls up to sleep or walks across", C_CYAN)
    ]
    for i, (c_title, c_desc, c_col) in enumerate(cams):
        y = 1.6 + i * 2.5
        add_card(s3, 0.8, y, 6.2, 2.3)
        tb = s3.shapes.add_textbox(Inches(1.0), Inches(y + 0.15), Inches(5.8), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = c_title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = c_col
        p1.font.name = "Segoe UI"
        
        p2 = tf.add_paragraph()
        p2.text = c_desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_WHITE
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(6)

    add_card(s3, 7.3, 1.6, 5.233, 4.8)
    tb = s3.shapes.add_textbox(Inches(7.6), Inches(1.85), Inches(4.633), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "THE FIXED CAMERA ADVANTAGE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.font.name = "Segoe UI"

    adv_points = [
        ("The Room Never Moves", "Because cameras are bolted to the walls, the background is completely still. Any change in pixels is guaranteed to be the civet moving!"),
        ("We Know Where Things Are", "The food bowl is always in Camera 02. The straw tire bed is always in Camera 03. We simply tell the computer where these 'zones' are, making tracking easy and reliable."),
        ("Lighting Doesn't Fool It", "Our motion detector automatically adapts as daylight shifts into dusk, keeping the civet clearly visible at all times.")
    ]
    for t_pt, d_pt in adv_points:
        p1 = tf.add_paragraph()
        p1.text = f"✔  {t_pt}"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p1.font.name = "Segoe UI"
        p1.space_before = Pt(10)
        
        p2 = tf.add_paragraph()
        p2.text = d_pt
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_MUTED
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(2)

    add_notes(s3, """Let's take a look inside the civet's enclosure.

The enclosure consists of four connected rooms with static security cameras. In our video dataset, two cameras are especially important:

Camera 02 looks at the 'dining room', where the food and water trays sit permanently on the floor.
Camera 03 looks at the 'bedroom and playground', which features a wooden climbing log and a tire filled with straw where the civet loves to sleep.

Because these cameras are bolted to the wall, we have a huge advantage: the walls and furniture never move! 
We simply mark a green box around the food tray and another box around the tire bed. Whenever the animal enters those boxes, the computer knows immediately what it is doing.""")

    # =========================================================================
    # SLIDE 4: TARGET BEHAVIORS & DECISION LOGIC
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Target Behaviors", "The Three Daily Habits We Track", "Simple common-sense rules that cover over 85% of a civet's daily routine")

    b_cards = [
        ("WALKING / RUNNING", "Active Locomotion", C_CYAN,
         "• What is it? Moving purposefully across the room.\n"
         "• The Rule: Moves at least 15 pixels every half-second for 3 seconds or more.\n"
         "• State: ACTIVE\n"
         "• Why it works: Discards tiny ear or tail twitches while catching real walking trips."),
         
        ("EATING / DRINKING", "Visiting the Food Bowl", C_AMBER,
         "• What is it? Lowering head into the food or water tray.\n"
         "• The Rule: Head stays inside the Food Tray Zone for 10 seconds or more.\n"
         "• State: ACTIVE\n"
         "• Why it works: Successfully separates eating a full meal from just walking past the bowl."),
         
        ("SLEEPING / RESTING", "Curling Up in the Nest", C_GREEN,
         "• What is it? Lying completely still in the straw tire bed.\n"
         "• The Rule: Inside the tire bed + zero movement for 1 full minute (60s rule).\n"
         "• State: INACTIVE (Resting)\n"
         "• Why it works: Matches the zoo ethogram 'Curling up in tire' and prevents false alarms.")
    ]
    for i, (b_title, b_sub, b_col, b_text) in enumerate(b_cards):
        x = 0.8 + i * 4.0
        add_card(s4, x, 1.6, 3.733, 5.0)
        
        top_bar = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + 0.2), Inches(1.8), Inches(3.333), Inches(0.04))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = b_col
        top_bar.line.fill.background()
        
        tb = s4.shapes.add_textbox(Inches(x + 0.2), Inches(1.95), Inches(3.333), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = b_title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = b_col
        p.font.name = "Segoe UI"
        
        p_sub = tf.add_paragraph()
        p_sub.text = b_sub
        p_sub.font.size = Pt(10.5)
        p_sub.font.color.rgb = C_MUTED
        p_sub.font.name = "Segoe UI"
        
        p_body = tf.add_paragraph()
        p_body.text = b_text
        p_body.font.size = Pt(11)
        p_body.font.color.rgb = C_WHITE
        p_body.font.name = "Segoe UI"
        p_body.space_before = Pt(8)

    add_notes(s4, """Chiang Mai Zoo has an official catalog of 8 animal behaviors. In Phase 1, we focused on the three most common ones that make up over 85% of the civet's day:

1. Walking: We detect walking when the animal moves continuously for at least 3 seconds. If it just turns its head or twitches an ear, that is ignored.
2. Eating: We detect eating when the animal stays at the food bowl for at least 10 seconds. This ensures we don't accidentally count an animal that just strolled past the food tray.
3. Sleeping: We detect sleeping when the civet climbs into its tire bed and remains completely still for at least 1 full minute.

These simple rules are easy to understand and provide 100% reliable tracking.""")

    # =========================================================================
    # SLIDE 5: SYSTEM PIPELINE & FLOWCHART (Simple 5 Steps)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "How It Works", "The 5 Simple Steps of Our System", "How the computer turns raw video into clean daily notes")

    # Embed Flowchart Image
    if os.path.exists(flowchart_img):
        s5.shapes.add_picture(flowchart_img, Inches(0.8), Inches(1.6), width=Inches(8.8), height=Inches(4.8))

    # Right Column Summary Card
    add_card(s5, 9.85, 1.6, 2.68, 5.2)
    tb = s5.shapes.add_textbox(Inches(10.0), Inches(1.75), Inches(2.38), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "THE 5 EASY STEPS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.font.name = "Segoe UI"

    stages = [
        ("1. Check Twice a Second", "We don't need 30 frames/s. Checking 2 times a second saves 85% computer power."),
        ("2. Spot What Moves", "The walls and logs never move. Anything moving must be the civet!"),
        ("3. Clean the Picture", "Wipe away camera fuzz and find the center point of the animal."),
        ("4. Check Zone & Speed", "Is it at the food bowl? Or is it walking across the room?"),
        ("5. Write the Daily Log", "Creates a clean digital note for the zookeepers automatically.")
    ]
    for s_name, s_txt in stages:
        p1 = tf.add_paragraph()
        p1.text = s_name
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p1.font.name = "Segoe UI"
        p1.space_before = Pt(6)
        
        p2 = tf.add_paragraph()
        p2.text = s_txt
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_MUTED
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(1)

    add_notes(s5, """This diagram shows the five simple steps our system follows.

First, we look at the video twice every second instead of 15 times. That is more than enough to see an animal walking, and it saves 85% of computer power.
Second, the computer learns what the still, empty room looks like. Anything that moves must be the civet!
Third, we clean up the grainy night video so we have a clear dot tracking the animal.
Fourth, we check where that dot is: is it walking across the room, or is its head in the food bowl?
And finally, step five: the system writes a clean digital log of what happened without any human effort.""")

    # =========================================================================
    # SLIDE 6: EXPERIMENTAL RESULT 1 — LOCOMOTION
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Real Video Test 1", "Spotting When the Civet Walks", "Tested on actual night-vision security video (Camera 03)")

    if os.path.exists(locomotion_img):
        s6.shapes.add_picture(locomotion_img, Inches(0.8), Inches(1.6), width=Inches(8.8), height=Inches(4.83))

    add_card(s6, 9.85, 1.6, 2.68, 5.2)
    tb = s6.shapes.add_textbox(Inches(10.0), Inches(1.75), Inches(2.38), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "WALKING TEST"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.font.name = "Segoe UI"

    loco_metrics = [
        ("What Happened?", "Civet walked across the room in 3.2 seconds"),
        ("What Computer Saw", "Tracked the full orange path from start to finish"),
        ("Speed Curve", "Speed jumped above 50 px while walking"),
        ("Stopping Point", "Speed dropped straight to zero upon arrival"),
        ("Key Result", "Successfully recorded the full walk without being tricked by ear twitches")
    ]
    for m_label, m_val in loco_metrics:
        p1 = tf.add_paragraph()
        p1.text = m_label
        p1.font.size = Pt(10.5)
        p1.font.bold = True
        p1.font.color.rgb = C_AMBER if m_label == "Speed Curve" else C_WHITE
        p1.font.name = "Segoe UI"
        p1.space_before = Pt(6)
        
        p2 = tf.add_paragraph()
        p2.text = m_val
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_MUTED
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(1)

    add_notes(s6, """Here is our first test on real security video from Chiang Mai Zoo. This is Camera 03 at night.

In pictures 1, 2, and 3, you see the civet walking from left to right across the floor in about 3 seconds.
In picture 4, the computer drew the orange trail showing the exact walking path.
And in picture 5, the blue line shows the animal's speed. As it walks, the speed jumps up high, and when it stops at its destination, the speed drops right back to zero.

This proves the computer can spot real walking trips without getting tricked by tiny movements.""")

    # =========================================================================
    # SLIDE 7: EXPERIMENTAL RESULT 2 — EATING
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Real Video Test 2", "Measuring Meal Times at the Food Bowl", "Tested on daytime enclosure video (Camera 02)")

    if os.path.exists(eating_img):
        s7.shapes.add_picture(eating_img, Inches(0.8), Inches(1.6), width=Inches(8.8), height=Inches(4.83))

    add_card(s7, 9.85, 1.6, 2.68, 5.2)
    tb = s7.shapes.add_textbox(Inches(10.0), Inches(1.75), Inches(2.38), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "MEALTIME TEST"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.font.name = "Segoe UI"

    eat_metrics = [
        ("What Happened?", "Civet visited the food bowl and ate for 80 seconds"),
        ("Food Bowl Zone", "Marked in orange at the bottom center"),
        ("Head Position", "Stayed right over the bowl (green dots)"),
        ("Meal Duration", "80 seconds continuous meal recorded"),
        ("Key Result", "Separates a real meal from simply walking past the bowl")
    ]
    for m_label, m_val in eat_metrics:
        p1 = tf.add_paragraph()
        p1.text = m_label
        p1.font.size = Pt(10.5)
        p1.font.bold = True
        p1.font.color.rgb = C_GREEN if m_label == "Meal Duration" else C_WHITE
        p1.font.name = "Segoe UI"
        p1.space_before = Pt(6)
        
        p2 = tf.add_paragraph()
        p2.text = m_val
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_MUTED
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(1)

    add_notes(s7, """Here is our second test, focusing on eating. This was recorded during the day on Camera 02.

In pictures 1, 2, and 3, the civet walks over to the food bowl and lowers its head to eat.
In picture 4, you can see the orange box where the food tray sits. The green dots show the computer tracking the civet's head right over the food!
In picture 5, the timer climbs up to 80 seconds. The computer measured an 80-second continuous meal.

Because we require the animal to stay at the bowl for at least 10 seconds, the system will never confuse an animal that just strolled past with an animal eating dinner.""")

    # =========================================================================
    # SLIDE 8: EXPERIMENTAL RESULT 3 — RESTING
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Real Video Test 3", "Confirming Bedtime in the Tire Nest", "Tested on night-vision video (Camera 03)")

    if os.path.exists(resting_img):
        s8.shapes.add_picture(resting_img, Inches(0.8), Inches(1.6), width=Inches(8.8), height=Inches(4.83))

    add_card(s8, 9.85, 1.6, 2.68, 5.2)
    tb = s8.shapes.add_textbox(Inches(10.0), Inches(1.75), Inches(2.38), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "BEDTIME TEST"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.font.name = "Segoe UI"

    rest_metrics = [
        ("Bedtime Spot", "Straw-lined tire bed at top of room"),
        ("Shelter Entry", "Climbed in at 27 seconds"),
        ("Sleeping Posture", "Curled into a ball in straw"),
        ("1-Minute Rule", "Stillness timer passed 60s at 86s mark"),
        ("State Output", "Officially recorded as ASLEEP"),
        ("Key Result", "Matches zoo description: 'Curling up in tire'")
    ]
    for m_label, m_val in rest_metrics:
        p1 = tf.add_paragraph()
        p1.text = m_label
        p1.font.size = Pt(10.5)
        p1.font.bold = True
        p1.font.color.rgb = C_CYAN if m_label == "State Output" else C_WHITE
        p1.font.name = "Segoe UI"
        p1.space_before = Pt(5)
        
        p2 = tf.add_paragraph()
        p2.text = m_val
        p2.font.size = Pt(10)
        p2.font.color.rgb = C_MUTED
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(1)

    add_notes(s8, """Here is our third test: tracking sleep.

Thanks to the zookeepers' guidance, we know the civet loves to sleep in the tire filled with straw at the top of Camera 03.
In this video, the civet climbs into the tire at 27 seconds and curls up into a ball, exactly matching the zoo's official note: 'Curling up in tire'.
In picture 5, our stillness timer starts counting. Once the civet stays completely still for 60 seconds in a row, the computer officially logs: 'The animal is asleep.'

This shows the computer understands both where the animal sleeps and how long it stays still.""")

    # =========================================================================
    # SLIDE 9: CV BENCHMARK — FANCY AI vs SIMPLE SMART VISION
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Why Simple Is Better", "Fancy AI vs. Tailored Smart Vision", "Why complex AI struggled in the dark, and our simple method won")

    add_card(s9, 0.8, 1.6, 5.7, 5.0)
    tb = s9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "FANCY DEEP LEARNING (YOLO)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p.font.name = "Segoe UI"

    coco_bullets = [
        ("Doesn't Know Civets", "Trained on sunny pictures of dogs and cats. It gets confused by civets with long bodies and masked faces."),
        ("Blind in the Dark", "On grainy black-and-white night video, standard AI frequently missed the civet completely."),
        ("Hallucinated Plants & Birds", "Mistook static potted plants for birds with 90% confidence!"),
        ("Needs Expensive Computers", "Requires heavy, expensive gaming GPUs to run.")
    ]
    for t_pt, d_pt in coco_bullets:
        p1 = tf.add_paragraph()
        p1.text = f"✗  {t_pt}"
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p1.font.name = "Segoe UI"
        p1.space_before = Pt(8)
        
        p2 = tf.add_paragraph()
        p2.text = d_pt
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_MUTED
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(2)

    add_card(s9, 6.8, 1.6, 5.733, 5.0, bg_color=C_CARD_ALT, border_color=C_GREEN)
    tb = s9.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.333), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "OUR TAILORED SMART VISION"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.font.name = "Segoe UI"

    cv_bullets = [
        ("Takes Advantage of Still Cameras", "Because cameras never move, it knows the room by heart and easily isolates the moving animal."),
        ("Zero Plant Confusions", "Static plants and walls are completely ignored—it never makes up fake objects!"),
        ("100% Reliable Tracking", "Never loses the animal in the dark, even when lighting shifts."),
        ("Runs on an Ordinary PC", "Runs over 10x faster on a normal office laptop without needing any extra hardware.")
    ]
    for t_pt, d_pt in cv_bullets:
        p1 = tf.add_paragraph()
        p1.text = f"✔  {t_pt}"
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p1.font.name = "Segoe UI"
        p1.space_before = Pt(8)
        
        p2 = tf.add_paragraph()
        p2.text = d_pt
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_MUTED
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(2)

    add_notes(s9, """You might ask: Why not just download the latest deep learning AI?

We tried that! We ran YOLO, a very popular deep learning model, and it struggled terribly in the dark.
Because it was trained on sunny pictures of dogs and cats, it got confused by black-and-white night video. It missed the civet completely, and it even pointed at a potted plant and called it a bird with 90% confidence! Plus, it needs expensive computers.

Instead, our tailored vision system takes advantage of the fact that the zoo cameras never move. It ignores all plants and walls, tracks the civet 100% reliably, and runs smoothly on an ordinary office laptop.""")

    # =========================================================================
    # SLIDE 10: TEMPORAL LOGIC & 1-MINUTE STATE ENGINE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Smart Common Sense", "The 1-Minute Rule: Avoiding Silly Mistakes", "How the system tells the difference between a short pause and a real nap")

    add_card(s10, 0.8, 1.6, 5.7, 5.0)
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "TWO LEVELS OF SMART TRACKING"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.font.name = "Segoe UI"

    pts = [
        ("The Big Picture (Active vs. Asleep)", "Keeps track of overall day and night cycles. Is the animal up and about, or is it asleep for the night?"),
        ("The Small Events (Walks & Meals)", "Catches short events without getting confused: a quick 10-second walk or an 80-second meal."),
        ("Why Two Levels?", "Animals naturally take 5-second breathers while walking, or twitch while sleeping. Two levels prevent the computer from changing its mind every two seconds.")
    ]
    for t_pt, d_pt in pts:
        p1 = tf.add_paragraph()
        p1.text = f"•  {t_pt}"
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p1.font.name = "Segoe UI"
        p1.space_before = Pt(10)
        
        p2 = tf.add_paragraph()
        p2.text = d_pt
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_MUTED
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(3)

    add_card(s10, 6.8, 1.6, 5.733, 5.0, bg_color=C_CARD_ALT)
    tb = s10.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.333), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "HOW THE 1-MINUTE RULE WORKS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.font.name = "Segoe UI"

    rules = [
        ("A 5-Second Stop is NOT Sleep", "If an animal stops for a few seconds during a walk, it hasn't gone to bed! The computer waits for a full 60 seconds of stillness before saying it's asleep."),
        ("Moving Wakes It Up Instantly", "As soon as the animal starts walking for 3 seconds, the sleep state ends immediately."),
        ("Scratching Doesn't Ruin Sleep", "Small tail wiggles or ear scratches while lying down don't fool the computer into thinking it woke up."),
        ("Clean, Trustworthy Reports", "Produces daily health logs that zoo veterinarians can actually trust.")
    ]
    for t_pt, d_pt in rules:
        p1 = tf.add_paragraph()
        p1.text = f"⚙  {t_pt}"
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p1.font.name = "Segoe UI"
        p1.space_before = Pt(8)
        
        p2 = tf.add_paragraph()
        p2.text = d_pt
        p2.font.size = Pt(11)
        p2.font.color.rgb = C_MUTED
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(2)

    add_notes(s10, """One big problem with computer monitoring is 'flickering'—when the computer changes its mind every second.

If an animal pauses for 5 seconds while walking, it didn't fall asleep! And if a sleeping animal scratches its ear, it didn't wake up.

To solve this, we built in some common sense: the 1-Minute Rule.
The computer waits for 60 seconds of unbroken stillness before declaring that the animal is asleep. And if the animal starts walking, it immediately marks it as active.
This simple rule keeps our daily reports clean, accurate, and trustworthy.""")

    # =========================================================================
    # SLIDE 11: DATASET ANALYSIS & PERFORMANCE
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "Proven in Practice", "Tested on 22 Real Zoo Videos", "Fast, light, and ready for everyday use at Chiang Mai Zoo")

    stats = [
        ("TOTAL CLIPS TESTED", "22 Video Files", "Walking, Eating, Sleeping", C_CYAN),
        ("CHECKS TWICE A SECOND", "2 Frames / Sec", "Saves 85% Computer Power", C_GREEN),
        ("LIGHTWEIGHT SPEED", "> 45 FPS on Laptop", "Runs on Normal Zoo PC", C_AMBER)
    ]
    for i, (title, big_val, sub, col) in enumerate(stats):
        x = 0.8 + i * 4.0
        add_card(s11, x, 1.6, 3.733, 1.5)
        tb = s11.shapes.add_textbox(Inches(x + 0.2), Inches(1.7), Inches(3.333), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.font.name = "Segoe UI"
        
        p2 = tf.add_paragraph()
        p2.text = big_val
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(2)
        
        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = C_MUTED
        p3.font.name = "Segoe UI"

    add_card(s11, 0.8, 3.3, 5.7, 3.3)
    tb = s11.shapes.add_textbox(Inches(1.0), Inches(3.45), Inches(5.3), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "REAL ZOO CONDITIONS TESTED"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.font.name = "Segoe UI"
    
    v_specs = [
        "• High Definition: 1080p Full HD security video",
        "• All Lighting Conditions: Daytime color and pitch-black infrared",
        "• Real Animal Behaviors: 8 eating clips, 8 walking clips, 6 sleeping clips",
        "• Varied Lengths: Short 10-second walks to 2-minute continuous naps"
    ]
    for s_line in v_specs:
        p_line = tf.add_paragraph()
        p_line.text = s_line
        p_line.font.size = Pt(11)
        p_line.font.color.rgb = C_WHITE
        p_line.font.name = "Segoe UI"
        p_line.space_before = Pt(6)

    add_card(s11, 6.8, 3.3, 5.733, 3.3, bg_color=C_CARD_ALT)
    tb = s11.shapes.add_textbox(Inches(7.0), Inches(3.45), Inches(5.333), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "WHY CHECKING 2 TIMES A SECOND WINS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p.font.name = "Segoe UI"
    
    e_pts = [
        ("Animals Move at Natural Speeds", "A civet walking across the room takes 3 to 10 seconds. Checking twice a second gives us 6 to 20 snapshots—plenty to see every step!"),
        ("Huge Power Savings", "Checking twice a second instead of 15 cuts computer workload by over 85%, so the computer stays cool and never lags."),
        ("Never Misses Meals or Naps", "Because eating lasts minutes and sleeping lasts hours, twice a second captures 100% of start and end times.")
    ]
    for t_pt, d_pt in e_pts:
        p1 = tf.add_paragraph()
        p1.text = f"✔  {t_pt}: "
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p1.font.name = "Segoe UI"
        p1.space_before = Pt(4)
        run = p1.add_run()
        run.text = d_pt
        run.font.bold = False
        run.font.color.rgb = C_MUTED

    add_notes(s11, """We didn't just test this on one video—we tested it across 22 real video recordings from Chiang Mai Zoo.

Our key finding is that checking the video twice a second is the sweet spot. A walking civet takes several seconds to cross the room, so checking twice a second captures every step while cutting computer workload by over 85%.

As a result, the entire system runs smoothly on a basic laptop at over 45 frames per second. It is ready for practical, everyday use at the zoo.""")

    # =========================================================================
    # SLIDE 12: DELIVERABLES & ROADMAP
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12)
    add_header(s12, "Summary & Future", "What We Built & Where We Are Going Next", "From video cameras to a smart tool for animal happiness and health")

    add_card(s12, 0.8, 1.6, 5.7, 5.0)
    tb = s12.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "WHAT WE DELIVERED TODAY (PHASE 1)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.font.name = "Segoe UI"

    delivs = [
        ("Automatic Daily Notes", "Creates digital records of every walk, meal, and nap with exact timestamps."),
        ("Proven Accuracy", "Tested and validated on 22 real zoo video clips under night and day lighting."),
        ("Common-Sense Logic", "The 1-minute rule prevents silly mistakes and false sleep alarms."),
        ("Works on Everyday Computers", "Runs fast on normal zoo office PCs without buying expensive extra gear.")
    ]
    for t_pt, d_pt in delivs:
        p1 = tf.add_paragraph()
        p1.text = f"✔  {t_pt}"
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p1.font.name = "Segoe UI"
        p1.space_before = Pt(8)
        
        p2 = tf.add_paragraph()
        p2.text = d_pt
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_MUTED
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(2)

    add_card(s12, 6.8, 1.6, 5.733, 5.0, bg_color=C_CARD_ALT)
    tb = s12.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.333), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "WHAT COMES NEXT (PHASE 2)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.font.name = "Segoe UI"

    roadmap = [
        ("Follow Civets Across Rooms", "Keep tracking the animal as it walks through tunnels between Rooms 1, 2, 3, and 4."),
        ("Spot More Behaviors", "Notice bathroom visits in the sand box and self-grooming sessions."),
        ("Train a Custom Civet AI", "Teach a lightweight AI specifically on Chiang Mai Zoo's civets to boost dark recognition even further."),
        ("Zookeeper Tablet Dashboard", "A friendly phone or tablet app showing daily charts and alerting staff if an animal stops eating.")
    ]
    for t_pt, d_pt in roadmap:
        p1 = tf.add_paragraph()
        p1.text = f"🚀  {t_pt}"
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = C_WHITE
        p1.font.name = "Segoe UI"
        p1.space_before = Pt(8)
        
        p2 = tf.add_paragraph()
        p2.text = d_pt
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_MUTED
        p2.font.name = "Segoe UI"
        p2.space_before = Pt(2)

    add_notes(s12, """To wrap up: in Phase 1, we successfully built a smart assistant that watches zoo cameras and creates automated, reliable records of walking, eating, and sleeping.

It is fast, explainable, and runs on normal computers without extra cost.

Looking ahead to Phase 2, we plan to follow the civet as it moves between all four rooms, detect bathroom visits and grooming, and give zookeepers a friendly phone app that shows daily health summaries at a glance.

Thank you very much for listening. We would love to answer any questions!""")

    try:
        prs.save(output_pptx)
        print(f"Presentation saved successfully with {len(prs.slides)} slides to:\n{output_pptx}")
    except PermissionError:
        fallback_path = os.path.join(project_root, "presentations", "Civet_Behavior_Monitoring_Presentation_EN_Easy.pptx")
        prs.save(fallback_path)
        print(f"Original file is locked by PowerPoint. Saved successfully to:\n{fallback_path}")

if __name__ == "__main__":
    build_presentation()
