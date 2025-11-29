# main.py
import json
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
import prompts

load_dotenv()

# Kiểm tra Key & Base URL
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError("OPENAI_API_KEY is missing")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# --- UTILS ---
def read_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- LAYER 1: DATA ANALYST (UPDATED) ---
def run_layer_1():
    print("\n--- PROCESSING LAYER 1 ---")
    
    logs = read_json('data/daily_logs.json')
    if not logs: return

    formatted_prompt = prompts.LAYER_1_USER_PROMPT.format(logs=json.dumps(logs))

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompts.LAYER_1_SYSTEM_ROLE},
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=0
        )
        
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "")

        full_data = json.loads(content)

        # --- LOGIC MỚI ĐỂ TÁCH SUMMARY ---
        # 1. Lấy đoạn văn ra riêng
        summary_text = full_data.get("narrative", "")
        
        # 2. Tạo một bản copy chỉ chứa dữ liệu cấu trúc (xóa narrative đi)
        structured_report = full_data.copy()
        if "narrative" in structured_report:
            del structured_report["narrative"]

        # 3. Lưu file (Lưu cái có cấu trúc để Layer 2 dùng)
        save_json('data/report_layer_1.json', structured_report)

        # 4. OUTPUT THEO ĐÚNG FORMAT BẠN CẦN
        # Dòng 1: JSON dữ liệu
        print(f"Report:{json.dumps(structured_report)}")
        # Dòng 2: Đoạn văn mô tả
        print(f"SUMMARY:{summary_text}")
        
    except Exception as e:
        print(f"Layer 1 Error: {e}")

# --- LAYER 2: ADVISOR (Giữ nguyên) ---
def run_layer_2():
    print("\n--- PROCESSING LAYER 2 ---")

    report_data = read_json('data/report_layer_1.json')
    medical_data = read_json('data/medical_records.json')
    
    if not report_data or not medical_data:
        print("Missing input files. Run Layer 1 first.")
        return

    formatted_prompt = prompts.LAYER_2_USER_PROMPT.format(
        report=json.dumps(report_data),
        records=json.dumps(medical_data)
    )

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompts.LAYER_2_SYSTEM_ROLE},
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=0.7
        )

        advice_text = response.choices[0].message.content.strip()

        final_data = {"suggestion": advice_text, "source": report_data}
        save_json('data/final_advice.json', final_data)

        print(f"Suggestion:{advice_text}")

    except Exception as e:
        print(f"Layer 2 Error: {e}")

# --- ROUTER CONTROL ---
def main():
    while True:
        print("\n=== SYSTEM MENU ===")
        print("1. Run Layer 1")
        print("2. Run Layer 2")
        print("3. Exit")
        choice = input("Select: ")

        if choice == '1':
            run_layer_1()
        elif choice == '2':
            run_layer_2()
        elif choice == '3':
            sys.exit()

if __name__ == "__main__":
    main()