import math
from datetime import datetime
import requests

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ",
       "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tí", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ",
       "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CHI_MONTH = ["", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi",
             "Thân", "Dậu", "Tuất", "Hợi", "Tí", "Sửu"]
TIETKHI = [
    "Xuân phân", "Thanh minh", "Cốc vũ",
    "Lập hạ", "Tiểu mãn", "Mang chủng",
    "Hạ chí", "Tiểu thử", "Đại thử",
    "Lập thu", "Xử thử", "Bạch lộ",
    "Thu phân", "Hàn lộ", "Sương giáng",
    "Lập đông", "Tiểu tuyết", "Đại tuyết",
    "Đông chí", "Tiểu hàn", "Đại hàn",
    "Lập xuân", "Vũ thủy", "Kinh trập"
]
LE = {
    'solar': [
        {'d': 1, 'm': 1, 'i': 'Tết Dương lịch'},
        {'d': 9, 'm': 1, 'i': 'Ngày Học sinh - Sinh viên Việt Nam'},
        {'d': 3, 'm': 2, 'i': 'Ngày thành lập Đảng Cộng sản Việt Nam'},
        {'d': 27, 'm': 2, 'i': 'Ngày Thầy thuốc Việt Nam'},
        {'d': 8, 'm': 3, 'i': 'Ngày Quốc tế Phụ Nữ'},
        {'d': 26, 'm': 3, 'i': 'Ngày thành lập Đoàn Thanh niên Cộng sản Hồ Chí Minh'},
        {'d': 21, 'm': 4, 'i': 'Ngày Sách Việt Nam'},
        {'d': 30, 'm': 4, 'i': 'Ngày Thống nhất đất nước'},
        {'d': 1, 'm': 5, 'i': 'Ngày Quốc tế Lao động'},
        {'d': 15, 'm': 5, 'i': 'Ngày thành lập Đội Thiếu niên Tiền phong Hồ Chí Minh'},
        {'d': 19, 'm': 5, 'i': 'Ngày sinh của Chủ tịch Hồ Chí Minh'},
        {'d': 1, 'm': 6, 'i': 'Ngày Quốc tế Thiếu nhi'},
        {'d': 5, 'm': 6, 'i': 'Ngày Bác Hồ ra đi tìm đường cứu nước'},
        {'d': 27, 'm': 7, 'i': 'Ngày Thương binh Liệt sĩ'},
        {'d': 19, 'm': 8, 'i': 'Ngày Cách mạng tháng Tám thành công'},
        {'d': 2, 'm': 9, 'i': 'Ngày Quốc khánh'},
        {'d': 13, 'm': 10, 'i': 'Ngày Doanh nhân Việt Nam'},
        {'d': 20, 'm': 10, 'i': 'Ngày thành lập Hội Phụ nữ Việt Nam'},
        {'d': 20, 'm': 11, 'i': 'Ngày Nhà giáo Việt Nam'},
        {'d': 22, 'm': 12, 'i': 'Ngày thành lập Quân đội Nhân dân Việt Nam'},
        {'d': 24, 'm': 12, 'i': 'Ngày Lễ Giáng Sinh'}
    ],
    'lunar': [
        {'d': 1, 'm': 1, 'i': 'Tết Nguyên Đán'},
        {'d': 2, 'm': 1, 'i': 'Mồng 2 Tết Nguyên Đán'},
        {'d': 3, 'm': 1, 'i': 'Mồng 3 Tết Nguyên Đán'},
        {'d': 15, 'm': 1, 'i': 'Tết Nguyên tiêu'},
        {'d': 3, 'm': 3, 'i': 'Tết Hàn thực'},
        {'d': 10, 'm': 3, 'i': 'Giỗ Tổ Hùng Vương'},
        {'d': 15, 'm': 4, 'i': 'Lễ Phật Đản'},
        {'d': 5, 'm': 5, 'i': 'Tết Đoan ngọ'},
        {'d': 15, 'm': 7, 'i': 'Vu Lan'},
        {'d': 15, 'm': 8, 'i': 'Tết Trung thu'},
        {'d': 23, 'm': 12, 'i': 'Ông Táo chầu trời'}
    ]
}

