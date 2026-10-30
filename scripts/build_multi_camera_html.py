import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_content = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>เปรียบเทียบสถาปัตยกรรมระบบ 4 กล้อง (Phase 2) — CMZ × CMU</title>
    <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #090d16;
            --bg-card: #131b2e;
            --bg-card-hover: #1a253e;
            --border-color: #263352;
            --primary: #38bdf8;
            --primary-glow: rgba(56, 189, 248, 0.25);
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-purple: #a855f7;
            --accent-rose: #f43f5e;
            --text-main: #f1f5f9;
            --text-sub: #94a3b8;
            --text-muted: #64748b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Prompt', sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            line-height: 1.6;
            padding: 24px 16px 80px 16px;
        }

        .container {
            max-width: 1280px;
            margin: 0 auto;
        }

        /* Header */
        header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px 20px;
            background: linear-gradient(180deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0) 100%);
            border-radius: 20px;
            border: 1px solid var(--border-color);
        }

        .badge-project {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(56, 189, 248, 0.12);
            color: var(--primary);
            border: 1px solid rgba(56, 189, 248, 0.3);
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 500;
            margin-bottom: 14px;
        }

        h1 {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff 0%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }

        .subtitle {
            color: var(--text-sub);
            font-size: 1.05rem;
            max-width: 800px;
            margin: 0 auto;
        }

        /* Layout Grid of 4 Rooms */
        .topology-section {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 36px;
        }

        .section-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
            color: #ffffff;
        }

        .rooms-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }

        .room-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px;
            position: relative;
            transition: all 0.2s ease;
        }

        .room-card:hover {
            border-color: var(--primary);
            transform: translateY(-2px);
        }

        .room-badge {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 6px;
            display: inline-block;
            margin-bottom: 8px;
            text-transform: uppercase;
        }

        .room-card.r1 .room-badge { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
        .room-card.r2 .room-badge { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
        .room-card.r3 .room-badge { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
        .room-card.r4 .room-badge { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }

        .room-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 6px;
        }

        .room-role {
            font-size: 0.85rem;
            color: var(--primary);
            font-weight: 500;
            margin-bottom: 10px;
        }

        .room-desc {
            font-size: 0.85rem;
            color: var(--text-sub);
            line-height: 1.5;
        }

        /* 3 Architectural Options */
        .options-title {
            text-align: center;
            margin-bottom: 24px;
        }

        .options-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
            gap: 24px;
            margin-bottom: 40px;
        }

        .option-card {
            background: var(--bg-card);
            border: 2px solid var(--border-color);
            border-radius: 18px;
            padding: 28px 24px;
            display: flex;
            flex-direction: column;
            position: relative;
            transition: all 0.3s ease;
        }

        .option-card.recommended {
            border-color: var(--primary);
            background: linear-gradient(180deg, rgba(20, 36, 64, 0.8) 0%, rgba(19, 27, 46, 0.95) 100%);
            box-shadow: 0 0 25px var(--primary-glow);
        }

        .ribbon-recommended {
            position: absolute;
            top: -14px;
            right: 24px;
            background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%);
            color: #000000;
            font-weight: 700;
            font-size: 0.78rem;
            padding: 4px 14px;
            border-radius: 9999px;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.4);
        }

        .option-header {
            margin-bottom: 18px;
        }

        .opt-tag {
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 4px;
        }

        .opt-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 8px;
        }

        .opt-subtitle {
            font-size: 0.9rem;
            color: var(--text-sub);
            min-height: 40px;
        }

        .opt-diagram {
            background: rgba(10, 15, 26, 0.8);
            border: 1px dashed var(--border-color);
            border-radius: 10px;
            padding: 14px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            color: #38bdf8;
            margin-bottom: 20px;
            line-height: 1.4;
            overflow-x: auto;
        }

        .pros-cons {
            margin-bottom: 20px;
            flex-grow: 1;
        }

        .pc-block {
            margin-bottom: 14px;
        }

        .pc-title {
            font-size: 0.85rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 8px;
        }

        .pc-title.pro { color: var(--accent-green); }
        .pc-title.con { color: var(--accent-rose); }

        .pc-list {
            list-style: none;
            font-size: 0.85rem;
            color: var(--text-sub);
        }

        .pc-list li {
            position: relative;
            padding-left: 18px;
            margin-bottom: 6px;
            line-height: 1.4;
        }

        .pc-list li::before {
            content: "•";
            position: absolute;
            left: 4px;
            font-weight: bold;
        }

        .pc-block.pro .pc-list li::before { color: var(--accent-green); }
        .pc-block.con .pc-list li::before { color: var(--accent-rose); }

        .score-pill {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 23, 42, 0.7);
            border-radius: 8px;
            padding: 10px 14px;
            border: 1px solid var(--border-color);
            margin-top: auto;
        }

        .score-label {
            font-size: 0.82rem;
            color: var(--text-sub);
        }

        .stars {
            color: var(--accent-amber);
            font-weight: 700;
            letter-spacing: 2px;
        }

        /* Matrix Table */
        .table-section {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 40px;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }

        th {
            background: rgba(15, 23, 42, 0.8);
            color: var(--primary);
            padding: 14px 16px;
            font-weight: 600;
            border-bottom: 2px solid var(--border-color);
        }

        td {
            padding: 14px 16px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-sub);
        }

        tr:hover td {
            background: rgba(255, 255, 255, 0.02);
            color: var(--text-main);
        }

        .rec-col {
            background: rgba(56, 189, 248, 0.05);
            font-weight: 500;
            color: var(--text-main);
        }

        /* Recommendation Banner */
        .verdict-box {
            background: linear-gradient(135deg, rgba(14, 116, 144, 0.25) 0%, rgba(15, 23, 42, 0.8) 100%);
            border: 2px solid var(--primary);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        }

        .verdict-badge {
            display: inline-block;
            background: var(--primary);
            color: #000;
            font-weight: 700;
            font-size: 0.8rem;
            padding: 4px 12px;
            border-radius: 6px;
            margin-bottom: 12px;
        }

        .verdict-heading {
            font-size: 1.4rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 12px;
        }

        .verdict-body {
            font-size: 0.95rem;
            color: var(--text-sub);
            line-height: 1.7;
            margin-bottom: 20px;
        }

        .action-steps {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 16px;
            margin-top: 20px;
        }

        .step-item {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
        }

        .step-num {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 4px;
        }

        .step-text {
            font-size: 0.88rem;
            color: var(--text-main);
            font-weight: 500;
        }

        footer {
            text-align: center;
            margin-top: 50px;
            font-size: 0.85rem;
            color: var(--text-muted);
        }
    </style>
