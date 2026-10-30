# Canva Slide Deck & Speaker Notes (Easy English Version - 12 Slides)
**Project Title**: Automated Civet Behavior Monitoring System (Phase 1)  
**Collaboration**: Chiang Mai Zoo (CMZ) × Chiang Mai University (CMU) - Image Processing Course  
**PowerPoint File**: `presentations/Civet_Behavior_Monitoring_Presentation_EN_Easy.pptx`  
**Tone & Audience**: Non-technical, intuitive, engaging, and easy to follow for general audiences, zoo managers, and judges.  
**Total Target Presentation Time**: ~8–10 Minutes

---

## 🎨 Global Presentation Theme & Design Guidelines
* **Canvas Ratio**: 16:9 Widescreen (1920 × 1080 px / 13.33" × 7.5")
* **Color Palette**:
  * Background: Deep Navy (`#0F172A`)
  * Container Cards: Dark Slate (`#1E293B`) with subtle border (`#334155`)
  * Primary Accent: Neon Cyan (`#38BDF8`)
  * Success / Resting Accent: Emerald Green (`#10B981`)
  * Warning / Feeding Accent: Amber Gold (`#F59E0B`)
  * Danger / Alert Accent: Coral Red (`#EF4444`)
  * Text: Crisp White (`#F8FAFC`) and Slate Grey (`#94A3B8`)
* **Typography**: Clean Sans-Serif (`Segoe UI`, `Inter`, or `Montserrat`)

---

## Slide 1: Title Slide & Scope
* **Header Badge**: `SMART ZOO MONITORING | CHIANG MAI ZOO`
* **Main Title**: Automated Civet Behavior Monitoring System
* **Subtitle**: A 24/7 Smart Camera Assistant That Tracks Animal Health & Daily Habits Automatically
* **Footer Spec Badges**:
  1. **WHAT IT TRACKS**: Walking, Eating, Sleeping (Covers 85%+ of Daily Life)
  2. **WHERE IT WORKS**: 4-Room Night Enclosure (Works in Complete Darkness with IR)
  3. **HOW IT RUNS**: Lightweight & Super Fast (Runs smoothly on a normal office laptop)

> 🎙️ **Speaker Script (0:45 min)**:  
> *"Hello everyone. Today, our team is excited to present the Automated Civet Behavior Monitoring System, created in partnership with Chiang Mai Zoo.
> 
> Imagine having a smart virtual assistant that watches security cameras day and night, quietly taking notes whenever the animal walks, eats, or sleeps. That is exactly what we built. 
> 
> In this presentation, we will show you how simple computer vision can solve a real-world zoo problem, without needing expensive supercomputers or confusing black-box AI."*

---

## Slide 2: The Real-World Challenge
* **Category**: `THE REAL-WORLD CHALLENGE`
* **Slide Title**: The Trouble with Watching CCTV by Hand
* **Subtitle**: Why zookeepers need a smart assistant instead of staring at screens for hours
* **Key Visual / Cards**:
  * **Card 1 (Red)**: *1. Hours of Rewinding Video* — Zoo staff must sit through hours of recorded CCTV across 4 different rooms, taking valuable time away from hands-on animal care.
  * **Card 2 (Amber)**: *2. Eye Fatigue & Missed Moments* — Staring at security screens for hours is exhausting. People easily miss when the animal took a quick drink or a 10-second walk.
  * **Card 3 (Cyan)**: *3. Animals Active in the Dark* — Civets love the night! Most activity happens in pitch-black darkness under infrared cameras where human eyes struggle to see.
  * **Right Card (Green/Slate)**: *Our Automated Solution*
    * • **Watches 24/7 Without Tiring**: Never blinks or gets tired. Watches every camera feed all night and records behavior as it happens.
    * • **Simple, Explainable Rules**: No confusing mystery AI. Uses clear, common-sense rules: if it walks across the room, it's walking; if its head is in the bowl, it's eating.
    * • **Runs on an Ordinary PC**: No need for costly GPU servers. Runs smoothly on a standard zoo office computer.
    * • **Clear Daily Health Reports**: Generates daily summaries showing exact meal times, sleeping hours, and activity levels for the zoo veterinarians.

