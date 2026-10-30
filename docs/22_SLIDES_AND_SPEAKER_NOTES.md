# Presentation Deck: 22.pptx (Concise & Easy English Version)
**Theme & Layout**: Direct match with `presentations/1.pptx` (Canva 20.0" × 11.25" Widescreen Theme)  
**File Location**: `presentations/22.pptx`  
**Tone & Audience**: Non-technical, intuitive, conversational, human language. Easy to understand for any listener, professor, or zoo staff.

---

## 📋 Slide-by-Slide Overview & Speaker Notes

### Slide 1: Title Slide
* **Category Badge**: `SMART ZOO MONITORING | CHIANG MAI ZOO`
* **Main Title**: Automated Civet Behavior Monitoring System
* **Subtitle**: A 24/7 Smart Camera Assistant That Tracks Animal Habits Automatically

> 🎙️ **Speaker Script (0:45 min)**:  
> *"Hello everyone. Today, our team is excited to present the Automated Civet Behavior Monitoring System, created in partnership with Chiang Mai Zoo.  
> Imagine having a smart virtual assistant that watches security cameras day and night, quietly taking notes whenever the animal walks, eats, or sleeps. That is exactly what we built.  
> In this presentation, we will show you how simple, practical computer vision can solve a real-world zoo problem, without needing expensive supercomputers or confusing black-box AI."*

---

### Slide 2: The Real-World Problem
* **Category**: `THE REAL-WORLD PROBLEM`
* **Slide Title**: Watching Security Cameras by Hand Doesn't Work
* **Body Points**:
  * **1. Hours of Staring at Screens**: Zoo staff must manually scrub through hours of CCTV across 4 rooms, stealing time away from direct animal care.
  * **2. Animals Active in the Dark**: Civets are nocturnal. Most activity happens in pitch-black night under black-and-white infrared cameras.
  * **3. People Blink, Computers Don't**: Human observers easily get tired during long night shifts and miss quick meals or short walks.
  * **The Goal**: A 24/7 smart camera assistant that automatically creates clean, daily health logs of walking, eating, and sleeping.

> 🎙️ **Speaker Script (0:50 min)**:  
> *"Right now, zookeepers have to manually review hours of security footage, rewinding and fast-forwarding across four separate screens while taking notes on paper sheets with pens.  
> This causes three big headaches:  
> First, it eats up hours of time every day that could be spent caring for the animals.  
> Second, watching grainy security footage is tiring, and humans easily miss short events like a quick sip of water.  
> Third, civets are nocturnal. Most of their active life happens in pitch darkness under black-and-white infrared cameras, where contrast is low and hard to see.  
> Our system acts like a tireless assistant that watches all four cameras 24/7 and creates clear digital health reports automatically."*

---

### Slide 3: The Zoo Enclosure
* **Category**: `THE ZOO ENCLOSURE`
* **Slide Title**: Understanding the Civet's 4-Room Home
* **Body Points**:
  * **The Resident: 'Hompom'**: A solitary, nocturnal Large Spotted Civet living in 4 linearly connected rooms (Room 1 ⇄ 2 ⇄ 3 ⇄ 4).
  * **The Dining Room (Camera 02)**: Food and water bowls are placed permanently on the floor at the bottom center.
  * **The Bedroom (Camera 03)**: Features a climbing log and a straw-filled tire bed where Hompom loves to sleep.
  * **The Fixed-Camera Advantage**: Cameras never move! The background stays still. If something moves, it's guaranteed to be our civet.

> 🎙️ **Speaker Script (0:45 min)**:  
> *"Let's take a look inside the civet's enclosure.  
> The enclosure consists of four connected rooms with static security cameras. In our video dataset, two cameras are especially important:  
> Camera 02 looks at the 'dining room', where the food and water trays sit permanently on the floor.  
> Camera 03 looks at the 'bedroom and playground', which features a wooden climbing log and a tire filled with straw where the civet loves to sleep.  
> Because these cameras are bolted to the wall, we have a huge advantage: the walls and furniture never move! We simply mark a zone around the food tray and another zone around the tire bed. Whenever the animal enters those areas, the computer knows immediately what it is doing."*

---

### Slide 4: Target Behaviors (3 Cards)
* **Category**: `TARGET BEHAVIORS`
* **Slide Title**: The 3 Daily Habits We Track (85%+ of Daily Life)
* **Card 1: 1. Sleeping (Resting)**
  * • Curled up in straw tire bed
  * • Completely still for 1 full minute
  * • Distinguishes true sleep from a quick pause
* **Card 2: 2. Walking (Locomotion)**
  * • Walking or climbing across rooms
  * • Moving continuously for 3+ seconds
  * • Ignores ear twitches and tail wiggles