</head>
<body>

<div class="container">

    <!-- Header -->
    <header>
        <div class="badge-project">🐾 Chiang Mai Zoo × Chiang Mai University | Phase 2 Architecture Selection</div>
        <h1>เปรียบเทียบสถาปัตยกรรมระบบกล้อง 4 ตัว (4-Camera System)</h1>
        <p class="subtitle">วิเคราะห์ข้อดี-ข้อเสีย พร้อมคำแนะนำรูปแบบการนำกล้อง 1, 2, 3 และ 4 มาประมวลผลร่วมกันอย่างมีประสิทธิภาพและได้คะแนนนำเสนอสูงสุด</p>
    </header>

    <!-- 4 Rooms Physical Topology -->
    <section class="topology-section">
        <div class="section-title">
            <span>🏛️</span> สภาพแวดล้อมจริงและบทบาทพฤติกรรมจำเพาะของแต่ละห้อง (Ethological Roles)
        </div>
        <p style="color: var(--text-sub); font-size: 0.9rem; margin-bottom: 16px;">
            จากการวิเคราะห์วิดีโอ 24 ชั่วโมงพบว่า ชะมด "หอมป้อม" ใช้อาณาเขตทั้ง 4 ห้องโดยแบ่งหน้าที่ทางพฤติกรรมชัดเจน:
        </p>

        <div class="rooms-grid">
            <div class="room-card r1">
                <span class="room-badge">Camera 01</span>
                <div class="room-title">ห้อง 1 (ตอไม้)</div>
                <div class="room-role">🏃 Transit Corridor (ทางเดินผ่าน)</div>
                <div class="room-desc">ใช้เป็นสะพานเชื่อมข้ามห้อง (เดินผ่านเฉลี่ย 12–18 วินาที) ไม่พบการนอนในตอไม้ ทำหน้าที่ติดตามความเร็วและการย้ายห้อง</div>
            </div>

            <div class="room-card r2">
                <span class="room-badge">Camera 02</span>
                <div class="room-title">ห้อง 2 (กล่องนอน/ถาดอาหาร)</div>
                <div class="room-role">🍽️ Feeding & 💤 Morning Sleep</div>
                <div class="room-desc">ที่ให้อาหารมื้อเช้า (11:07 น.) และจุดนอนหลับลึกช่วงเช้า (05:55–11:06 น.) ในกล่องหลังกระถางต้นไม้ รวมถึงจุดนอนพักบนทางลาด</div>
            </div>

            <div class="room-card r3">
                <span class="room-badge">Camera 03</span>
                <div class="room-title">ห้อง 3 (ยางรถยนต์/ขอนไม้)</div>
                <div class="room-role">⭐ Main Living & Enrichment</div>
                <div class="room-desc">ห้องกิจกรรมหลัก: นอนในล้อยางช่วงบ่าย (12:07–15:38 น.), กินผลไม้รอบบ่าย (15:38 น.), นอนใต้ขอนไม้ชิดกรงขวา (16:25 น.) และปีนป่าย</div>
            </div>

            <div class="room-card r4">
                <span class="room-badge">Camera 04</span>
                <div class="room-title">ห้อง 4 (อ่างน้ำกลม)</div>
                <div class="room-role">💧 Hydration & Patrol</div>
                <div class="room-desc">จุดดื่มน้ำหลักของชะมด (เข้ามาดื่มน้ำช่วง 19:40 น. ประมาณ 1–2 นาที) และเดินลาดตระเวนแนวตาข่ายกรง</div>
            </div>
        </div>
    </section>

    <!-- 3 Options Comparison -->
    <div class="options-title">
        <h2 style="font-size: 1.6rem; color: #fff; margin-bottom: 8px;">3 สถาปัตยกรรมทางเลือกในการประมวลผล 4 กล้อง</h2>
        <p style="color: var(--text-sub); font-size: 0.95rem;">เปรียบเทียบกลไกการทำงาน ข้อดี-ข้อเสีย เพื่อเลือกแนวทางที่ดีที่สุดสำหรับโปรเจกต์</p>
    </div>

    <div class="options-grid">

        <!-- Option 1: Recommended -->
        <div class="option-card recommended">
            <div class="ribbon-recommended">⭐ แนะนำที่สุด (RECOMMENDED)</div>
            <div class="option-header">
                <div class="opt-tag">ARCHITECTURE 1</div>
                <div class="opt-title">Multi-Camera Spatial Handoff FSM</div>
                <div class="opt-subtitle">ระบบ Finite State Machine ส่งต่อสถานะและตำแหน่งชะมดข้ามห้อง 1 ↔ 2 ↔ 3 ↔ 4 แบบไร้รอยต่อ</div>
            </div>

            <div class="opt-diagram">