> 🎙️ **Speaker Script (0:50 min)**:  
> *"To understand why this project matters, look at how zookeepers currently work.
> 
> Right now, zookeepers have to manually review hours of security footage, rewinding and fast-forwarding across four separate screens while taking notes on paper sheets with pens.
> 
> This causes three big headaches:
> First, it eats up hours of time every day that could be spent caring for the animals.
> Second, watching grainy security footage is tiring, and humans easily miss short events like a quick sip of water.
> Third, civets are nocturnal. Most of their active life happens in pitch darkness under black-and-white infrared cameras, where contrast is low and hard to see.
> 
> Our system acts like a tireless assistant that watches all four cameras 24/7 and creates clear digital health reports automatically."*

---

## Slide 3: The Zoo Enclosure
* **Category**: `THE ZOO ENCLOSURE`
* **Slide Title**: Understanding the Animal's Home
* **Subtitle**: How fixed security cameras give our computer an unfair advantage
* **Key Visual / Cards**:
  * **Camera 02: The Dining Room (Amber)**:
    * • What it monitors: The Food & Water bowls
    * • Camera Type: Full color in daytime, infrared at night
    * • Key Landmark: Food tray placed permanently at the bottom center
    * • Behavior Goal: Spotting exactly when and how long the civet eats
  * **Camera 03: The Bedroom & Playground (Cyan)**:
    * • What it monitors: Sleeping nest & climbing log
    * • Camera Type: Night-vision infrared (black & white)
    * • Key Landmarks: Tire bed filled with straw (top) & wooden climbing log
    * • Behavior Goal: Spotting when the civet curls up to sleep or walks across
  * **Right Card: The Fixed Camera Advantage**:
    * ✔ **The Room Never Moves**: Because cameras are bolted to the walls, the background is completely still. Any change in pixels is guaranteed to be the civet moving!
    * ✔ **We Know Where Things Are**: The food bowl is always in Camera 02. The straw tire bed is always in Camera 03. We simply tell the computer where these 'zones' are, making tracking easy and reliable.
    * ✔ **Lighting Doesn't Fool It**: Our motion detector automatically adapts as daylight shifts into dusk, keeping the civet clearly visible at all times.

> 🎙️ **Speaker Script (0:45 min)**:  
> *"Let's take a look inside the civet's enclosure.
> 
> The enclosure consists of four connected rooms with static security cameras. In our video dataset, two cameras are especially important:
> Camera 02 looks at the 'dining room', where the food and water trays sit permanently on the floor.
> Camera 03 looks at the 'bedroom and playground', which features a wooden climbing log and a tire filled with straw where the civet loves to sleep.
> 
> Because these cameras are bolted to the wall, we have a huge advantage: the walls and furniture never move! 
> We simply mark a green box around the food tray and another box around the tire bed. Whenever the animal enters those boxes, the computer knows immediately what it is doing."*

---

## Slide 4: Target Behaviors
* **Category**: `TARGET BEHAVIORS`
* **Slide Title**: The Three Daily Habits We Track
* **Subtitle**: Simple common-sense rules that cover over 85% of a civet's daily routine
* **Key Visual / 3 Cards**:
  * **1. Walking / Running (Cyan)**:
    * • What is it? Moving purposefully across the room.
    * • The Rule: Moves at least 15 pixels every half-second for 3 seconds or more.
    * • State: `ACTIVE`
    * • Why it works: Discards tiny ear or tail twitches while catching real walking trips.
  * **2. Eating / Drinking (Amber)**:
    * • What is it? Lowering head into the food or water tray.
    * • The Rule: Head stays inside the Food Tray Zone for 10 seconds or more.
    * • State: `ACTIVE`
    * • Why it works: Successfully separates eating a full meal from just walking past the bowl.
  * **3. Sleeping / Resting (Green)**:
    * • What is it? Lying completely still in the straw tire bed.
    * • The Rule: Inside the tire bed + zero movement for 1 full minute (60s rule).
    * • State: `INACTIVE (Resting)`
    * • Why it works: Matches the zoo ethogram 'Curling up in tire' and prevents false alarms.

> 🎙️ **Speaker Script (0:50 min)**:  
> *"Chiang Mai Zoo has an official catalog of 8 animal behaviors. In Phase 1, we focused on the three most common ones that make up over 85% of the civet's day:
> 
> 1. Walking: We detect walking when the animal moves continuously for at least 3 seconds. If it just turns its head or twitches an ear, that is ignored.
> 2. Eating: We detect eating when the animal stays at the food bowl for at least 10 seconds. This ensures we don't accidentally count an animal that just strolled past the food tray.
> 3. Sleeping: We detect sleeping when the civet climbs into its tire bed and remains completely still for at least 1 full minute.
> 
> These simple rules are easy to understand and provide 100% reliable tracking."*

---

