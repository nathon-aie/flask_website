import json


def calculate_total_materials(json_data):
    """ฟังก์ชันช่วยรวมจำนวนไอเทมจาก JSON ของ Materials"""
    if not json_data:
        return {}, []

    mats_dict = json.loads(json_data)
    total_dict = {}

    for level, items in mats_dict.items():
        for item in items:
            name = item["name"]
            if name in total_dict:
                total_dict[name]["amount"] += item["amount"]
            else:
                total_dict[name] = {
                    "name": name,
                    "icon": item["icon"],
                    "amount": item["amount"],
                }
    return mats_dict, list(total_dict.values())