def julian_day_from_date(dd, mm, yy):
    temp_a = int((14 - mm) / 12.)
    temp_year = yy + 4800 - temp_a
    temp_month = mm + 12 * temp_a - 3
    julian_day = (dd + int((153*temp_month + 2) / 5.) +
                  365 * temp_year + int(temp_year / 4.) -
                  int(temp_year/100.) + int(temp_year/400)
                  - 32045)
    if julian_day < 2299161:
        julian_day = dd + int((153*temp_month + 2)/5.) \
            + 365*temp_year + int(temp_year/4.) - 32083
    return julian_day

def julian_day_to_date(julian_day):

    if julian_day > 2299160:
        # After 5/10/1582, Gregorian calendar
        temp_a = julian_day + 32044
        temp_b = int((4 * temp_a + 3) / 146097.)
        temp_c = temp_a - int((temp_b * 146097) / 4.)
    else:
        temp_b = 0
        temp_c = julian_day + 32082
    temp_d = int((4 * temp_c + 3) / 1461.)
    temp_e = temp_c - int((1461 * temp_d) / 4.)
    temp_m = int((5 * temp_e + 2) / 153.)
    _day = temp_e - int((153 * temp_m + 2) / 5.) + 1
    _month = temp_m + 3 - 12 * int(temp_m / 10.)
    _year = temp_b * 100 + temp_d - 4800 + int(temp_m / 10.)
    return [_day, _month, _year]

def new_moon(k_th):

    time_julian = k_th / 1236.85
    time_julian_2 = time_julian * time_julian
    time_julian_3 = time_julian_2 * time_julian
    degree_to_radian = math.pi / 180
    julian_day_1 = (2415020.75933 + 29.53058868 * k_th +
                    0.0001178 * time_julian_2 -
                    0.000000155 * time_julian_3)
    julian_day_1 = (julian_day_1 +
                    0.00033*math.sin((166.56 + 132.87*time_julian -
                                      0.009173 * time_julian_2) *
                                     degree_to_radian))
    mean_new_moon = (359.2242 + 29.10535608*k_th -
                     0.0000333*time_julian_2 - 0.00000347*time_julian_3)
    sun_mean_anomaly = (306.0253 + 385.81691806*k_th +
                        0.0107306*time_julian_2 + 0.00001236*time_julian_3)
    moon_mean_anomaly = (21.2964 + 390.67050646*k_th -
                         0.0016528*time_julian_2 - 0.00000239*time_julian_3)
    moon_arg_lat = ((0.1734 - 0.000393*time_julian) *
                    math.sin(mean_new_moon*degree_to_radian) +
                    0.0021*math.sin(2*degree_to_radian*mean_new_moon))
    moon_arg_lat = (moon_arg_lat -
                    0.4068*math.sin(sun_mean_anomaly*degree_to_radian)
                    + 0.0161*math.sin(degree_to_radian*2*sun_mean_anomaly))
    moon_arg_lat = (moon_arg_lat -
                    0.0004*math.sin(degree_to_radian*3*sun_mean_anomaly))
    moon_arg_lat = (moon_arg_lat +
                    0.0104*math.sin(degree_to_radian*2*moon_mean_anomaly)
                    - 0.0051 * math.sin(degree_to_radian *
                                        (mean_new_moon + sun_mean_anomaly)))
    moon_arg_lat = (moon_arg_lat -
                    0.0074*math.sin(degree_to_radian *
                                    (mean_new_moon - sun_mean_anomaly))
                    + 0.0004*math.sin(degree_to_radian *
                                      (2*moon_mean_anomaly + mean_new_moon)))
    moon_arg_lat = (moon_arg_lat - 0.0004*math.sin(degree_to_radian *
                                                   (2*moon_mean_anomaly -
                                                    mean_new_moon))
                    - 0.0006 * math.sin(degree_to_radian *
                                        (2*moon_mean_anomaly
                                         + sun_mean_anomaly)))
    moon_arg_lat = (moon_arg_lat + 0.0010*math.sin(degree_to_radian *
                                                   (2*moon_mean_anomaly -
                                                    sun_mean_anomaly))
                    + 0.0005*math.sin(degree_to_radian *
                                      (2*sun_mean_anomaly + mean_new_moon))
                    )
    if time_julian < -11:
        deltat = (0.001 + 0.000839*time_julian + 0.0002261*time_julian_2
                  - 0.00000845*time_julian_3 -
                  0.000000081*time_julian*time_julian_3)
    else:
        deltat = -0.000278 + 0.000265*time_julian + 0.000262*time_julian_2
    new_julian_day = julian_day_1 + moon_arg_lat - deltat
    return new_julian_day

