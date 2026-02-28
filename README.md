# Basic FGO Database

## จัดทำโดย:

ชื่อ: นายพลกฤต บัวลอย  
รหัสนักศคึกษา: 6810110223  

---

## ภาพรวม

เว็บที่สร้างด้วย Flask เพื่อแสดงข้อมูลเกี่ยวกับตัวละคร (Servant) ในเกม Fate/Grand Order (FGO) เว็บจะดึงข้อมูลตัวละครจาก Atlas Academy API จัดเก็บในฐานข้อมูล SQLite 
และมี Interface ที่สามารถดูรายละเอียดตัวละครได้

---

## โครงสร้างโครงการ

### **app.py** - เซิร์ฟเวอร์แอปพลิเคชัน Flask
ใช้จัดการการกำหนดเส้นทางและการแสดงผลหน้าเว็บ

```
- เริ่มต้น Flask app ด้วยการตั้งค่าฐานข้อมูล SQLite
- "/" และ "/class/all" → แสดงตัวละครทั้งหมดในแกลเลอรี่
- "/class/<class_name>" → กรองตัวละครตามคลาส
- "/servant/<id>/<name>" → แสดงข้อมูลโดยละเอียดของตัวละครที่เลือก
  (ใช้ฟังก์ชันช่วยในการคำนวณวัสดุทั้งหมดที่ต้องการสำหรับการอัพเกรด)
```

---

### **models.py** - แบบจำลองฐานข้อมูล
กำหนดโครงสร้างฐานข้อมูล (Schema) สำหรับการเก็บข้อมูลตัวละคร

```
คอลัมน์ตาราง Servant:
- ข้อมูลพื้นฐาน: servant_id, name, class_name, rarity, cost
- สถิติ: atk_base, atk_max, hp_base, hp_max
- ข้อมูลตัวละคร: gender, attribute, traits
- รูปภาพ: graph_url_asc1-4, costume URLs
- ข้อมูลเกมเพลย์: active_skill, append_skill, noble_phantasms (เก็บเป็น JSON)
- วัสดุ: ascension_materials, skill_materials, append_skill_materials (เก็บเป็น JSON)
```

**Properties:**
- `costumes_list` - แยกวิเคราะห์ URL ของรูปประมาณ
- `skills_list` - แปลงข้อมูล JSON Active Skills เป็นลิสต์ Python
- `append_skills_list` - แปลงข้อมูล JSON Append Skills เป็นลิสต์ Python
- `nps_list` - แปลงข้อมูล JSON NP เป็นลิสต์ Python

---

### **utils.py** - ฟังก์ชันช่วยเหลือ
มีฟังก์ชันช่วยเหลือสำหรับประมวลผลข้อมูลวัสดุ

```
calculate_total_materials(json_data)
  - แยกวิเคราะห์ข้อมูลวัสดุ JSON จากฐานข้อมูล
  - รวมวัสดุจากทุกระดับ
  - คืนค่า: (Materials, Total Materials)
  
ใช้ใน: การแสดงข้อกำหนดวัสดุสำหรับการเสริมอำนาจ/การอัพเกรดทักษะ
```

---

### **pull_data.py** - สคริปต์นำเข้าข้อมูล
ดึงข้อมูลตัวละครจาก Atlas Academy API และเติมข้อมูลลงในฐานข้อมูล

```json
กระบวนการ:
1. ลบฐานข้อมูลเดิมและสร้างตารางใหม่
2. ดึงข้อมูลตัวละครทั้งหมดจาก: https://api.atlasacademy.io/export/NA/nice_servant.json
3. กรองเฉพาะตัวละครประเภท normal และ heroine
4. สำหรับตัวละครแต่ละตัว:
   - แยกและจัดรูปแบบลักษณะเฉพาะและ URL ของ Costume
   - ประมวลผลวัสดุ (Ascension, Active Skills, Append Skills) เป็นรูปแบบที่อ่านง่าย
   - แยกวิเคราะห์ NP พร้อมคำอธิบายที่ clean เรียบร้อยs
   - เรียงลำดับ Skills ตามหมายเลข
   - เก็บทุกอย่างในตาราง Servant
5. บันทึก ~400+ ตัวละครลงในฐานข้อมูล
```

---

### **templates/**
เทมเพลต HTML สำหรับการแสดงผลหน้าเว็บด้วยสไตล์ Bootstrap 5

