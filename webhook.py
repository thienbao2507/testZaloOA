from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/zalo-webhook', methods=['POST'])
def zalo_webhook():
    data = request.get_json()
    print("✅ Nhận webhook:", data)

    try:
        # Kiểm tra nếu là sự kiện tin nhắn từ user
        if data.get('event_name') == 'user_send_text':
            user_id = data['sender']['id']
            msg = data['message']
            print(f"User {user_id} gửi tin nhắn: {msg}")

        elif data.get('event_name') == 'user_send_image':
            user_id = data['sender']['id']
            image_list = data['message']['attachments']
            for img in image_list:
                img_url = img['payload']['url']
                download_image(img_url, user_id)
    except Exception as e:
        print("❌ Lỗi xử lý webhook:", e)

    return jsonify({"status": "received"})

def download_image(url, user_id):
    resp = requests.get(url)
    filename = f"image_from_{user_id}.jpg"
    with open(filename, 'wb') as f:
        f.write(resp.content)
    print(f"💾 Đã lưu ảnh: {filename}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