def sun_longitude(jdn):

    time_in_julian = (jdn - 2451545.0) / 36525.
    # Time in Julian centuries
    # from 2000-01-01 12:00:00 GMT
    time_in_julian_2 = time_in_julian * time_in_julian
    degree_to_radian = math.pi / 180.  # degree to radian
    mean_time = (357.52910 + 35999.05030*time_in_julian
                 - 0.0001559*time_in_julian_2 -
                 0.00000048 * time_in_julian*time_in_julian_2)
    # mean anomaly, degree
    mean_degree = (280.46645 + 36000.76983*time_in_julian +
                   0.0003032*time_in_julian_2)
    # mean longitude, degree
    mean_long_degree = ((1.914600 - 0.004817*time_in_julian -
                         0.000014*time_in_julian_2)
                        * math.sin(degree_to_radian*mean_time))
    mean_long_degree += ((0.019993 - 0.000101*time_in_julian) *
                         math.sin(degree_to_radian*2*mean_time) +
                         0.000290*math.sin(degree_to_radian*3*mean_time))
    long_degree = mean_degree + mean_long_degree  # true longitude, degree
    long_degree = long_degree * degree_to_radian
    long_degree = long_degree - math.pi*2*(int(long_degree / (math.pi*2)))
    # Normalize to (0, 2*math.pi)
    return long_degree

def get_sun_longitude(dayNumber, timeZone):

    return int(sun_longitude(dayNumber - 0.5 - timeZone / 24)
               / math.pi*6)


def get_new_moon_day(k, timeZone):

    return int(new_moon(k) + 0.5 + timeZone / 24.)

def get_lunar_month_11(yy, timeZone):

    off = julian_day_from_date(31, 12, yy) - 2415021.
    k = int(off / 29.530588853)
    lunar_month = get_new_moon_day(k, timeZone)
    sun_long = get_sun_longitude(lunar_month, timeZone)
    # sun longitude at local midnight
    if sun_long >= 9:
        lunar_month = get_new_moon_day(k - 1, timeZone)
    return lunar_month

def get_leap_month_offset(a11, timeZone):

    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    last = 0
    i = 1  # start with month following lunar month 11
    arc = get_sun_longitude(get_new_moon_day(k + i, timeZone),
                            timeZone)
    while True:
        last = arc
        i += 1
        arc = get_sun_longitude(get_new_moon_day(k + i, timeZone),
                                timeZone)
        if not (arc != last and i < 14):
            break
    return i - 1

def solar_to_lunar(solar_dd, solar_mm, solar_yy, time_zone=7):

    time_zone = 7
    day_number = julian_day_from_date(solar_dd, solar_mm, solar_yy)
    k = int((day_number - 2415021.076998695) / 29.530588853)
    month_start = get_new_moon_day(k + 1, time_zone)
    if month_start > day_number:
        month_start = get_new_moon_day(k, time_zone)
    # alert(dayNumber + " -> " + monthStart)
    a11 = get_lunar_month_11(solar_yy, time_zone)
    b11 = a11
    if a11 >= month_start:
        lunar_year = solar_yy
        a11 = get_lunar_month_11(solar_yy - 1, time_zone)
    else:
        lunar_year = solar_yy + 1
        b11 = get_lunar_month_11(solar_yy + 1, time_zone)
    lunar_day = day_number - month_start + 1
    diff = int((month_start - a11) / 29.)
    lunar_leap = 0
    lunar_month = diff + 11
    if b11 - a11 > 365:
        leap_month_diff = \
            get_leap_month_offset(a11, time_zone)
        if diff >= leap_month_diff:
            lunar_month = diff + 10
        if diff == leap_month_diff:
            lunar_leap = 1
    if lunar_month > 12:
        lunar_month = lunar_month - 12
    if lunar_month >= 11 and diff < 4:
        lunar_year -= 1
    return [lunar_day, lunar_month, lunar_year, lunar_leap]