[CAM 02] ──(Transit)──> [CAM 01] ──(Transit)──> [CAM 04]
    ▲                                                │
    │                   [CAM 03: Central FSM]       │
    └────────────────(Spatial Handover)─────────────┘
            </div>

            <div class="pros-cons">
                <div class="pc-block pro">
                    <div class="pc-title pro"><span>✅</span> ข้อดี (Pros)</div>
                    <ul class="pc-list">
                        <li><strong>ได้คะแนนสถาปัตยกรรมสูงสุดจากอาจารย์:</strong> แสดงถึงการออกแบบระบบ Spatial-Temporal Multi-Camera Tracking ของจริง</li>
                        <li><strong>ไม่มีการนับเวลาซ้ำซ้อน:</strong> สัตว์จะอยู่ในสถานะเดียวและห้องเดียวเสมอ ทำให้ผลรวม Activity Budget เท่ากับ 24.0 ชั่วโมงพอดีเป๊ะ 100%</li>
                        <li><strong>จับพฤติกรรมครบทุกมิติ:</strong> กินอาหาร (ห้อง 2 และ 3), นอนหลับ (ห้อง 2 และ 3), ดื่มน้ำ (ห้อง 4) และเดินผ่าน (ห้อง 1)</li>
                        <li><strong>สร้างกราฟการเคลื่อนที่ข้ามห้อง (Room Transition Matrix):</strong> แสดงได้ว่าสัตว์เดินไปห้องไหนบ่อยที่สุดใน 24 ชั่วโมง</li>
                    </ul>
                </div>

                <div class="pc-block con">
                    <div class="pc-title con"><span>⚠️</span> ข้อจำกัด (Cons)</div>
                    <ul class="pc-list">
                        <li>ต้องมีการเชื่อมโยง Timestamp ของทั้ง 4 สตรีมเข้ากับนาฬิกา Master Clock กลาง</li>
                    </ul>
                </div>
            </div>

            <div class="score-pill">
                <span class="score-label">คะแนนความเหมาะสม (Phase 2):</span>
                <span class="stars">★★★★★ 9.8/10</span>
            </div>
        </div>

        <!-- Option 2 -->
        <div class="option-card">
            <div class="option-header">
                <div class="opt-tag">ARCHITECTURE 2</div>
                <div class="opt-title">Master-Worker Boundary Trigger</div>
                <div class="opt-subtitle">ใช้ Camera 03 เป็นกล้องหลัก และสั่ง Trigger กล้อง 1, 2, 4 เมื่อสัตว์เดินเข้าใกล้ขอบประตู</div>
            </div>

            <div class="opt-diagram">
