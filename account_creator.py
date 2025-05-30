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

class AccountCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filmora Credit Farm - Account Creator")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        
        # Biến để kiểm soát việc dừng
        self.stop_flag = False
        self.is_running = False
        
        # Tạo giao diện
        self.create_widgets()
        
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
        """Thiết lập Chrome driver với chế độ ẩn danh"""
        try:
            self.log("🔧 Đang thiết lập ChromeDriver...")
            
            chrome_options = Options()
            chrome_options.add_argument("--incognito")
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
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # Thêm user agent để tránh bị phát hiện
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
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
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                self.log("✅ ChromeDriver đã sẵn sàng!")
                return driver
            else:
                raise Exception("Không thể tạo ChromeDriver")
                
        except Exception as e:
            self.log(f"❌ Lỗi khi thiết lập ChromeDriver: {str(e)}")
            raise e
        
    def create_single_account(self, invite_link, account_num):
        """Tạo một tài khoản duy nhất"""
        driver = None
        try:
            self.log(f"🔄 Bắt đầu tạo account #{account_num}")
            
            # Thiết lập driver
            driver = self.setup_driver()
            wait = WebDriverWait(driver, 15)
            
            # Bước 1: Vào mail.tm để lấy email
            self.log(f"📧 Đang lấy email tạm thời...")
            driver.get("https://mail.tm/vi/")
            time.sleep(5)
            
            # Lấy email
            email_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[1]/div/div/input")))
            email = email_input.get_attribute("value")
            self.log(f"✅ Email nhận được: {email}")
            
            # Copy email vào clipboard
            pyperclip.copy(email)
            self.log(f"📋 Đã copy email vào clipboard")
            
            # Bước 2: Mở link mời và kích hoạt popup
            self.log(f"🔗 Đang mở liên kết mời...")
            driver.execute_script(f"window.open('{invite_link}', '_blank');")
            wait.until(lambda d: len(d.window_handles) == 2)
            driver.switch_to.window(driver.window_handles[1])
            
            time.sleep(1)
            self.log(f"📄 Trang đã load, đang kích hoạt popup đăng ký...")
            
            # Scroll lên đầu trang và focus
            driver.execute_script("window.scrollTo(0, 0);")
            driver.execute_script("document.body.focus();")
            time.sleep(0.5)
            
            # Bấm Tab 12 lần để tới nút Sign Up Now
            self.log(f"🎹 Bấm Tab 12 lần để tới nút Sign Up Now...")
            for i in range(12):
                pyautogui.press('tab')
                time.sleep(0.1)
            
            # Bấm Enter để mở popup
            self.log(f"🎹 Bấm Enter để mở popup đăng ký...")
            pyautogui.press('enter')
            time.sleep(1)
            
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
                time.sleep(0.1)
            
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
            time.sleep(1)
            
            # Bước 4: Quay lại email để lấy mã xác nhận
            self.log(f"📬 Đang lấy mã xác nhận từ email...")
            driver.switch_to.default_content()
            driver.switch_to.window(driver.window_handles[0])
            
            # Lấy mã xác nhận
            verification_code = None
            max_retries = 6
            email_clicked = False
            
            for retry in range(max_retries):
                try:
                    self.log(f"🔄 Lần thử {retry + 1}/{max_retries} - Đang kiểm tra email...")
                    
                    if not email_clicked:
                        driver.refresh()
                        time.sleep(2)
                    
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
                            time.sleep(1)
                            self.log(f"✅ Đã click vào email")
                        else:
                            time.sleep(10)
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
                                time.sleep(3)
                                email_clicked = False
                    
                except Exception as e:
                    self.log(f"⚠️ Lỗi lần {retry + 1}: {str(e)}")
                    email_clicked = False
                    time.sleep(10)
            
            if not verification_code:
                self.log(f"❌ Không lấy được mã xác nhận")
                return False
            
            # Bước 5: Nhập mã xác nhận
            self.log(f"🔄 Đang nhập mã xác nhận...")
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)
            
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
                time.sleep(0.1)
            pyautogui.press('enter')
            
            self.log(f"✅ Đã hoàn thành nhập mã xác nhận")
            
            # Đợi 5 giây rồi tắt trình duyệt
            self.log(f"⏳ Đợi 2 giây rồi tắt trình duyệt...")
            time.sleep(2)
            
            self.log(f"🎉 Account #{account_num} hoàn thành! Đang tắt trình duyệt...")
            return True
                
        except Exception as e:
            self.log(f"❌ Lỗi tạo account #{account_num}: {str(e)}")
            return False
            
        finally:
            if driver:
                driver.quit()
                self.log(f"🔧 Đã tắt trình duyệt cho account #{account_num}")
                
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
        """Worker thread để tạo account"""
        success_count = 0
        failed_count = 0
        
        self.log(f"🚀 Bắt đầu tạo {account_count} account...")
        
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
                
            # Nghỉ giữa các lần tạo
            if i < account_count and not self.stop_flag:
                self.log(f"⏳ Nghỉ 1 giây trước khi tạo account tiếp theo...")
                time.sleep(1)
                
        # Hoàn thành
        self.log(f"🏁 Hoàn thành! Thành công: {success_count}/{account_count}")
        self.log(f"🏆 Tổng điểm đạt được: {success_count * 100} điểm")
        
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