def zodiac_year(year):

    can_index = (year + 6) % 10
    chi_index = (year + 8) % 12
    return "{} {}".format(CAN[can_index], CHI[chi_index])

def zodiac_day(solar_dd, solar_mm, solar_yy):

    julian_day = julian_day_from_date(solar_dd, solar_mm, solar_yy)
    can_index = (julian_day + 9) % 10
    chi_index = (julian_day + 1) % 12
    return "{} {}".format(CAN[can_index], CHI[chi_index])

def lunar_leap(yy):

    if yy % 19 in [0, 3, 6, 9, 11, 14, 17]:
        return 1
    else:
        return 0

def zodiac_month(month, year):

    can_index = (year * 12 + month + 3) % 10
    return "{} {}".format(CAN[can_index], CHI_MONTH[month])

def tiet_khi(dd, mm, yy, timeZone=7):
    jd = julian_day_from_date(dd, mm, yy)
    long_degree = sun_longitude(jd + 1)
    index = int(long_degree / (math.pi / 12))
    return TIETKHI[index]

def check_holiday_solar(dd, mm, LE):
    for item in LE['solar']:
        if item['d'] == dd and item['m'] == mm:
            return f"{item['i']} ({item['d']}/{item['m']} DL)"
    return ''

def check_holiday_lunar(dd, mm, LE):
    for item in LE['lunar']:
        if item['d'] == dd and item['m'] == mm:
            return f"{item['i']} ({item['d']}/{item['m']} ÂL)"
    return ''

def get_holiday_string(sd, sm, ld, lm, LE):
    res = check_holiday_lunar(ld, lm, LE)
    tmp = check_holiday_solar(sd, sm, LE)
    if tmp:
        res = tmp if not res else f"{res}, {tmp}"
    return res

def send_to_openhab(item, value):
    url = f"http://10.0.1.71:8080/rest/items/{item}/state"
    headers = {"Content-Type": "text/plain"}
    try:
        requests.put(url, data=value, headers=headers, timeout=3)
    except Exception as e:
        print(f"Failed to send to {item}: {e}")

def main():

    today = datetime.today()
    solar_dd = today.day
    solar_mm = today.month
    solar_yy = today.year
    time_zone = 7

    lunar_day = solar_to_lunar(solar_dd, solar_mm, solar_yy, time_zone)
    _zodiac_year = zodiac_year(solar_yy)
    _zodiac_month = zodiac_month(lunar_day[1], lunar_day[3])
    _zodiac_day = zodiac_day(solar_dd, solar_mm, solar_yy)
    _tiet_khi = tiet_khi(solar_dd, solar_mm, solar_yy, time_zone)
    _holiday = get_holiday_string(solar_dd, solar_mm, lunar_day[0], lunar_day[1], LE)
    _phatlich = lunar_day[3] + 544 if (lunar_day[1] > 4 or (lunar_day[1] == 4 and lunar_day[0] >= 15)) else lunar_day[2] + 543

    send_to_openhab("AL_Today", f"{lunar_day[2]:04d}-{lunar_day[1]:02d}-{lunar_day[0]:02d}T00:00:00.000+0700")
    send_to_openhab("AL_CanChiNgay", _zodiac_day.encode("utf-8"))
    send_to_openhab("AL_CanChiThang", _zodiac_month.encode("utf-8"))
    send_to_openhab("AL_CanChiNam", _zodiac_year.encode("utf-8"))
    send_to_openhab("AL_TietKhi", _tiet_khi.encode("utf-8"))
    send_to_openhab("AL_Holiday", _holiday.encode("utf-8"))
    send_to_openhab("AL_ThangNhuan", f"{lunar_day[3]}")
    send_to_openhab("AL_PhatLich", f"{_phatlich}")


if __name__ == "__main__":
    main()