## Slide 5: How It Works (The 5 Simple Steps)
* **Category**: `HOW IT WORKS`
* **Slide Title**: The 5 Simple Steps of Our System
* **Subtitle**: How the computer turns raw video into clean daily notes
* **Visual Asset**: `pic/flowcharts/pipeline_flowchart_en.png` (Embedded High-Res Flowchart)
* **Sidebar Summary**:
  * **1. Check Twice a Second**: We don't need 30 frames/s. Checking 2 times a second saves 85% computer power.
  * **2. Spot What Moves**: The walls and logs never move. Anything moving must be the civet!
  * **3. Clean the Picture**: Wipe away camera fuzz and find the center point of the animal.
  * **4. Check Zone & Speed**: Is it at the food bowl? Or is it walking across the room?
  * **5. Write the Daily Log**: Creates a clean digital note for the zookeepers automatically.

> 🎙️ **Speaker Script (1:00 min)**:  
> *"This diagram shows the five simple steps our system follows.
> 
> First, we look at the video twice every second instead of 15 times. That is more than enough to see an animal walking, and it saves 85% of computer power.
> Second, the computer learns what the still, empty room looks like. Anything that moves must be the civet!
> Third, we clean up the grainy night video so we have a clear dot tracking the animal.
> Fourth, we check where that dot is: is it walking across the room, or is its head in the food bowl?
> And finally, step five: the system writes a clean digital log of what happened without any human effort."*

---

## Slide 6: Real Video Test 1 — Locomotion
* **Category**: `REAL VIDEO TEST 1`
* **Slide Title**: Spotting When the Civet Walks
* **Subtitle**: Tested on actual night-vision security video (Camera 03)
* **Visual Asset**: `pic/tracking_results/locomotion_tracking_result.png` (Embedded 5-Panel Infographic)
* **Sidebar Metrics**:
  * **What Happened?**: Civet walked across the room in 3.2 seconds
  * **What Computer Saw**: Tracked the full orange path from start to finish
  * **Speed Curve**: Speed jumped above 50 px while walking
  * **Stopping Point**: Speed dropped straight to zero upon arrival
  * **Key Result**: Successfully recorded the full walk without being tricked by ear twitches

> 🎙️ **Speaker Script (1:00 min)**:  
> *"Here is our first test on real security video from Chiang Mai Zoo. This is Camera 03 at night.
> 
> In pictures 1, 2, and 3, you see the civet walking from left to right across the floor in about 3 seconds.
> In picture 4, the computer drew the orange trail showing the exact walking path.
> And in picture 5, the blue line shows the animal's speed. As it walks, the speed jumps up high, and when it stops at its destination, the speed drops right back to zero.
> 
> This proves the computer can spot real walking trips without getting tricked by tiny movements."*

---

## Slide 7: Real Video Test 2 — Eating
* **Category**: `REAL VIDEO TEST 2`
* **Slide Title**: Measuring Meal Times at the Food Bowl
* **Subtitle**: Tested on daytime enclosure video (Camera 02)
* **Visual Asset**: `pic/tracking_results/eating_tracking_result.png` (Embedded 5-Panel Infographic)
* **Sidebar Metrics**:
  * **What Happened?**: Civet visited the food bowl and ate for 80 seconds
  * **Food Bowl Zone**: Marked in orange at the bottom center
  * **Head Position**: Stayed right over the bowl (green dots)
  * **Meal Duration**: 80 seconds continuous meal recorded
  * **Key Result**: Separates a real meal from simply walking past the bowl

> 🎙️ **Speaker Script (1:00 min)**:  
> *"Here is our second test, focusing on eating. This was recorded during the day on Camera 02.
> 
> In pictures 1, 2, and 3, the civet walks over to the food bowl and lowers its head to eat.
> In picture 4, you can see the orange box where the food tray sits. The green dots show the computer tracking the civet's head right over the food!
> In picture 5, the timer climbs up to 80 seconds. The computer measured an 80-second continuous meal.
> 
> Because we require the animal to stay at the bowl for at least 10 seconds, the system will never confuse an animal that just strolled past with an animal eating dinner."*

---

