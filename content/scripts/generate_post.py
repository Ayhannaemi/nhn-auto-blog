import os
import requests
from datetime import date

# Gemini API key
GEMINI_API_KEY = os.environ.get("AIzaSyAtPtlYFt3ywP_muneh0G2TzxDAZPiI2i8")

# WordPress API
WP_URL = os.environ.get("https://arenapc.shop/wp-json/wp/v2/posts")  # مثلا https://example.com/wp-json/wp/v2/posts
WP_TOKEN = os.environ.get("
define('JWT_AUTH_SECRET_KEY', '6f#r3HrZ@jbn4+J-[Th>Kn{5%13^Di#4(($d6(gq*.3LXtSNnuO;)ezXBU[M$,VU');")  # JWT token

# امروز
today = date.today()
file_name = f"content/{today}.md"

# 1. گرفتن محتوا از Gemini
def generate_content():
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": "یک پست تکنولوژی کوتاه و جذاب برای وبلاگ بنویس",
        "max_output_tokens": 500
    }
    response = requests.post("https://gemini.googleapis.com/v1beta2/text:generate", json=data, headers=headers)
    content = response.json().get("output_text", "محتوا آماده نشد")
    return content

# 2. ذخیره در فایل Markdown
content = generate_content()
with open(file_name, "w", encoding="utf-8") as f:
    f.write(content)

# 3. ارسال به وردپرس
def post_to_wordpress(content):
    headers = {
        "Authorization": f"Bearer {WP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "title": f"پست {today}",
        "content": content,
        "status": "publish"
    }
    r = requests.post(WP_URL, json=data, headers=headers)
    print(r.status_code, r.text)

post_to_wordpress(content)
