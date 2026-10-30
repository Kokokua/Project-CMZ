# แผนการดำเนินงานและสถาปัตยกรรมทางเทคนิค (Project Technical Specification & Plan)
## ระบบตรวจติดตามพฤติกรรมชะมดแผงสันหางดำในสวนสัตว์เชียงใหม่ (Automated Civet Behavior Monitoring System)

---

## 1. บทนำและบริบทโครงการ (Project Context & Objectives)
- **โจทย์จริงจากหน้างาน**: สวนสัตว์เชียงใหม่ (Chiang Mai Zoo - CMZ) ดูแลชะมดแผงสันหางดำ (*Large spotted civet*) ตัวแทนชื่อ **"หอมป้อม"** ซึ่งเป็นสัตว์รักสันโดษ หากินกลางคืน (Nocturnal)
- **สภาพแวดล้อม (Physical Setup)**: 
  - อาศัยอยู่ในกรง 4 ห้องเชื่อมต่อกันแบบเรียงลำดับ: `Room 1 → Room 2 → Room 3 → Room 4`
  - ติดตั้งกล้องวงจรปิดมุมสูง 4 ตัว (1 ตัวต่อ 1 ห้อง: Camera 01 - 04) ส่องเห็นทางเชื่อมและพื้นที่กิจกรรม
  - มีจุดบดบัง (Occlusion) เช่น กล่องไม้สำหรับนอนในห้อง 2, ตอไม้กลวงในห้อง 1, ยางรถยนต์ในห้อง 3
- **Pain Point ปัจจุบัน**: เจ้าหน้าที่ต้องนั่งดูภาพย้อนหลัง 4 หน้าจอและจดบันทึกลงในกระดาษ **Observation Sheet** ด้วยมือ ซึ่งใช้เวลาสูงมากและขึ้นกับดุลยพินิจของแต่ละบุคคล
- **เป้าหมาย Phase 1**: พัฒนาระบบ AI + Computer Vision และ Temporal Logic เพื่อแปลงวิดีโอ 4 กล้องให้เป็น **Structured Digital Behavior Log** โดยเน้น Concept, Data Analysis, Pipeline Architecture และ Evaluation Plan

---

## 2. ขอบเขตพฤติกรรมใน Phase 1 (Target Behaviors)
อิงตาม **Ethogram มาตรฐานของสวนสัตว์เชียงใหม่** โดยคัดเลือก 3 พฤติกรรมหลักสำหรับเฟสแรก:

1. **Resting (การพักผ่อน / Inactive)**:
   - ครอบคลุม: นอนเหยียด (Stretched out), หมอบ (Lying down), ขดตัวในยางรถ (Curling up), นอนในกล่องไม้ (Sleep in a box), นั่งหรือยืนนิ่ง
2. **Locomotion (การเดิน / Active)**:
   - ก้าวเดินต่อเนื่องเปลี่ยนตำแหน่ง เดินสำรวจ หรือเดินข้ามห้อง
3. **Eating (การกินอาหารและน้ำ)**:
   - ก้มหัวกินอาหารจากถาด หรือเลียน้ำจากอ่างน้ำ (ก้มหัวบริเวณ Food/Water Tray)
- *(หมายเหตุ: การขับถ่าย Urination/Defecation, แต่งขน Grooming และการทำอาณาเขต Territorial Marking ถูกยกยอดไปเป็น Future Work เนื่องจากยังไม่มีคลิปใน Dataset)*

---

## 3. ข้อมูลสถิติของ Dataset จริง (Dataset Exploration & Findings)

จากการสกัดค่า Metadata ในไฟล์วิดีโอตัวอย่าง 22 คลิป ในโฟลเดอร์ `dataset/`:

| หมวดหมู่ (Behavior) | จำนวนคลิป | ความยาวรวม (วินาที) | ความยาวเฉลี่ย | ช่วงความยาวคลิป |
| :--- | :---: | :---: | :---: | :---: |
| **Eating** | 5 | 254.44 s (~4.2 นาที) | ~50.9 s | 8.80s – 80.72s |
| **Locomotion** | 10 | 138.72 s (~2.3 นาที) | ~13.9 s | **8.00s – 28.88s** |
| **Resting** | 7 | 658.67 s (~11.0 นาที) | ~94.1 s | 30.88s – 219.92s |
| **รวมทั้งหมด** | **22** | **1,051.83 s (~17.5 นาที)** | - | - |

