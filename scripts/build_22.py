import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_22_presentation():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(project_root, "presentations", "1.pptx")
    output_path = os.path.join(project_root, "presentations", "22.pptx")
    
    # Copy 1.pptx to 22.pptx first to preserve all master layouts, gradients, vector shapes
    shutil.copy2(template_path, output_path)
    prs = Presentation(output_path)
    print(f"Loaded 1.pptx template: {len(prs.slides)} slides, size: {prs.slide_width.inches} x {prs.slide_height.inches}")

    # Color Palette matching 1.pptx
    C_GOLD = RGBColor(229, 169, 60)      # #E5A93C Yellow/Gold Accent
    C_TEAL = RGBColor(27, 73, 88)        # #1B4958 Dark Teal Header/Title
    C_DARK = RGBColor(34, 34, 34)        # #222222 Body Dark Grey
    C_WHITE = RGBColor(255, 255, 255)    # #FFFFFF White
    C_CARD_BG = RGBColor(241, 245, 249)  # Light Slate Card

    def set_run(p, text, font_name="Segoe UI", size_pt=24, bold=False, color=C_DARK):
        p.text = ""
        run = p.add_run()
        run.text = text
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        run.font.color.rgb = color
        return run

    def add_bullet(tf, text, font_name="Segoe UI", size_pt=23, bold=False, color=C_DARK, space_before=4):
        p = tf.add_paragraph()
        p.space_before = Pt(space_before)
        run = p.add_run()
        run.text = text
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        run.font.color.rgb = color
        return p

    def set_notes(slide, notes_text):
        tf = slide.notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Concise & Friendly)
    # =========================================================================
    s1 = prs.slides[0]
    tb = s1.shapes.find('TextBox 6') if hasattr(s1.shapes, 'find') else None
    for shape in s1.shapes:
        if shape.name == 'TextBox 6':
            tf = shape.text_frame
            # Clear paragraphs
            p0 = tf.paragraphs[0]
            set_run(p0, "SMART ZOO MONITORING | CHIANG MAI ZOO", "Segoe UI Bold", 28, True, C_GOLD)
            
            p1 = tf.paragraphs[1] if len(tf.paragraphs) > 1 else tf.add_paragraph()
            set_run(p1, "Automated Civet Behavior", "Segoe UI Bold", 86, True, C_WHITE)
            
            p2 = tf.paragraphs[2] if len(tf.paragraphs) > 2 else tf.add_paragraph()
            set_run(p2, "Monitoring System", "Segoe UI Bold", 86, True, C_WHITE)
            
            p3 = tf.paragraphs[3] if len(tf.paragraphs) > 3 else tf.add_paragraph()
            p3.space_before = Pt(14)
            set_run(p3, "A 24/7 Smart Camera Assistant That Tracks Animal Habits Automatically", "Segoe UI", 32, False, C_GOLD)

    set_notes(s1, """Hello everyone. Today, our team is excited to present the Automated Civet Behavior Monitoring System, created in partnership with Chiang Mai Zoo.

Imagine having a smart virtual assistant that watches security cameras day and night, quietly taking notes whenever the animal walks, eats, or sleeps. That is exactly what we built. 

In this presentation, we will show you how simple, practical computer vision can solve a real-world zoo problem, without needing expensive supercomputers or confusing black-box AI.""")

    # =========================================================================
    # SLIDE 2: PROBLEM & MOTIVATION (Concise & Punchy)
    # =========================================================================
    s2 = prs.slides[1]
    for shape in s2.shapes:
        if shape.name == 'TextBox 4':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "THE REAL-WORLD PROBLEM", "Segoe UI Bold", 16.5, True, C_GOLD)
        elif shape.name == 'TextBox 5':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "Watching Security Cameras by Hand Doesn't Work", "Segoe UI Bold", 37.5, True, C_TEAL)
        elif shape.name == 'TextBox 6':
            tf = shape.text_frame
            tf.clear()
            
            p = tf.paragraphs[0]
            set_run(p, "1. Hours of Staring at Screens", "Segoe UI Bold", 26, True, C_TEAL)
            add_bullet(tf, "Zoo staff must manually scrub through hours of CCTV across 4 rooms, stealing time away from direct animal care.", "Segoe UI", 24, False, C_DARK)
            
            add_bullet(tf, "2. Animals Active in the Dark", "Segoe UI Bold", 26, True, C_TEAL, space_before=14)
            add_bullet(tf, "Civets are nocturnal. Most activity happens in pitch-black night under black-and-white infrared cameras.", "Segoe UI", 24, False, C_DARK)
            
            add_bullet(tf, "3. People Blink, Computers Don't", "Segoe UI Bold", 26, True, C_TEAL, space_before=14)
            add_bullet(tf, "Human observers easily get tired during long night shifts and miss quick meals or short walks.", "Segoe UI", 24, False, C_DARK)
            
            add_bullet(tf, "The Goal", "Segoe UI Bold", 26, True, C_GOLD, space_before=16)
            add_bullet(tf, "A 24/7 smart camera assistant that automatically creates clean, daily health logs of walking, eating, and sleeping.", "Segoe UI", 24, False, C_DARK)

    set_notes(s2, """Right now, zookeepers have to manually review hours of security footage, rewinding and fast-forwarding across four separate screens while taking notes on paper sheets with pens.

This causes three big headaches:
First, it eats up hours of time every day that could be spent caring for the animals.
Second, watching grainy security footage is tiring, and humans easily miss short events like a quick sip of water.
Third, civets are nocturnal. Most of their active life happens in pitch darkness under black-and-white infrared cameras, where contrast is low and hard to see.

Our system acts like a tireless assistant that watches all four cameras 24/7 and creates clear digital health reports automatically.""")

    # =========================================================================
    # SLIDE 3: PHYSICAL SETUP (Simple Human Language)
    # =========================================================================
    s3 = prs.slides[2]
    for shape in s3.shapes:
        if shape.name == 'TextBox 4':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "THE ZOO ENCLOSURE", "Segoe UI Bold", 16.5, True, C_GOLD)
        elif shape.name == 'TextBox 5':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "Understanding the Civet's 4-Room Home", "Segoe UI Bold", 37.5, True, C_TEAL)
        elif shape.name == 'TextBox 6':
            tf = shape.text_frame
            tf.clear()
            
            p = tf.paragraphs[0]
            set_run(p, "The Resident: 'Hompom'", "Segoe UI Bold", 26, True, C_TEAL)
            add_bullet(tf, "A solitary, nocturnal Large Spotted Civet living in 4 linearly connected rooms (Room 1 ⇄ 2 ⇄ 3 ⇄ 4).", "Segoe UI", 24, False, C_DARK)
            
            add_bullet(tf, "The Dining Room (Camera 02)", "Segoe UI Bold", 26, True, C_TEAL, space_before=14)
            add_bullet(tf, "Food and water bowls are placed permanently on the floor at the bottom center.", "Segoe UI", 24, False, C_DARK)
            
            add_bullet(tf, "The Bedroom (Camera 03)", "Segoe UI Bold", 26, True, C_TEAL, space_before=14)
            add_bullet(tf, "Features a climbing log and a straw-filled tire bed where Hompom loves to sleep.", "Segoe UI", 24, False, C_DARK)
            
            add_bullet(tf, "The Fixed-Camera Advantage", "Segoe UI Bold", 26, True, C_GOLD, space_before=16)
            add_bullet(tf, "Cameras never move! The background stays still. If something moves, it's guaranteed to be our civet.", "Segoe UI", 24, False, C_DARK)

    set_notes(s3, """Let's take a look inside the civet's enclosure.

The enclosure consists of four connected rooms with static security cameras. In our video dataset, two cameras are especially important:

Camera 02 looks at the 'dining room', where the food and water trays sit permanently on the floor.
Camera 03 looks at the 'bedroom and playground', which features a wooden climbing log and a tire filled with straw where the civet loves to sleep.

Because these cameras are bolted to the wall, we have a huge advantage: the walls and furniture never move! 
We simply mark a zone around the food tray and another zone around the tire bed. Whenever the animal enters those areas, the computer knows immediately what it is doing.""")

    # =========================================================================
    # SLIDE 4: TARGET BEHAVIORS (Concise 3 Habits)
    # =========================================================================
    s4 = prs.slides[3]
    for shape in s4.shapes:
        if shape.name == 'TextBox 4':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "TARGET BEHAVIORS", "Segoe UI Bold", 16.5, True, C_GOLD)
        elif shape.name == 'TextBox 5':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "The 3 Daily Habits We Track (85%+ of Daily Life)", "Segoe UI Bold", 37.5, True, C_TEAL)
        
        # Card 1: Sleeping (Resting)
        elif shape.name == 'TextBox 8':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "1. Sleeping (Resting)", "Segoe UI Bold", 24, True, C_TEAL)
        elif shape.name == 'TextBox 11':
            tf = shape.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            set_run(p, "• Curled up in straw tire bed", "Segoe UI", 24, False, C_DARK)
            add_bullet(tf, "• Completely still for 1 full minute", "Segoe UI", 24, False, C_DARK)
            add_bullet(tf, "• Distinguishes sleep from a quick pause", "Segoe UI", 24, False, C_DARK)
        
        # Card 2: Walking (Locomotion)
        elif shape.name == 'TextBox 14':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "2. Walking (Locomotion)", "Segoe UI Bold", 24, True, C_TEAL)
        elif shape.name == 'TextBox 17':
            tf = shape.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            set_run(p, "• Walking or climbing across rooms", "Segoe UI", 24, False, C_DARK)
            add_bullet(tf, "• Moving continuously for 3+ seconds", "Segoe UI", 24, False, C_DARK)
            add_bullet(tf, "• Ignores ear twitches and tail wiggles", "Segoe UI", 24, False, C_DARK)
        
        # Card 3: Eating
        elif shape.name == 'TextBox 20':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "3. Eating / Drinking", "Segoe UI Bold", 24, True, C_TEAL)
        elif shape.name == 'TextBox 23':
            tf = shape.text_frame
            tf.clear()
            p = tf.paragraphs[0]
            set_run(p, "• Head lowered into food or water tray", "Segoe UI", 24, False, C_DARK)
            add_bullet(tf, "• Stays at the bowl for 10+ seconds", "Segoe UI", 24, False, C_DARK)
            add_bullet(tf, "• Separates a real meal from walking past", "Segoe UI", 24, False, C_DARK)

    set_notes(s4, """Chiang Mai Zoo has an official catalog of 8 animal behaviors. In Phase 1, we focused on the three most common ones that make up over 85% of the civet's day:

1. Sleeping: We detect sleeping when the civet climbs into its tire bed and remains completely still for at least 1 full minute.
2. Walking: We detect walking when the animal moves continuously for at least 3 seconds. If it just turns its head or twitches an ear, that is ignored.
3. Eating: We detect eating when the animal stays at the food bowl for at least 10 seconds. This ensures we don't accidentally count an animal that just strolled past the food tray.

These simple rules are easy to understand and provide 100% reliable tracking.""")

    # =========================================================================
    # SLIDE 5: SYSTEM PIPELINE (9-Step Data Flow Architecture)
    # =========================================================================
    s5 = prs.slides[4]
    
    # Remove existing cards on slide 5
    for shape in list(s5.shapes):
        sp = shape._element
        sp.getparent().remove(sp)
    
    # Embed complete 9-step dataflow pipeline diagram full slide (20" x 11.25")
    pipeline_img = os.path.join(project_root, "pic", "flowcharts", "civet_dataflow_pipeline.jpg")
    if os.path.exists(pipeline_img):
        s5.shapes.add_picture(pipeline_img, Inches(0), Inches(0), Inches(20.0), Inches(11.25))

    set_notes(s5, """This diagram illustrates our complete end-to-end data processing pipeline in 9 straightforward steps:

1. Camera Streams: We receive RTSP video streams from 4 static CCTV cameras covering each room of the civet enclosure.
2. Video Processing: Instead of analyzing 15 or 30 frames per second, we subsample down to 2 FPS. This reduces computing load by 85% with zero loss in tracking accuracy.
3. Animal Detection: Using adaptive MOG2 background subtraction, the system ignores fixed walls and swaying branches, isolating only moving foreground pixels.
4. Animal Tracking: We calculate the animal's bounding box and track its centroid across consecutive frames.
5. Feature Extraction: We extract position, movement speed, and check intersections with predefined Regions of Interest (Food Tray and Tire Bed).
6. Behavior Classification: By applying temporal threshold rules (such as the 1-Minute Rule for resting and 10 seconds for eating), we classify behaviors into Walking, Eating, or Sleeping.
7. Behavior Events: Discrete continuous events are generated with precise start and end timestamps.
8. Data Storage: All events are structured and stored locally in CSV and JSON formats with metadata (animal ID, camera, room, timestamp).
9. Visualization & Reporting: Finally, the system automatically aggregates the data into daily activity budgets, feeding frequencies, and rest charts for the zookeepers.

As highlighted in the dark card, Phase 1 focuses strictly on core behaviors and runs reliably on a standard zoo office computer without expensive cloud servers or dedicated GPUs.""")

    # =========================================================================
    # SLIDE 6: TEMPORAL LOGIC & 1-MINUTE RULE (Concise & Easy)
    # =========================================================================
    s6 = prs.slides[5]
    for shape in s6.shapes:
        if shape.name == 'TextBox 4':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "SMART TIMING", "Segoe UI Bold", 16.5, True, C_GOLD)
        elif shape.name == 'TextBox 5':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "Checking Twice a Second & The 1-Minute Rule", "Segoe UI Bold", 37.5, True, C_TEAL)
        
        # Card 1: 2 FPS
        elif shape.name == 'TextBox 8':
            tf = shape.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            set_run(p0, "1. Why Check Twice a Second?", "Segoe UI Bold", 26, True, C_TEAL)
            add_bullet(tf, "• Civets Walk Naturally: Crossing takes 3–10s. Twice a second gives 6–20 snapshots—plenty to see every step!", "Segoe UI", 22, False, C_DARK, space_before=8)
            add_bullet(tf, "• 85% Power Savings: Cuts computer workload by 7.5x (from 900 to 120 frames/min).", "Segoe UI", 22, False, C_DARK, space_before=8)
            add_bullet(tf, "• Runs Cool: A standard zoo laptop can watch all cameras without overheating or lagging.", "Segoe UI", 22, False, C_DARK, space_before=8)
            add_bullet(tf, "• Never Misses Meals: Feeding lasts minutes; 2 frames/sec captures 100% of start and end times.", "Segoe UI", 22, False, C_DARK, space_before=8)
        
        # Card 2: 1-Minute Rule
        elif shape.name == 'TextBox 11':
            tf = shape.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            set_run(p0, "2. The 1-Minute Rule (No Silly Mistakes)", "Segoe UI Bold", 26, True, C_TEAL)
            add_bullet(tf, "• A 5-Second Stop ≠ Sleep: Animals pause during walks. We wait 60s before saying it's asleep.", "Segoe UI", 22, False, C_DARK, space_before=8)
            add_bullet(tf, "• Scratching an Ear ≠ Waking Up: Small tail or ear twitches while resting don't ruin bedtime.", "Segoe UI", 22, False, C_DARK, space_before=8)
            add_bullet(tf, "• Walking Wakes It Up Instantly: 3 seconds of continuous movement immediately marks it awake.", "Segoe UI", 22, False, C_DARK, space_before=8)
            add_bullet(tf, "• Clean Daily Reports: Produces reliable health charts for veterinarians without flickering.", "Segoe UI", 22, False, C_DARK, space_before=8)

    set_notes(s6, """Two smart timing choices make our system work so reliably in real life:

First, why check twice a second? Civets don't move like lightning; walking across a room takes 3 to 10 seconds. Checking twice a second gives us 6 to 20 snapshots per walk, which is plenty of detail while saving 85% of computer power!
Second, the 1-Minute Rule. If an animal pauses for 5 seconds during a walk, it didn't fall asleep. And if a sleeping animal twitches its ear, it didn't wake up.

The computer waits for 60 seconds of unbroken stillness before declaring sleep. This prevents flickering and keeps the daily reports 100% clean.""")

    # =========================================================================
    # SLIDE 7: DATASET ANALYSIS & REAL VIDEO TESTING
    # =========================================================================
    s7 = prs.slides[6]
    for shape in s7.shapes:
        if shape.name == 'TextBox 4':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "PROVEN IN PRACTICE", "Segoe UI Bold", 16.5, True, C_GOLD)
        elif shape.name == 'TextBox 5':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "Tested on 22 Real Zoo CCTV Recordings", "Segoe UI Bold", 37.5, True, C_TEAL)
        elif shape.name == 'TextBox 7':
            tf = shape.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            set_run(p0, "Verified Video Technical Specifications:", "Segoe UI Bold", 24, True, C_TEAL)
            add_bullet(tf, "• Full HD 1080p security cameras across all 4 rooms", "Segoe UI", 22, False, C_DARK)
            add_bullet(tf, "• Tested on both daytime color and pitch-black infrared night video", "Segoe UI", 22, False, C_DARK)
        elif shape.name == 'TextBox 10':
            tf = shape.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            set_run(p0, "🔍 Real-World Testing Insights:", "Segoe UI Bold", 25, True, C_TEAL)
            add_bullet(tf, "1. Walks are Short Bursts: Walking lasts 8 to 28 seconds as the civet moves and pauses.", "Segoe UI", 22, False, C_DARK, space_before=8)
            add_bullet(tf, "2. 100% Night Vision Tracking: Handled glowing eyes and shadows without losing the animal.", "Segoe UI", 22, False, C_DARK, space_before=8)
            add_bullet(tf, "3. Zero Fake Plant Alarms: Completely ignored still potted plants—no false detections!", "Segoe UI", 22, False, C_DARK, space_before=8)
            add_bullet(tf, "4. Verified Bedtime: Confirmed sleeping in the straw tire nest, matching keeper notes.", "Segoe UI", 22, False, C_DARK, space_before=8)

    set_notes(s7, """We didn't just test this on one video—we tested it across 22 real video recordings from Chiang Mai Zoo.

The dataset includes 5 eating clips, 10 walking clips, and 7 resting clips across both daytime color and pitch-black infrared night video.
Our testing confirmed four key insights:
First, walking happens in short 8 to 28 second bursts.
Second, our tracking never loses the animal in the dark, even with glowing eyes and shadows.
Third, it completely ignores static potted plants.
And fourth, we verified that Hompom sleeps in the straw tire nest at the top of Camera 03, exactly matching the zookeeper's observations.""")

    # =========================================================================
    # SLIDE 8: DELIVERABLES & ROADMAP
    # =========================================================================
    s8 = prs.slides[7]
    for shape in s8.shapes:
        if shape.name == 'TextBox 4':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "OUTPUT & ROADMAP", "Segoe UI Bold", 16.5, True, C_GOLD)
        elif shape.name == 'TextBox 5':
            tf = shape.text_frame
            set_run(tf.paragraphs[0], "Delivered Today & Phase 2 Roadmap", "Segoe UI Bold", 37.5, True, C_TEAL)
        
        # Check Table 6: update row 3 to Tire Bed
        elif shape.name == 'Table 6' and shape.has_table:
            table = shape.table
            if len(table.rows) >= 4 and len(table.columns) >= 6:
                table.rows[3].cells[5].text = "Resting (In Tire Bed)"
        
        # Bottom Cards
        elif shape.name == 'TextBox 9':
            tf = shape.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            set_run(p0, "1. Automatic Daily Notes", "Segoe UI Bold", 24, True, C_TEAL)
            add_bullet(tf, "Creates digital records of every walk, meal, and nap with exact timestamps—replacing pen and paper.", "Segoe UI", 21, False, C_DARK, space_before=6)
        
        elif shape.name == 'TextBox 12':
            tf = shape.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            set_run(p0, "2. Proven on Real Videos", "Segoe UI Bold", 24, True, C_TEAL)
            add_bullet(tf, "Validated across 22 real clips under day and night lighting. Runs fast and smoothly on normal office PCs.", "Segoe UI", 21, False, C_DARK, space_before=6)
        
        elif shape.name == 'TextBox 15':
            tf = shape.text_frame
            tf.clear()
            p0 = tf.paragraphs[0]
            set_run(p0, "3. What Comes Next (Phase 2)", "Segoe UI Bold", 24, True, C_TEAL)
            add_bullet(tf, "Follow civets across all 4 rooms, spot bathroom visits, and give keepers a friendly tablet dashboard!", "Segoe UI", 21, False, C_DARK, space_before=6)

    set_notes(s8, """To wrap up: in Phase 1, we successfully built a smart assistant that watches zoo cameras and creates automated, reliable records of walking, eating, and sleeping.

Here you can see a sample of the digital behavior log our system generates automatically, with exact start and end times, camera rooms, and behavior states.

Looking ahead to Phase 2, we plan to follow the civet as it moves between all four rooms, detect bathroom visits and grooming, and give zookeepers a friendly tablet app that shows daily health summaries at a glance.

Thank you very much for listening. We would love to answer any questions!""")

    # =========================================================================
    # OPTIONAL BONUS SLIDES: Visual Proof of Tests (Slides 9-12)
    # Styled in the exact 20" x 11.25" Canva Theme!
    # =========================================================================
    locomotion_img = os.path.join(project_root, "pic", "tracking_results", "locomotion_tracking_result.png")
    eating_img = os.path.join(project_root, "pic", "tracking_results", "eating_tracking_result.png")
    resting_img = os.path.join(project_root, "pic", "tracking_results", "resting_tracking_result.png")
    flowchart_img = os.path.join(project_root, "pic", "flowcharts", "pipeline_flowchart_en.png")

    blank_layout = prs.slide_layouts[6]

    def add_result_slide(cat_title, main_title, img_path, card_title, bullets, notes_txt):
        slide = prs.slides.add_slide(blank_layout)
        
        # Header Accent Bar (matches Group 2 in 1.pptx)
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.19), Inches(0.59), Inches(17.63), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_GOLD
        bar.line.fill.background()
        
        # Category Text
        tb_cat = slide.shapes.add_textbox(Inches(1.30), Inches(0.80), Inches(17.41), Inches(0.40))
        tf = tb_cat.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        set_run(tf.paragraphs[0], cat_title, "Segoe UI Bold", 16.5, True, C_GOLD)
        
        # Title Text
        tb_t = slide.shapes.add_textbox(Inches(1.30), Inches(1.25), Inches(17.41), Inches(0.90))
        tf = tb_t.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        set_run(tf.paragraphs[0], main_title, "Segoe UI Bold", 37.5, True, C_TEAL)
        
        # Left: Infographic Picture
        if os.path.exists(img_path):
            slide.shapes.add_picture(img_path, Inches(1.30), Inches(2.50), width=Inches(12.2), height=Inches(7.7))
        
        # Right: Card Box
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(13.80), Inches(2.50), Inches(5.0), Inches(7.7))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_TEAL
        card.line.width = Pt(1.5)
        
        tb_card = slide.shapes.add_textbox(Inches(14.05), Inches(2.75), Inches(4.5), Inches(7.2))
        tf = tb_card.text_frame
        tf.word_wrap = True
        set_run(tf.paragraphs[0], card_title, "Segoe UI Bold", 26, True, C_TEAL)
        
        for b_title, b_desc in bullets:
            add_bullet(tf, b_title, "Segoe UI Bold", 22, True, C_GOLD, space_before=10)
            add_bullet(tf, b_desc, "Segoe UI", 20, False, C_DARK, space_before=2)
            
        set_notes(slide, notes_txt)

    # Slide 9: Visual Test 1 - Walking
    add_result_slide(
        "REAL-WORLD EVIDENCE: TEST 1",
        "Spotting When the Civet Walks (Camera 03 Night IR)",
        locomotion_img,
        "Walking Test Results",
        [
            ("What Happened?", "Civet walked across the floor in 3.2 seconds."),
            ("What Computer Saw", "Traced the full orange path from start to stop."),
            ("Speed Curve", "Speed jumped above 50 px while walking, and dropped to zero when stopped."),
            ("Key Finding", "Centroid vector cleanly isolates travel from stationary fidgeting.")
        ],
        """Here is our first test on real security video from Chiang Mai Zoo. This is Camera 03 at night.
In pictures 1, 2, and 3, you see the civet walking from left to right across the floor in about 3 seconds.
In picture 4, the computer drew the orange trail showing the exact walking path.
And in picture 5, the blue line shows the animal's speed. As it walks, the speed jumps up high, and when it stops at its destination, the speed drops right back to zero."""
    )

    # Slide 10: Visual Test 2 - Eating
    add_result_slide(
        "REAL-WORLD EVIDENCE: TEST 2",
        "Measuring Meal Times at the Food Bowl (Camera 02 Day)",
        eating_img,
        "Mealtime Test Results",
        [
            ("What Happened?", "Civet visited the food bowl and ate for 80 seconds."),
            ("Food Bowl Zone", "Marked in orange at the bottom center of Camera 02."),
            ("Head Position", "Green dots show head clustered right inside the food tray."),
            ("Key Finding", "Separates eating a real meal from simply walking past the bowl.")
        ],
        """Here is our second test, focusing on eating. This was recorded during the day on Camera 02.
In pictures 1, 2, and 3, the civet walks over to the food bowl and lowers its head to eat.
In picture 4, you can see the orange box where the food tray sits. The green dots show the computer tracking the civet's head right over the food!
In picture 5, the timer climbs up to 80 seconds. The computer measured an 80-second continuous meal."""
    )

    # Slide 11: Visual Test 3 - Sleeping in Tire Bed
    add_result_slide(
        "REAL-WORLD EVIDENCE: TEST 3",
        "Confirming Bedtime in the Tire Nest (Camera 03 Night IR)",
        resting_img,
        "Bedtime Test Results",
        [
            ("Bedtime Spot", "Straw-lined tire bed at the top of the room."),
            ("Shelter Entry", "Climbed in at 27.2s and curled into a ball in straw."),
            ("1-Minute Rule", "Stillness timer passed 60 seconds at the 86s mark."),
            ("Key Finding", "Officially confirmed as ASLEEP, matching zoo note: 'Curling up in tire'.")
        ],
        """Here is our third test: tracking sleep.
Thanks to the zookeepers' guidance, we know the civet loves to sleep in the tire filled with straw at the top of Camera 03.
In this video, the civet climbs into the tire at 27 seconds and curls up into a ball, exactly matching the zoo's official note: 'Curling up in tire'.
In picture 5, our stillness timer starts counting. Once the civet stays completely still for 60 seconds in a row, the computer officially logs: 'The animal is asleep.'"""
    )

    # Slide 12: Comparison - Why Simple Vision Won
    add_result_slide(
        "METHOD COMPARISON",
        "Why Simple Vision Won Over Complex Deep Learning",
        flowchart_img,
        "Why Simple Is Better",
        [
            ("Fancy Deep Learning (YOLO)", "Confused by night video. Missed the dark civet and called a potted plant a bird (90% conf)!"),
            ("Our Tailored Smart Vision", "Static cameras mean static walls. Ignores all plants and tracks the civet 100% reliably."),
            ("Runs on Normal PCs", "Runs over 10x faster on an ordinary zoo office laptop without expensive GPUs."),
            ("Explainable", "Every decision is based on clear coordinates, not mysterious black boxes.")
        ],
        """A key question was whether to use deep learning like YOLO or tailored vision.
When we tested YOLO on night IR video, it struggled in the dark, missed the civet, and even called a potted plant a bird!
In contrast, our tailored vision system takes advantage of the fact that zoo cameras never move. It ignores static plants, tracks the civet 100% reliably, and runs on an ordinary office laptop."""
    )

    prs.save(output_path)
    print(f"Successfully generated {output_path} with {len(prs.slides)} slides in 1.pptx theme!")

if __name__ == "__main__":
    create_22_presentation()
