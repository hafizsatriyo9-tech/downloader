from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"

if not os.path.exists(DOWNLOAD_DIR):
    os.mkdir(DOWNLOAD_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    msg = "⏳ Downloading..."

    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'outtmpl': f'{DOWNLOAD_DIR}/%(id)s.%(ext)s',
        'restrictfilenames': True,
        'retries': 5,
        'socket_timeout': 30,
        'format': 'mp4/best',
        'merge_output_format': 'mp4',
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            
            # Download video
            ydl.download([url])
            
        # Kirim file sebagai response
        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"❌ Gagal download.\nError: {e}"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