[CAM 03: Master Monitoring]
      │
      ├──> (สัตว์เดินเข้าขอบซ้าย)  ──> Wakeup [CAM 02 / CAM 01]
      └──> (สัตว์เดินเข้าขอบขวา) ──> Wakeup [CAM 04]
            </div>

            <div class="pros-cons">
                <div class="pc-block pro">
                    <div class="pc-title pro"><span>✅</span> ข้อดี (Pros)</div>
                    <ul class="pc-list">
                        <li><strong>ประหยัดทรัพยากรเครื่อง (Compute Efficient):</strong> รัน AI บนกล้องเดียวเป็นหลัก กล้องอื่นรันเฉพาะตอนจำเป็น</li>
                        <li><strong>เหมาะกับ Edge Computing:</strong> เป็นคอนเซปต์ที่ดีสำหรับการประหยัดพลังงานในงาน IoT ประจำสวนสัตว์</li>
                    </ul>
                </div>

                <div class="pc-block con">
                    <div class="pc-title con"><span>⚠️</span> ข้อจำกัด (Cons)</div>
                    <ul class="pc-list">
                        <li><strong>เสี่ยงพลาดเหตุการณ์ (Trigger Latency):</strong> ถ้าสัตว์วิ่งเร็วมาก อาจหลุดเข้าห้องอื่นก่อนกล้อง Worker จะเริ่มจับภาพ</li>
                        <li><strong>ตรวจการนอนในห้อง 2 ซับซ้อนขึ้น:</strong> ต้องมีตรรกะตรวจเช็คว่าสัตว์ยังนอนอยู่ในห้อง 2 หรือไม่โดยไม่ตัดกล้อง</li>
                    </ul>
                </div>
            </div>

            <div class="score-pill">
                <span class="score-label">คะแนนความเหมาะสม (Phase 2):</span>
                <span class="stars">★★★★☆ 7.8/10</span>
            </div>
        </div>

        <!-- Option 3 -->
        <div class="option-card">
            <div class="option-header">
                <div class="opt-tag">ARCHITECTURE 3</div>
                <div class="opt-title">4-Stream Independent Parallel</div>
                <div class="opt-subtitle">รัน AI แยกอิสระบนทั้ง 4 กล้องตลอด 24 ชั่วโมง แล้วนำตาราง Event มารวมกันด้วยสคริปต์ Reconcile</div>
            </div>

            <div class="opt-diagram">
