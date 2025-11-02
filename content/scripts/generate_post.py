import os
import requests
from datetime import date
import base64

# ===========================
# مقادیر ثابت (Secrets جایگذاری شده)
# ===========================
GEMINI_API_KEY = "AIzaSyAtPtlYFt3ywP_muneh0G2TzxDAZPiI2i8"
WP_URL = "https://arenapc.shop/wp-json/wp/v2/posts"
WP_USER = "ayhan"
WP_APP_PASSWORD = "RKf9 17cU kEJ7 Mrz7 l9Is yYno"

# ===========================
# نام فایل Markdown روزانه
# ===========================
today = date.today()
file_name = f"content/{today}.md"

# ===========================
# تولید محتوا از Gemini AI
# ===========================
def generate_content():
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": "یک پست تکنولوژی کوتاه و جذاب برای وبلاگ بنویس",
        "max_output_tokens": 500
    }
    response = requests.post(
        "https://gemini.googleapis.com/v1beta2/text:generate",
        json=data,
        headers=headers
    )
    try:
        content = response.json().get("output_text", "محتوا آماده نشد")
    except Exception as e:
        content = f"خطا در دریافت محتوا: {e}"
    return content

# ===========================
# ذخیره محتوا در Markdown
# ===========================
content = generate_content()
os.makedirs("content", exist_ok=True)
with open(file_name, "w", encoding="utf-8") as f:
    f.write(content)

# ===========================
# ارسال به وردپرس
# ===========================
def post_to_wordpress(content):
    # Basic Auth با نام کاربری و Application Password
    auth_str = f"{WP_USER}:{WP_APP_PASSWORD}"
    auth_bytes = auth_str.encode("utf-8")
    auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")
    
    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/json"
    }
    data = {
        "title": f"پست {today}",
        "content": content,
        "status": "publish"
    }
    try:
        r = requests.post(WP_URL, json=data, headers=headers)
        print(f"Status Code: {r.status_code}")
        print(r.text)
    except Exception as e:
        print(f"خطا در ارسال به وردپرس: {e}")

post_to_wordpress(content)
