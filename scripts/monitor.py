import requests
import csv
import time
import datetime
import pytz
import os
import speedtest

print("Menjalankan speedtest...")

try:
    st = speedtest.Speedtest()
    try:
        st.get_servers([45311, 3697, 62263]) 
    except Exception:
        st.get_servers([]) 
    st.get_best_server()
    download = round(st.download() / 1_000_000, 2)
    upload = round(st.upload() / 1_000_000, 2)
    ping = round(st.results.ping, 2)
except Exception as e:
    print("Speedtest gagal:", e)
    download = upload = ping = 0.0

# Daftar website ITS
urls = [
    "https://portal.its.ac.id",
    "https://classroom.its.ac.id",
    "https://presensi.its.ac.id"
]

# Timestamp dengan zona waktu Surabaya (Asia/Jakarta)
zona = pytz.timezone("Asia/Jakarta")
timestamp = datetime.datetime.now(zona).strftime("%Y-%m-%d %H:%M:%S WIB")

# File hasil
workspace = os.getenv("GITHUB_WORKSPACE", ".")
filename = os.path.join(workspace, "hasil_pengujian.csv")

# Header CSV
header = [
    "timestamp",
    "url",
    "status_code",
    "total_bytes",
    "elapsed_time",
    "ping_ms",
    "download_Mbps",
    "upload_Mbps"
]

rows = []
for url in urls:
    try:
        start = time.time()
        response = requests.get(url, timeout=20)
        end = time.time()
        elapsed = round(end - start, 3)
        total_bytes = len(response.content)
        status_code = response.status_code
    except Exception:
        elapsed = 0
        total_bytes = 0
        status_code = 0
    rows.append([timestamp, url, status_code, total_bytes, elapsed, ping, download, upload])

# Simpan ke CSV 
try:
    with open(filename, "x", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
except FileExistsError:
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

print("Pengujian selesai. Hasil disimpan di", filename)
