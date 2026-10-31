p = r'D:\CMU\4th\1 st\image processing\project cmz\scripts\build_phase2_outcomes_first_slides.py'
with open(p, 'r', encoding='utf-8') as f:
    text = f.read()

target1 = 'p.text = "1. สลับกล้องอัตโนมัติ & พิมพ์บันทึก CSV สด (Multi-Cam Handoff)"'
repl1 = 'p.text = "1. สลับกล้องอัตโนมัติ & พิมพ์บันทึก CSV สด (04:39 Unified Sync)"'

target2 = 'p.text = "2. การนอนในที่หลบภัย & ตรวจสอบ 4 กล้องพร้อมกัน (Shelter Sleep Sync)"'
repl2 = 'p.text = "2. การนอนในที่หลบภัย & ตรวจสอบ 4 กล้องเวลาเดียวกัน (04:39 Sync)"'

text = text.replace(target1, repl1)
text = text.replace(target2, repl2)

with open(p, 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated Slide 5 titles.")
