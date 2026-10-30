import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def create_presentation_script():
    doc = docx.Document()

    # Margins
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    HEX_TEAL = '1B4958'
    HEX_GOLD = 'D97706'
    HEX_DARK = '1E293B'
    HEX_BG_LIGHT = 'F8FAFC'

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), fill_hex)
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=180, right=180):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    # Document Header
    p_tag = doc.add_paragraph()
    p_tag.paragraph_format.space_before = Pt(0)
    p_tag.paragraph_format.space_after = Pt(2)
    r_tag = p_tag.add_run('CHIANG MAI ZOO × CMU | IMAGE PROCESSING PROJECT')
    r_tag.font.name = 'Segoe UI'
    r_tag.font.size = Pt(10)
    r_tag.font.bold = True
    r_tag.font.color.rgb = RGBColor(217, 119, 6)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run('Phase 1 Presentation Script: Automated Civet Behavior Monitoring')
    r_title.font.name = 'Segoe UI Semibold'
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(27, 73, 88)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run('10–15 Minutes Verbatim English Script • Structured & Divided for 3 Team Members')
    r_sub.font.name = 'Segoe UI'
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    # Speaker Allocation Summary Table
    table = doc.add_table(rows=4, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    headers = ['Speaker', 'Slides Covered', 'Core Focus Area', 'Est. Time']
    col_widths = [Inches(1.2), Inches(1.3), Inches(3.2), Inches(1.1)]

    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        set_cell_background(hdr_cells[i], HEX_TEAL)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = 'Segoe UI'
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    speaker_rows = [
        ('Speaker 1', 'Slides 1 – 6\n(6 slides)', 'Problem Background, Enclosure Conditions (4 rooms, 1 civet, 4 cams), Target Habits, Official Ethogram & Observation Distinction', '~4.0 mins'),
        ('Speaker 2', 'Slides 7 – 11\n(5 slides)', 'Observation Checklist, Real-World Zoo Challenges, 3-Step Baseline, Relational Data Model (No UI) & 9-Step Pipeline', '~4.0 mins'),
        ('Speaker 3', 'Slides 12 – 17\n(6 slides)', 'Validation on 22 Zoo Videos, Visual Evidence Demos (Walk/Eat/Sleep), Rule-Based vs Deep Learning & Phase 2 Outlook', '~4.5 mins')
    ]

    for row_idx, data in enumerate(speaker_rows, start=1):
        row_cells = table.rows[row_idx].cells
        bg = HEX_BG_LIGHT if row_idx % 2 == 1 else 'FFFFFF'
        for c_idx, text in enumerate(data):
            row_cells[c_idx].width = col_widths[c_idx]
            set_cell_background(row_cells[c_idx], bg)
            p = row_cells[c_idx].paragraphs[0]
            if c_idx in [0, 1, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = 'Segoe UI'
            r.font.size = Pt(9.5)
            if c_idx == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(27, 73, 88)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    def add_slide_script(slide_num, speaker_tag, title_text, duration_text, visual_cue, script_text, handover_text=None):
        p_hdr = doc.add_paragraph()
        p_hdr.paragraph_format.space_before = Pt(14)
        p_hdr.paragraph_format.space_after = Pt(2)
        p_hdr.paragraph_format.keep_with_next = True
        
        r_spk = p_hdr.add_run(f'[{speaker_tag}] ')
        r_spk.font.name = 'Segoe UI'
        r_spk.font.bold = True
        r_spk.font.size = Pt(11)
        r_spk.font.color.rgb = RGBColor(217, 119, 6)

        r_num = p_hdr.add_run(f'Slide {slide_num}: {title_text}')
        r_num.font.name = 'Segoe UI Semibold'
        r_num.font.bold = True
        r_num.font.size = Pt(12)
        r_num.font.color.rgb = RGBColor(27, 73, 88)

        r_dur = p_hdr.add_run(f'  ({duration_text})')
        r_dur.font.name = 'Segoe UI'
        r_dur.font.size = Pt(9.5)
        r_dur.font.color.rgb = RGBColor(100, 116, 139)

        p_cue = doc.add_paragraph()
        p_cue.paragraph_format.space_before = Pt(0)
        p_cue.paragraph_format.space_after = Pt(4)
        p_cue.paragraph_format.keep_with_next = True
        r_cue_lbl = p_cue.add_run('Visual / Slide Action: ')
        r_cue_lbl.font.name = 'Segoe UI'
        r_cue_lbl.font.bold = True
        r_cue_lbl.font.size = Pt(9.5)
        r_cue_lbl.font.color.rgb = RGBColor(71, 85, 105)
        r_cue = p_cue.add_run(visual_cue)
        r_cue.font.name = 'Segoe UI'
        r_cue.font.italic = True
        r_cue.font.size = Pt(9.5)
        r_cue.font.color.rgb = RGBColor(71, 85, 105)

        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.8)
        set_cell_background(cell, HEX_BG_LIGHT)
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        
        p_box = cell.paragraphs[0]
        p_box.paragraph_format.space_before = Pt(2)
        p_box.paragraph_format.space_after = Pt(2)
        r_ico = p_box.add_run('🎙️ Spoken Script:\n')
        r_ico.font.name = 'Segoe UI'
        r_ico.font.bold = True
        r_ico.font.size = Pt(10)
        r_ico.font.color.rgb = RGBColor(27, 73, 88)

        for para in script_text.strip().split('\n\n'):
            p_para = cell.add_paragraph()
            p_para.paragraph_format.space_before = Pt(3)
            p_para.paragraph_format.space_after = Pt(3)
            r_txt = p_para.add_run(para.strip())
            r_txt.font.name = 'Segoe UI'
            r_txt.font.size = Pt(10.5)
            r_txt.font.color.rgb = RGBColor(30, 41, 59)

        if handover_text:
            p_hand = doc.add_paragraph()
            p_hand.paragraph_format.space_before = Pt(6)
            p_hand.paragraph_format.space_after = Pt(10)
            r_h_lbl = p_hand.add_run('➡️ Handover Transition: ')
            r_h_lbl.font.name = 'Segoe UI'
            r_h_lbl.font.bold = True
            r_h_lbl.font.size = Pt(10)
            r_h_lbl.font.color.rgb = RGBColor(217, 119, 6)
            r_h_txt = p_hand.add_run(handover_text)
            r_h_txt.font.name = 'Segoe UI'
            r_h_txt.font.italic = True
            r_h_txt.font.bold = True
            r_h_txt.font.size = Pt(10)
            r_h_txt.font.color.rgb = RGBColor(27, 73, 88)
        else:
            p_space = doc.add_paragraph()
            p_space.paragraph_format.space_before = Pt(2)
            p_space.paragraph_format.space_after = Pt(4)

    # =========================================================================
    # PART 1: SPEAKER 1 (Slides 1 to 6)
    # =========================================================================
    p_sec1 = doc.add_paragraph()
    p_sec1.paragraph_format.space_before = Pt(18)
    p_sec1.paragraph_format.space_after = Pt(4)
    r_sec1 = p_sec1.add_run('PART 1 — SPEAKER 1: BACKGROUND, ENCLOSURE & ETHOGRAM')
    r_sec1.font.name = 'Segoe UI Semibold'
    r_sec1.font.bold = True
    r_sec1.font.size = Pt(14)
    r_sec1.font.color.rgb = RGBColor(27, 73, 88)

    # Slide 1
    add_slide_script(
        1, "Speaker 1", "Title & Introduction", "0:40 min",
        "Display title slide. Smile and make eye contact with the professor and audience.",
        """Good afternoon, Professor and classmates. Today, our team is excited to present Phase 1 of our Image Processing Project: the Automated Civet Behavior Monitoring System, developed in collaboration with Chiang Mai Zoo.

Our project tackles a real-world operational challenge: how to automatically track, classify, and log the daily activities of a Large Spotted Civet using Computer Vision, without relying on expensive hardware or mystery black-box AI.

In this Phase 1 presentation, we will walk you through the physical conditions of the zoo enclosure, our behavioral ethogram, the observation challenges, our rule-based vision methodology, and our complete end-to-end data processing pipeline."""
    )

    # Slide 2
    add_slide_script(
        2, "Speaker 1", "The Real-World Problem", "0:45 min",
        "Point to the 3 numbered problem cards on the slide as you speak.",
        """Let's begin with the problem zookeepers face every day.

Currently, staff must manually review hours of security camera footage across four separate monitors, fast-forwarding and rewinding while taking notes with pen and paper. This creates three critical bottlenecks:

First, it consumes hours of valuable staff time that should be spent on direct animal care.
Second, civets are nocturnal. Most of their active life occurs in pitch darkness under black-and-white infrared cameras, where low contrast makes detection exhausting for human eyes.
Third, people get tired during long night shifts and inevitably miss short events, like a quick sip of water or a 10-second stroll.

Our goal for Phase 1 is to build a 24/7 smart camera assistant that automatically generates clean digital health records of walking, eating, and sleeping."""
    )

    # Slide 3
    add_slide_script(
        3, "Speaker 1", "The Zoo Enclosure & Conditions", "0:45 min",
        "Emphasize the 3 key conditions required in the project rubric: 4 rooms, 1 animal, 4 cameras.",
        """To solve this, we must understand the exact physical conditions at Chiang Mai Zoo.

As outlined in our project requirements, our setup consists of:
Four linearly connected rooms—Room 1 connecting to 2, 3, and 4.
One solitary resident: 'Hompom', an adult Large Spotted Civet.
And four fixed CCTV cameras, one per room, recording at 1080p resolution.

Two cameras capture the vast majority of activities: Camera 02 monitors the 'dining room', where food and water bowls sit permanently on the floor. Camera 03 monitors the 'bedroom', containing a climbing log and a straw-filled tire bed where Hompom loves to sleep.

Because these cameras are bolted to the walls, we gain a massive Computer Vision advantage: the background is completely static! If anything moves, it is almost certainly our civet."""
    )

    # Slide 4
    add_slide_script(
        4, "Speaker 1", "Target Behaviors", "0:45 min",
        "Point to the 3 behavior cards: Sleeping, Walking, Eating.",
        """Next, let's look at the target behaviors. In Phase 1, we focused on the three daily habits that make up over 85% of Hompom's life:

1. Sleeping or Resting: The civet enters its straw tire bed and remains motionless. We enforce a 1-Minute Rule: it must stay still for 60 consecutive seconds to distinguish deep sleep from a momentary pause.
2. Walking or Locomotion: Moving across rooms. To avoid false triggers from ear twitches or tail wiggles, the animal must move continuously for at least 3 seconds.
3. Eating and Drinking: Lowering its head into the permanent food bowl for at least 10 seconds, cleanly separating a genuine meal from an animal simply walking past the bowl.

These deterministic rules are easy to explain, mathematically transparent, and 100% auditable by veterinarians."""
    )

    # Slide 5
    add_slide_script(
        5, "Speaker 1", "Official Ethogram vs Dataset Coverage", "0:45 min",
        "Point to the table showing Active/Inactive groups and the 'Phase 1 handling' column.",
        """Here, we align Chiang Mai Zoo's official 8-behavior ethogram with our real-world dataset.

The zoo categorizes behaviors into two macro-states: Active and Inactive.
In our video recordings, three core behaviors are observable: Resting (Inactive), Walking (Active), and Eating/Drinking (Active).

What about the remaining official behaviors—such as urination, defecation, and grooming? Because they do not appear in the current footage, our system explicitly logs them as 'Unknown' rather than forcing a wrong guess. Furthermore, 'pacing together' is physically impossible in Phase 1 because Hompom lives alone in this enclosure.

Treating 'Unknown' as a legitimate label prevents false positives and ensures data integrity."""
    )

    # Slide 6
    add_slide_script(
        6, "Speaker 1", "Behavior vs Observation Conditions", "0:40 min",
        "Point to the left box (Animal behavior) and right box (Observation conditions).",
        """A core objective of Phase 1 is strictly distinguishing Animal Behavior from Observation Conditions.

Animal Behavior describes what the civet is doing: walking, climbing, resting, or eating.
Observation Conditions describe how the scene appears on camera: daytime color versus night infrared, low illumination, glowing reflective eyes, shadows, and occlusions from fences or plants.

Our fundamental design rule is: Observation conditions describe the video feed, not the animal. By logging them in separate data fields, if the camera view is obstructed or too dark, the system flags the environmental condition and records behavior as 'Unknown', rather than corrupting health logs with inaccurate behavior classifications.""",
        handover_text="Now, I will hand over to Speaker 2, who will present our observation challenges, baseline methodology, data model, and our complete 9-step processing pipeline."
    )

    # =========================================================================
    # PART 2: SPEAKER 2 (Slides 7 to 11)
    # =========================================================================
    p_sec2 = doc.add_paragraph()
    p_sec2.paragraph_format.space_before = Pt(18)
    p_sec2.paragraph_format.space_after = Pt(4)
    r_sec2 = p_sec2.add_run('PART 2 — SPEAKER 2: CHALLENGES, METHODOLOGY & PIPELINE')
    r_sec2.font.name = 'Segoe UI Semibold'
    r_sec2.font.bold = True
    r_sec2.font.size = Pt(14)
    r_sec2.font.color.rgb = RGBColor(27, 73, 88)

    # Slide 7
    add_slide_script(
        7, "Speaker 2", "Challenges and Observation Checklist", "0:45 min",
        "Point to the 4 challenge cards at the top, then reference the structured table below.",
        """Thank you, Speaker 1. Now, let's examine the real-world image-processing challenges in the zoo and our structured observation checklist.

We identified four primary challenges:
1. Night Infrared Footage: Lacks RGB color channels and produces glowing reflective eyes. We engineered our vision algorithms to rely on luminance contrast and spatial shape rather than color.
2. Occlusions by Plants and Wire Fences: When the animal briefly slips behind a post, our tracker bridges the gap across short frames.
3. Cross-Room Transit: When the civet leaves the camera view, tracking identity is handed over to the adjacent room's camera.
4. Standing Still vs Resting: Both have zero velocity. We separate them by observing duration: resting requires sustained stillness over time.

Below is our Phase 1 Observation Checklist schema. Each observation records structured metadata: timestamp, camera room, visibility, behavior state, lighting modality, and occlusion flags."""
    )

    # Slide 8
    add_slide_script(
        8, "Speaker 2", "How It Works: A Simple 3-Step Baseline", "0:45 min",
        "Point sequentially to Stage 1, Stage 2, and Stage 3 cards.",
        """To detect these behaviors reliably, we designed a transparent 3-Stage Baseline methodology:

Stage 1 is Motion Detection: Instead of processing video at 15 frames per second, we subsample down to 2 FPS. Using adaptive MOG2 background subtraction, the computer models the empty enclosure and isolates moving foreground pixels, ignoring static walls and potted plants in both daytime color and night infrared.

Stage 2 is Location Tracking: We extract the civet's centroid coordinates and bounding box. By tracking position and velocity over time, the system determines if the animal is traveling or positioned directly over the Food Tray ROI.

Stage 3 is Common-Sense Decision: We apply our debounce logic—such as the 60-second stillness rule for sleeping. This produces clean health logs and runs effortlessly on a standard zoo office PC without expensive GPUs."""
    )

    # Slide 9
    add_slide_script(
        9, "Speaker 2", "Data Model Concept (No UI / App Required)", "0:45 min",
        "Point to the ER relationship diagram (Room -> Camera -> Animal -> BehaviorEvent).",
        """Following the Phase 1 instructions, our assignment explicitly requires designing an AI and Data Model, with no need to build a UI or application.

Here is our relational Data Model:
We define Room, Camera, and Animal entities connected via one-to-many relationships. A room contains cameras, and cameras observe the animal.

The core operational entity is 'BehaviorEvent'. Each record stores:
- Event ID, Animal ID, and Camera ID
- Macro State: Active or Inactive
- Specific Behavior: Walking, Resting, Eating, or Unknown
- Start and End Timestamps, Duration in seconds, and Confidence Score.

This structured schema allows veterinarians and researchers to query daily behavioral budgets directly using standard SQL or CSV tools without needing a custom front-end app."""
    )

    # Slide 10
    add_slide_script(
        10, "Speaker 2", "Complete 9-Step Data Flow Pipeline", "0:50 min",
        "Trace the 9 steps across the diagram: Top row (1-5), bottom row (6-9), and point to the Phase 1 Scope box.",
        """This diagram illustrates our complete end-to-end Data Flow Pipeline in 9 modular steps:

1. Camera Streams: Captures 1080p RTSP video feeds from all 4 rooms.
2. Video Processing: 2 FPS temporal subsampling, cutting processing overhead by 85%.
3. Animal Detection: Adaptive MOG2 background subtraction isolates foreground civet pixels.
4. Animal Tracking: Centroid extraction and bounding box trajectory tracking.
5. Feature Extraction: Calculates speed and checks intersections with Food Tray and Tire ROIs.
6. Behavior Classification: Debounce temporal thresholding for Walk, Eat, and Sleep.
7. Behavior Events: Generates discrete events with verified start and end timestamps.
8. Data Storage: Relational CSV and JSON logs populated directly into our data model.
9. Visualization: Aggregates daily activity budgets, feeding frequencies, and sleep charts.

As emphasized in the dark card, Phase 1 focuses strictly on core behaviors and runs reliably on standard zoo office hardware."""
    )

    # Slide 11
    add_slide_script(
        11, "Speaker 2", "Smart Timing: 2 FPS & The 1-Minute Rule", "0:45 min",
        "Point to Card 1 (2 FPS) and Card 2 (1-Minute Rule).",
        """Two smart timing decisions ensure our system runs reliably in real zoo deployments:

First, why check twice a second? Civets move at a natural pace; crossing a room takes 3 to 10 seconds. At 2 FPS, we obtain 6 to 20 snapshots per walk—plenty of fidelity to track every movement, while saving 85% of computing power (dropping from 900 to 120 frames per minute). It runs cool and never lags.

Second, the 1-Minute Rule prevents silly classification mistakes. If a civet pauses for 5 seconds during a walk, it hasn't fallen asleep. And if a sleeping civet twitches an ear or moves its tail, it hasn't woken up!
The system requires 60 seconds of continuous stillness before declaring sleep, eliminating sensor flicker.""",
        handover_text="Now, I’ll hand over to Speaker 3, who will present our real-world test results on 22 zoo CCTV clips, visual evidence demonstrations, and our Phase 2 roadmap."
    )

    # =========================================================================
    # PART 3: SPEAKER 3 (Slides 12 to 17)
    # =========================================================================
    p_sec3 = doc.add_paragraph()
    p_sec3.paragraph_format.space_before = Pt(18)
    p_sec3.paragraph_format.space_after = Pt(4)
    r_sec3 = p_sec3.add_run('PART 3 — SPEAKER 3: TESTING, EVIDENCE, METHOD COMPARISON & ROADMAP')
    r_sec3.font.name = 'Segoe UI Semibold'
    r_sec3.font.bold = True
    r_sec3.font.size = Pt(14)
    r_sec3.font.color.rgb = RGBColor(27, 73, 88)

    # Slide 12
    add_slide_script(
        12, "Speaker 3", "Proven in Practice: Tested on 22 Zoo Recordings", "0:45 min",
        "Point to the breakdown table (Eating: 5 clips, Locomotion: 10 clips, Resting: 7 clips).",
        """Thank you, Speaker 2. We didn't just test our pipeline on sample frames—we evaluated it rigorously across 22 real CCTV video recordings provided by Chiang Mai Zoo, totaling over 17.5 minutes of footage.

As shown in the table, our dataset covers:
- 5 Eating clips averaging 50.9 seconds
- 10 Locomotion clips averaging 13.9 seconds (demonstrating short movement bursts)
- 7 Resting clips averaging 94.1 seconds.

Our real-world testing confirmed four key insights:
First, walks are short, intermittent bursts.
Second, tracking never lost the animal in pitch darkness, handling glowing eyes and shadows.
Third, zero false positives from static potted plants.
And fourth, we verified that Hompom rests in the straw tire nest, perfectly matching keeper notes."""
    )

    # Slide 13
    add_slide_script(
        13, "Speaker 3", "Real-World Evidence: Test 1 (Walking)", "0:45 min",
        "Point to the orange trajectory trail and the speed curve in the test image.",
        """Here is our first visual evidence test: Locomotion on Camera 03 during night infrared.

In this recording, the civet walked across the enclosure floor in 3.2 seconds.
In the computer tracking view, you can see the continuous orange trail tracing Hompom's exact path from start to stop.

Looking at the speed curve below, the calculated velocity spikes sharply above 50 pixels while traveling and drops cleanly back to zero once the animal halts.
This confirms that our centroid motion vector effectively isolates travel from stationary fidgeting."""
    )

    # Slide 14
    add_slide_script(
        14, "Speaker 3", "Real-World Evidence: Test 2 (Eating)", "0:45 min",
        "Point to the orange Food Bowl ROI and the green head tracking points.",
        """Our second visual test evaluates Feeding on Camera 02 during daytime color video.

In this clip, Hompom visits the food bowl and eats continuously for 80 seconds.
The orange bounding box marks our calibrated Food Tray ROI at the bottom center of the room.
The green tracking clusters show the animal's head positioned directly inside the bowl.

By requiring the civet to remain inside the ROI for at least 10 seconds, our system accurately logs an 80-second meal event while ignoring animals that simply stroll past the food bowl."""
    )

    # Slide 15
    add_slide_script(
        15, "Speaker 3", "Real-World Evidence: Test 3 (Resting)", "0:45 min",
        "Point to the tire bed location and the stillness timer graph.",
        """Our third test validates Bedtime Resting on Camera 03 at night.

Thanks to keeper guidance, we know Hompom sleeps inside the straw-lined tire at the top of the room.
In this video, the civet enters the tire bed at 27.2 seconds and curls into a ball, matching the official zoo log: 'Curling up in tire'.

Our stillness counter tracks continuous immobility. Once the timer crosses 60 seconds at the 86-second mark, the system officially logs the behavior state as 'Resting'. This confirms 100% agreement with ground-truth keeper observations."""
    )

    # Slide 16
    add_slide_script(
        16, "Speaker 3", "Method Comparison: Baseline vs Deep Learning", "0:45 min",
        "Point to the comparison bullets between Pretrained Deep Learning (YOLO) and Rule-Based Baseline.",
        """A vital question in computer vision is: Why start with a tailored rule-based baseline instead of deep learning like YOLO?

When we tested off-the-shelf YOLOv8 on night infrared footage, it struggled significantly: it failed to detect the dark civet under infrared contrast, and it even hallucinated, classifying a potted plant as a bird with 90% confidence!

In contrast, our rule-based vision pipeline exploits the fact that zoo cameras are completely stationary. It inherently ignores static vegetation, successfully tracked the civet across all 22 test recordings, and runs smoothly on an ordinary office PC without expensive GPUs.

This establishes an auditable, reliable ground-truth baseline against which we can train and evaluate deep models in Phase 2."""
    )

    # Slide 17
    add_slide_script(
        17, "Speaker 3", "Phase 1 Deliverables & Phase 2 Outlook", "0:50 min",
        "Point to the deliverables cards and conclude with Q&A invitation.",
        """To summarize our Phase 1 submission:
We have delivered a fully validated, vision-based behavior monitoring pipeline tailored to Chiang Mai Zoo's 4-room civet enclosure.

What we delivered today in Phase 1:
1. An official ethogram mapping, observation checklist, and relational structured data model.
2. A lightweight 2 FPS rule-based baseline verified across 22 real CCTV videos under day and night conditions.
3. Automated digital generation of start/end timestamps and behavior logs without needing complex UI or GPU hardware.

Looking ahead to Phase 2 at the end of October, as outlined in the course syllabus, we will expand with Deep Learning:
- Task 1: CNN-based Image Classification for fine-grained postures.
- Task 2: Custom-trained YOLO Detection for robust multi-room bounding boxes.
- Task 3: Keypoint Pose Estimation for detailed body angle and movement speed analysis.

Thank you very much for your time and attention. We would now be glad to answer any questions!"""
    )

    # =========================================================================
    # APPENDIX: Q&A CHEAT SHEET
    # =========================================================================
    doc.add_page_break()
    p_qa = doc.add_paragraph()
    p_qa.paragraph_format.space_before = Pt(12)
    p_qa.paragraph_format.space_after = Pt(4)
    r_qa = p_qa.add_run('APPENDIX: QUICK Q&A CHEAT SHEET FOR THE TEAM')
    r_qa.font.name = 'Segoe UI Semibold'
    r_qa.font.bold = True
    r_qa.font.size = Pt(14)
    r_qa.font.color.rgb = RGBColor(27, 73, 88)

    qa_list = [
        ("Q1: Why didn't you use Deep Learning (YOLO) for Phase 1?",
         "Speaker 3 or Any",
         "Answer: In Phase 1, our primary objective was establishing an auditable baseline, observation checklist, and structured data model. Off-the-shelf YOLO failed on night infrared footage and hallucinated on plants. Our rule-based baseline leveraged stationary cameras to achieve 100% tracking reliability on real zoo videos. In Phase 2, we will use our labeled Phase 1 dataset to fine-tune YOLO, CNN, and Pose Keypoint models."),
        
        ("Q2: Why do you subsample video to 2 FPS instead of 15 or 30 FPS?",
         "Speaker 2",
         "Answer: Civet behavior is relatively slow—crossing a room takes 3 to 10 seconds, and eating lasts several minutes. At 2 FPS, we still get 6 to 20 snapshots per walk, which captures start and end times within 0.5 seconds, while saving 85% of computational load so it runs cool on normal zoo PCs."),
        
        ("Q3: Why is there no user interface or mobile app in Phase 1?",
         "Speaker 2",
         "Answer: The Phase 1 project guidelines explicitly specified: '**Design only AI/Data model, no need to design UI/App'. We focused our engineering strictly on the vision pipeline, relational ER data model (Room, Camera, Animal, BehaviorEvent), and structured CSV/JSON data logging."),

        ("Q4: How do you handle behaviors not in the dataset, like grooming or urination?",
         "Speaker 1",
         "Answer: Our system logs unobserved or unsupported behaviors as 'Unknown' rather than forcing an inaccurate classification. This preserves scientific data integrity until more labeled recordings are collected.")
    ]

    for q, who, a in qa_list:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8)
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(f'{q} ')
        r_q.font.name = 'Segoe UI'
        r_q.font.bold = True
        r_q.font.size = Pt(11)
        r_q.font.color.rgb = RGBColor(217, 119, 6)
        r_who = p_q.add_run(f'({who})')
        r_who.font.name = 'Segoe UI'
        r_who.font.italic = True
        r_who.font.size = Pt(9.5)
        r_who.font.color.rgb = RGBColor(100, 116, 139)

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(0)
        p_a.paragraph_format.space_after = Pt(6)
        r_a = p_a.add_run(a)
        r_a.font.name = 'Segoe UI'
        r_a.font.size = Pt(10)
        r_a.font.color.rgb = RGBColor(30, 41, 59)

    # Save documents
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "finish")
    os.makedirs(out_dir, exist_ok=True)
    out1 = os.path.join(out_dir, "Phase_1_Presentation_Script_3_People.docx")
    out2 = os.path.join(out_dir, "Image_Processing_Presentation_Script_3_Speakers.docx")

    doc.save(out1)
    doc.save(out2)
    print(f"Document saved successfully to:\n{out1}\n{out2}")

if __name__ == '__main__':
    create_presentation_script()