* **Card 3: 3. Eating / Drinking**
  * • Head lowered into food or water tray
  * • Stays at the bowl for 10+ seconds
  * • Separates a real meal from walking past

> 🎙️ **Speaker Script (0:50 min)**:  
> *"Chiang Mai Zoo has an official catalog of 8 animal behaviors. In Phase 1, we focused on the three most common ones that make up over 85% of the civet's day:  
> 1. Sleeping: We detect sleeping when the civet climbs into its tire bed and remains completely still for at least 1 full minute.  
> 2. Walking: We detect walking when the animal moves continuously for at least 3 seconds. If it just turns its head or twitches an ear, that is ignored.  
> 3. Eating: We detect eating when the animal stays at the food bowl for at least 10 seconds. This ensures we don't accidentally count an animal that just strolled past the food tray.  
> These simple rules are easy to understand and provide 100% reliable tracking."*

---

### Slide 5: System Pipeline (Complete 9-Step Data Flow Architecture)
* **Category**: `SYSTEM PIPELINE`
* **Slide Title**: Complete Data Flow Pipeline (9-Step End-to-End Architecture)
* **Visual**: Full-slide high-resolution diagram `civet_dataflow_pipeline.jpg` with 9 sequential cards, gold connectors, and Phase 1 Scope card.
* **Pipeline Breakdown**:
  1. **Camera Streams**: 4 CCTV cameras, one per room (1080p RTSP feeds)
  2. **Video Processing**: 2 FPS subsampling, saves 85% compute load
  3. **Animal Detection**: Adaptive MOG2 vision, ignores static background/plants
  4. **Animal Tracking**: Centroid extraction & bounding box tracking
  5. **Feature Extraction**: Position, speed, Food Tray & Tire ROIs
  6. **Behavior Classification**: 1-min debounce rule, Walk, Eat, Sleep
  7. **Behavior Events**: Timestamped continuous start & end event records
  8. **Data Storage**: Animal, Camera, Room, CSV & JSON structured logs
  9. **Visualization**: Daily activity budget, feeding & sleep charts for keepers
* **Phase 1 Scope**: Core behavior tracking (Walk, Eat, Sleep) running lightweight edge vision on standard zoo office PC—no expensive GPU or complex servers needed.

> 🎙️ **Speaker Script (1:00 min)**:  
> *"This diagram illustrates our complete end-to-end data processing pipeline in 9 straightforward steps:  
> 1. Camera Streams: We receive RTSP video streams from 4 static CCTV cameras covering each room of the civet enclosure.  
> 2. Video Processing: Instead of analyzing 15 or 30 frames per second, we subsample down to 2 FPS. This reduces computing load by 85% with zero loss in tracking accuracy.  
> 3. Animal Detection: Using adaptive MOG2 background subtraction, the system ignores fixed walls and swaying branches, isolating only moving foreground pixels.  
> 4. Animal Tracking: We calculate the animal's bounding box and track its centroid across consecutive frames.  
> 5. Feature Extraction: We extract position, movement speed, and check intersections with predefined Regions of Interest (Food Tray and Tire Bed).  
> 6. Behavior Classification: By applying temporal threshold rules (such as the 1-Minute Rule for resting and 10 seconds for eating), we classify behaviors into Walking, Eating, or Sleeping.  
> 7. Behavior Events: Discrete continuous events are generated with precise start and end timestamps.  
> 8. Data Storage: All events are structured and stored locally in CSV and JSON formats with metadata.  
> 9. Visualization & Reporting: Finally, the system automatically aggregates the data into daily activity budgets, feeding frequencies, and rest charts for the zookeepers.  
> As highlighted in the dark card, Phase 1 focuses strictly on core behaviors and runs reliably on a standard zoo office computer without expensive cloud servers or dedicated GPUs."*

---

### Slide 6: Smart Timing (Twice a Second & The 1-Minute Rule)
* **Category**: `SMART TIMING`
* **Slide Title**: Checking Twice a Second & The 1-Minute Rule
* **Card 1: 1. Why Check Twice a Second?**
  * • **Civets Walk Naturally**: Crossing takes 3–10s. Twice a second gives 6–20 snapshots—plenty to see every step!
  * • **85% Power Savings**: Cuts computer workload by 7.5x (from 900 to 120 frames/min).
  * • **Runs Cool**: A standard zoo laptop can watch all cameras without overheating or lagging.
  * • **Never Misses Meals**: Feeding lasts minutes; 2 frames/sec captures 100% of start and end times.
* **Card 2: 2. The 1-Minute Rule (No Silly Mistakes)**
  * • **A 5-Second Stop ≠ Sleep**: Animals pause during walks. We wait 60s before saying it's asleep.
  * • **Scratching an Ear ≠ Waking Up**: Small tail or ear twitches while resting don't ruin bedtime.
  * • **Walking Wakes It Up Instantly**: 3 seconds of continuous movement immediately marks it awake.
  * • **Clean Daily Reports**: Produces reliable health charts for veterinarians without flickering.