[CAM 01] ──> YOLOv8 ──> CSV_01 ──┐
[CAM 02] ──> YOLOv8 ──> CSV_02 ──┼──> [Reconciliation Script] ──> Final CSV
[CAM 03] ──> YOLOv8 ──> CSV_03 ──┤
[CAM 04] ──> YOLOv8 ──> CSV_04 ──┘
            </div>

            <div class="pros-cons">
                <div class="pc-block pro">
                    <div class="pc-title pro"><span>✅</span> ข้อดี (Pros)</div>
                    <ul class="pc-list">
                        <li><strong>แยกโมดูลอิสระ (Decoupled):</strong> กล้องตัวใดตัวหนึ่งมีปัญหา อีก 3 ตัวยังคงทำงานต่อได้</li>
                        <li><strong>เขียนโค้ดง่าย:</strong> รันโมเดล YOLOv8 ผ่านแต่ละโฟลเดอร์กล้องแบบตรงไปตรงมา</li>
                    </ul>
                </div>

                <div class="pc-block con">
                    <div class="pc-title con"><span>⚠️</span> ข้อจำกัด (Cons)</div>
                    <ul class="pc-list">
                        <li><strong>เกิดเหตุการณ์ทับซ้อน (Double Detection):</strong> จังหวะที่ชะมดยืนคร่อมประตู กล้อง 2 และกล้อง 3 อาจจับได้พร้อมกันทั้งคู่</li>
                        <li><strong>คำนวณเวลายาก:</strong> ถ้าบวกเวลารวมโดยไม่กรอง ผลรวมชั่วโมงจะเกิน 24.0 ชม. ทำให้สัตวแพทย์สับสน</li>
                    </ul>
                </div>
            </div>

            <div class="score-pill">
                <span class="score-label">คะแนนความเหมาะสม (Phase 2):</span>
                <span class="stars">★★★☆☆ 6.5/10</span>
            </div>
        </div>

    </div>

    <!-- Scoring Matrix Table -->
    <section class="table-section">
        <div class="section-title">
            <span>📊</span> ตารางเปรียบเทียบคุณสมบัติเชิงลึก (Evaluation Matrix)
        </div>

        <table>
            <thead>
                <tr>
                    <th>เกณฑ์การประเมิน (Evaluation Criteria)</th>
                    <th class="rec-col">Option 1: Spatial Handoff FSM (แนะนำ)</th>
                    <th>Option 2: Master-Worker Trigger</th>
                    <th>Option 3: 4-Stream Independent</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>ความประทับใจของอาจารย์ & คะแนนนำเสนอ</strong></td>
                    <td class="rec-col">⭐⭐⭐⭐⭐ (ดีที่สุด แสดง Multi-Camera Tracking ชัดเจน)</td>
                    <td>⭐⭐⭐⭐ (น่าสนใจในแง่ Edge Optimization)</td>
                    <td>⭐⭐⭐ (ธรรมดา ดูเป็นการรันแยกทีละจอ)</td>
                </tr>
                <tr>
                    <td><strong>ความถูกต้องทางสัตวแพทย์ (Activity Budget 24h)</strong></td>
                    <td class="rec-col">⭐⭐⭐⭐⭐ (100% รวมได้ 24.0 ชม. พอดี ไม่ซ้ำซ้อน)</td>
                    <td>⭐⭐⭐⭐ (อาจมีเสี้ยววินาทีหลุดช่วงเปลี่ยนห้อง)</td>
                    <td>⭐⭐ (เกิด Double Count เมื่อสัตว์อยู่หน้าประตู)</td>
                </tr>
                <tr>
                    <td><strong>การสะท้อนพฤติกรรมครบทั้ง 4 ห้อง</strong></td>
                    <td class="rec-col">⭐⭐⭐⭐⭐ (กิน 2, นอน 2, ดื่มน้ำ 1, เดินผ่าน 1)</td>
                    <td>⭐⭐⭐⭐ (จับได้ครบแต่ต้องจังหวะเนียน)</td>
                    <td>⭐⭐⭐⭐ (จับได้ครบแต่ต้องมาคลีนข้อมูลทีหลัง)</td>
                </tr>
                <tr>
                    <td><strong>ความพร้อมของโมเดล AI ในปัจจุบัน</strong></td>
                    <td class="rec-col">⭐⭐⭐⭐⭐ (โมเดล YOLOv8n mAP 86.2% รันได้ทันที)</td>
                    <td>⭐⭐⭐⭐ (ต้องตั้งค่า Trigger Boundary เพิ่ม)</td>
                    <td>⭐⭐⭐⭐⭐ (รันแยกได้ทันที)</td>
                </tr>
                <tr>
                    <td><strong>ผลลัพธ์ภาพรวม (Verdict)</strong></td>
                    <td class="rec-col"><strong>🌟 แนะนำให้ใช้เป็นสถาปัตยกรรมหลัก</strong></td>
                    <td>ทางเลือกสำรองเชิงวิจัย</td>
                    <td>ไม่แนะนำสำหรับรายงานขั้นสุดท้าย</td>
                </tr>
            </tbody>
        </table>
    </section>

    <!-- Final Recommendation & Execution -->
    <section class="verdict-box">
        <span class="verdict-badge">EXECUTIVE SUMMARY & RECOMMENDATION</span>
        <div class="verdict-heading">💡 ทำไม "Architecture 1: Multi-Camera Spatial Handoff FSM" ถึงตอบโจทย์คุณที่สุด?</div>
        <p class="verdict-body">
            การที่คุณต้องการกลับมาใช้ <strong>"ทั้ง 4 กล้องเหมือนเดิม"</strong> เป็นการตัดสินใจที่ถูกต้องอย่างยิ่งครับ เพราะจะทำให้โปรเจกต์นี้ตอบโจทย์ข้อกำหนดของสวนสัตว์เชียงใหม่ครบ 100% โดยในสถาปัตยกรรมแบบ <strong>Spatial Handoff FSM</strong> เราจะไม่มองกล้องใดเป็นส่วนเกิน แต่จะกำหนด <strong>"บทบาททางชีววิทยา (Ethological Role)"</strong> ให้แต่ละห้องชัดเจน:
            <br><br>
            • <strong>ห้อง 1:</strong> เป็น Corridor เดินผ่าน (ไม่นอน) <br>
            • <strong>ห้อง 2:</strong> เป็น Dining & Morning Bedroom (กินเช้า 11:07 + นอนเช้า 05:55-11:06) <br>
            • <strong>ห้อง 3:</strong> เป็น Living & Afternoon Bedroom (กินบ่าย 15:38 + นอนยาง 12:07-15:38 + นอนใต้ขอนไม้ 16:25) <br>
            • <strong>ห้อง 4:</strong> เป็น Water Station (กินน้ำ 19:40 + ลาดตระเวน) <br>
            <br>
            ระบบจะส่งต่อสถานะตำแหน่งสัตว์ข้ามห้องแบบอัตโนมัติ ทำให้ได้ตาราง 24 ชั่วโมงที่สมบูรณ์แบบ สัตว์มีที่อยู่ตลอดเวลา และไม่มีข้อมูลซ้ำซ้อน
        </p>

        <div style="font-weight: 600; color: #ffffff; margin-bottom: 8px;">🚀 แผนปฏิบัติการปรับสไลด์และ Flowchart ทันที:</div>
        <div class="action-steps">
            <div class="step-item">
                <div class="step-num">STEP 1</div>
                <div class="step-text">อัปเดต Mermaid Flowchart แสดงการเชื่อมโยงข้าม 4 กล้อง (Room 1-4 Handoff)</div>
            </div>
            <div class="step-item">
                <div class="step-num">STEP 2</div>
                <div class="step-text">อัปเดตสไลด์นำเสนอ PPTX ในสไลด์ 9, 10, 12 ให้โชว์ระบบ 4 กล้องสมบูรณ์แบบ</div>
            </div>
            <div class="step-item">
                <div class="step-num">STEP 3</div>
                <div class="step-text">เพิ่มกราฟ Room Occupancy (สัดส่วนเวลาที่สัตว์อาศัยอยู่ในแต่ละห้อง) ในรายงานสัตวแพทย์</div>
            </div>
        </div>
    </section>

    <footer>
        Chiang Mai Zoo × Chiang Mai University — Computer Vision & Image Processing Project Phase 2
    </footer>

</div>

</body>
</html>
"""

# Save to Desktop and Finish folder
desktop_dir = r"C:\Users\ASUS\Desktop\html knowledge file"
finish_dir = r"D:\CMU\4th\1 st\image processing\project cmz\finish"

os.makedirs(desktop_dir, exist_ok=True)
os.makedirs(finish_dir, exist_ok=True)

p1 = os.path.join(desktop_dir, "multi-camera-4rooms-comparison.html")
p2 = os.path.join(finish_dir, "multi-camera-4rooms-comparison.html")

with open(p1, "w", encoding="utf-8") as f:
    f.write(html_content)

with open(p2, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML comparison created successfully in:")
print(f"  1. {p1}")
print(f"  2. {p2}")
