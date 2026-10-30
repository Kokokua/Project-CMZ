import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

desktop_dir = r"C:\Users\ASUS\Desktop\html knowledge file"
os.makedirs(desktop_dir, exist_ok=True)
out_path = os.path.join(desktop_dir, "phase2-options-comparison.html")

html_content = """<!DOCTYPE html>
<html lang="th" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Phase 2 Architectural Options & Comprehensive Trade-Off Analysis | Chiang Mai Zoo x CMU</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            zoo: {
              teal: '#1B4958',
              teallight: '#2A667A',
              tealdark: '#0F2C36',
              gold: '#E5A93C',
              golddark: '#C88B22',
              goldlight: '#F8DF9E',
              darkbg: '#0B1318',
              carddark: '#132128',
              cardborder: '#233945',
              surface: '#1A2B34'
            }
          },
          fontFamily: {
            sans: ['"TH Sarabun New"', 'THSarabunNew', 'Sarabun', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'Fira Code', 'Consolas', 'monospace']
          }
        }
      }
    }
  </script>

  <!-- Google Fonts: Sarabun & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Sarabun:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap" rel="stylesheet">
  
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <style>
    body {
      font-family: 'Sarabun', sans-serif;
      font-size: 16px;
      line-height: 1.6;
    }
    .mono {
      font-family: 'JetBrains Mono', monospace;
    }
    .glass-card {
      background: rgba(19, 33, 40, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(42, 102, 122, 0.35);
    }
    .gold-glow {
      box-shadow: 0 0 25px -5px rgba(229, 169, 60, 0.3);
    }
    .teal-glow {
      box-shadow: 0 0 25px -5px rgba(27, 73, 88, 0.5);
    }
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0B1318; }
    ::-webkit-scrollbar-thumb { background: #1B4958; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #E5A93C; }
  </style>
</head>
<body class="bg-slate-50 dark:bg-zoo-darkbg text-slate-800 dark:text-slate-100 transition-colors duration-300 antialiased selection:bg-zoo-gold selection:text-zoo-darkbg">

  <!-- Header -->
  <header class="sticky top-0 z-40 bg-white/90 dark:bg-zoo-darkbg/90 backdrop-blur-md border-b border-slate-200 dark:border-zoo-cardborder transition-colors">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-zoo-teal to-zoo-tealdark flex items-center justify-center border border-zoo-gold/40 shadow-md">
          <i data-lucide="git-branch" class="w-6 h-6 text-zoo-gold"></i>
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <span class="px-2 py-0.5 rounded text-xs font-bold bg-zoo-gold/20 text-zoo-gold border border-zoo-gold/40">PHASE 2 MASTER PLAN</span>
            <span class="text-xs text-slate-500 dark:text-slate-400 font-mono">DEADLINE: 31 OCT 2026 NOON</span>
          </div>
          <h1 class="text-xl font-bold tracking-tight text-zoo-teal dark:text-white flex items-center gap-2">
            Civet AI Phase 2: ตัวเลือกการพัฒนาและตารางเปรียบเทียบเชิงลึกทุกมิติ
          </h1>
        </div>
      </div>

      <!-- Theme Toggle & Links -->
      <div class="flex items-center space-x-3">
        <a href="#matrix-section" class="hidden sm:inline-flex px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-zoo-teal/20 text-zoo-teallight dark:text-cyan-400 border border-zoo-teal/40 hover:bg-zoo-teal/30 transition-all">
          <i data-lucide="table" class="w-3.5 h-3.5 mr-1.5"></i> ตารางเปรียบเทียบ
        </a>
        <button id="theme-toggle" class="p-2.5 rounded-lg border border-slate-300 dark:border-zoo-cardborder bg-slate-100 dark:bg-zoo-carddark text-slate-700 dark:text-zoo-gold hover:border-zoo-gold transition-all" title="Toggle Theme">
          <i data-lucide="moon" class="w-5 h-5 hidden dark:block"></i>
          <i data-lucide="sun" class="w-5 h-5 block dark:hidden"></i>
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-12">

    <!-- Hero Context Section -->
    <section class="p-8 rounded-3xl bg-gradient-to-br from-white to-slate-100 dark:from-zoo-carddark dark:to-zoo-surface border border-slate-200 dark:border-zoo-cardborder shadow-xl">
      <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
        <div class="space-y-3 max-w-3xl">
          <div class="flex items-center gap-2">
            <span class="px-3 py-1 rounded-full text-xs font-mono font-bold bg-zoo-gold/15 text-zoo-gold border border-zoo-gold/30">
              BRIDGING PHASE 1 TO CAMERA 1-4
            </span>
            <span class="text-xs text-slate-400 font-mono">Chiang Mai Zoo × CMU 2026</span>
          </div>
          <h2 class="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            การเปลี่ยนผ่านจากคลิปย่อย 22 คลิป สู่การประมวลผลกล้องวงจรปิดจริง Camera 1 – 4
          </h2>
          <p class="text-base text-slate-600 dark:text-slate-300 leading-relaxed">
            ใน Phase 1 เราได้สร้าง Proof of Concept ด้วยเทคนิค Image Processing บนคลิปสั้นที่ถูกตัดมาแล้ว 22 คลิป แต่สำหรับ <strong>Phase 2</strong> สวนสัตว์เชียงใหม่ได้มอบไฟล์วิดีโอกล้องวงจรปิดบันทึกต่อเนื่องรอบ 24 ชั่วโมงจาก <strong>Camera 1 ถึง Camera 4</strong> รวม 31 ไฟล์ (~25.5 GB) ที่เพิ่งจัดเรียงเสร็จ หน้าที่ของเราคือการเลือกสถาปัตยกรรม AI ที่เหมาะสม ตอบโจทย์อาจารย์ครบถ้วน และส่งงานได้ทันกำหนด <strong>31 ต.ค. เวลา 12:00 น.</strong>
          </p>
        </div>
        <div class="p-6 rounded-2xl bg-slate-900 border border-slate-800 text-center min-w-[260px] space-y-2 shadow-2xl">
          <div class="text-xs font-mono text-slate-400 uppercase tracking-wider">เวลาก่อนกำหนดส่งงาน</div>
          <div class="text-3xl font-black text-amber-400 font-mono">~48 ชั่วโมง</div>
          <div class="text-xs text-slate-400">วันเสาร์ที่ 31 ต.ค. 2026 (เที่ยงวัน)</div>
          <div class="pt-2 border-t border-slate-800 text-[11px] text-emerald-400 font-mono">
            RTX 3050 Laptop พร้อมใช้งาน
          </div>
        </div>
      </div>

      <!-- Teacher's 4 Core Requirements Matrix -->
      <div class="mt-8 pt-6 border-t border-slate-200 dark:border-zoo-cardborder">
        <h4 class="text-xs font-mono font-bold text-zoo-gold uppercase tracking-wider mb-4">
          ข้อกำหนด 4 ข้อที่ต้องส่งอาจารย์ใน Phase 2 (Mandatory Deliverables)
        </h4>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="p-4 rounded-xl bg-white dark:bg-zoo-darkbg/70 border border-slate-200 dark:border-zoo-cardborder space-y-1">
            <div class="text-xs font-mono text-emerald-400 font-bold">01. TRAIN MODEL</div>
            <div class="text-sm font-bold text-slate-800 dark:text-white">เทรนโมเดล AI</div>
            <p class="text-xs text-slate-500">เลือกคลิปตัวแทนที่เหมาะสมที่สุด ไม่ต้องรัน 25GB ทั้งหมด สกัดเฟรมสำคัญแล้วเทรน</p>
          </div>
          <div class="p-4 rounded-xl bg-white dark:bg-zoo-darkbg/70 border border-slate-200 dark:border-zoo-cardborder space-y-1">
            <div class="text-xs font-mono text-cyan-400 font-bold">02. EXPLAIN MODEL</div>
            <div class="text-sm font-bold text-slate-800 dark:text-white">อธิบายโมเดล AI</div>
            <p class="text-xs text-slate-500">อธิบายสถาปัตยกรรม (เช่น YOLOv8) เหตุผลที่เลือก โครงสร้าง C2f และ Anchor-free</p>
          </div>
          <div class="p-4 rounded-xl bg-white dark:bg-zoo-darkbg/70 border border-slate-200 dark:border-zoo-cardborder space-y-1">
            <div class="text-xs font-mono text-purple-400 font-bold">03. ACTIVE / INACTIVE</div>
            <div class="text-sm font-bold text-slate-800 dark:text-white">ออกแบบตาราง & กราฟ</div>
            <p class="text-xs text-slate-500">สร้างตารางพฤติกรรม (Event Log) และภาพสรุป Activity Budget สัดส่วน Active vs Inactive</p>
          </div>
          <div class="p-4 rounded-xl bg-white dark:bg-zoo-darkbg/70 border border-slate-200 dark:border-zoo-cardborder space-y-1">
            <div class="text-xs font-mono text-amber-400 font-bold">04. GITHUB & ROBOFLOW</div>
            <div class="text-sm font-bold text-slate-800 dark:text-white">ส่งมอบลิงก์ซอร์สโค้ด</div>
            <p class="text-xs text-slate-500">ลิงก์ GitHub Repository ของโปรเจกต์ และลิงก์ชุดข้อมูล Annotation บน Roboflow</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 3 Strategic Options Deep-Dive Cards -->
    <section class="space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-xs font-mono text-zoo-gold font-bold">THREE STRATEGIC PATHWAYS</span>
          <h3 class="text-2xl font-bold text-slate-900 dark:text-white">3 แผนตัวเลือกในการพัฒนาสถาปัตยกรรม Phase 2</h3>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">

        <!-- OPTION 1 -->
        <div class="relative p-7 rounded-3xl bg-white dark:bg-zoo-carddark border-2 border-emerald-500 shadow-xl flex flex-col justify-between">
          <div class="absolute -top-3.5 right-6 px-3.5 py-1 rounded-full text-xs font-mono font-bold bg-emerald-500 text-slate-950 uppercase tracking-wide shadow-md">
            RECOMMENDED (แนะนำสูงสุด) 🌟
          </div>

          <div class="space-y-5">
            <div>
              <span class="text-xs font-mono text-emerald-400 font-bold">OPTION 01: END-TO-END DIRECT CLASSIFICATION</span>
              <h4 class="text-xl font-bold text-slate-900 dark:text-white mt-1">
                YOLOv8 Dual-Class Detection
              </h4>
              <p class="text-xs text-slate-500 dark:text-slate-400 font-mono mt-0.5">
                Classes: [civet_active, civet_inactive] + 1-Minute Rule
              </p>
            </div>

            <p class="text-sm text-slate-600 dark:text-slate-300">
              สกัดเฟรม 150–200 ภาพจาก Camera 1–4 ทำ Label แยกเป็น 2 คลาสโดยตรง: <strong>civet_active</strong> (กำลังเดิน วิ่ง กิน สำรวจ) และ <strong>civet_inactive</strong> (นอนราบ ขดตัว หมอบนิ่ง) จากนั้นเทรน YOLOv8n ให้จำแนกพฤติกรรมใน Forward Pass เดียว และใช้กฎ 1 นาที (1-Minute Rule) จาก Phase 1 กรองสถานะไม่ให้กระพริบ
            </p>

            <!-- Architecture Diagram Micro -->
            <div class="p-3.5 rounded-xl bg-slate-900 font-mono text-xs text-emerald-300 space-y-1 border border-slate-800">
              <div>Raw CCTV Frame (Camera 1-4)</div>
              <div class="text-slate-500">  │</div>
              <div>  ▼ YOLOv8n Head (End-to-End)</div>
              <div>  ├─ Output 1: civet_active BBox (Conf 0.94)</div>
              <div>  └─ Output 2: civet_inactive BBox (Conf 0.91)</div>
              <div class="text-slate-500">  │</div>
              <div>  ▼ Temporal 1-Minute Zoological Smoothing</div>
              <div>  └─► Active / Inactive CSV & Activity Budget</div>
            </div>

            <!-- Pros -->
            <div class="space-y-2">
              <div class="text-xs font-bold text-emerald-400 font-mono flex items-center gap-1.5">
                <i data-lucide="check" class="w-4 h-4"></i> ข้อดี (PROS):
              </div>
              <ul class="text-xs text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                <li><strong>ตรงโจทย์อาจารย์ 100%:</strong> โมเดล AI เป็นตัวจำแนก Active/Inactive ด้วยตัวเองจาก Visual Features อย่างแท้จริง</li>
                <li><strong>สถาปัตยกรรมกระชับ:</strong> โมเดลเดียวจบ (Single Network) ทำงานเรียลไทม์ 45–60 FPS</li>
                <li><strong>นำเสนอง่ายและทรงพลัง:</strong> โชว์ภาพ Bounding Box สีเขียว (Active) และสีส้ม (Inactive) สื่อสารเข้าใจทันที</li>
                <li><strong>เสร็จทันกำหนดแน่นอน:</strong> ใช้เวลาสกัดเฟรมและเทรนรวมประมาณ 1 - 1.5 ชั่วโมง</li>
              </ul>
            </div>

            <!-- Cons -->
            <div class="space-y-2">
              <div class="text-xs font-bold text-rose-400 font-mono flex items-center gap-1.5">
                <i data-lucide="alert-circle" class="w-4 h-4"></i> ข้อจำกัด (CONS):
              </div>
              <ul class="text-xs text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                <li>ต้องทำ Annotation แยก 2 คลาสบน Roboflow</li>
                <li>หากสัตว์หยุดยืนนิ่งชั่วคราวแต่ยังตื่นอยู่ ภาพนิ่งอาจคล้ายการนอน จึงต้องมีตรรกะหน่วงเวลา 1 นาทีช่วยกำกับ</li>
              </ul>
            </div>
          </div>

          <div class="mt-6 pt-4 border-t border-slate-200 dark:border-zoo-cardborder text-center">
            <span class="text-xs font-bold text-emerald-400 font-mono">ความคุ้มค่า: สูงสุด ⭐⭐⭐⭐⭐ | ความเสี่ยง: ต่ำสุด</span>
          </div>
        </div>

        <!-- OPTION 2 -->
        <div class="relative p-7 rounded-3xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-xl flex flex-col justify-between">
          <div class="space-y-5">
            <div>
              <span class="text-xs font-mono text-cyan-400 font-bold">OPTION 02: HYBRID AI + KINEMATIC FUSION</span>
              <h4 class="text-xl font-bold text-slate-900 dark:text-white mt-1">
                YOLOv8 Detection + Phase 1 Motion Engine
              </h4>
              <p class="text-xs text-slate-500 dark:text-slate-400 font-mono mt-0.5">
                Classes: [civet] + Speed Vector & ROI Intersection
              </p>
            </div>

            <p class="text-sm text-slate-600 dark:text-slate-300">
              เทรน YOLOv8 ให้ตรวจจับเฉพาะตำแหน่งตัวชะมด (คลาสเดียว: <strong>civet</strong>) โดย AI รับผิดชอบการตัดปัญหาเรื่องแสงเงาและมุมมองข้าม 4 ห้อง จากนั้นส่งพิกัด Bounding Box Centroid เข้าสู่ <strong>Kinematic Engine</strong> ของ Phase 1 เพื่อวัดความเร็ว (Speed Vector px/s) และการทับซ้อน ROI ถาดอาหาร/ที่นอน เพื่อจำแนก Active/Inactive
            </p>

            <!-- Architecture Diagram Micro -->
            <div class="p-3.5 rounded-xl bg-slate-900 font-mono text-xs text-cyan-300 space-y-1 border border-slate-800">
              <div>Raw CCTV Frame (Camera 1-4)</div>
              <div class="text-slate-500">  │</div>
              <div>  ▼ YOLOv8n Detector (1 Class: civet)</div>
              <div>  │ BBox (X, Y, W, H) -> Centroid (cx, cy)</div>
              <div>  ▼ Kinematic Engine (Phase 1 Logic)</div>
              <div>  ├─ Speed vt = sqrt(Δcx² + Δcy²) / Δt</div>
              <div>  └─ ROI Check: Food Tray & Tire Bed</div>
              <div>  ▼ Zoological 1-Minute State Machine</div>
              <div>  └─► Active / Inactive CSV & Activity Budget</div>
            </div>

            <!-- Pros -->
            <div class="space-y-2">
              <div class="text-xs font-bold text-cyan-400 font-mono flex items-center gap-1.5">
                <i data-lucide="check" class="w-4 h-4"></i> ข้อดี (PROS):
              </div>
              <ul class="text-xs text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                <li><strong>Annotation ง่ายที่สุด:</strong> ล้อมกรอบเฉพาะตัวสัตว์อย่างเดียว ไม่ต้องกังวลว่าเฟรมนั้นสัตว์ทำพฤติกรรมอะไร</li>
                <li><strong>ความแม่นยำเชิงฟิสิกส์สูง:</strong> คำนวณจากการก้าวเดินจริง ไม่มีปัญหาภาพนิ่งหลอก</li>
                <li><strong>ต่อยอด Phase 1 ได้ 100%:</strong> ดึงโค้ด Centroid, ROI และ FSM เดิมที่เขียนและทดสอบไว้แล้วมาต่อยอดได้ทันที</li>
              </ul>
            </div>

            <!-- Cons -->
            <div class="space-y-2">
              <div class="text-xs font-bold text-rose-400 font-mono flex items-center gap-1.5">
                <i data-lucide="alert-circle" class="w-4 h-4"></i> ข้อจำกัด (CONS):
              </div>
              <ul class="text-xs text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                <li>โมเดล AI ส่งออกแค่ตำแหน่งกล่อง สิทธิการตัดสินใจอยู่ที่ Rule-based ภายนอก</li>
                <li>อาจารย์บางท่านอาจมองว่า AI ยังไม่ได้จำแนกพฤติกรรมโดยตรง (Indirect Classification)</li>
              </ul>
            </div>
          </div>

          <div class="mt-6 pt-4 border-t border-slate-200 dark:border-zoo-cardborder text-center">
            <span class="text-xs font-bold text-cyan-400 font-mono">ความคุ้มค่า: สูงมาก ⭐⭐⭐⭐ | ความเสี่ยง: ต่ำมาก</span>
          </div>
        </div>

        <!-- OPTION 3 -->
        <div class="relative p-7 rounded-3xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-xl flex flex-col justify-between opacity-85">
          <div class="space-y-5">
            <div>
              <span class="text-xs font-mono text-purple-400 font-bold">OPTION 03: TWO-STAGE DEEP LEARNING</span>
              <h4 class="text-xl font-bold text-slate-900 dark:text-white mt-1">
                YOLOv8 Crop + Secondary CNN Classifier
              </h4>
              <p class="text-xs text-slate-500 dark:text-slate-400 font-mono mt-0.5">
                Stage 1: Detector + Stage 2: ResNet/MobileNet
              </p>
            </div>

            <p class="text-sm text-slate-600 dark:text-slate-300">
              ใช้โมเดล Deep Learning แยกกัน 2 ตัว: โมเดลตัวแรก (YOLOv8) ตรวจจับและทำการครอปภาพเฉพาะตัวชะมด จากนั้นส่งต่อภาพ Crop เข้าสู่โมเดล CNN ตัวที่สอง (เช่น ResNet-18 หรือ MobileNetV3) เพื่อจำแนกท่วงท่าละเอียด (Lying, Standing, Eating, Walking)
            </p>

            <!-- Architecture Diagram Micro -->
            <div class="p-3.5 rounded-xl bg-slate-900 font-mono text-xs text-purple-300 space-y-1 border border-slate-800">
              <div>Raw CCTV Frame (Camera 1-4)</div>
              <div class="text-slate-500">  │</div>
              <div>  ▼ Stage 1: YOLOv8 Detector</div>
              <div>  │ Crop BBox Image Patch (224x224)</div>
              <div>  ▼ Stage 2: MobileNet / ResNet</div>
              <div>  │ Softmax [Sleep, Walk, Eat, Stand]</div>
              <div>  ▼ Aggregation to Active / Inactive</div>
              <div>  └─► Active / Inactive CSV Table</div>
            </div>

            <!-- Pros -->
            <div class="space-y-2">
              <div class="text-xs font-bold text-purple-400 font-mono flex items-center gap-1.5">
                <i data-lucide="check" class="w-4 h-4"></i> ข้อดี (PROS):
              </div>
              <ul class="text-xs text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                <li>มีความเป็นงานวิจัยทางวิชาการขั้นสูง (Academic Prestige)</li>
                <li>สามารถจำแนกท่วงท่าย่อยที่ละเอียดอ่อนได้ (เช่น นอนขด vs นอนเหยียด)</li>
              </ul>
            </div>

            <!-- Cons -->
            <div class="space-y-2">
              <div class="text-xs font-bold text-rose-400 font-mono flex items-center gap-1.5">
                <i data-lucide="alert-circle" class="w-4 h-4"></i> ข้อควรระวัง (HIGH RISK):
              </div>
              <ul class="text-xs text-slate-600 dark:text-slate-300 space-y-1.5 list-disc list-inside">
                <li><strong>เวลาไม่พอ:</strong> ต้องเตรียม 2 Dataset และเทรน 2 โมเดล เสี่ยงส่งงานไม่ทัน 31 ต.ค.</li>
                <li>กินทรัพยากรสูง ประมวลผลได้ช้า (15–20 FPS)</li>
                <li>มีปัญหา Cascading Error หาก Stage 1 ครอปพลาด Stage 2 จะจำแนกผิดทันที</li>
              </ul>
            </div>
          </div>

          <div class="mt-6 pt-4 border-t border-slate-200 dark:border-zoo-cardborder text-center">
            <span class="text-xs font-bold text-rose-400 font-mono">ความคุ้มค่า: ปานกลาง ⭐⭐⭐ | ความเสี่ยง: สูงมาก ⚠️</span>
          </div>
        </div>

      </div>
    </section>

    <!-- Side-by-Side Detailed Comparison Matrix -->
    <section id="matrix-section" class="p-8 rounded-3xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-xl space-y-6">
      <div class="flex items-center justify-between">
        <div>
          <span class="text-xs font-mono text-zoo-gold font-bold">COMPREHENSIVE TRADE-OFF MATRIX</span>
          <h3 class="text-2xl font-bold text-slate-900 dark:text-white">ตารางเปรียบเทียบเชิงลึกทุกมิติการประเมิน</h3>
        </div>
        <span class="text-xs font-mono text-slate-400">เปรียบเทียบ 10 เกณฑ์หลัก</span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm border-collapse">
          <thead>
            <tr class="border-b border-slate-200 dark:border-zoo-cardborder bg-slate-50 dark:bg-zoo-surface/50 text-xs font-mono text-slate-500 dark:text-slate-400">
              <th class="p-4 w-1/4">มิติการประเมิน (Criteria)</th>
              <th class="p-4 w-1/4 text-emerald-400 font-bold bg-emerald-500/5 border-x border-emerald-500/20">
                Option 1: YOLOv8 Direct (2-Class) 🌟
              </th>
              <th class="p-4 w-1/4 text-cyan-400 font-bold">Option 2: Hybrid YOLO + Kinematic</th>
              <th class="p-4 w-1/4 text-purple-400 font-bold">Option 3: Two-Stage (YOLO + CNN)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200 dark:divide-zoo-cardborder text-xs sm:text-sm">
            <tr>
              <td class="p-4 font-bold text-slate-800 dark:text-white">1. ความตรงกับโจทย์ของอาจารย์</td>
              <td class="p-4 text-emerald-400 font-bold bg-emerald-500/5 border-x border-emerald-500/20">
                ⭐⭐⭐⭐⭐ ดีเลิศ<br/>
                <span class="text-xs font-normal text-slate-400">AI จำแนก Active/Inactive ด้วยตนเอง</span>
              </td>
              <td class="p-4 text-cyan-400 font-semibold">
                ⭐⭐⭐⭐ ดีมาก<br/>
                <span class="text-xs font-normal text-slate-400">AI จับกล่อง + โค้ดคณิตศาสตร์ตัดสิน</span>
              </td>
              <td class="p-4 text-purple-400">
                ⭐⭐⭐⭐ ดีมาก<br/>
                <span class="text-xs font-normal text-slate-400">AI จำแนก แต่ซับซ้อนเกินโจทย์</span>
              </td>
            </tr>

            <tr>
              <td class="p-4 font-bold text-slate-800 dark:text-white">2. เวลาในการพัฒนา (Dev Time)</td>
              <td class="p-4 text-emerald-400 font-bold bg-emerald-500/5 border-x border-emerald-500/20">
                ⏱️ ~1.5 - 2 ชั่วโมง<br/>
                <span class="text-xs font-normal text-emerald-400">ทันกำหนด 31 ต.ค. แน่นอน 100%</span>
              </td>
              <td class="p-4 text-cyan-400">
                ⏱️ ~1 ชั่วโมง<br/>
                <span class="text-xs font-normal text-cyan-400">เร็วที่สุดเพราะนำโค้ดเดิมมาต่อ</span>
              </td>
              <td class="p-4 text-rose-400 font-bold">
                ⏱️ ~6 - 8 ชั่วโมง<br/>
                <span class="text-xs font-normal text-rose-400">เสี่ยงสูงมากที่จะส่งไม่ทันเที่ยง 31 ต.ค.</span>
              </td>
            </tr>

            <tr>
              <td class="p-4 font-bold text-slate-800 dark:text-white">3. ความยากในการทำ Annotation</td>
              <td class="p-4 text-slate-700 dark:text-slate-300 bg-emerald-500/5 border-x border-emerald-500/20">
                ปานกลาง<br/>
                <span class="text-xs text-slate-400">150–200 เฟรม แยก 2 คลาสบน Roboflow</span>
              </td>
              <td class="p-4 text-emerald-400 font-semibold">
                ง่ายที่สุด<br/>
                <span class="text-xs text-slate-400">150 เฟรม ล้อมแค่ตัวชะมด 1 คลาส</span>
              </td>
              <td class="p-4 text-rose-400 font-semibold">
                ยากที่สุด<br/>
                <span class="text-xs text-slate-400">ต้องล้อมกล่อง และแยกภาพครอป 4 โฟลเดอร์</span>
              </td>
            </tr>

            <tr>
              <td class="p-4 font-bold text-slate-800 dark:text-white">4. ความเร็วในการประมวลผล (FPS)</td>
              <td class="p-4 font-mono text-emerald-400 font-bold bg-emerald-500/5 border-x border-emerald-500/20">
                45 - 60+ FPS<br/>
                <span class="text-xs font-sans text-slate-400">รันเรียลไทม์ได้สบายบน RTX 3050</span>
              </td>
              <td class="p-4 font-mono text-cyan-400 font-semibold">
                50 - 65+ FPS<br/>
                <span class="text-xs font-sans text-slate-400">เร็วมาก พิกัดเวกเตอร์ใช้เวลา 0.1ms</span>
              </td>
              <td class="p-4 font-mono text-rose-400 font-semibold">
                15 - 20 FPS<br/>
                <span class="text-xs font-sans text-slate-400">ช้าลงเพราะต้อง Forward 2 โมเดล</span>
              </td>
            </tr>

            <tr>
              <td class="p-4 font-bold text-slate-800 dark:text-white">5. การรองรับภาพกลางคืน (Night IR)</td>
              <td class="p-4 text-emerald-400 bg-emerald-500/5 border-x border-emerald-500/20">
                ดีเยี่ยม<br/>
                <span class="text-xs text-slate-400">เทรนด้วยเฟรมขาวดำผสมใน Dataset</span>
              </td>
              <td class="p-4 text-emerald-400">
                ดีเยี่ยม<br/>
                <span class="text-xs text-slate-400">จับกล่องตัวสัตว์ได้แม่นทั้งวัน/คืน</span>
              </td>
              <td class="p-4 text-slate-400">
                ปานกลาง<br/>
                <span class="text-xs text-slate-400">ภาพขาวดำครอปขนาดเล็กเสียรายละเอียด</span>
              </td>
            </tr>

            <tr>
              <td class="p-4 font-bold text-slate-800 dark:text-white">6. การเชื่อมต่อ 4 กล้อง (Camera 1-4)</td>
              <td class="p-4 text-emerald-400 bg-emerald-500/5 border-x border-emerald-500/20">
                ไร้รอยต่อ<br/>
                <span class="text-xs text-slate-400">โมเดลตรวจจับได้ทุกห้องด้วย weights เดียว</span>
              </td>
              <td class="p-4 text-cyan-400">
                ไร้รอยต่อ<br/>
                <span class="text-xs text-slate-400">ใช้แผนผังห้องและ ROI ร่วมกัน</span>
              </td>
              <td class="p-4 text-slate-400">
                ซับซ้อน<br/>
                <span class="text-xs text-slate-400">ต้องปรับจูนกล้องแต่ละตัวเพิ่มเติม</span>
              </td>
            </tr>

            <tr>
              <td class="p-4 font-bold text-slate-800 dark:text-white">7. การสร้างตาราง Active / Inactive</td>
              <td class="p-4 text-emerald-400 font-bold bg-emerald-500/5 border-x border-emerald-500/20">
                ส่งออก CSV ได้ทันที<br/>
                <span class="text-xs text-slate-400">ระบุเวลาเริ่ม-จบ-สถานะตรงตามที่ต้องการ</span>
              </td>
              <td class="p-4 text-cyan-400 font-semibold">
                ส่งออก CSV ได้ทันที<br/>
                <span class="text-xs text-slate-400">มีคอลัมน์ความเร็วและพิกัดเสริม</span>
              </td>
              <td class="p-4 text-purple-400">
                ส่งออก CSV ได้<br/>
                <span class="text-xs text-slate-400">แต่ต้องแปลงจากคลาสย่อยเป็น Macro state</span>
              </td>
            </tr>

            <tr>
              <td class="p-4 font-bold text-slate-800 dark:text-white">8. การนำเสนอและการอธิบาย (Explainability)</td>
              <td class="p-4 text-emerald-400 font-bold bg-emerald-500/5 border-x border-emerald-500/20">
                ชัดเจน ตรงประเด็น<br/>
                <span class="text-xs text-slate-400">อธิบายง่าย: "AI มองภาพแล้วรู้ทันทีว่าตื่นหรือนอน"</span>
              </td>
              <td class="p-4 text-cyan-400">
                เชิงลึกแบบไฮบริด<br/>
                <span class="text-xs text-slate-400">ต้องอธิบายทั้ง AI และสูตรคณิตศาสตร์</span>
              </td>
              <td class="p-4 text-slate-400">
                ซับซ้อนเกินไป<br/>
                <span class="text-xs text-slate-400">กินเวลาในการนำเสนอสไลด์ 3 คน</span>
              </td>
            </tr>

            <tr>
              <td class="p-4 font-bold text-slate-800 dark:text-white">9. การจัดทำ Deliverables (GitHub/Roboflow)</td>
              <td class="p-4 text-emerald-400 font-bold bg-emerald-500/5 border-x border-emerald-500/20">
                มีลิงก์พร้อมส่ง 100%<br/>
                <span class="text-xs text-slate-400">Roboflow Annotation + GitHub Repo</span>
              </td>
              <td class="p-4 text-cyan-400">
                มีลิงก์พร้อมส่ง 100%<br/>
                <span class="text-xs text-slate-400">Roboflow Annotation + GitHub Repo</span>
              </td>
              <td class="p-4 text-slate-400">
                ต้องทำ 2 ลิงก์<br/>
                <span class="text-xs text-slate-400">ลิงก์ Object Detection + Classification</span>
              </td>
            </tr>

            <tr class="bg-slate-100/50 dark:bg-zoo-surface/30">
              <td class="p-4 font-extrabold text-slate-900 dark:text-white">10. สรุปคำแนะนำ (Verdict)</td>
              <td class="p-4 text-emerald-400 font-black bg-emerald-500/10 border-x border-emerald-500/40">
                🌟 แนะนำสูงสุด (BEST CHOICE)<br/>
                <span class="text-xs font-normal text-slate-300">คุ้มค่า ตรงโจทย์ เสี่ยงต่ำ เสร็จทันแน่นอน</span>
              </td>
              <td class="p-4 text-cyan-400 font-bold">
                ⚡ แผนสำรองที่ดีเยี่ยม<br/>
                <span class="text-xs font-normal text-slate-400">ทำง่ายสุด หากเวลากระชั้นชิดมาก</span>
              </td>
              <td class="p-4 text-rose-400 font-bold">
                ⚠️ ไม่แนะนำสำหรับเฟสนี้<br/>
                <span class="text-xs font-normal text-slate-400">เหมาะกับวิทยานิพนธ์ระยะยาว ไม่เหมาะกับ 48 ชม.</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Sample Output Preview: What Teachers Will Receive -->
    <section class="p-8 rounded-3xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-xl space-y-6">
      <div>
        <span class="text-xs font-mono text-zoo-gold font-bold">OUTPUT DESIGN SPECIFICATION</span>
        <h3 class="text-2xl font-bold text-slate-900 dark:text-white">ตัวอย่างผลลัพธ์ที่จะส่งให้อาจารย์ (Deliverables Preview)</h3>
      </div>

      <!-- Two Column Layout: Table and Visualization Mockup -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        <!-- Part A: The Active / Inactive CSV Event Table -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <h4 class="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <i data-lucide="file-spreadsheet" class="w-5 h-5 text-emerald-400"></i> ตารางบันทึกพฤติกรรม (Behavior Event Log)
            </h4>
            <span class="text-xs font-mono text-emerald-400">daily_behavior_log.csv</span>
          </div>

          <div class="overflow-x-auto rounded-xl border border-slate-200 dark:border-zoo-cardborder bg-slate-900 text-xs font-mono">
            <table class="w-full text-left">
              <thead>
                <tr class="bg-slate-800 text-slate-400 border-b border-slate-700">
                  <th class="p-2.5">Event ID</th>
                  <th class="p-2.5">Time Range</th>
                  <th class="p-2.5">Room</th>
                  <th class="p-2.5">Macro State</th>
                  <th class="p-2.5">Behavior</th>
                  <th class="p-2.5">Dur(s)</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-800 text-slate-300">
                <tr>
                  <td class="p-2.5 text-zoo-gold">EVT-001</td>
                  <td class="p-2.5">11:07:30 - 11:09:12</td>
                  <td class="p-2.5">Room 2</td>
                  <td class="p-2.5 text-emerald-400 font-bold">ACTIVE</td>
                  <td class="p-2.5">Locomotion</td>
                  <td class="p-2.5">102 s</td>
                </tr>
                <tr>
                  <td class="p-2.5 text-zoo-gold">EVT-002</td>
                  <td class="p-2.5">11:09:40 - 11:14:25</td>
                  <td class="p-2.5">Room 2</td>
                  <td class="p-2.5 text-emerald-400 font-bold">ACTIVE</td>
                  <td class="p-2.5">Eating</td>
                  <td class="p-2.5">285 s</td>
                </tr>
                <tr>
                  <td class="p-2.5 text-zoo-gold">EVT-003</td>
                  <td class="p-2.5">11:15:00 - 11:15:45</td>
                  <td class="p-2.5">R2 ➔ R3</td>
                  <td class="p-2.5 text-emerald-400 font-bold">ACTIVE</td>
                  <td class="p-2.5">Transit</td>
                  <td class="p-2.5">45 s</td>
                </tr>
                <tr>
                  <td class="p-2.5 text-zoo-gold">EVT-004</td>
                  <td class="p-2.5">11:17:10 - 12:20:00</td>
                  <td class="p-2.5">Room 3</td>
                  <td class="p-2.5 text-amber-400 font-bold">INACTIVE</td>
                  <td class="p-2.5">Resting</td>
                  <td class="p-2.5">3,770 s</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p class="text-xs text-slate-500">
            * สอดคล้องกับแบบฟอร์ม Observation Checklist ของสวนสัตว์ สามารถเปิดใน Microsoft Excel หรือ Pandas ได้ทันที
          </p>
        </div>

        <!-- Part B: Visualization / Activity Budget -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <h4 class="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <i data-lucide="pie-chart" class="w-5 h-5 text-zoo-gold"></i> การแสดงผลทางภาพ (Activity Budget Visualization)
            </h4>
            <span class="text-xs font-mono text-zoo-gold">vet_activity_report.png</span>
          </div>

          <div class="p-5 rounded-xl border border-slate-200 dark:border-zoo-cardborder bg-slate-900 space-y-4">
            <!-- Progress Bar Visualization -->
            <div>
              <div class="flex justify-between text-xs font-mono mb-1 text-slate-300">
                <span class="text-emerald-400 font-bold">ACTIVE: 38.5% (เดิน, กิน)</span>
                <span class="text-amber-400 font-bold">INACTIVE: 61.5% (นอนพัก)</span>
              </div>
              <div class="w-full h-4 rounded-full bg-slate-800 overflow-hidden flex">
                <div class="bg-emerald-500 h-full" style="width: 38.5%"></div>
                <div class="bg-amber-500 h-full" style="width: 61.5%"></div>
              </div>
            </div>

            <!-- Behavioral Breakdown Chips -->
            <div class="grid grid-cols-3 gap-2 text-center text-xs">
              <div class="p-2.5 rounded-lg bg-slate-800/80 border border-slate-700">
                <div class="text-slate-400">Locomotion</div>
                <div class="text-sm font-bold text-emerald-400 font-mono">1.8 ชม.</div>
              </div>
              <div class="p-2.5 rounded-lg bg-slate-800/80 border border-slate-700">
                <div class="text-slate-400">Eating</div>
                <div class="text-sm font-bold text-cyan-400 font-mono">0.6 ชม.</div>
              </div>
              <div class="p-2.5 rounded-lg bg-slate-800/80 border border-slate-700">
                <div class="text-slate-400">Resting</div>
                <div class="text-sm font-bold text-amber-400 font-mono">3.8 ชม.</div>
              </div>
            </div>
          </div>
          <p class="text-xs text-slate-500">
            * สัตวแพทย์สามารถตรวจเช็กพฤติกรรมผิดปกติ เช่น หากชะมดนอนเกิน 85% หรือไม่ยอมลุกมากินอาหาร ระบบจะ Flag แจ้งเตือน
          </p>
        </div>

      </div>
    </section>

    <!-- Execution Roadmap: Next Steps to Complete by 31 Oct -->
    <section class="p-8 rounded-3xl bg-gradient-to-r from-zoo-teal/30 via-zoo-surface to-zoo-carddark border border-zoo-gold/30 shadow-2xl space-y-6">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-zoo-gold text-zoo-darkbg flex items-center justify-center font-bold">
          <i data-lucide="rocket" class="w-6 h-6"></i>
        </div>
        <div>
          <h3 class="text-2xl font-bold text-white">ขั้นตอนการลงมือทำทันที (Immediate Action Plan)</h3>
          <p class="text-sm text-zoo-gold">แนวทาง Option 1 ผสมผสานจุดแข็ง Phase 1 (ใช้เวลา 1.5 ชม.)</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
        <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-1.5">
          <span class="px-2 py-0.5 rounded bg-zoo-gold/20 text-zoo-gold font-mono font-bold">STEP 01</span>
          <div class="font-bold text-white text-sm">สกัดเฟรมตัวแทน 150 ภาพ</div>
          <p class="text-slate-400">ดึงเฉพาะช่วงที่มีชะมดจาก Cam 2 (กิน/เดิน) และ Cam 3 (นอน) ตัดช่วงกรงเปล่าทิ้ง</p>
        </div>

        <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-1.5">
          <span class="px-2 py-0.5 rounded bg-zoo-gold/20 text-zoo-gold font-mono font-bold">STEP 02</span>
          <div class="font-bold text-white text-sm">Auto-Label & Roboflow</div>
          <p class="text-slate-400">ใช้สคริปต์วาดกล่องอัตโนมัติ อัปโหลดขึ้น Roboflow ได้ Public Annotation Link ทันที</p>
        </div>

        <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-1.5">
          <span class="px-2 py-0.5 rounded bg-zoo-gold/20 text-zoo-gold font-mono font-bold">STEP 03</span>
          <div class="font-bold text-white text-sm">เทรน YOLOv8n บน GPU</div>
          <p class="text-slate-400">รันเทรน 30 epochs บน RTX 3050 ในเครื่อง ใช้เวลา ~10 นาที ได้ไฟล์ best.pt</p>
        </div>

        <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-1.5">
          <span class="px-2 py-0.5 rounded bg-zoo-gold/20 text-zoo-gold font-mono font-bold">STEP 04</span>
          <div class="font-bold text-white text-sm">ออกตาราง & สไลด์ส่งงาน</div>
          <p class="text-slate-400">รันวิดีโอกล้องจริง สร้างไฟล์ตาราง CSV, กราฟ Activity Budget และอัปเดตสไลด์นำเสนอ</p>
        </div>
      </div>
    </section>

  </main>

  <footer class="border-t border-slate-200 dark:border-zoo-cardborder py-8 text-center text-xs text-slate-500 font-mono">
    Chiang Mai Zoo x CMU Computer Vision Project | Phase 2 Architectural Blueprint & Options Matrix
  </footer>

  <script>
    lucide.createIcons();
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.addEventListener('click', () => {
      document.documentElement.classList.toggle('dark');
      lucide.createIcons();
    });
  </script>
</body>
</html>
"""

with open(out_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully updated HTML: {out_path}")
print(f"File size: {os.path.getsize(out_path) / 1024:.1f} KB")