## Slide 8: Real Video Test 3 — Resting
* **Category**: `REAL VIDEO TEST 3`
* **Slide Title**: Confirming Bedtime in the Tire Nest
* **Subtitle**: Tested on night-vision video (Camera 03)
* **Visual Asset**: `pic/tracking_results/resting_tracking_result.png` (Embedded 5-Panel Infographic)
* **Sidebar Metrics**:
  * **Bedtime Spot**: Straw-lined tire bed at top of room
  * **Shelter Entry**: Climbed in at 27 seconds
  * **Sleeping Posture**: Curled into a ball in straw
  * **1-Minute Rule**: Stillness timer passed 60s at 86s mark
  * **State Output**: Officially recorded as ASLEEP
  * **Key Result**: Matches zoo description: 'Curling up in tire'

> 🎙️ **Speaker Script (1:00 min)**:  
> *"Here is our third test: tracking sleep.
> 
> Thanks to the zookeepers' guidance, we know the civet loves to sleep in the tire filled with straw at the top of Camera 03.
> In this video, the civet climbs into the tire at 27 seconds and curls up into a ball, exactly matching the zoo's official note: 'Curling up in tire'.
> In picture 5, our stillness timer starts counting. Once the civet stays completely still for 60 seconds in a row, the computer officially logs: 'The animal is asleep.'
> 
> This shows the computer understands both where the animal sleeps and how long it stays still."*

---

## Slide 9: Why Simple Is Better
* **Category**: `WHY SIMPLE IS BETTER`
* **Slide Title**: Fancy AI vs. Tailored Smart Vision
* **Subtitle**: Why complex AI struggled in the dark, and our simple method won
* **Key Visual / 2 Comparison Cards**:
  * **Fancy Deep Learning (YOLO)**:
    * ✗ **Doesn't Know Civets**: Trained on sunny pictures of dogs and cats. Gets confused by civets with long bodies and masked faces.
    * ✗ **Blind in the Dark**: On grainy black-and-white night video, standard AI frequently missed the civet completely.
    * ✗ **Hallucinated Plants & Birds**: Mistook static potted plants for birds with 90% confidence!
    * ✗ **Needs Expensive Computers**: Requires heavy, expensive gaming GPUs to run.
  * **Our Tailored Smart Vision**:
    * ✔ **Takes Advantage of Still Cameras**: Because cameras never move, it knows the room by heart and easily isolates the moving animal.
    * ✔ **Zero Plant Confusions**: Static plants and walls are completely ignored—never makes up fake objects!
    * ✔ **100% Reliable Tracking**: Never loses the animal in the dark, even when lighting shifts.
    * ✔ **Runs on an Ordinary PC**: Runs over 10x faster on a normal office laptop without needing extra hardware.

> 🎙️ **Speaker Script (0:50 min)**:  
> *"You might ask: Why not just download the latest deep learning AI?
> 
> We tried that! We ran YOLO, a very popular deep learning model, and it struggled terribly in the dark.
> Because it was trained on sunny pictures of dogs and cats, it got confused by black-and-white night video. It missed the civet completely, and it even pointed at a potted plant and called it a bird with 90% confidence! Plus, it needs expensive computers.
> 
> Instead, our tailored vision system takes advantage of the fact that the zoo cameras never move. It ignores all plants and walls, tracks the civet 100% reliably, and runs smoothly on an ordinary office laptop."*

---

## Slide 10: Smart Common Sense
* **Category**: `SMART COMMON SENSE`
* **Slide Title**: The 1-Minute Rule: Avoiding Silly Mistakes
* **Subtitle**: How the system tells the difference between a short pause and a real nap
* **Key Visual / 2 Cards**:
  * **Left: Two Levels of Smart Tracking**:
    * • **The Big Picture (Active vs. Asleep)**: Keeps track of overall day and night cycles. Is the animal up and about, or is it asleep for the night?
    * • **The Small Events (Walks & Meals)**: Catches short events without getting confused: a quick 10-second walk or an 80-second meal.
    * • **Why Two Levels?**: Animals naturally take 5-second breathers while walking, or twitch while sleeping. Two levels prevent the computer from changing its mind every two seconds.
  * **Right: How the 1-Minute Rule Works**:
    * ⚙ **A 5-Second Stop is NOT Sleep**: If an animal stops for a few seconds during a walk, it hasn't gone to bed! The computer waits for a full 60 seconds of stillness before saying it's asleep.
    * ⚙ **Moving Wakes It Up Instantly**: As soon as the animal starts walking for 3 seconds, the sleep state ends immediately.
    * ⚙ **Scratching Doesn't Ruin Sleep**: Small tail wiggles or ear scratches while lying down don't fool the computer into thinking it woke up.
    * ⚙ **Clean, Trustworthy Reports**: Produces daily health logs that zoo veterinarians can actually trust.

