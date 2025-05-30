# 🎬 Filmora Credit Farm - Ứng Dụng Tạo Tài Khoản Tự Động

Ứng dụng Python với giao diện đồ họa để tự động tạo tài khoản với Selenium và email tạm thời từ [Mail.tm](https://mail.tm/vi/).

## ✨ Tính năng

- 🎯 **Giao diện đơn giản**: Tkinter GUI thân thiện với người dùng
- 🔄 **Tự động hoàn toàn**: Từ lấy email đến tạo tài khoản
- 🤖 **Selenium automation**: Chạy trong chế độ ẩn danh
- 📊 **Theo dõi thời gian thực**: Thống kê thành công/thất bại
- 🏆 **Hệ thống tính điểm**: 100 điểm cho mỗi account thành công
- ⛔ **Dừng bất cứ lúc nào**: Kiểm soát hoàn toàn quá trình
- 🔒 **Bảo mật cao**: Không lưu trữ thông tin cá nhân

## 📸 Preview Giao Diện

```
🎬 FILMORA CREDIT FARM
┌─────────────────────────────────────────┐
│ 🔗 Liên kết mời: [___________________] │
│ 📊 Số account: [5]                     │
│ 🚀 BẮT ĐẦU THỰC HIỆN  ⛔ DỪNG         │
├─────────────────────────────────────────┤
│ ✅ Thành công: 3  ❌ Thất bại: 1       │
│ 🏆 Điểm: 300 điểm                      │
├─────────────────────────────────────────┤
│ 📝 Nhật Ký Hoạt Động                   │
│ [10:30:15] 🔄 Bắt đầu tạo account #1   │
│ [10:30:18] ✅ Email: abc@mail.tm       │
│ [10:30:25] 🎉 Account #1 thành công!   │
└─────────────────────────────────────────┘
```

## 📋 Yêu cầu hệ thống

- **Windows 10/11** (đã test)
- **Python 3.7+** với tkinter
- **Google Chrome browser** (phiên bản mới nhất)
- **Kết nối internet ổn định**

## 🚀 Hướng dẫn cài đặt

### Cách 1: Cài đặt nhanh (Khuyến nghị)

1. **Tải xuống tất cả files**
2. **Double-click vào `install.bat`**
3. **Double-click vào `run.bat`** để chạy ứng dụng

### Cách 2: Cài đặt thủ công

1. **Kiểm tra Python:**
   ```cmd
   python --version
   ```

2. **Cài đặt dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Kiểm tra cài đặt:**
   ```cmd
   python test_imports.py
   ```

4. **Chạy ứng dụng:**
   ```cmd
   python account_creator.py
   ```

## 🎮 Hướng dẫn sử dụng

### Bước 1: Khởi động
- Chạy ứng dụng bằng `run.bat` hoặc `python account_creator.py`
- Giao diện sẽ hiện với màu đen/xanh professional

### Bước 2: Cấu hình
- **Liên kết mời**: Dán URL invite vào ô đầu tiên
- **Số account**: Chọn từ 1-100 (khuyến nghị 5-10 cho lần đầu)

### Bước 3: Thực hiện
- Nhấn **"🚀 BẮT ĐẦU THỰC HIỆN"**
- Theo dõi log real-time trong khung bên dưới
- Có thể nhấn **"⛔ DỪNG"** bất cứ lúc nào

### Bước 4: Theo dõi
- **Thành công**: Số account tạo thành công
- **Thất bại**: Số account thất bại  
- **Điểm**: Tổng điểm đạt được (100/account)

## 🔧 Quy trình hoạt động chi tiết

```
1. 📧 Truy cập Mail.tm → Lấy email tạm thời
2. 🔗 Mở link invite → Click nút đăng ký  
3. 📝 Điền form → Email + password random
4. 📬 Check email → Lấy mã xác nhận
5. ✅ Nhập mã → Hoàn tất đăng ký
6. 🎯 Kiểm tra → Xác nhận "Try it Now"
```

## 📊 Hệ thống điểm

| Kết quả | Điểm | Mô tả |
|---------|------|-------|
| ✅ Thành công | +100 | Account được tạo và xác thực thành công |
| ❌ Thất bại | 0 | Lỗi trong quá trình tạo |
| 🏆 Tổng điểm | N×100 | N = số account thành công |

## ⚠️ Lưu ý quan trọng

### Bảo mật
- ✅ Chạy trong chế độ ẩn danh (Incognito)
- ✅ Mỗi account dùng email tạm thời riêng
- ✅ Mật khẩu được tạo ngẫu nhiên
- ✅ Không lưu trữ thông tin đăng nhập
- ✅ Không thu thập dữ liệu cá nhân

### Hiệu suất
- ⏱️ Mỗi account mất khoảng 30-60 giây
- 🔄 Có độ trễ 5 giây giữa các lần tạo
- 🌐 Phụ thuộc vào tốc độ internet
- 💻 ChromeDriver sẽ tự động tải xuống

### Giới hạn
- 📝 Tối đa 100 account/lần chạy
- 🔄 Có thể chạy nhiều lần
- ⚡ Không quá tải hệ thống

## 🛠️ Khắc phục sự cố

### Lỗi thường gặp

#### ❌ "ChromeDriver not found"
```cmd
pip install webdriver-manager --upgrade
python test_imports.py
```

#### ❌ "Selenium timeout"  
- Kiểm tra kết nối internet
- Thử giảm số lượng account
- Restart ứng dụng

#### ❌ "Email không nhận được"
- Đợi thêm 10-15 giây
- Refresh trang mail.tm
- Thử account khác

#### ❌ "Python không tìm thấy"
- Cài đặt Python từ [python.org](https://python.org)
- Chọn "Add to PATH" khi cài đặt

### Cách debug

1. **Chạy test imports:**
   ```cmd
   python test_imports.py
   ```

2. **Kiểm tra Chrome:**
   - Cập nhật lên phiên bản mới nhất
   - Restart máy tính

3. **Xem log chi tiết:**
   - Theo dõi khung log trong ứng dụng
   - Chụp màn hình nếu có lỗi

## 🔐 Chính sách bảo mật

- 🚫 **Không lưu trữ** mật khẩu
- 🚫 **Không thu thập** thông tin cá nhân  
- 🚫 **Không kết nối** server ngoài
- ✅ **Chạy local** 100% trên máy bạn
- ✅ **Open source** - có thể kiểm tra code

## 📂 Cấu trúc files

```
📁 Filmora Credit Farm/
├── 📄 account_creator.py    # File chính
├── 📄 requirements.txt      # Dependencies  
├── 📄 test_imports.py       # Test imports
├── 📄 install.bat          # Cài đặt nhanh
├── 📄 run.bat              # Chạy ứng dụng  
└── 📄 README.md            # Hướng dẫn này
```

## 📞 Hỗ trợ

### Trước khi báo lỗi:
1. ✅ Chạy `python test_imports.py`
2. ✅ Kiểm tra kết nối internet
3. ✅ Cập nhật Chrome browser
4. ✅ Thử restart ứng dụng

### Nếu vẫn lỗi:
- 📸 Chụp màn hình log
- 📝 Mô tả chi tiết bước bị lỗi
- 💻 Cho biết Windows version
- 🐍 Cho biết Python version

## 🏆 Credits

**Phát triển bởi:** Filmora Credit Farm Team  
**Ngôn ngữ:** Python 3.12+  
**GUI Framework:** Tkinter  
**Automation:** Selenium WebDriver  
**Email Service:** [Mail.tm](https://mail.tm/vi/)  

---

### 🌟 Tính năng trong tương lai

- [ ] Hỗ trợ nhiều email provider
- [ ] Lưu lịch sử thành công
- [ ] Proxy support
- [ ] Multi-threading
- [ ] Export thống kê

### 📅 Changelog

**v1.0.0** (2024)
- ✅ Giao diện đầy đủ
- ✅ Automation hoàn chỉnh  
- ✅ Hệ thống điểm
- ✅ Error handling
- ✅ Batch files

---

🎯 **Happy Farming!** 🎬 