- **index.html** - Gallery แสดงตัวละครทั้งหมดพร้อมปุ่มกรอง Class
- **servant_detail.html** - มุมมองโดยละเอียดพร้อมข้อมูลพื้นฐาน Materials Skills และ Noble Phantasm

---

## การรัน

### **ข้อกำหนดเบื้องต้น**
- Python 3.7 ขึ้นไป
- pip

### **ขั้นตอนที่ 1: Install**

เปิด PowerShell ในไดเรกทอรีของโครงการและรัน:

```powershell
# สร้างสภาพแวดล้อมเสมือน
python -m venv .venv

# เปิดใช้งานสภาพแวดล้อมเสมือน
.\.venv\Scripts\Activate.ps1

# ติดตั้งแพ็คเกจที่ต้องการ
pip install flask flask-sqlalchemy requests
```

### **ขั้นตอนที่ 2: นำเข้าข้อมูลตัวละคร**

รันสคริปต์ดึงข้อมูลเพื่อเติมข้อมูลลงในฐานข้อมูล SQLite:

```powershell
python pull_data.py
```

สิ่งนี้จะ:
- สร้างฐานข้อมูล SQLite `servants.db` ใหม่ในโฟลเดอร์ `instance/`
- ดึงและประมวลผล ~400+ ตัวละครจาก Atlas Academy API
- ใช้เวลาประมาณ 1-2 นาทีในการทำให้สำเร็จ
- ผลลัพธ์: `[+] Saved XXX servants to SQLite.`

### **ขั้นตอนที่ 3: รัน Server Flask**

เริ่มต้นเซิร์ฟเวอร์การพัฒนา:

```powershell
python app.py
```

ผลลัพธ์:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### **ขั้นตอนที่ 4: เข้าถึงเว็บไซต์**

เปิดเว็บเบราว์เซอร์และไปที่:

```
http://localhost:5000
```

---

## วิธีการใช้งาน

1. **เรียกดูตัวละครทั้งหมด** - คลิก "All Servants" เพื่อดู Gallery ที่สมบูรณ์
2. **กรองตามคลาส** - ใช้ปุ่มเพื่อดูตัวละครตาม Class
3. **ดูรายละเอียด** - คลิกที่การ์ดตัวละครใดๆ เพื่อดู:
   - รูปแบบการเสริมอำนาจของตัวละคร
   - Stats พื้นฐานและสูงสุด (ATK/HP)
   - Attributes, Traits
   - Active Skills
   - Append Skills
   - Noble Phantasm
   - Ascension Materials
   - Active Skills Materials
   - Append Skills Materials

---

## เทคโนโลยีที่ใช้

- **Backend:** Flask
- **ฐานข้อมูล:** SQLite กับ SQLAlchemy ORM
- **Frontend:** HTML, CSS, Bootstrap 5
- **เทมเพลต:** Jinja2
- **แหล่งข้อมูล:** Atlas Academy API

---

## หมายเหตุ

- ตำแหน่งไฟล์ฐานข้อมูล: `instance/servants.db`
- รัน `python pull_data.py` อีกครั้งได้ตลอดเวลาเพื่อรีเฟรชข้อมูลจาก API
- แอปพลิเคชันทำงานในโหมดการตรวจสอบโดยค่าเริ่มต้น (โหลดซ้ำอัตโนมัติเมื่อมีการเปลี่ยนแปลงโค้ด)
- สำหรับการปรับใช้งานเชิงผลิตภาพ ให้เปลี่ยน `app.run(debug=False)`

---

## การแก้ปัญหา

**ปัญหา:** "ModuleNotFoundError: No module named 'flask'"  
**วิธีแก้:** รัน `pip install flask flask-sqlalchemy requests`

**ปัญหา:** การทำงานฐานข้อมูลช้า  
**วิธีแก้:** เป็นเรื่องปกติในการรันครั้งแรก ฐานข้อมูลจะถูกสร้างและเติมข้อมูลครั้งเดียว

**ปัญหา:** ไม่สามารถเชื่อมต่อกับ localhost:5000  
**วิธีแก้:** ตรวจสอบให้แน่ใจว่าเซิร์ฟเวอร์ Flask กำลังทำงานและไม่มีบริการอื่นใช้พอร์ต 5000