> 🎙️ **Speaker Script (0:45 min)**:  
> *"Two smart timing choices make our system work so reliably in real life:  
> First, why check twice a second? Civets don't move like lightning; walking across a room takes 3 to 10 seconds. Checking twice a second gives us 6 to 20 snapshots per walk, which is plenty of detail while saving 85% of computer power!  
> Second, the 1-Minute Rule. If an animal pauses for 5 seconds during a walk, it didn't fall asleep. And if a sleeping animal twitches its ear, it didn't wake up.  
> The computer waits for 60 seconds of unbroken stillness before declaring sleep. This prevents flickering and keeps the daily reports 100% clean."*

---

### Slide 7: Proven in Practice (Tested on 22 Real Videos)
* **Category**: `PROVEN IN PRACTICE`
* **Slide Title**: Tested on 22 Real Zoo CCTV Recordings
* **Table (5x4 Breakdown)**:
  * Eating: 5 clips | 254.4 s (~4.2 min) | 50.9 seconds average
  * Locomotion: 10 clips | 138.7 s (~2.3 min) | 13.9 s average (Short bursts!)
  * Resting: 7 clips | 658.7 s (~11.0 min) | 94.1 seconds average
  * Total: 22 clips | 1,051.8 s (~17.5 min)
* **Video Specs**: Full HD 1080p security cameras across all 4 rooms, tested on day color and infrared night.
* **Key Testing Insights**:
  1. Walks are Short Bursts (8 to 28s)
  2. 100% Night Vision Tracking (never lost in the dark)
  3. Zero Fake Plant Alarms (ignores static greenery)
  4. Verified Bedtime in the Straw Tire Nest

> 🎙️ **Speaker Script (0:45 min)**:  
> *"We didn't just test this on one video—we tested it across 22 real video recordings from Chiang Mai Zoo.  
> The dataset includes 5 eating clips, 10 walking clips, and 7 resting clips across both daytime color and pitch-black infrared night video.  
> Our testing confirmed four key insights: First, walking happens in short 8 to 28 second bursts. Second, our tracking never loses the animal in the dark. Third, it completely ignores static potted plants. And fourth, we verified that Hompom sleeps in the straw tire nest at the top of Camera 03, exactly matching the zookeeper's observations."*

---

### Slide 8: Deliverables & Roadmap
* **Category**: `OUTPUT & ROADMAP`
* **Slide Title**: Delivered Today & Phase 2 Roadmap
* **Digital Event Log Sample (Table 4x6)**:
  * 001 | 09:09:44 | 09:09:55 | Room 3 (Cam 03) | Active | Locomotion (Walking)
  * 002 | 09:23:26 | 09:24:46 | Room 2 (Cam 02) | Active | Eating (Food Tray)
  * 003 | 19:41:09 | 20:15:00 | Room 3 (Cam 03) | Inactive | Resting (In Tire Bed)
* **Card 1: 1. Automatic Daily Notes** — Digital records of every walk, meal, and nap with exact timestamps—replacing pen and paper.
* **Card 2: 2. Proven on Real Videos** — Validated across 22 real clips under day and night lighting. Runs fast and smoothly on normal office PCs.
* **Card 3: 3. What Comes Next (Phase 2)** — Follow civets across all 4 rooms, spot bathroom visits, and give keepers a friendly tablet dashboard!

> 🎙️ **Speaker Script (0:45 min)**:  
> *"To wrap up: in Phase 1, we successfully built a smart assistant that watches zoo cameras and creates automated, reliable records of walking, eating, and sleeping.  
> Here you can see a sample of the digital behavior log our system generates automatically, with exact start and end times, camera rooms, and behavior states.  
> Looking ahead to Phase 2, we plan to follow the civet as it moves between all four rooms, detect bathroom visits and grooming, and give zookeepers a friendly tablet app that shows daily health summaries at a glance.  
> Thank you very much for listening. We would love to answer any questions!"*

---

### Slides 9–12: Visual Proof from Real CCTV Footage
* **Slide 9**: Real Video Evidence 1 — Spotting When the Civet Walks (Camera 03 Night IR, 5-panel infographic).
* **Slide 10**: Real Video Evidence 2 — Measuring Meal Times at the Food Bowl (Camera 02 Day, 80s feeding bout).
* **Slide 11**: Real Video Evidence 3 — Confirming Bedtime in the Tire Nest (Camera 03 Night IR, 1-min rule crossing at 86s).
* **Slide 12**: Method Comparison — Why Simple Vision Won Over Complex Deep Learning (YOLO vs. Tailored Motion Vision).
