import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import re
from selenium.webdriver.common.keys import Keys
import pyautogui
import pyperclip
import subprocess
import os
import platform

class AccountCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filmora Credit Farm - Account Creator Pro")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        
        # Biến để kiểm soát việc dừng
        self.stop_flag = False
        self.is_running = False
        
        # Danh sách User Agents để rotation
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        # Tạo giao diện
        self.create_widgets()
        
    def reset_network_ip(self):
        """Reset IP mạng thông qua việc restart network adapter"""
        try:
            self.log("🔄 Đang reset IP mạng...")
            
            if platform.system() == "Windows":
                # Lấy danh sách network adapters
                result = subprocess.run(['netsh', 'interface', 'show', 'interface'], 
                                      capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    # Tìm adapter đang hoạt động (Connected)
                    lines = result.stdout.split('\n')
                    active_adapters = []
                    
                    for line in lines:
                        if 'Connected' in line and ('Wi-Fi' in line or 'Ethernet' in line or 'Local Area Connection' in line):
                            parts = line.split()
                            if len(parts) >= 4:
                                adapter_name = ' '.join(parts[3:])
                                active_adapters.append(adapter_name.strip())
                    
                    if active_adapters:
                        adapter_name = active_adapters[0]  # Lấy adapter đầu tiên
                        self.log(f"📡 Đang reset adapter: {adapter_name}")
                        
                        # Disable adapter
                        subprocess.run(['netsh', 'interface', 'set', 'interface', adapter_name, 'disabled'], 
                                     timeout=15, check=False)
                        time.sleep(3)
                        
                        # Enable adapter
                        subprocess.run(['netsh', 'interface', 'set', 'interface', adapter_name, 'enabled'], 
                                     timeout=15, check=False)
                        
                        self.log("⏳ Đợi adapter kết nối lại...")
                        time.sleep(8)
                        
                        # Flush DNS
                        subprocess.run(['ipconfig', '/flushdns'], timeout=10, check=False)
                        
                        # Release và renew IP
                        subprocess.run(['ipconfig', '/release'], timeout=15, check=False)
                        time.sleep(2)
                        subprocess.run(['ipconfig', '/renew'], timeout=20, check=False)
                        
                        self.log("✅ Reset IP mạng thành công!")
                        time.sleep(5)  # Đợi thêm để đảm bảo kết nối ổn định
                        
                    else:
                        self.log("⚠️ Không tìm thấy adapter mạng hoạt động")
                        
            else:
                # Linux/Mac - restart network manager
                self.log("🐧 Đang reset mạng trên Linux/Mac...")
                try:
                    subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], timeout=15, check=False)
                    time.sleep(5)
                    self.log("✅ Reset mạng thành công!")
                except:
                    self.log("⚠️ Cần quyền sudo để reset mạng trên Linux/Mac")
                    
        except subprocess.TimeoutExpired:
            self.log("⚠️ Timeout khi reset mạng, tiếp tục...")
        except Exception as e:
            self.log(f"⚠️ Lỗi khi reset IP mạng: {str(e)}")
            self.log("🔄 Tiếp tục mà không reset IP...")
            
    def get_random_user_agent(self):
        """Lấy User Agent ngẫu nhiên"""
        return random.choice(self.user_agents)
        
    def add_random_delay(self, min_delay=1, max_delay=3):
        """Thêm delay ngẫu nhiên để tránh detection"""
        delay = random.uniform(min_delay, max_delay)
        self.log(f"⏳ Delay ngẫu nhiên: {delay:.1f}s")
        time.sleep(delay)

    def create_widgets(self):
        # Frame chính
        main_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Tiêu đề
        title_label = tk.Label(main_frame, text="🎬 FILMORA CREDIT FARM", 
                              font=('Arial', 24, 'bold'), 
                              fg='#e74c3c', bg='#2c3e50')
        title_label.pack(pady=(0, 30))
        
        # Frame cấu hình
        config_frame = tk.LabelFrame(main_frame, text="Cấu Hình", 
                                   font=('Arial', 12, 'bold'),
                                   fg='#ecf0f1', bg='#34495e', 
                                   relief='raised', bd=2)
        config_frame.pack(fill='x', pady=(0, 20))
        
        # Liên kết mời
        link_frame = tk.Frame(config_frame, bg='#34495e')
        link_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(link_frame, text="🔗 Liên kết mời:", 
                font=('Arial', 11, 'bold'), 
                fg='#ecf0f1', bg='#34495e').pack(anchor='w')
        
        self.link_entry = tk.Entry(link_frame, font=('Arial', 11), 
                                  width=80, relief='flat', bd=5)
        self.link_entry.pack(fill='x', pady=(5, 0))
        
        # Số lượng account
        count_frame = tk.Frame(config_frame, bg='#34495e')
        count_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(count_frame, text="📊 Số account cần tạo:", 
                font=('Arial', 11, 'bold'), 
                fg='#ecf0f1', bg='#34495e').pack(anchor='w')
        
        self.count_var = tk.StringVar(value="1")
        count_spinbox = tk.Spinbox(count_frame, from_=1, to=100, 
                                  textvariable=self.count_var,
                                  font=('Arial', 11), width=10,
                                  relief='flat', bd=5)
        count_spinbox.pack(anchor='w', pady=(5, 0))
        
        # Frame điều khiển
        control_frame = tk.Frame(main_frame, bg='#2c3e50')
        control_frame.pack(fill='x', pady=(0, 20))
        
        # Nút thực hiện
        self.start_button = tk.Button(control_frame, text="🚀 BẮT ĐẦU THỰC HIỆN", 
                                     font=('Arial', 12, 'bold'),
                                     bg='#27ae60', fg='white',
                                     relief='raised', bd=3,
                                     padx=20, pady=10,
                                     command=self.start_creation)
        self.start_button.pack(side='left', padx=(0, 10))
        
        # Nút dừng
        self.stop_button = tk.Button(control_frame, text="⛔ DỪNG", 
                                    font=('Arial', 12, 'bold'),
                                    bg='#e74c3c', fg='white',
                                    relief='raised', bd=3,
                                    padx=20, pady=10,
                                    command=self.stop_creation,
                                    state='disabled')
        self.stop_button.pack(side='left')
        
        # Frame thống kê
        stats_frame = tk.LabelFrame(main_frame, text="Thống Kê", 
                                  font=('Arial', 12, 'bold'),
                                  fg='#ecf0f1', bg='#34495e',
                                  relief='raised', bd=2)
        stats_frame.pack(fill='x', pady=(0, 20))
        
        stats_inner = tk.Frame(stats_frame, bg='#34495e')
        stats_inner.pack(fill='x', padx=15, pady=10)
        
        # Thành công
        self.success_var = tk.StringVar(value="0")
        tk.Label(stats_inner, text="✅ Thành công:", 
                font=('Arial', 11, 'bold'), 
                fg='#27ae60', bg='#34495e').pack(side='left')
        tk.Label(stats_inner, textvariable=self.success_var,
                font=('Arial', 11, 'bold'), 
                fg='#27ae60', bg='#34495e').pack(side='left', padx=(5, 20))
        
        # Thất bại
        self.failed_var = tk.StringVar(value="0")
        tk.Label(stats_inner, text="❌ Thất bại:", 
                font=('Arial', 11, 'bold'), 
                fg='#e74c3c', bg='#34495e').pack(side='left')
        tk.Label(stats_inner, textvariable=self.failed_var,
                font=('Arial', 11, 'bold'), 
                fg='#e74c3c', bg='#34495e').pack(side='left', padx=(5, 20))
        
        # Điểm
        self.score_var = tk.StringVar(value="0")
        tk.Label(stats_inner, text="🏆 Điểm:", 
                font=('Arial', 11, 'bold'), 
                fg='#f39c12', bg='#34495e').pack(side='left')
        tk.Label(stats_inner, textvariable=self.score_var,
                font=('Arial', 11, 'bold'), 
                fg='#f39c12', bg='#34495e').pack(side='left', padx=(5, 0))
        
        # Khung log
        log_frame = tk.LabelFrame(main_frame, text="📝 Nhật Ký Hoạt Động", 
                                font=('Arial', 12, 'bold'),
                                fg='#ecf0f1', bg='#34495e',
                                relief='raised', bd=2)
        log_frame.pack(fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                font=('Consolas', 10),
                                                bg='#1e1e1e', fg='#00ff00',
                                                insertbackground='white',
                                                relief='flat', bd=5)
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Log ban đầu
        self.log("🎯 Ứng dụng đã sẵn sàng!")
        self.log("💡 Nhập liên kết mời và số account cần tạo, sau đó nhấn 'BẮT ĐẦU THỰC HIỆN'")
        
    def log(self, message):
        """Ghi log với timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def generate_password(self, length=12):
        """Tạo mật khẩu ngẫu nhiên có ít nhất 1 chữ thường, 1 chữ hoa, 1 số"""
        import random
        import string
        
        if length < 3:
            length = 3  # Tối thiểu để có đủ 1 thường, 1 hoa, 1 số
            
        # Đảm bảo có ít nhất 1 ký tự từ mỗi loại
        password = [
            random.choice(string.ascii_lowercase),  # 1 chữ thường
            random.choice(string.ascii_uppercase),  # 1 chữ hoa  
            random.choice(string.digits)            # 1 số
        ]
        
        # Điền phần còn lại bằng ký tự ngẫu nhiên
        remaining_length = length - 3
        all_characters = string.ascii_letters + string.digits
        
        for _ in range(remaining_length):
            password.append(random.choice(all_characters))
        
        # Trộn các ký tự để vị trí ngẫu nhiên
        random.shuffle(password)
        
        return ''.join(password)

    def setup_driver(self):
        """Thiết lập Chrome driver với chế độ ẩn danh và anti-detection nâng cao"""
        try:
            self.log("🔧 Đang thiết lập ChromeDriver với bảo mật cao...")
            
            chrome_options = Options()
            
            # Chế độ ẩn danh
            chrome_options.add_argument("--incognito")
            
            # Anti-detection cơ bản
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_argument("--disable-dev-tools")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-ipc-flooding-protection")
            
            # Anti-detection nâng cao
            chrome_options.add_argument("--disable-features=VizDisplayCompositor,VizHitTestSurfaceLayer")
            chrome_options.add_argument("--disable-features=UserAgentClientHint")
            chrome_options.add_argument("--disable-client-side-phishing-detection")
            chrome_options.add_argument("--disable-component-extensions-with-background-pages")
            chrome_options.add_argument("--disable-default-apps")
            chrome_options.add_argument("--disable-features=Translate")
            chrome_options.add_argument("--disable-hang-monitor")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-prompt-on-repost")
            chrome_options.add_argument("--disable-sync")
            chrome_options.add_argument("--disable-domain-reliability")
            chrome_options.add_argument("--disable-features=AudioServiceOutOfProcess")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-background-networking")
            chrome_options.add_argument("--disable-breakpad")
            chrome_options.add_argument("--disable-component-update")
            chrome_options.add_argument("--disable-datasaver-prompt")
            chrome_options.add_argument("--disable-desktop-notifications")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-ipc-flooding-protection")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-service-autorun")
            chrome_options.add_argument("--password-store=basic")
            chrome_options.add_argument("--use-mock-keychain")
            chrome_options.add_argument("--disable-features=WebRtcRemoteEventLog")
            chrome_options.add_argument("--disable-remote-fonts")
            chrome_options.add_argument("--disable-permissions-api")
            
            # Randomize screen size để tránh fingerprinting
            screen_sizes = [
                "--window-size=1366,768",
                "--window-size=1920,1080", 
                "--window-size=1440,900",
                "--window-size=1536,864",
                "--window-size=1280,720"
            ]
            chrome_options.add_argument(random.choice(screen_sizes))
            
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # User agent ngẫu nhiên
            user_agent = self.get_random_user_agent()
            chrome_options.add_argument(f"--user-agent={user_agent}")
            self.log(f"🎭 User Agent: {user_agent[:50]}...")
            
            # Prefs để disable thêm các tính năng tracking
            prefs = {
                "profile.default_content_setting_values": {
                    "notifications": 2,
                    "geolocation": 2,
                    "media_stream": 2,
                },
                "profile.managed_default_content_settings": {
                    "images": 2
                },
                "profile.default_content_settings": {
                    "popups": 0
                },
                "datareduction.proxy.enabled": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_setting_values.geolocation": 2,
                "profile.managed_default_content_settings.images": 2,
                "webkit.webprefs.loads_images_automatically": False,
                "profile.managed_default_content_settings.media_stream": 2
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            driver = None
            
            # Cách 1: Thử với executable_path trực tiếp
            try:
                self.log("🔄 Đang sử dụng ChromeDriver có sẵn...")
                driver = webdriver.Chrome(options=chrome_options)
                self.log("✅ Thành công!")
            except Exception as e1:
                self.log(f"⚠️ ChromeDriver có sẵn thất bại: {str(e1)}")
                
                # Cách 2: Force download lại ChromeDriver
                try:
                    self.log("🔄 Đang tải lại ChromeDriver...")
                    import shutil
                    import os
                    
                    # Xóa cache của webdriver-manager
                    cache_path = os.path.expanduser("~/.wdm")
                    if os.path.exists(cache_path):
                        shutil.rmtree(cache_path)
                        self.log("🗑️ Đã xóa cache ChromeDriver")
                    
                    # Tải lại ChromeDriver
                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    self.log("✅ Tải lại thành công!")
                except Exception as e2:
                    self.log(f"❌ Tất cả cách đều thất bại!")
                    self.log(f"Lỗi chi tiết: {str(e2)}")
                    raise Exception(f"Không thể khởi tạo ChromeDriver. Vui lòng kiểm tra:\n1. Chrome browser đã cài đặt chưa\n2. Cập nhật Chrome lên phiên bản mới nhất\n3. Restart máy tính")
            
            if driver:
                # Thêm script anti-detection
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                # Hide automation indicators
                driver.execute_cdp_cmd('Runtime.evaluate', {
                    "expression": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en', 'vi']
                    });
                    
                    window.chrome = {
                        runtime: {}
                    };
                    
                    Object.defineProperty(navigator, 'permissions', {
                        get: () => ({
                            query: () => Promise.resolve({state: 'granted'})
                        })
                    });
                    """
                })
                
                self.log("✅ ChromeDriver đã sẵn sàng với bảo mật cao!")
                return driver
            else:
                raise Exception("Không thể tạo ChromeDriver")
                
        except Exception as e:
            self.log(f"❌ Lỗi khi thiết lập ChromeDriver: {str(e)}")
            raise e
        
    def create_single_account(self, invite_link, account_num):
        """Tạo một tài khoản duy nhất với bảo mật cao"""
        driver = None
        try:
            self.log(f"🔄 Bắt đầu tạo account #{account_num} với bảo mật cao")
            
            # Reset IP mạng trước khi tạo account (trừ account đầu tiên)
            if account_num > 1:
                self.reset_network_ip()
            
            # Random delay trước khi bắt đầu
            self.add_random_delay(2, 5)
            
            # Thiết lập driver
            driver = self.setup_driver()
            wait = WebDriverWait(driver, 15)
            
            # Clear cookies và storage
            driver.delete_all_cookies()
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
            
            # Bước 1: Vào mail.tm để lấy email
            self.log(f"📧 Đang lấy email tạm thời...")
            driver.get("https://mail.tm/vi/")
            
            # Random delay
            self.add_random_delay(3, 6)
            
            # Lấy email
            email_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[1]/div/div/input")))
            email = email_input.get_attribute("value")
            self.log(f"✅ Email nhận được: {email}")
            
            # Copy email vào clipboard
            pyperclip.copy(email)
            self.log(f"📋 Đã copy email vào clipboard")
            
            # Random delay
            self.add_random_delay(1, 3)
            
            # Bước 2: Mở link mời và kích hoạt popup
            self.log(f"🔗 Đang mở liên kết mời...")
            driver.execute_script(f"window.open('{invite_link}', '_blank');")
            wait.until(lambda d: len(d.window_handles) == 2)
            driver.switch_to.window(driver.window_handles[1])
            
            # Random delay
            self.add_random_delay(2, 4)
            self.log(f"📄 Trang đã load, đang kích hoạt popup đăng ký...")
            
            # Scroll lên đầu trang và focus
            driver.execute_script("window.scrollTo(0, 0);")
            driver.execute_script("document.body.focus();")
            time.sleep(0.5)
            
            # Bấm Tab 12 lần để tới nút Sign Up Now
            self.log(f"🎹 Bấm Tab 12 lần để tới nút Sign Up Now...")
            for i in range(12):
                pyautogui.press('tab')
                time.sleep(random.uniform(0.1, 0.2))  # Random delay giữa các lần bấm
            
            # Bấm Enter để mở popup
            self.log(f"🎹 Bấm Enter để mở popup đăng ký...")
            pyautogui.press('enter')
            self.add_random_delay(1, 2)
            
            # Kiểm tra popup đã mở
            iframe_found = driver.find_elements(By.XPATH, "//iframe[contains(@src, 'accounts.wondershare.com')]")
            if iframe_found:
                self.log(f"✅ Popup đăng ký đã mở thành công!")
            else:
                self.log(f"❌ Popup chưa mở, thử tiếp tục...")
            
            # Bước 3: Điền thông tin đăng ký bằng Tab
            self.log(f"📝 Đang điền thông tin đăng ký...")
            
            # Tab 6 lần đến trường email
            for i in range(6):
                pyautogui.press('tab')
                time.sleep(random.uniform(0.1, 0.2))
            
            # Dán email
            self.log(f"📧 Dán email: {email}")
            pyautogui.hotkey('ctrl', 'v')
            
            # Tab 1 lần đến trường password
            pyautogui.press('tab')
            time.sleep(0.1)
            
            # Tạo và dán mật khẩu
            password = self.generate_password()
            pyperclip.copy(password)
            self.log(f"🔐 Dán mật khẩu: {password}")
            pyautogui.hotkey('ctrl', 'v')
            
            # Tab 1 lần đến nút tạo tài khoản và Enter
            pyautogui.press('tab')
            time.sleep(0.1)
            pyautogui.press('enter')
            
            self.log(f"✅ Đã hoàn thành điền form đăng ký")
            self.add_random_delay(1, 2)
            
            # Bước 4: Quay lại email để lấy mã xác nhận
            self.log(f"📬 Đang lấy mã xác nhận từ email...")
            driver.switch_to.default_content()
            driver.switch_to.window(driver.window_handles[0])
            
            # Lấy mã xác nhận
            verification_code = None
            max_retries = 6
            email_clicked = False
            
            for retry in range(max_retries):
                if self.stop_flag:
                    return False
                    
                try:
                    self.log(f"🔄 Lần thử {retry + 1}/{max_retries} - Đang kiểm tra email...")
                    
                    if not email_clicked:
                        driver.refresh()
                        self.add_random_delay(2, 3)
                    
                    # Thử lấy mã từ preview trước
                    try:
                        preview_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/main/div[2]/div[2]/ul/li/a/div/div/div[2]/div[2]/div/div[2]")
                        preview_text = preview_element.text.strip()
                        self.log(f"📄 Preview email: {preview_text}")
                        
                        if "verification code is:" in preview_text.lower():
                            code_patterns = [
                                r'verification code is:\s*(\d{4,8})',
                                r'code is:\s*(\d{4,8})',
                                r':\s*(\d{6})',
                                r'\b(\d{6})\b',
                                r'\b(\d{5})\b',
                                r'\b(\d{4})\b'
                            ]
                            
                            for pattern in code_patterns:
                                code_match = re.search(pattern, preview_text, re.IGNORECASE)
                                if code_match:
                                    verification_code = code_match.group(1) if code_match.groups() else code_match.group()
                                    self.log(f"🔢 Mã xác nhận: {verification_code}")
                                    break
                            
                            if verification_code:
                                break
                    except NoSuchElementException:
                        pass
                    
                    # Nếu chưa có mã, click vào email
                    if not verification_code and not email_clicked:
                        email_selectors = [
                            "/html/body/div[1]/div/div[2]/main/div[2]/div[2]/ul/li/a/div",
                            "//div[contains(@class, 'email-item')]//a",
                            "//li[contains(@class, 'email')]//a",
                            "//a[contains(@href, 'message')]"
                        ]
                        
                        email_link = None
                        for selector in email_selectors:
                            try:
                                email_link = driver.find_element(By.XPATH, selector)
                                break
                            except NoSuchElementException:
                                continue
                        
                        if email_link:
                            email_link.click()
                            email_clicked = True
                            self.add_random_delay(1, 2)
                            self.log(f"✅ Đã click vào email")
                        else:
                            self.add_random_delay(8, 12)
                            continue
                    
                    # Tìm mã trong nội dung email chi tiết
                    if not verification_code and email_clicked:
                        verification_selectors = [
                            "/html/body/p/span/table/tbody/tr/td/table/tbody/tr[2]/td/div[2]",
                            "//div[contains(@class, 'verification-code')]",
                            "//td[contains(text(), 'verification') or contains(text(), 'code')]",
                            "//p[contains(text(), 'code') or contains(text(), 'verification')]",
                            "//*[contains(text(), '6')]"
                        ]
                        
                        verification_element = None
                        for selector in verification_selectors:
                            try:
                                verification_element = driver.find_element(By.XPATH, selector)
                                break
                            except NoSuchElementException:
                                continue
                        
                        if verification_element:
                            verification_text = verification_element.text.strip()
                            self.log(f"📄 Nội dung email: {verification_text}")
                            
                            code_patterns = [r'\b\d{6}\b', r'\b\d{5}\b', r'\b\d{4}\b']
                            for pattern in code_patterns:
                                code_match = re.search(pattern, verification_text)
                                if code_match:
                                    verification_code = code_match.group()
                                    self.log(f"🔢 Mã xác nhận: {verification_code}")
                                    break
                            
                            if verification_code:
                                break
                        else:
                            if email_clicked and retry < max_retries - 1:
                                driver.refresh()
                                self.add_random_delay(3, 5)
                                email_clicked = False
                    
                except Exception as e:
                    self.log(f"⚠️ Lỗi lần {retry + 1}: {str(e)}")
                    email_clicked = False
                    self.add_random_delay(8, 12)
            
            if not verification_code:
                self.log(f"❌ Không lấy được mã xác nhận")
                return False
            
            # Bước 5: Nhập mã xác nhận
            self.log(f"🔄 Đang nhập mã xác nhận...")
            driver.switch_to.window(driver.window_handles[1])
            self.add_random_delay(2, 3)
            
            # Chuyển vào iframe nếu có
            try:
                iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'accounts.wondershare.com')]")
                driver.switch_to.frame(iframe)
                self.log(f"✅ Đã chuyển vào iframe")
            except:
                pass
            
            # Nhập mã bằng Tab và Ctrl+V
            pyperclip.copy(verification_code)
            
            # Tab 1 lần đến trường mã xác nhận
            pyautogui.press('tab')
            time.sleep(0.1)
            
            # Dán mã xác nhận
            self.log(f"📝 Dán mã xác nhận: {verification_code}")
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            
            # Tab đến nút xác nhận và Enter
            for i in range(6):
                pyautogui.press('tab')
                time.sleep(random.uniform(0.1, 0.2))
            pyautogui.press('enter')
            
            self.log(f"✅ Đã hoàn thành nhập mã xác nhận")
            
            # Đợi 5 giây rồi tắt trình duyệt
            self.log(f"⏳ Đợi 2 giây rồi tắt trình duyệt...")
            self.add_random_delay(2, 3)
            
            self.log(f"🎉 Account #{account_num} hoàn thành! Đang tắt trình duyệt...")
            return True
                
        except Exception as e:
            self.log(f"❌ Lỗi tạo account #{account_num}: {str(e)}")
            return False
            
        finally:
            if driver:
                try:
                    driver.quit()
                    self.log(f"🔧 Đã tắt trình duyệt cho account #{account_num}")
                except:
                    pass

    def start_creation(self):
        """Bắt đầu quá trình tạo account"""
        if self.is_running:
            return
            
        invite_link = self.link_entry.get().strip()
        if not invite_link:
            messagebox.showerror("Lỗi", "Vui lòng nhập liên kết mời!")
            return
            
        try:
            account_count = int(self.count_var.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng account không hợp lệ!")
            return
            
        self.is_running = True
        self.stop_flag = False
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        
        # Reset thống kê
        self.success_var.set("0")
        self.failed_var.set("0")
        self.score_var.set("0")
        
        # Chạy trong thread riêng
        thread = threading.Thread(target=self.creation_worker, args=(invite_link, account_count))
        thread.daemon = True
        thread.start()
        
    def creation_worker(self, invite_link, account_count):
        """Worker thread để tạo account với bảo mật cao"""
        success_count = 0
        failed_count = 0
        
        self.log(f"🚀 Bắt đầu tạo {account_count} account với bảo mật cao...")
        self.log(f"🛡️ Tính năng bảo mật: Reset IP mạng, User Agent rotation, Random delays")
        
        for i in range(1, account_count + 1):
            if self.stop_flag:
                self.log("⛔ Đã dừng theo yêu cầu người dùng")
                break
                
            success = self.create_single_account(invite_link, i)
            
            if success:
                success_count += 1
                score = success_count * 100
                self.success_var.set(str(success_count))
                self.score_var.set(f"{score} điểm")
                self.log(f"🏆 Điểm hiện tại: {score}")
            else:
                failed_count += 1
                self.failed_var.set(str(failed_count))
                
            # Nghỉ giữa các lần tạo với delay ngẫu nhiên
            if i < account_count and not self.stop_flag:
                delay_time = random.randint(15, 30)  # Delay dài hơn để tránh detection
                self.log(f"⏳ Nghỉ {delay_time} giây trước khi tạo account tiếp theo...")
                for _ in range(delay_time):
                    if self.stop_flag:
                        break
                    time.sleep(1)
                
        # Hoàn thành
        self.log(f"🏁 Hoàn thành! Thành công: {success_count}/{account_count}")
        self.log(f"🏆 Tổng điểm đạt được: {success_count * 100} điểm")
        self.log(f"🛡️ Đã sử dụng tính năng bảo mật cao để tránh capcha")
        
        self.is_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

    def stop_creation(self):
        """Dừng quá trình tạo account"""
        self.stop_flag = True
        self.log("⚠️ Đang dừng...")

def main():
    root = tk.Tk()
    app = AccountCreatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 