### ข้อกำหนดทางเทคนิคของวิดีโอ:
- **Resolution**: `1920×1080` (Full HD) ทุกคลิป
- **Frame Rate ดั้งเดิม**: `15.0 FPS` (เข้ารหัส H.265/HEVC)
- **การปรับแต่ง Frame Rate (Sampling Rate)**: 
  - **ปรับลดลงเหลือ 2 FPS (Sample ทุก 0.5 วินาที)** 
  - **เหตุผล**: พฤติกรรมชะมดเปลี่ยนในระดับวินาที การใช้ 2 FPS ลดภาระการประมวลผลลงถึง 7.5 เท่า (จาก 900 เฟรม/นาที เหลือเพียง 120 เฟรม/นาที) แต่ยังคงความต่อเนื่องของการวัดระยะเดิน (Centroid Displacement) ได้อย่างแม่นยำ

---

## 4. สถาปัตยกรรมระบบ AI และขั้นตอนการประมวลผล (AI Architecture & Pipeline)

```
[ 4 Cameras (1080p @ 15fps) ]
            │
            ▼ (Downsample to 2 FPS)
[ Step 1: Pre-trained YOLOv8 Detection ] ──► ตรวจจับชะมด (BBox, Confidence)
            │
            ▼
[ Step 2: Feature & Motion Extraction ]
  ├── BBox Centroid Displacement (คำนวณระยะการเคลื่อนที่ ΔX, ΔY)
  └── Food Zone ROI Filter (ตรวจสอบตำแหน่งว่าอยู่ในพิกัดถาดอาหารหรือไม่)
            │
            ▼
[ Step 3: Temporal Rule Engine (Finite State Machine with Debounce) ]
  ├── Macro State Transition: Active ⇄ Inactive (เกณฑ์ 1 นาที / 120 เฟรม)
  └── Micro Event Detection: บันทึกช่วงเวลาของ Locomotion และ Eating
            │
            ▼
[ Step 4: Multi-Camera Fusion & Room Tracking ] ──► เชื่อมโยงไทม์ไลน์ 4 ห้อง
            │
            ▼
[ Output: Structured Behavior Log & Dashboard ]
```

### รายละเอียดแต่ละขั้นตอน:

### ขั้นที่ 1: ตรวจจับชะมด (Civet Detection)
- **โมเดลที่เลือก**: **YOLOv8 (Ultralytics)** Pre-trained weights
- **แนวทาง**:
  1. เริ่มต้นด้วย **Zero-shot / Pre-trained COCO** (ทดสอบคลาส `cat` หรือ `dog` ซึ่งมีสรีระและ 4 ขาใกล้เคียงกับชะมด)
  2. หากผลการทดสอบเบื้องต้นพบปัญหาในโหมดอินฟราเรด (IR Night Vision) จะทำการ Fine-tune ด้วยภาพตัวอย่างจากคลิปประมาณ 50–100 เฟรม

### ขั้นที่ 2: สกัดการเคลื่อนไหวและพื้นที่ (Motion & Spatial Heuristics)
- **การเคลื่อนที่ (Motion Metric)**:
  - คำนวณระยะห่างของจุดกึ่งกลาง Bounding Box (Centroid Displacement) ระหว่างเฟรมที่ $t$ และ $t-1$:
    $$D_t = \sqrt{(X_t - X_{t-1})^2 + (Y_t - Y_{t-1})^2}$$
  - หาก $D_t > \text{Threshold}_{\text{motion}}$ ถือว่ามีกิจกรรมเคลื่อนไหว
- **พื้นที่อาหาร (Food Zone ROI)**:
  - กำหนดพิกัดพื้นที่ถาดอาหารและอ่างน้ำ (Region of Interest) แบบ Static Polygon ของแต่ละกล้อง
  - หาก Centroid ของชะมดอยู่ในโซนนี้ และค่าการเคลื่อนที่ต่ำ $\rightarrow$ มีเงื่อนไขเข้าสู่พฤติกรรม `Eating`

### ขั้นที่ 3: กฎเวลาและการสลับสถานะ (Temporal State Machine / 1-Minute Rule)
- **Macro State (Inactive ⇄ Active)**:
  - **Active $\rightarrow$ Inactive**: ชะมดต้องอยู่นิ่ง (หรือเข้ากล่องนอน/มุมอับ) ต่อเนื่องครบ **1 นาที (120 เฟรมที่ 2 FPS)** จึงจะเปลี่ยนสถานะ
  - **Inactive $\rightarrow$ Active**: ชะมดต้องเคลื่อนไหวต่อเนื่องครบ **1 นาที** จึงจะสลับเป็น Active (ป้องกันการตื่นเท็จจากการแค่นอนขยับตัว)