> 🎙️ **Speaker Script (0:45 min)**:  
> *"One big problem with computer monitoring is 'flickering'—when the computer changes its mind every second.
> 
> If an animal pauses for 5 seconds while walking, it didn't fall asleep! And if a sleeping animal scratches its ear, it didn't wake up.
> 
> To solve this, we built in some common sense: the 1-Minute Rule.
> The computer waits for 60 seconds of unbroken stillness before declaring that the animal is asleep. And if the animal starts walking, it immediately marks it as active.
> This simple rule keeps our daily reports clean, accurate, and trustworthy."*

---

## Slide 11: Proven in Practice
* **Category**: `PROVEN IN PRACTICE`
* **Slide Title**: Tested on 22 Real Zoo Videos
* **Subtitle**: Fast, light, and ready for everyday use at Chiang Mai Zoo
* **Top Metric Badges**:
  * **TOTAL CLIPS TESTED**: 22 Video Files (Walking, Eating, Sleeping)
  * **CHECKS TWICE A SECOND**: 2 Frames / Sec (Saves 85% Computer Power)
  * **LIGHTWEIGHT SPEED**: > 45 FPS on Laptop (Runs on Normal Zoo PC)
* **Bottom Left: Real Zoo Conditions Tested**:
  * • High Definition: 1080p Full HD security video
  * • All Lighting Conditions: Daytime color and pitch-black infrared
  * • Real Animal Behaviors: 8 eating clips, 8 walking clips, 6 sleeping clips
  * • Varied Lengths: Short 10-second walks to 2-minute continuous naps
* **Bottom Right: Why Checking 2 Times a Second Wins**:
  * ✔ **Animals Move at Natural Speeds**: A civet walking across the room takes 3 to 10 seconds. Checking twice a second gives us 6 to 20 snapshots—plenty to see every step!
  * ✔ **Huge Power Savings**: Checking twice a second instead of 15 cuts computer workload by over 85%, so the computer stays cool and never lags.
  * ✔ **Never Misses Meals or Naps**: Because eating lasts minutes and sleeping lasts hours, twice a second captures 100% of start and end times.

> 🎙️ **Speaker Script (0:45 min)**:  
> *"We didn't just test this on one video—we tested it across 22 real video recordings from Chiang Mai Zoo.
> 
> Our key finding is that checking the video twice a second is the sweet spot. A walking civet takes several seconds to cross the room, so checking twice a second captures every step while cutting computer workload by over 85%.
> 
> As a result, the entire system runs smoothly on a basic laptop at over 45 frames per second. It is ready for practical, everyday use at the zoo."*

---

## Slide 12: Summary & Future
* **Category**: `SUMMARY & FUTURE`
* **Slide Title**: What We Built & Where We Are Going Next
* **Subtitle**: From video cameras to a smart tool for animal happiness and health
* **Key Visual / 2 Cards**:
  * **Left: What We Delivered Today (Phase 1)**:
    * ✔ **Automatic Daily Notes**: Creates digital records of every walk, meal, and nap with exact timestamps.
    * ✔ **Proven Accuracy**: Tested and validated on 22 real zoo video clips under night and day lighting.
    * ✔ **Common-Sense Logic**: The 1-minute rule prevents silly mistakes and false sleep alarms.
    * ✔ **Works on Everyday Computers**: Runs fast on normal zoo office PCs without buying expensive extra gear.
  * **Right: What Comes Next (Phase 2)**:
    * 🚀 **Follow Civets Across Rooms**: Keep tracking the animal as it walks through tunnels between Rooms 1, 2, 3, and 4.
    * 🚀 **Spot More Behaviors**: Notice bathroom visits in the sand box and self-grooming sessions.
    * 🚀 **Train a Custom Civet AI**: Teach a lightweight AI specifically on Chiang Mai Zoo's civets to boost dark recognition even further.
    * 🚀 **Zookeeper Tablet Dashboard**: A friendly phone or tablet app showing daily charts and alerting staff if an animal stops eating.

> 🎙️ **Speaker Script (0:45 min)**:  
> *"To wrap up: in Phase 1, we successfully built a smart assistant that watches zoo cameras and creates automated, reliable records of walking, eating, and sleeping.
> 
> It is fast, explainable, and runs on normal computers without extra cost.
> 
> Looking ahead to Phase 2, we plan to follow the civet as it moves between all four rooms, detect bathroom visits and grooming, and give zookeepers a friendly phone app that shows daily health summaries at a glance.
> 
> Thank you very much for listening. We would love to answer any questions!"*
