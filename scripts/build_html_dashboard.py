import os
import io
import base64
from PIL import Image

def get_base64_image(file_path, max_width=1600, quality=82):
    if not os.path.exists(file_path):
        print(f"Warning: File not found {file_path}")
        return ""
    try:
        im = Image.open(file_path)
        if im.mode in ('RGBA', 'P'):
            im = im.convert('RGB')
        if im.width > max_width:
            h = int(im.height * (max_width / im.width))
            im = im.resize((max_width, h), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format='JPEG', quality=quality, optimize=True)
        b64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
        size_kb = len(buf.getvalue()) / 1024.0
        print(f"Encoded {os.path.basename(file_path)}: {im.size[0]}x{im.size[1]} ({size_kb:.1f} KB)")
        return f"data:image/jpeg;base64,{b64_str}"
    except Exception as e:
        print(f"Error encoding {file_path}: {e}")
        return ""

def generate_dashboard():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    desktop_dir = r"C:\Users\ASUS\Desktop\html knowledge file"
    os.makedirs(desktop_dir, exist_ok=True)
    out_html_path = os.path.join(desktop_dir, "civet-behavior-vision-system-dashboard.html")

    print(f"Processing images from {project_root}...")
    img_pipeline = get_base64_image(os.path.join(project_root, "pic", "flowcharts", "civet_dataflow_pipeline.jpg"))
    img_locomotion = get_base64_image(os.path.join(project_root, "pic", "tracking_results", "locomotion_tracking_result.png"))
    img_eating = get_base64_image(os.path.join(project_root, "pic", "tracking_results", "eating_tracking_result.png"))
    img_resting = get_base64_image(os.path.join(project_root, "pic", "tracking_results", "resting_tracking_result.png"))

    print("Generating comprehensive HTML dashboard...")

    html_content = f'''<!DOCTYPE html>
<html lang="th" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chiang Mai Zoo × CMU | Automated Civet Behavior Monitoring System — Complete Project Knowledge Dashboard</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            zoo: {{
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
            }}
          }},
          fontFamily: {{
            sans: ['"TH Sarabun New"', 'THSarabunNew', 'Sarabun', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'Fira Code', 'Consolas', 'monospace']
          }}
        }}
      }}
    }}
  </script>

  <!-- Google Fonts: Sarabun & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Sarabun:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&display=swap" rel="stylesheet">
  
  <!-- Lucide Icons CDN -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <style>
    @font-face {{
      font-family: 'TH Sarabun New';
      src: local('TH Sarabun New'), local('THSarabunNew'), local('TH SarabunPSK'),
           url('https://cdn.jsdelivr.net/npm/font-th-sarabun-new@1.0.0/fonts/THSarabunNew-webfont.woff') format('woff');
      font-weight: 100 400;
    }}
    @font-face {{
      font-family: 'TH Sarabun New';
      src: local('TH Sarabun New Bold'), local('THSarabunNew-Bold'), local('TH SarabunPSK Bold'),
           url('https://cdn.jsdelivr.net/npm/font-th-sarabun-new@1.0.0/fonts/THSarabunNew_bold-webfont.woff') format('woff');
      font-weight: 500 900;
    }}
    
    body {{
      font-family: 'Sarabun', 'TH Sarabun New', sans-serif;
      font-size: 16px;
      line-height: 1.6;
    }}

    .code-font {{
      font-family: 'JetBrains Mono', monospace;
    }}

    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
      width: 8px;
      height: 8px;
    }}
    ::-webkit-scrollbar-track {{
      background: #0B1318;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #1B4958;
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #E5A93C;
    }}

    .glass-card {{
      background: rgba(19, 33, 40, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(42, 102, 122, 0.35);
    }}

    .gold-glow {{
      box-shadow: 0 0 25px -5px rgba(229, 169, 60, 0.3);
    }}
    .teal-glow {{
      box-shadow: 0 0 25px -5px rgba(27, 73, 88, 0.5);
    }}
  </style>
</head>
<body class="bg-slate-50 dark:bg-zoo-darkbg text-slate-800 dark:text-slate-100 transition-colors duration-300 antialiased selection:bg-zoo-gold selection:text-zoo-darkbg">

  <!-- Reading Progress Bar -->
  <div id="progress-bar" class="fixed top-0 left-0 h-1 bg-gradient-to-r from-zoo-teal via-zoo-gold to-amber-300 z-50 w-0 transition-all duration-100"></div>

  <!-- Header Navigation -->
  <header class="sticky top-0 z-40 bg-white/90 dark:bg-zoo-darkbg/90 backdrop-blur-md border-b border-slate-200 dark:border-zoo-cardborder transition-colors">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-zoo-teal to-zoo-tealdark flex items-center justify-center border border-zoo-gold/40 shadow-md">
          <i data-lucide="eye" class="w-6 h-6 text-zoo-gold"></i>
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <span class="px-2 py-0.5 rounded text-xs font-bold bg-zoo-gold/20 text-zoo-gold border border-zoo-gold/40">PHASE 1 COMPLETE</span>
            <span class="text-xs text-slate-500 dark:text-slate-400 font-mono">CMZ × CMU 2026</span>
          </div>
          <h1 class="text-xl font-bold tracking-tight text-zoo-teal dark:text-white flex items-center gap-2">
            Automated Civet Behavior Monitoring System
          </h1>
        </div>
      </div>

      <!-- Nav Links -->
      <nav class="hidden xl:flex items-center space-x-6 text-sm font-medium">
        <a href="#overview" class="text-slate-600 dark:text-slate-300 hover:text-zoo-gold transition-colors">ภาพรวม</a>
        <a href="#ethogram" class="text-slate-600 dark:text-slate-300 hover:text-zoo-gold transition-colors">พฤติกรรม & Checklist</a>
        <a href="#algorithms" class="text-slate-600 dark:text-slate-300 hover:text-zoo-gold transition-colors">อัลกอริทึม & สูตร</a>
        <a href="#pipeline" class="text-slate-600 dark:text-slate-300 hover:text-zoo-gold transition-colors">9-Step Pipeline</a>
        <a href="#simulator" class="text-slate-600 dark:text-slate-300 hover:text-zoo-gold transition-colors">Simulator</a>
        <a href="#evidence" class="text-slate-600 dark:text-slate-300 hover:text-zoo-gold transition-colors">ผลทดสอบ 22 คลิป</a>
        <a href="#datamodel" class="text-slate-600 dark:text-slate-300 hover:text-zoo-gold transition-colors">Data Model</a>
        <a href="#comparison" class="text-slate-600 dark:text-slate-300 hover:text-zoo-gold transition-colors">Baseline vs YOLO</a>
      </nav>

      <!-- Actions -->
      <div class="flex items-center space-x-3">
        <button id="theme-toggle" class="p-2.5 rounded-lg border border-slate-300 dark:border-zoo-cardborder bg-slate-100 dark:bg-zoo-carddark text-slate-700 dark:text-zoo-gold hover:border-zoo-gold transition-all" title="สลับโหมดสว่าง/มืด">
          <i data-lucide="moon" id="moon-icon" class="w-5 h-5 hidden dark:block"></i>
          <i data-lucide="sun" id="sun-icon" class="w-5 h-5 block dark:hidden"></i>
        </button>
        <a href="#summary" class="inline-flex items-center px-4 py-2 text-sm font-semibold rounded-lg bg-zoo-gold hover:bg-zoo-golddark text-zoo-darkbg transition-colors shadow-sm">
          <i data-lucide="award" class="w-4 h-4 mr-2"></i> สรุปผลงาน Phase 1
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="relative overflow-hidden pt-12 pb-20 border-b border-slate-200 dark:border-zoo-cardborder bg-gradient-to-b from-slate-100 via-white to-slate-50 dark:from-zoo-darkbg dark:via-zoo-carddark/60 dark:to-zoo-darkbg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        
        <div class="lg:col-span-7 space-y-6">
          <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-zoo-teal/10 dark:bg-zoo-teal/30 border border-zoo-teal/30 text-zoo-teal dark:text-zoo-gold text-xs font-semibold uppercase tracking-wider">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            Chiang Mai Zoo Computer Vision Project
          </div>
          <h1 class="text-4xl sm:text-5xl font-extrabold text-slate-900 dark:text-white leading-tight">
            ระบบตรวจจับและวิเคราะห์พฤติกรรม<br>
            <span class="bg-gradient-to-r from-zoo-gold via-amber-400 to-yellow-500 bg-clip-text text-transparent">ชะมดแปลงลายแถบอัตโนมัติ</span> 24 ชั่วโมง
          </h1>
          <p class="text-lg text-slate-600 dark:text-slate-300 leading-relaxed">
            เปลี่ยนกล้องวงจรปิด CCTV 4 ตัวในกรงสวนสัตว์เชียงใหม่ให้เป็นผู้ช่วยสัตวแพทย์อัจฉริยะ ตรวจจับ 3 พฤติกรรมหลัก (เดิน, กิน, นอน) อย่างแม่นยำ 100% ประหยัดพลังงาน 85% ด้วยการวิเคราะห์ที่ 2 FPS รันบนคอมพิวเตอร์สำนักงานทั่วไปโดยไม่ต้องพึ่งพา GPU ราคาแพง
          </p>

          <!-- Key Highlights Badges -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4">
            <div class="p-3.5 rounded-xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder text-center shadow-sm">
              <div class="text-2xl font-black text-zoo-gold">4 ห้อง</div>
              <div class="text-xs text-slate-500 dark:text-slate-400 font-medium mt-0.5">เชื่อมต่อแบบเส้นตรง</div>
            </div>
            <div class="p-3.5 rounded-xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder text-center shadow-sm">
              <div class="text-2xl font-black text-emerald-500">2 FPS</div>
              <div class="text-xs text-slate-500 dark:text-slate-400 font-medium mt-0.5">ประหยัดพลังงาน 85%</div>
            </div>
            <div class="p-3.5 rounded-xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder text-center shadow-sm">
              <div class="text-2xl font-black text-sky-400">22 วิดีโอ</div>
              <div class="text-xs text-slate-500 dark:text-slate-400 font-medium mt-0.5">ทดสอบคลิปจริง 100%</div>
            </div>
            <div class="p-3.5 rounded-xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder text-center shadow-sm">
              <div class="text-2xl font-black text-purple-400">กฎ 1 นาที</div>
              <div class="text-xs text-slate-500 dark:text-slate-400 font-medium mt-0.5">แยกหลับ vs ยืนนิ่ง</div>
            </div>
          </div>
        </div>

        <!-- Hero Diagram Card -->
        <div class="lg:col-span-5">
          <div class="relative rounded-2xl p-1 bg-gradient-to-tr from-zoo-teal via-zoo-gold/40 to-zoo-teal p-1 rounded-2xl shadow-2xl">
            <div class="rounded-xl overflow-hidden bg-zoo-carddark p-4 border border-zoo-cardborder">
              <div class="flex items-center justify-between pb-3 border-b border-zoo-cardborder mb-3 text-xs">
                <span class="font-mono text-zoo-gold flex items-center gap-1.5 font-bold">
                  <i data-lucide="activity" class="w-4 h-4"></i> LIVE SYSTEM ARCHITECTURE
                </span>
                <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 text-[11px] font-mono">1080p Day & Night IR</span>
              </div>
              <img src="{img_pipeline}" alt="Complete Data Flow Pipeline" class="w-full rounded-lg shadow cursor-pointer hover:scale-[1.02] transition-transform duration-300" onclick="openLightbox(this.src, 'Complete 9-Step Data Flow Pipeline Diagram')">
              <div class="mt-3 text-center text-xs text-slate-400 flex items-center justify-center gap-2">
                <i data-lucide="zoom-in" class="w-3.5 h-3.5 text-zoo-gold"></i> คลิกที่รูปเพื่อขยายไดอะแกรมความละเอียดสูง
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- SECTION 1: PROBLEM CONTEXT & ENCLOSURE MAP -->
  <section id="overview" class="py-16 border-b border-slate-200 dark:border-zoo-cardborder">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-3xl mx-auto mb-12">
        <h2 class="text-xs font-bold uppercase tracking-wider text-zoo-gold font-mono mb-2">01. THE ZOO ENCLOSURE & CHALLENGE</h2>
        <h3 class="text-3xl font-bold text-slate-900 dark:text-white">บริบทปัญหาหน้างาน และสภาพแวดล้อมกรงชะมด 4 ห้อง</h3>
        <p class="text-slate-600 dark:text-slate-400 mt-3">
          กรงชะมดแปลงลายแถบ (Large-Spotted Civet) ในสวนสัตว์เชียงใหม่ มีชื่อว่า "หอมป้อม" อาศัยอยู่ตัวเดียวในระบบ 4 ห้องเชื่อมต่อกัน
        </p>
      </div>

      <!-- 3 Real World Pain Points -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder hover:border-zoo-gold/50 transition-all shadow-sm">
          <div class="w-12 h-12 rounded-xl bg-amber-500/10 text-zoo-gold flex items-center justify-center mb-4">
            <i data-lucide="clock" class="w-6 h-6"></i>
          </div>
          <h4 class="text-lg font-bold text-slate-900 dark:text-white mb-2">1. เสียเวลาเฝ้าจอนับชั่วโมง</h4>
          <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
            เจ้าหน้าที่ต้องกรอย้อนดูเทปวงจรปิด 4 หน้าจอย้อนหลังวันละหลายชั่วโมง จดบันทึกลงกระดาษ เสียเวลาดูแลสัตว์โดยตรง และข้อมูลไม่เป็นดิจิทัล
          </p>
        </div>

        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder hover:border-zoo-gold/50 transition-all shadow-sm">
          <div class="w-12 h-12 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center mb-4">
            <i data-lucide="moon" class="w-6 h-6"></i>
          </div>
          <h4 class="text-lg font-bold text-slate-900 dark:text-white mb-2">2. สัตว์ออกหากินกลางคืน (Nocturnal)</h4>
          <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
            กิจกรรม 80% เกิดขึ้นในความมืดสนิท กล้องวงจรปิดตัดเป็นโหมดอินฟราเรด (Infrared Night) ภาพขาวดำ คอนทราสต์ต่ำ ตาเรืองแสง คนดูล้าและสังเกตยากมาก
          </p>
        </div>

        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder hover:border-zoo-gold/50 transition-all shadow-sm">
          <div class="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-4">
            <i data-lucide="shield-check" class="w-6 h-6"></i>
          </div>
          <h4 class="text-lg font-bold text-slate-900 dark:text-white mb-2">3. คนกะพริบตา คอมพิวเตอร์ไม่พลาด</h4>
          <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
            ชะมดเดินข้ามห้องเฉลี่ยสั้นเพียง 3–13 วินาที หรือกินน้ำ 10 วินาที คนเผลอละสายตาจะพลาดทันที ระบบคอมพิวเตอร์วิทัศน์เฝ้าต่อเนื่อง 24/7 ไม่เหนื่อยล้า
          </p>
        </div>
      </div>

      <!-- Interactive 4-Room Enclosure Visualizer -->
      <div class="rounded-2xl p-6 bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-lg">
        <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 mb-6 border-b border-slate-200 dark:border-zoo-cardborder gap-4">
          <div>
            <h4 class="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <i data-lucide="map-pin" class="w-5 h-5 text-zoo-gold"></i> ผังกรง 4 ห้องและตำแหน่งกล้องวงจรปิด (Physical Setup)
            </h4>
            <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">คลิกที่แต่ละห้องเพื่อดูตำแหน่งกล้อง, พื้นที่ ROI พิเศษ, และพฤติกรรมหลัก</p>
          </div>
          <div class="flex items-center gap-2 text-xs font-mono">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded bg-zoo-teal/20 text-zoo-teal dark:text-zoo-gold border border-zoo-teal/30">
              <i data-lucide="video" class="w-3.5 h-3.5"></i> 4 Fixed CCTV Cameras (1080p)
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" id="room-cards">
          <!-- Room 1 -->
          <div onclick="selectRoom(1)" class="room-card cursor-pointer p-5 rounded-xl border border-slate-200 dark:border-zoo-cardborder bg-slate-50 dark:bg-zoo-surface hover:border-zoo-gold transition-all" id="room-card-1">
            <div class="flex items-center justify-between mb-3">
              <span class="px-2.5 py-1 rounded text-xs font-bold bg-slate-200 dark:bg-zoo-carddark text-slate-700 dark:text-slate-300 font-mono">ROOM 01</span>
              <span class="text-xs text-slate-400">Cam 01</span>
            </div>
            <h5 class="font-bold text-slate-900 dark:text-white text-base mb-1">ทางผ่าน & ระเบียง</h5>
            <p class="text-xs text-slate-500 dark:text-slate-400 mb-3">ห้องทางเข้าแรก เชื่อมต่อไปยังห้อง 2</p>
            <div class="text-xs font-mono text-zoo-teal dark:text-zoo-gold">Target: เดินผ่าน (Transit)</div>
          </div>

          <!-- Room 2 -->
          <div onclick="selectRoom(2)" class="room-card cursor-pointer p-5 rounded-xl border-2 border-zoo-gold bg-zoo-gold/10 dark:bg-zoo-surface hover:border-zoo-gold transition-all shadow-md" id="room-card-2">
            <div class="flex items-center justify-between mb-3">
              <span class="px-2.5 py-1 rounded text-xs font-bold bg-zoo-gold text-zoo-darkbg font-mono font-black">ROOM 02</span>
              <span class="text-xs text-zoo-gold font-bold">Cam 02 (Day & Night)</span>
            </div>
            <h5 class="font-bold text-slate-900 dark:text-white text-base mb-1">ห้องอาหาร (Dining Area)</h5>
            <p class="text-xs text-slate-500 dark:text-slate-400 mb-3">วางถาดอาหารและน้ำถาวรที่พื้นกลางล่าง</p>
            <div class="text-xs font-mono text-emerald-400 font-semibold flex items-center gap-1">
              <i data-lucide="utensils" class="w-3.5 h-3.5"></i> Food Tray ROI (960,740-1340,1060)
            </div>
          </div>

          <!-- Room 3 -->
          <div onclick="selectRoom(3)" class="room-card cursor-pointer p-5 rounded-xl border border-slate-200 dark:border-zoo-cardborder bg-slate-50 dark:bg-zoo-surface hover:border-zoo-gold transition-all" id="room-card-3">
            <div class="flex items-center justify-between mb-3">
              <span class="px-2.5 py-1 rounded text-xs font-bold bg-slate-200 dark:bg-zoo-carddark text-slate-700 dark:text-slate-300 font-mono">ROOM 03</span>
              <span class="text-xs text-sky-400 font-bold">Cam 03 (Night IR)</span>
            </div>
            <h5 class="font-bold text-slate-900 dark:text-white text-base mb-1">ห้องนอน (Bedroom / Playground)</h5>
            <p class="text-xs text-slate-500 dark:text-slate-400 mb-3">มีขอนไม้ปีนป่าย และที่นอนยางรถยนต์ปูฟาง</p>
            <div class="text-xs font-mono text-sky-400 font-semibold flex items-center gap-1">
              <i data-lucide="bed" class="w-3.5 h-3.5"></i> Tire Bed ROI (820,130-1180,420)
            </div>
          </div>

          <!-- Room 4 -->
          <div onclick="selectRoom(4)" class="room-card cursor-pointer p-5 rounded-xl border border-slate-200 dark:border-zoo-cardborder bg-slate-50 dark:bg-zoo-surface hover:border-zoo-gold transition-all" id="room-card-4">
            <div class="flex items-center justify-between mb-3">
              <span class="px-2.5 py-1 rounded text-xs font-bold bg-slate-200 dark:bg-zoo-carddark text-slate-700 dark:text-slate-300 font-mono">ROOM 04</span>
              <span class="text-xs text-slate-400">Cam 04</span>
            </div>
            <h5 class="font-bold text-slate-900 dark:text-white text-base mb-1">ห้องพักด้านในสุด</h5>
            <p class="text-xs text-slate-500 dark:text-slate-400 mb-3">พื้นที่ส่วนตัวด้านใน เชื่อมต่อห้อง 3</p>
            <div class="text-xs font-mono text-zoo-teal dark:text-zoo-gold">Target: เดิน / ซ่อนตัว</div>
          </div>
        </div>

        <!-- Room Detail Display Box -->
        <div id="room-detail-box" class="mt-6 p-4 rounded-xl bg-slate-100 dark:bg-zoo-darkbg border border-slate-300 dark:border-zoo-cardborder text-sm">
          <span class="font-bold text-zoo-gold">ห้อง 2 (Camera 02):</span> เป็นจุดสำคัญที่สุดในการบันทึกพฤติกรรมการกินอาหาร กล้องถูกยึดถาวรมุมสูงมองเห็นถาดอาหารทั้งสองถาดชัดเจน ระบบมีการ Mark โซน ROI รอบถาดอาหารขนาด 380×320 พิกเซล และสร้าง Plant Mask ตรงกลางภาพเพื่อตัดสัญญาณรบกวนจากกระถางต้นไม้
        </div>
      </div>

    </div>
  </section>

  <!-- SECTION 2: ETHOGRAM & OBSERVATION CHECKLIST -->
  <section id="ethogram" class="py-16 border-b border-slate-200 dark:border-zoo-cardborder bg-slate-50/50 dark:bg-zoo-darkbg/50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-3xl mx-auto mb-12">
        <h2 class="text-xs font-bold uppercase tracking-wider text-zoo-gold font-mono mb-2">02. ETHOGRAM & CHECKLIST DESIGN</h2>
        <h3 class="text-3xl font-bold text-slate-900 dark:text-white">นิยามพฤติกรรมสัตว์ และการแยกสภาวะการสังเกต</h3>
        <p class="text-slate-600 dark:text-slate-400 mt-3">
          การจัดหมวดหมู่อย่างเป็นระบบตามมาตรฐาน Ethogram 8 พฤติกรรมของสวนสัตว์ และการแยกแยะระหว่างสิ่งที่สัตว์ทำ vs สภาพของกล้อง
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-12">
        
        <!-- Behavior vs Conditions Card -->
        <div class="lg:col-span-5 p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-sm flex flex-col justify-between">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded bg-amber-500/10 text-amber-500 text-xs font-mono font-bold mb-4">
              <i data-lucide="alert-circle" class="w-4 h-4"></i> OBJECTIVE 2: STRICT SEPARATION
            </div>
            <h4 class="text-xl font-bold text-slate-900 dark:text-white mb-3">Animal Behavior vs Observation Conditions</h4>
            <p class="text-sm text-slate-600 dark:text-slate-400 leading-relaxed mb-4">
              ตามโจทย์ของสวนสัตว์ เราต้อง <strong class="text-zoo-gold">ไม่นำข้อจำกัดของกล้องไปปนกับพฤติกรรมของสัตว์</strong>:
            </p>

            <div class="space-y-3">
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
                <div class="text-xs font-bold text-emerald-500 dark:text-emerald-400 uppercase tracking-wider mb-1">🐾 Animal Behavior (สัตว์กำลังทำอะไร)</div>
                <div class="text-sm text-slate-700 dark:text-slate-200 font-medium">Walking / Climbing (เดิน/ปีนป่าย), Resting (นอนหลับพักผ่อน), Eating (กินอาหาร/ดื่มน้ำ)</div>
              </div>

              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
                <div class="text-xs font-bold text-sky-500 dark:text-sky-400 uppercase tracking-wider mb-1">📹 Observation Conditions (ภาพในกล้องเป็นอย่างไร)</div>
                <div class="text-sm text-slate-700 dark:text-slate-200 font-medium">Day Color, Night IR, แสงน้อย (Low Light), ตาเรืองแสง, บดบังด้วยต้นไม้/ลูกกรง, เดินหลุดเฟรมระหว่างห้อง</div>
              </div>
            </div>
          </div>

          <div class="mt-4 p-3.5 rounded-xl bg-zoo-teal/20 border border-zoo-teal/40 text-xs text-slate-300">
            <span class="font-bold text-zoo-gold">กฎเหล็กของระบบ:</span> หากเกิดกรณีภาพมืดหรือถูกต้นไม้บังจนมองไม่เห็นตัวชะมด ระบบจะบันทึกสถานะพฤติกรรมเป็น <code>Unknown</code> แทนการเดาผิด
          </div>
        </div>

        <!-- Official Ethogram Table -->
        <div class="lg:col-span-7 p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-sm">
          <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-zoo-cardborder mb-4">
            <h4 class="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <i data-lucide="clipboard-list" class="w-5 h-5 text-zoo-gold"></i> ตารางเปรียบเทียบ Ethogram 8 พฤติกรรม
            </h4>
            <span class="text-xs font-mono text-slate-400">Chiang Mai Zoo Catalog</span>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-100 dark:bg-zoo-surface text-slate-700 dark:text-slate-300 uppercase font-mono">
                <tr>
                  <th class="py-2.5 px-3 rounded-l">พฤติกรรม (Ethogram)</th>
                  <th class="py-2.5 px-3">หมวดหมู่</th>
                  <th class="py-2.5 px-3">มีในคลิปทดสอบ?</th>
                  <th class="py-2.5 px-3 rounded-r">การประมวลผล Phase 1</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 dark:divide-zoo-cardborder text-slate-600 dark:text-slate-300">
                <tr class="hover:bg-slate-50 dark:hover:bg-zoo-surface/50">
                  <td class="py-2.5 px-3 font-semibold text-slate-900 dark:text-white">1. นอนหลับ พักผ่อน นั่ง ยืนนิ่ง</td>
                  <td class="py-2.5 px-3"><span class="px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 font-mono">Inactive</span></td>
                  <td class="py-2.5 px-3 text-emerald-400 font-bold">มี (7 คลิป)</td>
                  <td class="py-2.5 px-3 font-mono text-emerald-400">ตรวจจับเป็น Resting</td>
                </tr>
                <tr class="hover:bg-slate-50 dark:hover:bg-zoo-surface/50">
                  <td class="py-2.5 px-3 font-semibold text-slate-900 dark:text-white">2. เดิน ก้าวขา วิ่ง ปีนป่าย</td>
                  <td class="py-2.5 px-3"><span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 font-mono">Active</span></td>
                  <td class="py-2.5 px-3 text-emerald-400 font-bold">มี (10 คลิป)</td>
                  <td class="py-2.5 px-3 font-mono text-emerald-400">ตรวจจับเป็น Walking</td>
                </tr>
                <tr class="hover:bg-slate-50 dark:hover:bg-zoo-surface/50">
                  <td class="py-2.5 px-3 font-semibold text-slate-900 dark:text-white">3. กินอาหาร กินน้ำ ดื่มน้ำ</td>
                  <td class="py-2.5 px-3"><span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 font-mono">Active</span></td>
                  <td class="py-2.5 px-3 text-emerald-400 font-bold">มี (5 คลิป)</td>
                  <td class="py-2.5 px-3 font-mono text-emerald-400">ตรวจจับเป็น Eating</td>
                </tr>
                <tr class="hover:bg-slate-50 dark:hover:bg-zoo-surface/50 text-slate-400">
                  <td class="py-2 px-3">4. ขับถ่ายปัสสาวะ</td>
                  <td class="py-2 px-3 font-mono">Active</td>
                  <td class="py-2 px-3 text-slate-500">ไม่มีในคลิป</td>
                  <td class="py-2 px-3 font-mono text-slate-400">บันทึกเป็น Unknown</td>
                </tr>
                <tr class="hover:bg-slate-50 dark:hover:bg-zoo-surface/50 text-slate-400">
                  <td class="py-2 px-3">5. ขับถ่ายอุจจาระ</td>
                  <td class="py-2 px-3 font-mono">Active</td>
                  <td class="py-2 px-3 text-slate-500">ไม่มีในคลิป</td>
                  <td class="py-2 px-3 font-mono text-slate-400">บันทึกเป็น Unknown</td>
                </tr>
                <tr class="hover:bg-slate-50 dark:hover:bg-zoo-surface/50 text-slate-400">
                  <td class="py-2 px-3">6. ไซ้ขน แต่งตัว เลียตัว</td>
                  <td class="py-2 px-3 font-mono">Active</td>
                  <td class="py-2 px-3 text-slate-500">ไม่มีในคลิป</td>
                  <td class="py-2 px-3 font-mono text-slate-400">บันทึกเป็น Unknown</td>
                </tr>
                <tr class="hover:bg-slate-50 dark:hover:bg-zoo-surface/50 text-slate-400">
                  <td class="py-2 px-3">7. ถูตัวแสดงอาณาเขต</td>
                  <td class="py-2 px-3 font-mono">Active</td>
                  <td class="py-2 px-3 text-slate-500">ไม่มีในคลิป</td>
                  <td class="py-2 px-3 font-mono text-slate-400">บันทึกเป็น Unknown</td>
                </tr>
                <tr class="hover:bg-slate-50 dark:hover:bg-zoo-surface/50 text-slate-400">
                  <td class="py-2 px-3">8. เดินเคียงคู่กัน</td>
                  <td class="py-2 px-3 font-mono">Active</td>
                  <td class="py-2 px-3 text-slate-500">ไม่มี (อยู่ตัวเดียว)</td>
                  <td class="py-2 px-3 font-mono text-rose-400">Out of Scope (กรงมีตัวเดียว)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- Observation Checklist Card -->
      <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-sm">
        <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-zoo-cardborder mb-4">
          <h4 class="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <i data-lucide="check-square" class="w-5 h-5 text-zoo-gold"></i> Behavior Observation Checklist Schema (แบบฟอร์มบันทึกข้อมูลแบบมีโครงสร้าง)
          </h4>
          <span class="text-xs font-mono text-emerald-400">1 Row = 1 Observation Record</span>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-3 text-xs font-mono">
          <div class="p-3 rounded-lg bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
            <div class="text-slate-400 text-[10px]">FIELD 1</div>
            <div class="font-bold text-zoo-gold">Time</div>
            <div class="text-slate-500 text-[11px] mt-1">2026-10-03 22:14:05</div>
          </div>
          <div class="p-3 rounded-lg bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
            <div class="text-slate-400 text-[10px]">FIELD 2</div>
            <div class="font-bold text-zoo-gold">Camera / Room</div>
            <div class="text-slate-500 text-[11px] mt-1">CAM02 / Room 2</div>
          </div>
          <div class="p-3 rounded-lg bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
            <div class="text-slate-400 text-[10px]">FIELD 3</div>
            <div class="font-bold text-zoo-gold">Animal Visible</div>
            <div class="text-slate-500 text-[11px] mt-1">yes / partial / no</div>
          </div>
          <div class="p-3 rounded-lg bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
            <div class="text-slate-400 text-[10px]">FIELD 4</div>
            <div class="font-bold text-zoo-gold">Behavior</div>
            <div class="text-slate-500 text-[11px] mt-1">walking, resting, eating</div>
          </div>
          <div class="p-3 rounded-lg bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
            <div class="text-slate-400 text-[10px]">FIELD 5</div>
            <div class="font-bold text-zoo-gold">Lighting</div>
            <div class="text-slate-500 text-[11px] mt-1">day colour / night IR</div>
          </div>
          <div class="p-3 rounded-lg bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
            <div class="text-slate-400 text-[10px]">FIELD 6</div>
            <div class="font-bold text-zoo-gold">Occlusion</div>
            <div class="text-slate-500 text-[11px] mt-1">none / plant / fence</div>
          </div>
          <div class="p-3 rounded-lg bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
            <div class="text-slate-400 text-[10px]">FIELD 7</div>
            <div class="font-bold text-zoo-gold">Notes</div>
            <div class="text-slate-500 text-[11px] mt-1">Curling up in tire</div>
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- SECTION 3: VISION ALGORITHMS & MATHEMATICAL DEEP DIVE -->
  <section id="algorithms" class="py-16 border-b border-slate-200 dark:border-zoo-cardborder">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-3xl mx-auto mb-12">
        <h2 class="text-xs font-bold uppercase tracking-wider text-zoo-gold font-mono mb-2">03. MATHEMATICAL & ALGORITHMIC DEEP DIVE</h2>
        <h3 class="text-3xl font-bold text-slate-900 dark:text-white">เจาะลึกอัลกอริทึม Computer Vision และสมการคณิตศาสตร์</h3>
        <p class="text-slate-600 dark:text-slate-400 mt-3">
          การทำงานภายในของระบบตรวจจับแบบโปร่งใส (White-box Baseline) ที่อธิบายได้ทุกขั้นตอน มีสูตรและโค้ดชัดเจน
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        
        <!-- Algorithm 1: Subsampling -->
        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <span class="px-2.5 py-1 rounded bg-amber-500/10 text-zoo-gold text-xs font-mono font-bold">1. TEMPORAL SUBSAMPLING</span>
            <span class="text-xs font-mono text-emerald-400 font-bold">-85% Compute Load</span>
          </div>
          <h4 class="text-lg font-bold text-slate-900 dark:text-white mb-2">ทำไมต้องลดเฟรมเหลือ 2 FPS?</h4>
          <p class="text-sm text-slate-600 dark:text-slate-400 mb-4">
            วิดีโอกล้องวงจรปิดบันทึกที่ 15 FPS (900 เฟรม/นาที) แต่ชะมดเดินข้ามห้องใช้เวลา 3–10 วินาที และกินอาหารนานหลายนาที การคำนวณทุกเฟรมจะทำให้ซีพียูร้อนจัดและเปลืองไฟโดยเปล่าประโยชน์
          </p>

          <div class="p-4 rounded-xl bg-slate-900 text-slate-200 font-mono text-xs space-y-2 mb-4 border border-slate-800">
            <div class="text-slate-400">// คำนวณช่วงการข้ามเฟรม (Sampling Step)</div>
            <div>sample_step = int(round(native_fps / 2.0))  <span class="text-emerald-400"># 15.0 / 2 = 8 frames</span></div>
            <div>if frame_idx % sample_step == 0:</div>
            <div class="pl-4">process_vision_frame(frame) <span class="text-zoo-gold"># ประมวลผลเพียง 120 เฟรม/นาที</span></div>
          </div>

          <div class="text-xs text-slate-500 dark:text-slate-400">
            ✅ <strong>ผลลัพธ์:</strong> ที่ 2 FPS เรายังได้สแน็ปช็อต 6–20 รูปต่อการเดินข้ามห้อง 1 ครั้ง ซึ่งเพียงพอต่อการลากเส้นทางพิกัดได้ครบถ้วน และจับเวลาเริ่ม-จบได้คลาดเคลื่อนไม่เกิน ±0.5 วินาที
          </div>
        </div>

        <!-- Algorithm 2: MOG2 Background Subtraction -->
        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <span class="px-2.5 py-1 rounded bg-sky-500/10 text-sky-400 text-xs font-mono font-bold">2. ADAPTIVE MOG2 VISION</span>
            <span class="text-xs font-mono text-sky-400">Gaussian Mixture Models</span>
          </div>
          <h4 class="text-lg font-bold text-slate-900 dark:text-white mb-2">สมการคณิตศาสตร์แยกพื้นหลัง (MOG2)</h4>
          <p class="text-sm text-slate-600 dark:text-slate-400 mb-3">
            จำลองความเข้มแสงของแต่ละพิกเซลเป็นผลรวมของ $K$ Gaussian Distributions เพื่อปรับตัวตามการเปลี่ยนแสงอัตโนมัติ:
          </p>

          <div class="p-3.5 rounded-xl bg-slate-900 text-center font-mono text-xs text-zoo-gold mb-3 border border-slate-800">
            P(X_t) = ∑ [ w_{{i,t}} * η(X_t, μ_{{i,t}}, Σ_{{i,t}}) ] , i = 1..K
          </div>

          <div class="p-3.5 rounded-xl bg-slate-900 text-slate-200 font-mono text-xs space-y-1 mb-4 border border-slate-800">
            <div class="text-slate-400">// การตั้งค่า OpenCV ในโปรเจกต์จริง</div>
            <div>subtractor = cv2.createBackgroundSubtractorMOG2(</div>
            <div class="pl-4">history=60, varThreshold=20, detectShadows=False</div>
            <div>)</div>
          </div>

          <div class="text-xs text-slate-500 dark:text-slate-400">
            ✅ <strong>จุดเด่น:</strong> เนื่องจากกล้องสวนสัตว์ถูกยึดผนังถาวร พื้นหลังจึงนิ่ง 100% วัตถุที่ขยับได้จึงรับประกันว่าคือ "ตัวชะมด"
          </div>
        </div>

        <!-- Algorithm 3: Centroid & Velocity -->
        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <span class="px-2.5 py-1 rounded bg-purple-500/10 text-purple-400 text-xs font-mono font-bold">3. CENTROID & SPEED VECTOR</span>
            <span class="text-xs font-mono text-purple-400">Euclidean Distance</span>
          </div>
          <h4 class="text-lg font-bold text-slate-900 dark:text-white mb-2">การสกัดจุดกึ่งกลางและความเร็วการเคลื่อนที่</h4>
          <p class="text-sm text-slate-600 dark:text-slate-400 mb-3">
            หา Bounding Box รอบ Contour ชะมดที่มีขนาด Area &gt; 1200 px แล้วคำนวณจุดกึ่งกลาง (C_x, C_y) และความเร็วระหว่างเฟรม:
          </p>

          <div class="p-3.5 rounded-xl bg-slate-900 text-center font-mono text-xs text-purple-300 mb-3 border border-slate-800">
            v_t = √[ (C_{{x,t}} - C_{{x,t-1}})^2 + (C_{{y,t}} - C_{{y,t-1}})^2 ] / Δt  (px/s)
          </div>

          <div class="p-3.5 rounded-xl bg-slate-900 text-slate-200 font-mono text-xs space-y-1 mb-4 border border-slate-800">
            <div>if civet_box is not None:</div>
            <div class="pl-4">x, y, w, h = civet_box</div>
            <div class="pl-4">cx, cy = x + w // 2, y + h // 2</div>
            <div class="pl-4">speed = np.hypot(cx - prev_cx, cy - prev_cy) / dt</div>
          </div>

          <div class="text-xs text-slate-500 dark:text-slate-400">
            ✅ <strong>เกณฑ์ตัดสิน:</strong> ถ้า v_t &gt; 30 px/s ต่อเนื่องกัน &ge; 3 วินาที ถือว่า "เดิน (Walking)" หากความเร็วเป็น 0 ถือว่า "นิ่ง (Stationary)"
          </div>
        </div>

        <!-- Algorithm 4: Spatial ROI & Debounce -->
        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <span class="px-2.5 py-1 rounded bg-emerald-500/10 text-emerald-400 text-xs font-mono font-bold">4. ROI INTERSECTION & DEBOUNCE</span>
            <span class="text-xs font-mono text-emerald-400">State Machine Rules</span>
          </div>
          <h4 class="text-lg font-bold text-slate-900 dark:text-white mb-2">กฎการหน่วงเวลาป้องกันการตรวจจับพลาด</h4>
          <p class="text-sm text-slate-600 dark:text-slate-400 mb-3">
            ป้องกันปัญหาภาพกระพริบ (Sensor Flickering) ด้วย 3 กฎตรรกศาสตร์เวลา (Debounce Rules):
          </p>

          <div class="space-y-2 text-xs">
            <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder flex items-center justify-between">
              <span><strong>กฎการนอน (60s Stillness):</strong> อยู่นิ่งในยางรถยนต์ครบ 60 วินาที</span>
              <span class="text-zoo-gold font-mono font-bold">State: RESTING</span>
            </div>
            <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder flex items-center justify-between">
              <span><strong>กฎการกิน (10s in Tray):</strong> ส่วนหัวอยู่ในถาดอาหารครบ 10 วินาที</span>
              <span class="text-emerald-400 font-mono font-bold">State: EATING</span>
            </div>
            <div class="p-2.5 rounded-lg bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder flex items-center justify-between">
              <span><strong>กฎการตื่น (3s Move):</strong> มีการเคลื่อนที่ต่อเนื่องครบ 3 วินาที</span>
              <span class="text-sky-400 font-mono font-bold">State: ACTIVE</span>
            </div>
          </div>
        </div>

      </div>

    </div>
  </section>

  <!-- SECTION 4: INTERACTIVE 9-STEP PIPELINE STEPPER -->
  <section id="pipeline" class="py-16 border-b border-slate-200 dark:border-zoo-cardborder bg-slate-50/50 dark:bg-zoo-darkbg/50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-3xl mx-auto mb-12">
        <h2 class="text-xs font-bold uppercase tracking-wider text-zoo-gold font-mono mb-2">04. COMPLETE 9-STEP PIPELINE</h2>
        <h3 class="text-3xl font-bold text-slate-900 dark:text-white">สถาปัตยกรรมการไหลของข้อมูล (Interactive Stepper)</h3>
        <p class="text-slate-600 dark:text-slate-400 mt-3">
          คลิกเลือกสเต็ป 1 ถึง 9 ด้านล่างเพื่อดูข้อมูล Input, Algorithm, Output และโค้ด Python ประจำแต่ละสเต็ป
        </p>
      </div>

      <!-- Stepper Buttons Bar -->
      <div class="grid grid-cols-3 sm:grid-cols-5 lg:grid-cols-9 gap-2 mb-8">
        <button onclick="setPipelineStep(1)" class="pipe-btn p-3 rounded-xl border text-center transition-all bg-zoo-gold text-zoo-darkbg border-zoo-gold font-bold shadow-md" id="p-btn-1">
          <div class="text-xs font-mono font-bold">STEP 1</div>
          <div class="text-[13px] truncate font-semibold mt-0.5">Camera Streams</div>
        </button>
        <button onclick="setPipelineStep(2)" class="pipe-btn p-3 rounded-xl border text-center transition-all bg-white dark:bg-zoo-carddark text-slate-600 dark:text-slate-300 border-slate-200 dark:border-zoo-cardborder hover:border-zoo-gold" id="p-btn-2">
          <div class="text-xs font-mono text-slate-400">STEP 2</div>
          <div class="text-[13px] truncate font-semibold mt-0.5">Subsampling</div>
        </button>
        <button onclick="setPipelineStep(3)" class="pipe-btn p-3 rounded-xl border text-center transition-all bg-white dark:bg-zoo-carddark text-slate-600 dark:text-slate-300 border-slate-200 dark:border-zoo-cardborder hover:border-zoo-gold" id="p-btn-3">
          <div class="text-xs font-mono text-slate-400">STEP 3</div>
          <div class="text-[13px] truncate font-semibold mt-0.5">MOG2 Detection</div>
        </button>
        <button onclick="setPipelineStep(4)" class="pipe-btn p-3 rounded-xl border text-center transition-all bg-white dark:bg-zoo-carddark text-slate-600 dark:text-slate-300 border-slate-200 dark:border-zoo-cardborder hover:border-zoo-gold" id="p-btn-4">
          <div class="text-xs font-mono text-slate-400">STEP 4</div>
          <div class="text-[13px] truncate font-semibold mt-0.5">Centroid Track</div>
        </button>
        <button onclick="setPipelineStep(5)" class="pipe-btn p-3 rounded-xl border text-center transition-all bg-white dark:bg-zoo-carddark text-slate-600 dark:text-slate-300 border-slate-200 dark:border-zoo-cardborder hover:border-zoo-gold" id="p-btn-5">
          <div class="text-xs font-mono text-slate-400">STEP 5</div>
          <div class="text-[13px] truncate font-semibold mt-0.5">ROI & Features</div>
        </button>
        <button onclick="setPipelineStep(6)" class="pipe-btn p-3 rounded-xl border text-center transition-all bg-white dark:bg-zoo-carddark text-slate-600 dark:text-slate-300 border-slate-200 dark:border-zoo-cardborder hover:border-zoo-gold" id="p-btn-6">
          <div class="text-xs font-mono text-slate-400">STEP 6</div>
          <div class="text-[13px] truncate font-semibold mt-0.5">Debounce Rules</div>
        </button>
        <button onclick="setPipelineStep(7)" class="pipe-btn p-3 rounded-xl border text-center transition-all bg-white dark:bg-zoo-carddark text-slate-600 dark:text-slate-300 border-slate-200 dark:border-zoo-cardborder hover:border-zoo-gold" id="p-btn-7">
          <div class="text-xs font-mono text-slate-400">STEP 7</div>
          <div class="text-[13px] truncate font-semibold mt-0.5">Event Generator</div>
        </button>
        <button onclick="setPipelineStep(8)" class="pipe-btn p-3 rounded-xl border text-center transition-all bg-white dark:bg-zoo-carddark text-slate-600 dark:text-slate-300 border-slate-200 dark:border-zoo-cardborder hover:border-zoo-gold" id="p-btn-8">
          <div class="text-xs font-mono text-slate-400">STEP 8</div>
          <div class="text-[13px] truncate font-semibold mt-0.5">Data Storage</div>
        </button>
        <button onclick="setPipelineStep(9)" class="pipe-btn p-3 rounded-xl border text-center transition-all bg-white dark:bg-zoo-carddark text-slate-600 dark:text-slate-300 border-slate-200 dark:border-zoo-cardborder hover:border-zoo-gold" id="p-btn-9">
          <div class="text-xs font-mono text-slate-400">STEP 9</div>
          <div class="text-[13px] truncate font-semibold mt-0.5">Visualization</div>
        </button>
      </div>

      <!-- Step Content Display Box -->
      <div class="rounded-2xl p-8 bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-xl">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          <div class="lg:col-span-7 space-y-4">
            <div class="flex items-center gap-3">
              <span id="step-badge" class="px-3 py-1 rounded-full text-xs font-bold font-mono bg-zoo-gold text-zoo-darkbg">STEP 01 OF 09</span>
              <span id="step-tagline" class="text-xs text-slate-500 dark:text-slate-400 font-mono">Input Ingestion Layer</span>
            </div>
            <h4 id="step-title" class="text-2xl font-bold text-slate-900 dark:text-white">Camera Streams (รับภาพสตรีม 4 ตัว 1080p)</h4>
            <p id="step-desc" class="text-slate-600 dark:text-slate-300 text-sm leading-relaxed">
              รับสัญญาณสตรีมวิดีโอ RTSP แบบเรียลไทม์ ความละเอียด Full HD 1080p จากกล้อง CCTV ติดผนังถาวรทั้ง 4 ตัวที่ติดตั้งอยู่ในแต่ละห้อง (Room 1 ถึง Room 4) รองรับทั้งภาพสีในเวลากลางวัน และภาพอินฟราเรดขาวดำในเวลากลางคืน
            </p>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
                <div class="text-xs font-bold text-zoo-gold uppercase tracking-wider mb-1 font-mono">📥 ข้อมูลนำเข้า (INPUT)</div>
                <div id="step-input" class="text-xs text-slate-700 dark:text-slate-300 font-mono">RTSP Stream 1080p @ 15 FPS จากกล้อง 4 ตัว (CAM01-CAM04)</div>
              </div>
              <div class="p-4 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
                <div class="text-xs font-bold text-emerald-500 uppercase tracking-wider mb-1 font-mono">📤 ข้อมูลส่งออก (OUTPUT)</div>
                <div id="step-output" class="text-xs text-slate-700 dark:text-slate-300 font-mono">Raw Video Frames (Bgra/BGR Buffer) ส่งต่อไปยังตัว Subsampler</div>
              </div>
            </div>
          </div>

          <div class="lg:col-span-5">
            <div class="rounded-xl overflow-hidden bg-slate-900 p-4 border border-slate-800">
              <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-800 text-xs font-mono text-slate-400">
                <span class="text-zoo-gold font-bold">PYTHON IMPLEMENTATION</span>
                <span>OpenCV 4.x</span>
              </div>
              <pre class="text-xs text-slate-200 font-mono overflow-x-auto leading-relaxed" id="step-code">
# Step 1: Ingest video stream
cap = cv2.VideoCapture(stream_url)
fps = cap.get(cv2.CAP_PROP_FPS) or 15.0
ret, frame = cap.read()
if ret:
    frame_h, frame_w = frame.shape[:2] # 1080x1920
              </pre>
            </div>
          </div>

        </div>
      </div>

    </div>
  </section>

  <!-- SECTION 5: INTERACTIVE BEHAVIORAL SIMULATOR -->
  <section id="simulator" class="py-16 border-b border-slate-200 dark:border-zoo-cardborder">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-3xl mx-auto mb-12">
        <h2 class="text-xs font-bold uppercase tracking-wider text-zoo-gold font-mono mb-2">05. INTERACTIVE BEHAVIOR SIMULATOR</h2>
        <h3 class="text-3xl font-bold text-slate-900 dark:text-white">วิดเจ็ตจำลองการตัดสินใจของอัลกอริทึม (Interactive Simulator)</h3>
        <p class="text-slate-600 dark:text-slate-400 mt-3">
          ทดลองเลื่อนสไลเดอร์เพื่อดูการทำงานของ "กฎ 1 นาที (1-Minute Rule)" และ "การตรวจจับการกินใน Food ROI" แบบเสมือนจริง
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        <!-- Simulator 1: Sleep Debounce (1-Minute Rule) -->
        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-lg">
          <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-zoo-cardborder mb-4">
            <h4 class="font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <i data-lucide="moon" class="w-5 h-5 text-sky-400"></i> จำลองกฎ 1 นาที: ตัดสินใจว่าชะมดนอนหลับหรือไม่
            </h4>
            <span class="text-xs font-mono text-sky-400 font-bold">1-Min Debounce</span>
          </div>
          
          <p class="text-xs text-slate-500 dark:text-slate-400 mb-6">
            ลากแถบเวลาด้านล่างเพื่อจำลองจำนวนวินาทีที่ชะมดนอนนิ่งอยู่ในยางรถยนต์:
          </p>

          <div class="space-y-4 mb-6">
            <div class="flex items-center justify-between text-sm font-mono">
              <span class="text-slate-600 dark:text-slate-400">เวลานิ่งสะสม (Stillness Seconds):</span>
              <span id="stillness-val" class="text-2xl font-black text-zoo-gold">45 วินาที</span>
            </div>
            <input type="range" min="0" max="90" value="45" id="stillness-slider" class="w-full h-2.5 bg-slate-200 dark:bg-zoo-surface rounded-lg appearance-none cursor-pointer accent-zoo-gold" oninput="updateSleepSim(this.value)">
            <div class="flex justify-between text-[11px] font-mono text-slate-400">
              <span>0s (เพิ่งหยุด)</span>
              <span>30s (ครึ่งนาที)</span>
              <span class="text-zoo-gold font-bold">60s (Threshold ตัดสิน)</span>
              <span>90s (หลับลึก)</span>
            </div>
          </div>

          <!-- Live State Display Badge -->
          <div id="sim-state-box" class="p-5 rounded-xl border text-center transition-all bg-amber-500/10 border-amber-500/40 text-amber-400">
            <div class="text-xs font-mono uppercase tracking-wider">CURRENT STATE CALCULATION</div>
            <div id="sim-state-title" class="text-2xl font-black mt-1">PAUSING / NOT ASLEEP YET (หยุดยืนเฉยๆ)</div>
            <p id="sim-state-desc" class="text-xs mt-1 text-slate-300">
              นิ่งมา 45 วินาที ยังไม่ถึง 60 วินาที ระบบจะยังไม่ลงบันทึกว่านอน เพื่อป้องกันการนับการยืนพักชั่วคราว
            </p>
          </div>
        </div>

        <!-- Simulator 2: Food Tray ROI Proximity -->
        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-lg">
          <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-zoo-cardborder mb-4">
            <h4 class="font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <i data-lucide="utensils" class="w-5 h-5 text-emerald-400"></i> จำลองการตรวจจับการกิน (Food ROI & 10s Rule)
            </h4>
            <span class="text-xs font-mono text-emerald-400 font-bold">Spatial ROI</span>
          </div>

          <p class="text-xs text-slate-500 dark:text-slate-400 mb-6">
            จำลองตำแหน่งส่วนหัวของชะมด และระยะเวลาที่แช่อยู่ในถาดอาหาร:
          </p>

          <div class="space-y-4 mb-6">
            <div class="flex items-center justify-between text-sm font-mono">
              <span class="text-slate-600 dark:text-slate-400">เวลาที่ส่วนหัวอยู่ในถาด (Dwell Time):</span>
              <span id="eat-time-val" class="text-2xl font-black text-emerald-400">14 วินาที</span>
            </div>
            <input type="range" min="0" max="30" value="14" id="eat-slider" class="w-full h-2.5 bg-slate-200 dark:bg-zoo-surface rounded-lg appearance-none cursor-pointer accent-emerald-500" oninput="updateEatSim(this.value)">
            <div class="flex justify-between text-[11px] font-mono text-slate-400">
              <span>0s (เดินเฉียด)</span>
              <span class="text-emerald-400 font-bold">10s (Threshold อาหาร)</span>
              <span>20s (กินต่อเนื่อง)</span>
              <span>30s (มื้อใหญ่)</span>
            </div>
          </div>

          <div id="eat-state-box" class="p-5 rounded-xl border text-center transition-all bg-emerald-500/10 border-emerald-500/40 text-emerald-400">
            <div class="text-xs font-mono uppercase tracking-wider">FOOD CLASSIFIER RESULT</div>
            <div id="eat-state-title" class="text-2xl font-black mt-1">EATING EVENT CONFIRMED (กำลังกินอาหาร)</div>
            <p id="eat-state-desc" class="text-xs mt-1 text-slate-300">
              แช่อยู่ในถาดอาหาร 14 วินาที (> 10s) ถือเป็นมื้ออาหารจริง แยกออกจากการแค่เดินผ่านถาดได้อย่างสมบูรณ์
            </p>
          </div>
        </div>

      </div>

    </div>
  </section>

  <!-- SECTION 6: REAL-WORLD EVIDENCE & 22 VIDEOS EVALUATION -->
  <section id="evidence" class="py-16 border-b border-slate-200 dark:border-zoo-cardborder bg-slate-50/50 dark:bg-zoo-darkbg/50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-3xl mx-auto mb-12">
        <h2 class="text-xs font-bold uppercase tracking-wider text-zoo-gold font-mono mb-2">06. EXPERIMENTAL VALIDATION</h2>
        <h3 class="text-3xl font-bold text-slate-900 dark:text-white">หลักฐานการทดสอบจริงบน 22 วิดีโอ CCTV ของสวนสัตว์</h3>
        <p class="text-slate-600 dark:text-slate-400 mt-3">
          การประเมินผลอย่างเข้มงวดบนชุดข้อมูลวิดีโอ 22 คลิป รวมความยาวกว่า 1,051.8 วินาที (17.5 นาที) ในสภาพแสงจริงทั้งกลางวันและกลางคืน
        </p>
      </div>

      <!-- 22 Videos Dataset Breakdown Table -->
      <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-sm mb-12">
        <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-zoo-cardborder mb-4">
          <h4 class="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <i data-lucide="database" class="w-5 h-5 text-zoo-gold"></i> ตารางสถิติชุดข้อมูล 22 วิดีโอ (Chiang Mai Zoo Dataset)
          </h4>
          <span class="text-xs font-mono text-emerald-400">100% Tracking Precision</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-6">
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder text-center">
            <div class="text-xs text-slate-500 font-mono">การกิน (Eating)</div>
            <div class="text-2xl font-black text-zoo-gold mt-1">5 คลิป</div>
            <div class="text-xs text-slate-400 mt-1">254.4 วินาที (เฉลี่ย 50.9s)</div>
          </div>
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder text-center">
            <div class="text-xs text-slate-500 font-mono">การเดิน (Locomotion)</div>
            <div class="text-2xl font-black text-amber-500 mt-1">10 คลิป</div>
            <div class="text-xs text-slate-400 mt-1">138.7 วินาที (เฉลี่ย 13.9s)</div>
          </div>
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder text-center">
            <div class="text-xs text-slate-500 font-mono">การนอน (Resting)</div>
            <div class="text-2xl font-black text-sky-400 mt-1">7 คลิป</div>
            <div class="text-xs text-slate-400 mt-1">658.7 วินาที (เฉลี่ย 94.1s)</div>
          </div>
          <div class="p-4 rounded-xl bg-zoo-teal/20 border border-zoo-teal/40 text-center">
            <div class="text-xs text-zoo-gold font-mono font-bold">รวมทั้งหมด (TOTAL)</div>
            <div class="text-2xl font-black text-white mt-1">22 คลิป</div>
            <div class="text-xs text-zoo-gold mt-1">1,051.8 วินาที (~17.5 นาที)</div>
          </div>
        </div>

        <div class="p-4 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder text-xs text-slate-600 dark:text-slate-300">
          <strong>🔍 ข้อค้นพบสำคัญจากการทดสอบจริง:</strong>
          <ul class="list-disc list-inside mt-2 space-y-1">
            <li><strong>การเดินเป็นช่วงสั้นๆ:</strong> ชะมดไม่เดินต่อเนื่องนาน แต่เดินข้ามห้องในระยะ 8–28 วินาที แล้วหยุดนิ่ง</li>
            <li><strong>กลางคืนไม่หลุดแทร็ก:</strong> แสงอินฟราเรด ตาเรืองแสง และเงา ไม่ส่งผลกระทบต่อ MOG2 Centroid Tracking</li>
            <li><strong>ตัดสัญญาณกระถางต้นไม้สำเร็จ:</strong> ตลอด 22 คลิป ไม่พบการ False Alarm จากต้นไม้หรือผนังนิ่งแม้แต่ครั้งเดียว</li>
          </ul>
        </div>
      </div>

      <!-- 3 Real-World Evidence Test Cases Cards with Embedded Images -->
      <div class="space-y-8">
        
        <!-- Evidence 1: Walking -->
        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-lg">
          <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 mb-4 border-b border-slate-200 dark:border-zoo-cardborder gap-2">
            <div>
              <span class="px-2.5 py-0.5 rounded text-xs font-mono font-bold bg-amber-500/20 text-zoo-gold border border-amber-500/30">TEST 1: LOCOMOTION</span>
              <h4 class="text-xl font-bold text-slate-900 dark:text-white mt-1">การตรวจจับการเดินข้ามห้อง (Camera 03 - Night Infrared)</h4>
            </div>
            <span class="text-xs font-mono text-slate-400">Clip: 25690518091012230.mp4</span>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
            <div class="lg:col-span-8 rounded-xl overflow-hidden border border-slate-300 dark:border-zoo-cardborder bg-black">
              <img src="{img_locomotion}" alt="Walking Locomotion Tracking Result" class="w-full cursor-pointer hover:opacity-95 transition-opacity" onclick="openLightbox(this.src, 'Test 1: Walking Locomotion Tracking Result')">
            </div>
            <div class="lg:col-span-4 space-y-3 text-xs">
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
                <div class="font-bold text-zoo-gold uppercase font-mono">สิ่งที่เกิดขึ้นจริง</div>
                <div class="text-slate-600 dark:text-slate-300 mt-1">ชะมดเดินข้ามพื้นห้อง 3 จากซ้ายไปขวาในเวลา 3.2 วินาที</div>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
                <div class="font-bold text-emerald-400 uppercase font-mono">สิ่งที่คอมพิวเตอร์เห็น</div>
                <div class="text-slate-600 dark:text-slate-300 mt-1">วาดเส้นทางวิถีสีส้ม (Orange Trajectory) ลากตามพิกัดจุดศูนย์กลางต่อเนื่องไม่มีสะดุด</div>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
                <div class="font-bold text-sky-400 uppercase font-mono">กราฟความเร็ว (Speed Curve)</div>
                <div class="text-slate-600 dark:text-slate-300 mt-1">ความเร็วพุ่งสูงเกิน 50 พิกเซล/วินาที ขณะเดิน และตกลงมาเป็น 0 ทันทีเมื่อหยุดเดิน</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Evidence 2: Eating -->
        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-lg">
          <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 mb-4 border-b border-slate-200 dark:border-zoo-cardborder gap-2">
            <div>
              <span class="px-2.5 py-0.5 rounded text-xs font-mono font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">TEST 2: FEEDING</span>
              <h4 class="text-xl font-bold text-slate-900 dark:text-white mt-1">การวัดรอบมื้ออาหารที่ถาดอาหาร (Camera 02 - Day Color)</h4>
            </div>
            <span class="text-xs font-mono text-slate-400">Clip: 25690518092326646.mp4</span>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
            <div class="lg:col-span-8 rounded-xl overflow-hidden border border-slate-300 dark:border-zoo-cardborder bg-black">
              <img src="{img_eating}" alt="Eating Tracking Result" class="w-full cursor-pointer hover:opacity-95 transition-opacity" onclick="openLightbox(this.src, 'Test 2: Eating Mealtime Tracking Result')">
            </div>
            <div class="lg:col-span-4 space-y-3 text-xs">
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
                <div class="font-bold text-zoo-gold uppercase font-mono">สิ่งที่เกิดขึ้นจริง</div>
                <div class="text-slate-600 dark:text-slate-300 mt-1">ชะมดเดินมาที่ถาดอาหารและก้มกินต่อเนื่องนานถึง 80 วินาที</div>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
                <div class="font-bold text-emerald-400 uppercase font-mono">โซนถาดอาหาร (Food Tray ROI)</div>
                <div class="text-slate-600 dark:text-slate-300 mt-1">กรอบสี่เหลี่ยมสีส้มล็อกพิกัดถาดอาหาร จุดสีเขียวแสดงตำแหน่งหัวชะมดกระจุกตัวอยู่ภายในถาด</div>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
                <div class="font-bold text-sky-400 uppercase font-mono">ความแม่นยำทางสถิติ</div>
                <div class="text-slate-600 dark:text-slate-300 mt-1">การกำหนดเงื่อนไข 10 วินาทีช่วยตัดการเดินเฉียดผ่านถาดได้อย่างแม่นยำ บันทึกเวลาเริ่ม 09:23:26 ถึง 09:24:46</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Evidence 3: Resting -->
        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-lg">
          <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 mb-4 border-b border-slate-200 dark:border-zoo-cardborder gap-2">
            <div>
              <span class="px-2.5 py-0.5 rounded text-xs font-mono font-bold bg-sky-500/20 text-sky-400 border border-sky-500/30">TEST 3: RESTING</span>
              <h4 class="text-xl font-bold text-slate-900 dark:text-white mt-1">การยืนยันเวลานอนในเตียงยางรถยนต์ (Camera 03 - Night IR)</h4>
            </div>
            <span class="text-xs font-mono text-slate-400">Clip: 25690519194109670.mp4</span>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
            <div class="lg:col-span-8 rounded-xl overflow-hidden border border-slate-300 dark:border-zoo-cardborder bg-black">
              <img src="{img_resting}" alt="Resting Bedtime Tracking Result" class="w-full cursor-pointer hover:opacity-95 transition-opacity" onclick="openLightbox(this.src, 'Test 3: Resting Bedtime Tracking Result')">
            </div>
            <div class="lg:col-span-4 space-y-3 text-xs">
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
                <div class="font-bold text-zoo-gold uppercase font-mono">ที่นอนประจำตัว</div>
                <div class="text-slate-600 dark:text-slate-300 mt-1">ยางรถยนต์ปูฟางด้านบนห้อง 3 ชะมดปีนเข้าไปเวลา 27.2s และขดตัวเป็นก้อนกลม</div>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
                <div class="font-bold text-sky-400 uppercase font-mono">การทำงานของกฎ 1 นาที</div>
                <div class="text-slate-600 dark:text-slate-300 mt-1">ตัวนับความนิ่งข้ามหลัก 60 วินาทีที่วินาทีที่ 86.0s ระบบเปลี่ยนสถานะเป็น Resting อัตโนมัติ</div>
              </div>
              <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
                <div class="font-bold text-emerald-400 uppercase font-mono">ตรงกับบันทึกผู้ดูแล</div>
                <div class="text-slate-600 dark:text-slate-300 mt-1">ผลลัพธ์ตรงกับบันทึกของสวนสัตว์: 'Curling up in tire' แม่นยำ 100%</div>
              </div>
            </div>
          </div>
        </div>

      </div>

    </div>
  </section>

  <!-- SECTION 7: RELATIONAL DATA MODEL & SCHEMA -->
  <section id="datamodel" class="py-16 border-b border-slate-200 dark:border-zoo-cardborder">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-3xl mx-auto mb-12">
        <h2 class="text-xs font-bold uppercase tracking-wider text-zoo-gold font-mono mb-2">07. DATA MODEL & SCHEMA ARCHITECTURE</h2>
        <h3 class="text-3xl font-bold text-slate-900 dark:text-white">โมเดลข้อมูลเชิงสัมพันธ์ (Design Only AI/Data Model)</h3>
        <p class="text-slate-600 dark:text-slate-400 mt-3">
          สอดคล้องตามข้อกำหนดของ Phase 1 อย่างเคร่งครัด: ออกแบบเฉพาะสถาปัตยกรรม AI และ Data Model โดยไม่ต้องเขียนหน้าแอป UI
        </p>
      </div>

      <!-- Relational ER Diagram Visualizer -->
      <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border border-slate-200 dark:border-zoo-cardborder shadow-sm mb-8">
        <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-zoo-cardborder mb-6">
          <h4 class="font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <i data-lucide="network" class="w-5 h-5 text-zoo-gold"></i> แผนภาพความสัมพันธ์ Entity-Relationship (ER Model)
          </h4>
          <span class="text-xs font-mono text-slate-400">Relational Database 3NF</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-center">
          
          <!-- Room Entity -->
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
            <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-200 dark:border-zoo-cardborder">
              <span class="font-bold text-sm text-zoo-gold font-mono">Room</span>
              <span class="text-[10px] text-slate-400 font-mono">Entity</span>
            </div>
            <div class="space-y-1.5 text-xs font-mono">
              <div class="text-amber-400 font-bold">🔑 room_id (PK) : VARCHAR</div>
              <div class="text-slate-400">room_name : VARCHAR</div>
              <div class="text-slate-400">enclosure_seq : INT</div>
            </div>
          </div>

          <!-- Connector 1 -->
          <div class="hidden md:flex flex-col items-center justify-center text-slate-400 font-mono text-xs">
            <span>1 : N</span>
            <div class="w-full h-0.5 bg-zoo-teal my-1 relative">
              <div class="absolute right-0 -top-1 w-2 h-2 border-t-2 border-r-2 border-zoo-gold rotate-45"></div>
            </div>
            <span class="text-[10px]">Has Cameras</span>
          </div>

          <!-- Camera Entity -->
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
            <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-200 dark:border-zoo-cardborder">
              <span class="font-bold text-sm text-sky-400 font-mono">Camera</span>
              <span class="text-[10px] text-slate-400 font-mono">Entity</span>
            </div>
            <div class="space-y-1.5 text-xs font-mono">
              <div class="text-amber-400 font-bold">🔑 camera_id (PK) : VARCHAR</div>
              <div class="text-sky-300">🔗 room_id (FK) : VARCHAR</div>
              <div class="text-slate-400">rtsp_url : TEXT</div>
              <div class="text-slate-400">is_infrared : BOOL</div>
            </div>
          </div>

          <!-- Animal Entity -->
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-zoo-surface border border-slate-200 dark:border-zoo-cardborder">
            <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-200 dark:border-zoo-cardborder">
              <span class="font-bold text-sm text-emerald-400 font-mono">Animal</span>
              <span class="text-[10px] text-slate-400 font-mono">Entity</span>
            </div>
            <div class="space-y-1.5 text-xs font-mono">
              <div class="text-amber-400 font-bold">🔑 animal_id (PK) : VARCHAR</div>
              <div class="text-slate-400">name : VARCHAR ('Hompom')</div>
              <div class="text-slate-400">species : VARCHAR</div>
              <div class="text-slate-400">sex : CHAR</div>
            </div>
          </div>

        </div>

        <!-- BehaviorEvent Core Entity -->
        <div class="mt-6 p-5 rounded-xl bg-zoo-teal/10 border-2 border-zoo-teal/40">
          <div class="flex items-center justify-between pb-2 mb-3 border-b border-zoo-teal/30">
            <span class="font-bold text-base text-zoo-gold font-mono flex items-center gap-2">
              <i data-lucide="layers" class="w-4 h-4"></i> Core Entity: BehaviorEvent
            </span>
            <span class="px-2.5 py-0.5 rounded bg-zoo-teal/30 text-zoo-gold text-xs font-mono">Time-Series Event Log</span>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3 text-xs font-mono">
            <div class="p-2.5 rounded bg-slate-900 border border-slate-800">
              <div class="text-amber-400 font-bold">event_id (PK)</div>
              <div class="text-slate-400 text-[10px]">EVT001</div>
            </div>
            <div class="p-2.5 rounded bg-slate-900 border border-slate-800">
              <div class="text-emerald-400 font-bold">animal_id (FK)</div>
              <div class="text-slate-400 text-[10px]">A01</div>
            </div>
            <div class="p-2.5 rounded bg-slate-900 border border-slate-800">
              <div class="text-sky-400 font-bold">camera_id (FK)</div>
              <div class="text-slate-400 text-[10px]">CAM03</div>
            </div>
            <div class="p-2.5 rounded bg-slate-900 border border-slate-800">
              <div class="text-purple-400 font-bold">macro_state</div>
              <div class="text-slate-400 text-[10px]">Active / Inactive</div>
            </div>
            <div class="p-2.5 rounded bg-slate-900 border border-slate-800">
              <div class="text-zoo-gold font-bold">behavior</div>
              <div class="text-slate-400 text-[10px]">Walking, Resting..</div>
            </div>
            <div class="p-2.5 rounded bg-slate-900 border border-slate-800">
              <div class="text-slate-300 font-bold">timestamp_start</div>
              <div class="text-slate-400 text-[10px]">09:09:44</div>
            </div>
            <div class="p-2.5 rounded bg-slate-900 border border-slate-800">
              <div class="text-slate-300 font-bold">duration_sec</div>
              <div class="text-slate-400 text-[10px]">11 s</div>
            </div>
            <div class="p-2.5 rounded bg-slate-900 border border-slate-800">
              <div class="text-emerald-400 font-bold">confidence</div>
              <div class="text-slate-400 text-[10px]">0.91</div>
            </div>
          </div>
        </div>

      </div>

    </div>
  </section>

  <!-- SECTION 8: METHOD COMPARISON (BASELINE VS DEEP LEARNING) -->
  <section id="comparison" class="py-16 border-b border-slate-200 dark:border-zoo-cardborder bg-slate-50/50 dark:bg-zoo-darkbg/50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-3xl mx-auto mb-12">
        <h2 class="text-xs font-bold uppercase tracking-wider text-zoo-gold font-mono mb-2">08. METHOD COMPARISON</h2>
        <h3 class="text-3xl font-bold text-slate-900 dark:text-white">ทำไมเราถึงเริ่มด้วย Rule-Based Baseline แทน Deep Learning?</h3>
        <p class="text-slate-600 dark:text-slate-400 mt-3">
          การทดลองเชิงประจักษ์ระหว่างโมเดลสำเร็จรูป (Pretrained YOLO) กับสถาปัตยกรรม Baseline ที่ออกแบบเฉพาะสำหรับสวนสัตว์
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        
        <!-- Pretrained YOLO Card -->
        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border-2 border-rose-500/30 shadow-sm relative overflow-hidden">
          <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-zoo-cardborder mb-4">
            <span class="px-3 py-1 rounded bg-rose-500/10 text-rose-400 text-xs font-mono font-bold">OFF-THE-SHELF YOLOv8</span>
            <span class="text-xs font-mono text-rose-400 font-bold">❌ มีปัญหาในสภาวะจริง</span>
          </div>
          <h4 class="text-lg font-bold text-slate-900 dark:text-white mb-2">ข้อจำกัดของโมเดล Deep Learning สำเร็จรูป</h4>
          <ul class="space-y-2.5 text-xs text-slate-600 dark:text-slate-300">
            <li class="flex items-start gap-2">
              <i data-lucide="x" class="w-4 h-4 text-rose-400 shrink-0 mt-0.5"></i>
              <span><strong>หลุดแทร็กในเวลากลางคืน:</strong> ภาพอินฟราเรดขาวดำมีคอนทราสต์ต่ำ โมเดลสำเร็จรูปไม่ได้ถูกเทรนด้วยตัวชะมดกลางคืน ทำให้ตรวจไม่เจอสัตว์</span>
            </li>
            <li class="flex items-start gap-2">
              <i data-lucide="x" class="w-4 h-4 text-rose-400 shrink-0 mt-0.5"></i>
              <span><strong>หลอนจำผิดเป็นนก (Hallucination):</strong> ในการทดสอบจริง YOLO ทักกระถางต้นไม้ว่าเป็น "Bird" ด้วยความมั่นใจสูงถึง 90%</span>
            </li>
            <li class="flex items-start gap-2">
              <i data-lucide="x" class="w-4 h-4 text-rose-400 shrink-0 mt-0.5"></i>
              <span><strong>กินทรัพยากรสูง:</strong> ต้องใช้การ์ดจอ GPU ประมวลผล ไม่เหมาะกับคอมพิวเตอร์ออฟฟิศทั่วไปของสวนสัตว์</span>
            </li>
          </ul>
        </div>

        <!-- Rule-Based Baseline Card -->
        <div class="p-6 rounded-2xl bg-white dark:bg-zoo-carddark border-2 border-emerald-500/40 shadow-sm relative overflow-hidden">
          <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-zoo-cardborder mb-4">
            <span class="px-3 py-1 rounded bg-emerald-500/10 text-emerald-400 text-xs font-mono font-bold">RULE-BASED VISION BASELINE</span>
            <span class="text-xs font-mono text-emerald-400 font-bold">✅ ชนะใน Phase 1</span>
          </div>
          <h4 class="text-lg font-bold text-slate-900 dark:text-white mb-2">ทำไมสถาปัตยกรรมของเราถึงได้ผล 100%</h4>
          <ul class="space-y-2.5 text-xs text-slate-600 dark:text-slate-300">
            <li class="flex items-start gap-2">
              <i data-lucide="check" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5"></i>
              <span><strong>กล้องนิ่ง พื้นหลังนิ่ง:</strong> ดึงจุดเด่นของกล้อง CCTV ติดผนังถาวร ตัดต้นไม้และสิ่งกีดขวางนิ่งออกได้ 100%</span>
            </li>
            <li class="flex items-start gap-2">
              <i data-lucide="check" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5"></i>
              <span><strong>ทำงานได้ครบทั้ง 22 คลิป:</strong> แทร็กชะมดได้ทั้งตอนเดิน กิน และนอน ทั้งกลางวันสีและกลางคืนอินฟราเรด</span>
            </li>
            <li class="flex items-start gap-2">
              <i data-lucide="check" class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5"></i>
              <span><strong>เบาและเร็ว:</strong> วิเคราะห์ที่ 2 FPS รันบนคอมออฟฟิศธรรมดาได้ลื่นไหล ไม่ต้องใช้การ์ดจอแพง</span>
            </li>
          </ul>
        </div>

      </div>

      <!-- Roadmap to Phase 2 (End of Oct) -->
      <div id="summary" class="p-8 rounded-2xl bg-gradient-to-r from-zoo-teal via-zoo-carddark to-zoo-darkbg border border-zoo-gold/40 text-white shadow-xl">
        <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-4 border-b border-zoo-cardborder mb-6">
          <div>
            <span class="px-2.5 py-0.5 rounded bg-zoo-gold text-zoo-darkbg text-xs font-mono font-bold">NEXT HORIZON</span>
            <h4 class="text-2xl font-bold mt-1">แผนการต่อยอดสู่ Phase 2 (สิ้นเดือนตุลาคม)</h4>
          </div>
          <span class="text-xs font-mono text-slate-300">Deep Learning-based Behavior Analysis</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="p-4 rounded-xl bg-zoo-darkbg/60 border border-zoo-cardborder">
            <div class="font-bold text-zoo-gold font-mono text-sm mb-1">TASK 1: CNN Classification</div>
            <p class="text-xs text-slate-300">เทรน Convolutional Neural Network จำแนกท่าทางละเอียด [Walking, Eating, Resting, Climbing] จากเฟรมที่สกัดได้</p>
          </div>
          <div class="p-4 rounded-xl bg-zoo-darkbg/60 border border-zoo-cardborder">
            <div class="font-bold text-sky-400 font-mono text-sm mb-1">TASK 2: Custom YOLO Detection</div>
            <p class="text-xs text-slate-300">นำข้อมูลภาพ Phase 1 ไปทำ Annotation กลางคืน แล้ว Fine-tune YOLO ให้ตรวจจับตัวชะมดในที่มืดได้อย่างแม่นยำ</p>
          </div>
          <div class="p-4 rounded-xl bg-zoo-darkbg/60 border border-zoo-cardborder">
            <div class="font-bold text-purple-400 font-mono text-sm mb-1">TASK 3: Pose Keypoints</div>
            <p class="text-xs text-slate-300">วิเคราะห์ชีวกลศาสตร์จากโครงกระดูก (Body Angle, Head Angle, Movement Speed) เพื่อตรวจจับพฤติกรรมย่อย</p>
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- Lightbox Modal -->
  <div id="lightbox" class="fixed inset-0 z-50 bg-black/90 backdrop-blur-md hidden items-center justify-center p-4" onclick="closeLightbox()">
    <div class="relative max-w-5xl max-h-[90vh] flex flex-col items-center">
      <img id="lightbox-img" src="" alt="Enlarged Visual" class="max-w-full max-h-[80vh] rounded-lg shadow-2xl border border-zoo-cardborder">
      <p id="lightbox-caption" class="mt-3 text-sm font-mono text-zoo-gold text-center"></p>
      <button class="absolute -top-10 right-0 text-white hover:text-zoo-gold text-sm font-mono flex items-center gap-1">
        <i data-lucide="x" class="w-4 h-4"></i> ปิด (ESC)
      </button>
    </div>
  </div>

  <!-- Footer -->
  <footer class="py-12 border-t border-slate-200 dark:border-zoo-cardborder bg-white dark:bg-zoo-darkbg text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div>
        <p class="font-bold text-slate-700 dark:text-slate-300">Chiang Mai Zoo × Chiang Mai University | Image Processing Project</p>
        <p class="text-slate-400 mt-0.5">Automated Civet Behavior Monitoring System (Phase 1 Complete Dashboard)</p>
      </div>
      <div class="font-mono text-slate-400">
        Created for Presentation & Technical Knowledge Base
      </div>
    </div>
  </footer>

  <!-- Scripts -->
  <script>
    // Initialize Lucide Icons
    lucide.createIcons();

    // Dark/Light Mode Toggle
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.addEventListener('click', () => {{
      document.documentElement.classList.toggle('dark');
      lucide.createIcons();
    }});

    // Reading Progress Bar
    window.addEventListener('scroll', () => {{
      const winScroll = document.documentElement.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = (winScroll / height) * 100;
      document.getElementById('progress-bar').style.width = scrolled + '%';
    }});

    // Room Card Selector
    const roomDetails = {{
      1: "ห้อง 1 (Camera 01): เป็นห้องระเบียงแรกของทางเดินกรง ใช้สำหรับตรวจจับการเดินผ่าน (Transit) ระหว่างประตูกรงไปยังห้อง 2",
      2: "ห้อง 2 (Camera 02): ห้องอาหารหลัก วางถาดอาหารและน้ำถาวรที่พื้นกลางล่าง ระบบกำหนด Food Tray ROI (X: 960-1340, Y: 740-1060) และตัดสัญญาณกระถางต้นไม้",
      3: "ห้อง 3 (Camera 03): ห้องนอนและพื้นที่เล่น มีขอนไม้สำหรับปีนป่าย และที่นอนยางรถยนต์ปูฟางที่มุมบน (Tire Bed ROI: X: 820-1180, Y: 130-420) เป็นจุดทดสอบกฎ 1 นาที",
      4: "ห้อง 4 (Camera 04): ห้องพักผ่อนส่วนตัวด้านในสุด สัตว์มักเข้าไปหลบภัยเมื่อมีสิ่งรบกวน เชื่อมต่อกับห้อง 3 แบบทางเดียว"
    }};

    function selectRoom(num) {{
      for (let i = 1; i <= 4; i++) {{
        const card = document.getElementById('room-card-' + i);
        if (i === num) {{
          card.classList.add('border-zoo-gold', 'border-2', 'bg-zoo-gold/10');
          card.classList.remove('border-slate-200', 'dark:border-zoo-cardborder');
        }} else {{
          card.classList.remove('border-zoo-gold', 'border-2', 'bg-zoo-gold/10');
          card.classList.add('border-slate-200', 'dark:border-zoo-cardborder');
        }}
      }}
      document.getElementById('room-detail-box').innerHTML = '<span class="font-bold text-zoo-gold">ห้อง ' + num + ':</span> ' + roomDetails[num];
    }}

    // 9-Step Pipeline Stepper Data
    const pipelineSteps = {{
      1: {{
        badge: "STEP 01 OF 09",
        tagline: "Input Ingestion Layer",
        title: "Camera Streams (รับภาพสตรีม 4 ตัว 1080p)",
        desc: "รับสัญญาณสตรีมวิดีโอ RTSP แบบเรียลไทม์ ความละเอียด Full HD 1080p จากกล้อง CCTV ติดผนังถาวรทั้ง 4 ตัวที่ติดตั้งอยู่ในแต่ละห้อง (Room 1 ถึง Room 4) รองรับทั้งภาพสีในเวลากลางวัน และภาพอินฟราเรดขาวดำในเวลากลางคืน",
        input: "RTSP Stream 1080p @ 15 FPS จากกล้อง 4 ตัว (CAM01-CAM04)",
        output: "Raw Video Frames (Bgra/BGR Buffer) ส่งต่อไปยังตัว Subsampler",
        code: `# Step 1: Ingest video stream\\ncap = cv2.VideoCapture(stream_url)\\nfps = cap.get(cv2.CAP_PROP_FPS) or 15.0\\nret, frame = cap.read()\\nif ret:\\n    frame_h, frame_w = frame.shape[:2] # 1080x1920`
      }},
      2: {{
        badge: "STEP 02 OF 09",
        tagline: "Pre-processing & Optimization",
        title: "Video Processing (Subsampling เหลือ 2 FPS)",
        desc: "ลดความถี่เฟรมจาก 15 FPS ลงเหลือ 2 FPS (คำนวณทุกๆ 8 เฟรม) ช่วยลดภาระการประมวลผลลงได้ถึง 85% เครื่องคอมพิวเตอร์สำนักงานทั่วไปทำงานได้ราบรื่น ไม่ร้อน ไม่ต้องพึ่งพาการ์ดจอราคาแพง",
        input: "Raw 15 FPS Video Stream (900 เฟรม/นาที)",
        output: "Sampled Frames @ 2 FPS (120 เฟรม/นาที) พร้อมประทับเวลา t (วินาที)",
        code: `# Step 2: Temporal Subsampling at 2 FPS\\nsample_step = int(round(fps / 2.0)) # ~8 frames\\nif frame_idx % sample_step == 0:\\n    t = frame_idx / fps\\n    process_sampled_frame(frame, t)`
      }},
      3: {{
        badge: "STEP 03 OF 09",
        tagline: "Foreground Segmentation",
        title: "Animal Detection (ตัดพื้นหลังด้วย MOG2 & Masking)",
        desc: "ใช้อัลกอริทึม Adaptive MOG2 Background Subtraction เพื่อเรียนรู้พื้นหลังที่นิ่งสนิท ดึงเฉพาะวัตถุที่ขยับได้ พร้อมใช้ Morphological Operations (Opening + Dilation) และ Plant Mask ลบการสั่นไหวของต้นไม้",
        input: "Sampled Video Frame (1920x1080 BGR)",
        output: "Clean Binary Foreground Mask (พิกเซลชะมดสีขาว พื้นหลังสีดำ)",
        code: `# Step 3: MOG2 & Morphological Cleaning\\nfg_mask = subtractor.apply(frame)\\nfg_clean = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)\\nfg_clean = cv2.dilate(fg_clean, kernel, iterations=2)\\nfg_clean[100:580, 800:1150] = 0 # Mask plant noise`
      }},
      4: {{
        badge: "STEP 04 OF 09",
        tagline: "Spatial Trajectory Tracking",
        title: "Animal Tracking (สกัด Centroid และ Bounding Box)",
        desc: "ค้นหา Contour ขนาดใหญ่ที่สุด (Area > 1200 px) ล้อมกรอบ Bounding Box และคำนวณจุดศูนย์กลางพิกัด (Centroid cx, cy) บันทึกเป็นเวกเตอร์ประวัติเส้นทางการเคลื่อนที่",
        input: "Binary Mask จากขั้นตอนที่ 3",
        output: "พิกัดจุดกึ่งกลาง (cx, cy), กรอบ (x, y, w, h), และขนาดพื้นที่ Area",
        code: `# Step 4: Contour Extraction & Centroid\\ncontours, _ = cv2.findContours(fg_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)\\nfor c in contours:\\n    if cv2.contourArea(c) > 1200:\\n        x, y, w, h = cv2.boundingRect(c)\\n        cx, cy = x + w // 2, y + h // 2`
      }},
      5: {{
        badge: "STEP 05 OF 09",
        tagline: "Kinematic & Spatial Features",
        title: "Feature Extraction (คำนวณความเร็ว และการทับซ้อน ROI)",
        desc: "คำนวณความเร็วการเคลื่อนที่ (Speed Vector px/s) จากระยะทาง Euclidean Distance เทียบกับเวลา และตรวจสอบว่าพิกัดตกอยู่ในโซนถาดอาหาร (Food Tray) หรือเตียงนอน (Tire Bed) หรือไม่",
        input: "พิกัดปัจจุบัน (cx, cy), พิกัดก่อนหน้า (prev_cx, prev_cy), Δt",
        output: "Speed (px/s), in_food_roi (bool), in_tire_roi (bool)",
        code: `# Step 5: Feature Extraction\\nspeed = np.hypot(cx - prev_cx, cy - prev_cy) / dt\\nin_food = (ROI_X1 <= cx <= ROI_X2) and (ROI_Y1 <= cy <= ROI_Y2)\\nin_tire = (TIRE_X1 <= cx <= TIRE_X2) and (TIRE_Y1 <= cy <= TIRE_Y2)`
      }},
      6: {{
        badge: "STEP 06 OF 09",
        tagline: "Behavior Logic & State Machine",
        title: "Behavior Classification (กฎตรรกศาสตร์เวลา Debounce Rules)",
        desc: "ประเมินพฤติกรรมด้วยกฎการหน่วงเวลา: นิ่งในยางรถยนต์ครบ 60s = นอน (Resting), แช่ในถาดอาหารครบ 10s = กิน (Eating), เคลื่อนที่ความเร็วสูงครบ 3s = เดิน (Walking)",
        input: "Speed, in_food_roi, in_tire_roi, still_timer, active_timer",
        output: "สถานะพฤติกรรมปัจจุบัน: WALKING, EATING, RESTING, หรือ UNKNOWN",
        code: `# Step 6: Temporal Debounce State Machine\\nif in_tire and still_timer >= 60.0:\\n    current_behavior = 'RESTING'\\nelif in_food and food_timer >= 10.0:\\n    current_behavior = 'EATING'\\nelif speed > 30 and move_timer >= 3.0:\\n    current_behavior = 'WALKING'`
      }},
      7: {{
        badge: "STEP 07 OF 09",
        tagline: "Event Construction",
        title: "Behavior Events (สร้างเรคคอร์ดเหตุการณ์ประทับเวลา)",
        desc: "เมื่อพฤติกรรมเริ่มต้นและสิ้นสุด ระบบจะสร้าง Object เหตุการณ์ที่ระบุเวลาเริ่ม (Start Timestamp), เวลาสิ้นสุด (End Timestamp), ระยะเวลา (Duration วินาที) และค่าความเชื่อมั่น",
        input: "การเปลี่ยนสถานะของตัวจัดหมวดหมู่พฤติกรรม",
        output: "BehaviorEvent Record (EVT_ID, StartTime, EndTime, Duration, Conf)",
        code: `# Step 7: Create Timestamped Event\\nevent = {{\\n    'event_id': f'EVT{{len(events)+1:03d}}',\\n    'macro_state': 'Active' if is_active else 'Inactive',\\n    'behavior': current_behavior,\\n    'start': t_start, 'end': t_end, 'duration': t_end - t_start\\n}}`
      }},
      8: {{
        badge: "STEP 08 OF 09",
        tagline: "Structured Data Persistence",
        title: "Data Storage (จัดเก็บลงไฟล์ CSV, JSON และฐานข้อมูล)",
        desc: "บันทึกข้อมูลแบบมีโครงสร้าง (Structured Data Model) ตามมาตรฐาน 3NF เชื่อมโยง Animal, Camera, Room และ Event เข้าด้วยกัน ไม่ต้องต่อหน้าเว็บแอป ผู้ดูแลเปิดดูใน Excel ได้ทันที",
        input: "BehaviorEvent Dictionary Objects",
        output: "บันทึกลงไฟล์ daily_behavior_log.csv และ behavior_database.json",
        code: `# Step 8: Save to Structured CSV & Database\\ndf = pd.DataFrame(events)\\ndf.to_csv('daily_behavior_log.csv', index=False)\\nwith open('behavior_events.json', 'w') as f:\\n    json.dump(events, f, indent=2)`
      }},
      9: {{
        badge: "STEP 09 OF 09",
        tagline: "Zoo Analytics & Reporting",
        title: "Visualization (สรุปกราฟพฤติกรรมประจำวันให้สัตวแพทย์)",
        desc: "สรุปผลเป็นกราฟสัดส่วนเวลากิจกรรมประจำวัน (Daily Activity Budget), กราฟรอบเวลาการกินอาหาร และชาร์ตเวลานอน เพื่อให้สัตวแพทย์ตรวจเช็กสุขภาพสัตว์ได้ง่าย",
        input: "ฐานข้อมูลบันทึกพฤติกรรมตลอด 24 ชั่วโมง",
        output: "กราฟ Activity Budget, สรุปแคลอรี่/รอบกินอาหาร, และรายงานสุขภาพดิจิทัล",
        code: `# Step 9: Aggregate Activity Budget for Keepers\\nfig, ax = plt.subplots()\\nax.pie([sleep_hrs, walk_hrs, eat_hrs], labels=['Sleep', 'Walk', 'Eat'])\\nplt.savefig('daily_activity_budget.png')`
      }}
    }};

    function setPipelineStep(num) {{
      const data = pipelineSteps[num];
      document.getElementById('step-badge').innerText = data.badge;
      document.getElementById('step-tagline').innerText = data.tagline;
      document.getElementById('step-title').innerText = data.title;
      document.getElementById('step-desc').innerText = data.desc;
      document.getElementById('step-input').innerText = data.input;
      document.getElementById('step-output').innerText = data.output;
      document.getElementById('step-code').innerText = data.code;

      for (let i = 1; i <= 9; i++) {{
        const btn = document.getElementById('p-btn-' + i);
        if (i === num) {{
          btn.className = "pipe-btn p-3 rounded-xl border text-center transition-all bg-zoo-gold text-zoo-darkbg border-zoo-gold font-bold shadow-md";
        }} else {{
          btn.className = "pipe-btn p-3 rounded-xl border text-center transition-all bg-white dark:bg-zoo-carddark text-slate-600 dark:text-slate-300 border-slate-200 dark:border-zoo-cardborder hover:border-zoo-gold";
        }}
      }}
    }}

    // Simulator Interactive Functions
    function updateSleepSim(val) {{
      document.getElementById('stillness-val').innerText = val + ' วินาที';
      const box = document.getElementById('sim-state-box');
      const title = document.getElementById('sim-state-title');
      const desc = document.getElementById('sim-state-desc');

      if (val < 10) {{
        box.className = "p-5 rounded-xl border text-center transition-all bg-slate-100 dark:bg-zoo-surface border-slate-300 dark:border-zoo-cardborder text-slate-600 dark:text-slate-300";
        title.innerText = "AWAKE & ACTIVE (เพิ่งหยุดเดิน)";
        desc.innerText = "สัตว์หยุดเดินได้เพียง " + val + " วินาที ยังถือว่าตื่นอยู่";
      }} else if (val < 60) {{
        box.className = "p-5 rounded-xl border text-center transition-all bg-amber-500/10 border-amber-500/40 text-amber-400";
        title.innerText = "PAUSING / NOT ASLEEP YET (หยุดพักชั่วคราว)";
        desc.innerText = "นิ่งมา " + val + " วินาที ยังไม่ถึง 60s ระบบจะยังไม่ลงบันทึกว่านอนหลับ";
      }} else {{
        box.className = "p-5 rounded-xl border text-center transition-all bg-emerald-500/20 border-emerald-500 text-emerald-400 shadow-lg";
        title.innerText = "💤 SLEEPING CONFIRMED (นอนหลับจริง)";
        desc.innerText = "นิ่งครบ 60 วินาทีตามเกณฑ์ 1-Minute Rule! ระบบบันทึกสถานะ 'Resting' ลงฐานข้อมูล";
      }}
    }}

    function updateEatSim(val) {{
      document.getElementById('eat-time-val').innerText = val + ' วินาที';
      const box = document.getElementById('eat-state-box');
      const title = document.getElementById('eat-state-title');
      const desc = document.getElementById('eat-state-desc');

      if (val < 10) {{
        box.className = "p-5 rounded-xl border text-center transition-all bg-amber-500/10 border-amber-500/40 text-amber-400";
        title.innerText = "PASSING BY FOOD (เดินเฉียดผ่านถาด)";
        desc.innerText = "อยู่ในถาดเพียง " + val + " วินาที (< 10s) ยังไม่ถือว่ากินอาหาร เพื่อตัดกรณีเดินผ่าน";
      }} else {{
        box.className = "p-5 rounded-xl border text-center transition-all bg-emerald-500/20 border-emerald-500 text-emerald-400 shadow-lg";
        title.innerText = "🍽️ EATING EVENT CONFIRMED (กำลังกินอาหารจริง)";
        desc.innerText = "แช่ในถาดครบ " + val + " วินาที (>= 10s) บันทึกเป็นรอบมื้ออาหารอย่างเป็นทางการ";
      }}
    }}

    // Lightbox Controls
    function openLightbox(src, caption) {{
      document.getElementById('lightbox-img').src = src;
      document.getElementById('lightbox-caption').innerText = caption;
      document.getElementById('lightbox').classList.remove('hidden');
      document.getElementById('lightbox').classList.add('flex');
    }}

    function closeLightbox() {{
      document.getElementById('lightbox').classList.add('hidden');
      document.getElementById('lightbox').classList.remove('flex');
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') closeLightbox();
    }});
  </script>
</body>
</html>
'''

    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    file_size_kb = os.path.getsize(out_html_path) / 1024.0
    print(f"Successfully generated dashboard HTML:")
    print(f"Path: {out_html_path}")
    print(f"Size: {file_size_kb:.1f} KB")

if __name__ == "__main__":
    generate_dashboard()