- **Micro Events**:
  - เมื่อระบบอยู่ในสถานะ `Active`:
    - กิจกรรมการเดินช่วงสั้นๆ (8–28 วินาที) จะถูกบันทึกเป็น Event `Locomotion`
    - กิจกรรมการก้มกินที่ถาดอาหาร จะถูกบันทึกเป็น Event `Eating` พร้อมเพิ่มความถี่ (Frequency count) สอดคล้องกับช่อง Tally Mark ของสวนสัตว์

### ขั้นที่ 4: การผสานข้อมูลข้ามกล้อง (Multi-Camera Fusion)
- ใช้ลำดับเวลา (Timestamp) ควบคู่กับ Topology ของห้อง (`Room 1 ⇄ Room 2 ⇄ Room 3 ⇄ Room 4`)
- เมื่อชะมดเดินหลุดจากขอบเฟรมของ Camera 1 และไปปรากฏตัวใน Camera 2 ภายในเวลาที่สมเหตุสมผล ระบบจะบันทึกเป็น Room Transition Event

---

## 5. รูปแบบผลลัพธ์ (Structured Event Log)
ระบบจะสร้าง Event Log ในรูปแบบดิจิทัล (JSON / CSV / SQLite) เพื่อทดแทนการจดกระดาษ:

| Event ID | Start Time | End Time | Duration (s) | Room / Camera | Macro State | Specific Behavior | Confidence |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 001 | 09:09:44 | 09:09:55 | 11 s | Room 3 (Cam 03) | Active | Locomotion | 0.92 |
| 002 | 09:23:26 | 09:24:46 | 80 s | Room 2 (Cam 02) | Active | Eating | 0.95 |
| 003 | 19:41:09 | 20:15:00 | >1 min | Room 2 (Cam 02) | Inactive | Resting (Box) | 0.88 |

---

## 6. แผนการประเมินผล (Evaluation Plan)
- **ตัววัดผล (Metrics)**:
  - Detection Level: Precision, Recall, mAP@50
  - Behavior Classification Level: Precision, Recall, F1-Score, Confusion Matrix
  - Temporal Event Level: IoU ของช่วงเวลาเริ่มต้น-สิ้นสุด (Temporal Boundary IoU)
- **กลยุทธ์การแบ่งข้อมูล (Data Splitting Strategy)**:
  - **Split by Clip / Recording Session เท่านั้น** (ห้ามสุ่มตามเฟรม เพื่อป้องกัน Data Leakage)
  - แบ่งตามช่วงเวลาที่บันทึก (เช่น วันที่ 18 พ.ค. สำหรับ Train, วันที่ 19 พ.ค. สำหรับ Validation, วันที่ 20 พ.ค. สำหรับ Test)

---

## 7. โครงสร้างสไลด์นำเสนอ (10 Slides Overview)
1. **Title**: ระบบตรวจติดตามพฤติกรรมชะมดแผงสันหางดำข้าม 4 ห้องด้วย AI
2. **Problem & Motivation**: การเฝ้าจอ 4 จอและบันทึกมือ (แสดงภาพจริงจาก Slide 5 & 19 ของ CMZ)
3. **Environment & Cameras**: ผัง 4 ห้อง, 4 กล้อง, จุดบดบัง (แสดงภาพ Slide 18)
4. **Behavior Ethogram**: นิยาม 3 พฤติกรรมหลัก (Resting, Locomotion, Eating)
5. **System Pipeline**: โฟลว์การทำงาน Preprocessing $\rightarrow$ YOLOv8 $\rightarrow$ Motion/ROI $\rightarrow$ FSM $\rightarrow$ Log
6. **Dataset & Video Spec**: สถิติ 22 คลิป, 1080p, 15 FPS $\rightarrow$ Downsample เหลือ 2 FPS
7. **Temporal Logic (1-Minute Rule)**: State Machine (Active ⇄ Inactive) ป้องกัน State Flicker
8. **AI Methodology**: เริ่มต้นด้วย Explainable Baseline (YOLO + Motion Rules) ก่อนต่อยอดโมเดลซับซ้อน
9. **Evaluation Plan**: ตัวชี้วัด F1-Score และการแบ่งข้อมูลแบบ Split by Session
10. **Expected Output & Next Steps**: ตัวอย่างตาราง Event Log และแผนการทดสอบในระยะถัดไป
