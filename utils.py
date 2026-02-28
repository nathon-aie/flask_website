import json


def calculate_total_materials(json_data):
    """
    ฟังก์ชันสำหรับคำนวณและรวมจำนวนไอเทมทั้งหมดจาก JSON ของ Materials

    Parameters:
        json_data (str): ข้อมูล JSON string ที่เก็บวัสดุแยกตามระดับ

    Returns:
        tuple: (dict ของวัสดุแยกตามระดับ, list ของวัสดุทั้งหมดที่รวมแล้ว)
    """
    # ตรวจสอบว่ามีข้อมูลหรือไม่ ถ้าไม่มีให้คืนค่า dict และ list เปล่า
    if not json_data:
        return {}, []

    # แปลง JSON string เป็น dictionary
    mats_dict = json.loads(json_data)

    # สร้าง dictionary เปล่าสำหรับเก็บผลรวมของวัสดุแต่ละชนิด
    total_dict = {}

    # วนลูปผ่านแต่ละระดับและไอเทมในแต่ละระดับ
    for level, items in mats_dict.items():
        for item in items:
            # ดึงชื่อไอเทม
            name = item["name"]

            # ถ้าไอเทมนี้มีอยู่แล้วใน total_dict ให้บวกจำนวนเพิ่ม
            if name in total_dict:
                total_dict[name]["amount"] += item["amount"]
            else:
                # ถ้ายังไม่มี ให้สร้างรายการใหม่พร้อมข้อมูลชื่อ ไอคอน และจำนวน
                total_dict[name] = {
                    "name": name,
                    "icon": item["icon"],
                    "amount": item["amount"],
                }

    # คืนค่า dictionary แบบแยกตามระดับ และ list ของวัสดุทั้งหมดที่รวมแล้ว
    return mats_dict, list(total_dict.values())
