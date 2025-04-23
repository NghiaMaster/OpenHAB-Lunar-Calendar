# OpenHAB-Lunar-Calendar
Âm lịch VIỆT NAM cho OpenHAB by [AIoT.io.vn](https://AIoT.io.vn). File được dựa trên bản gốc của repo: `https://github.com/quangvinh86/SolarLunarCalendar/blob/master/LunarSolar.py`
Được bổ sung thêm *Tiết Khí* và *Phật Lịch* dựa trên thuật toán của tác giả **Hồ Ngọc Đức**.

# Yêu càu
- Download file `OpenHABLunarCalendar.py`
- trên OpenHAB, tạo các items:
  - `AL_PhatLich` - String
  - `AL_ThangNhuan` - Number (0 = không nhuận, 1 = nhuận)
  - `AL_Holiday` - String
  - `AL_TietKhi` - String
  - `AL_CanChiNam` - String
  - `AL_CanChiThang` - String
  - `AL_CanChiNgay` - String
  - `AL_Today` - DateTime
- Chỉnh sửa thông tin ở các dòng `296`, `319-326`
- Vào `rules` tạo script cho script chạy vào 00:01 (0h đêm) hàng ngày

# Copy file vào Userdata của OpenHAB

- `mkdir /var/lib/openhab/amlich`
- `wget https://raw.githubusercontent.com/NghiaMaster/OpenHAB-Lunar-Calendar/refs/heads/main/OpenHABLunarCalendar.py`
- `cp OpenHABLunarCalendar.py /var/lib/openhab/amlich/`
- `chown openhab:openhab /var/lib/openhab/amlich/OpenHABLunarCalendar.py`
