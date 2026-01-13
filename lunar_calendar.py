"""
农历和节气转换模块
结合PHP CalendarController和JavaScript Bazi函数的精确实现
"""
from datetime import datetime
import time

# 天干地支
TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
DIZHI0 = ['丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子']  # 从丑开始的地支数组

# PHP代码中的sTermInfo数组 - 1900-2100年的节气数据（十六进制编码）
S_TERM_INFO = [
    '9778397bd097c36b0b6fc9274c91aa','97b6b97bd19801ec9210c965cc920e','97bcf97c3598082c95f8c965cc920f',
    '97bd0b06bdb0722c965ce1cfcc920f','b027097bd097c36b0b6fc9274c91aa','97b6b97bd19801ec9210c965cc920e',
    '97bcf97c359801ec95f8c965cc920f','97bd0b06bdb0722c965ce1cfcc920f','b027097bd097c36b0b6fc9274c91aa',
    '97b6b97bd19801ec9210c965cc920e','97bcf97c359801ec95f8c965cc920f','97bd0b06bdb0722c965ce1cfcc920f',
    'b027097bd097c36b0b6fc9274c91aa','9778397bd19801ec9210c965cc920e','97b6b97bd19801ec95f8c965cc920f',
    '97bd09801d98082c95f8e1cfcc920f','97bd097bd097c36b0b6fc9210c8dc2','9778397bd197c36c9210c9274c91aa',
    '97b6b97bd19801ec95f8c965cc920e','97bd09801d98082c95f8e1cfcc920f','97bd097bd097c36b0b6fc9210c8dc2',
    '9778397bd097c36c9210c9274c91aa','97b6b97bd19801ec95f8c965cc920e','97bcf97c3598082c95f8e1cfcc920f',
    '97bd097bd097c36b0b6fc9210c8dc2','9778397bd097c36c9210c9274c91aa','97b6b97bd19801ec9210c965cc920e',
    '97bcf97c3598082c95f8c965cc920f','97bd097bd097c35b0b6fc920fb0722','9778397bd097c36b0b6fc9274c91aa',
    '97b6b97bd19801ec9210c965cc920e','97bcf97c3598082c95f8c965cc920f','97bd097bd097c35b0b6fc920fb0722',
    '9778397bd097c36b0b6fc9274c91aa','97b6b97bd19801ec9210c965cc920e','97bcf97c359801ec95f8c965cc920f',
    '97bd097bd097c35b0b6fc920fb0722','9778397bd097c36b0b6fc9274c91aa','97b6b97bd19801ec9210c965cc920e',
    '97bcf97c359801ec95f8c965cc920f','97bd097bd097c35b0b6fc920fb0722','9778397bd097c36b0b6fc9274c91aa',
    '97b6b97bd19801ec9210c965cc920e','97bcf97c359801ec95f8c965cc920f','97bd097bd07f595b0b6fc920fb0722',
    '9778397bd097c36b0b6fc9210c8dc2','9778397bd19801ec9210c9274c920e','97b6b97bd19801ec95f8c965cc920f',
    '97bd07f5307f595b0b0bc920fb0722','7f0e397bd097c36b0b6fc9210c8dc2','9778397bd097c36c9210c9274c920e',
    '97b6b97bd19801ec95f8c965cc920f','97bd07f5307f595b0b0bc920fb0722','7f0e397bd097c36b0b6fc9210c8dc2',
    '9778397bd097c36c9210c9274c91aa','97b6b97bd19801ec9210c965cc920e','97bd07f1487f595b0b0bc920fb0722',
    '7f0e397bd097c36b0b6fc9210c8dc2','9778397bd097c36b0b6fc9274c91aa','97b6b97bd19801ec9210c965cc920e',
    '97bcf7f1487f595b0b0bb0b6fb0722','7f0e397bd097c35b0b6fc920fb0722','9778397bd097c36b0b6fc9274c91aa',
    '97b6b97bd19801ec9210c965cc920e','97bcf7f1487f595b0b0bb0b6fb0722','7f0e397bd097c35b0b6fc920fb0722',
    '9778397bd097c36b0b6fc9274c91aa','97b6b97bd19801ec9210c965cc920e','97bcf7f1487f531b0b0bb0b6fb0722',
    '7f0e397bd097c35b0b6fc920fb0722','9778397bd097c36b0b6fc9274c91aa','97b6b97bd19801ec9210c965cc920e',
    '97bcf7f1487f531b0b0bb0b6fb0722','7f0e397bd07f595b0b6fc920fb0722','9778397bd097c36b0b6fc9274c91aa',
    '97b6b97bd19801ec9210c9274c920e','97bcf7f0e47f531b0b0bb0b6fb0722','7f0e397bd07f595b0b0bc920fb0722',
    '9778397bd097c36b0b6fc9210c91aa','97b6b97bd197c36c9210c9274c920e','97bcf7f0e47f531b0b0bb0b6fb0722',
    '7f0e397bd07f595b0b0bc920fb0722','9778397bd097c36b0b6fc9210c8dc2','9778397bd097c36c9210c9274c920e',
    '97b6b7f0e47f531b0723b0b6fb0722','7f0e37f5307f595b0b0bc920fb0722','7f0e397bd097c36b0b6fc9210c8dc2',
    '9778397bd097c36b0b70c9274c91aa','97b6b7f0e47f531b0723b0b6fb0721','7f0e37f1487f595b0b0bb0b6fb0722',
    '7f0e397bd097c35b0b6fc9210c8dc2','9778397bd097c36b0b6fc9274c91aa','97b6b7f0e47f531b0723b0b6fb0721',
    '7f0e27f1487f595b0b0bb0b6fb0722','7f0e397bd097c35b0b6fc920fb0722','9778397bd097c36b0b6fc9274c91aa',
    '97b6b7f0e47f531b0723b0b6fb0721','7f0e27f1487f531b0b0bb0b6fb0722','7f0e397bd097c35b0b6fc920fb0722',
    '9778397bd097c36b0b6fc9274c91aa','97b6b7f0e47f531b0723b0b6fb0721','7f0e27f1487f531b0b0bb0b6fb0722',
    '7f0e397bd097c35b0b6fc920fb0722','9778397bd097c36b0b6fc9274c91aa','97b6b7f0e47f531b0723b0b6fb0721',
    '7f0e27f1487f531b0b0bb0b6fb0722','7f0e397bd07f595b0b0bc920fb0722','9778397bd097c36b0b6fc9274c91aa',
    '97b6b7f0e47f531b0723b0787b0721','7f0e27f0e47f531b0b0bb0b6fb0722','7f0e397bd07f595b0b0bc920fb0722',
    '9778397bd097c36b0b6fc9210c91aa','97b6b7f0e47f149b0723b0787b0721','7f0e27f0e47f531b0723b0b6fb0722',
    '7f0e397bd07f595b0b0bc920fb0722','9778397bd097c36b0b6fc9210c8dc2','977837f0e37f149b0723b0787b0721',
    '7f07e7f0e47f531b0723b0b6fb0722','7f0e37f5307f595b0b0bc920fb0722','7f0e397bd097c35b0b6fc9210c8dc2',
    '977837f0e37f14998082b0787b0721','7f07e7f0e47f531b0723b0b6fb0721','7f0e37f1487f595b0b0bb0b6fb0722',
    '7f0e397bd097c35b0b6fc9210c8dc2','977837f0e37f14998082b0787b06bd','7f07e7f0e47f531b0723b0b6fb0721',
    '7f0e27f1487f531b0b0bb0b6fb0722','7f0e397bd097c35b0b6fc920fb0722','977837f0e37f14998082b0787b06bd',
    '7f07e7f0e47f531b0723b0b6fb0721','7f0e27f1487f531b0b0bb0b6fb0722','7f0e397bd097c35b0b6fc920fb0722',
    '977837f0e37f14998082b0787b06bd','7f07e7f0e47f531b0723b0b6fb0721','7f0e27f1487f531b0b0bb0b6fb0722',
    '7f0e397bd07f595b0b0bc920fb0722','977837f0e37f14998082b0787b06bd','7f07e7f0e47f531b0723b0b6fb0721',
    '7f0e27f1487f531b0b0bb0b6fb0722','7f0e397bd07f595b0b0bc920fb0722','977837f0e37f14998082b0787b06bd',
    '7f07e7f0e47f149b0723b0787b0721','7f0e27f0e47f531b0b0bb0b6fb0722','7f0e397bd07f595b0b0bc920fb0722',
    '977837f0e37f14998082b0723b06bd','7f07e7f0e37f149b0723b0787b0721','7f0e27f0e47f531b0723b0b6fb0722',
    '7f0e397bd07f595b0b0bc920fb0722','977837f0e37f14898082b0723b02d5','7ec967f0e37f14998082b0787b0721',
    '7f07e7f0e47f531b0723b0b6fb0722','7f0e37f1487f595b0b0bb0b6fb0722','7f0e37f0e37f14898082b0723b02d5',
    '7ec967f0e37f14998082b0787b0721','7f07e7f0e47f531b0723b0b6fb0722','7f0e37f1487f531b0b0bb0b6fb0722',
    '7f0e37f0e37f14898082b0723b02d5','7ec967f0e37f14998082b0787b06bd','7f07e7f0e47f531b0723b0b6fb0721',
    '7f0e37f1487f531b0b0bb0b6fb0722','7f0e37f0e37f14898082b072297c35','7ec967f0e37f14998082b0787b06bd',
    '7f07e7f0e47f531b0723b0b6fb0721','7f0e27f1487f531b0b0bb0b6fb0722','7f0e37f0e37f14898082b072297c35',
    '7ec967f0e37f14998082b0787b06bd','7f07e7f0e47f531b0723b0b6fb0721','7f0e27f1487f531b0b0bb0b6fb0722',
    '7f0e37f0e366aa89801eb072297c35','7ec967f0e37f14998082b0787b06bd','7f07e7f0e47f149b0723b0787b0721',
    '7f0e27f1487f531b0b0bb0b6fb0722','7f0e37f0e366aa89801eb072297c35','7ec967f0e37f14998082b0723b06bd',
    '7f07e7f0e47f149b0723b0787b0721','7f0e27f0e47f531b0723b0b6fb0722','7f0e37f0e366aa89801eb072297c35',
    '7ec967f0e37f14998082b0723b06bd','7f07e7f0e37f14998083b0787b0721','7f0e27f0e47f531b0723b0b6fb0722',
    '7f0e37f0e366aa89801eb072297c35','7ec967f0e37f14898082b0723b02d5','7f07e7f0e37f14998082b0787b0721',
    '7f07e7f0e47f531b0723b0b6fb0722','7f0e36665b66aa89801e9808297c35','665f67f0e37f14898082b0723b02d5',
    '7ec967f0e37f14998082b0787b0721','7f07e7f0e47f531b0723b0b6fb0722','7f0e36665b66a449801e9808297c35',
    '665f67f0e37f14898082b0723b02d5','7ec967f0e37f14998082b0787b06bd','7f07e7f0e47f531b0723b0b6fb0721',
    '7f0e36665b66a449801e9808297c35','665f67f0e37f14898082b072297c35','7ec967f0e37f14998082b0787b06bd',
    '7f07e7f0e47f531b0723b0b6fb0721','7f0e26665b66a449801e9808297c35','665f67f0e37f1489801eb072297c35',
    '7ec967f0e37f14998082b0787b06bd','7f07e7f0e47f531b0723b0b6fb0721','7f0e27f1487f531b0b0bb0b6fb0722'
]

# 1984年基准时间戳（毫秒）- 对应JavaScript的y_d84
Y_D84 = 441734400726

def get_diff_days(year, month, day):
    """
    计算从1900年1月1日到指定日期的天数
    基于PHP的getDiffDays方法
    """
    solar_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    y_days = (year - 1900) * 365 + (year - 1900) // 4
    
    if month > 1:
        m_days = sum(solar_month[:month-1])
    else:
        m_days = 0
    
    # 处理闰年（PHP代码的逻辑）
    if year % 4 == 0:
        y_days -= 1  # 如果刚好是闰年，先减去当年闰的那一天
        if month > 2:
            m_days += 1  # 闰年过了二月要加一天
    
    return int(y_days + m_days + day)

def get_term(year, n):
    """
    传入公历年获得该年第n个节气的公历日期
    基于PHP的getTerm方法
    @param year: 公历年(1900-2100)
    @param n: 二十四节气中的第几个节气(1~24)；从n=1(小寒)算起
    @return: 日期（1-31）
    """
    if year < 1900 or year > 2100:
        return -1
    if n < 1 or n > 24:
        return -1
    
    table = S_TERM_INFO[year - 1900]
    
    # 解析十六进制字符串，每个5位十六进制数转换为十进制
    info = [
        int(table[0:5], 16),
        int(table[5:10], 16),
        int(table[10:15], 16),
        int(table[15:20], 16),
        int(table[20:25], 16),
        int(table[25:30], 16)
    ]
    
    # 提取每个节气的日期（每个info值包含4个节气）
    # PHP代码：substr($_info[0],0,1) 表示从十进制数的字符串表示中提取
    calday = []
    for i in range(6):
        info_str = str(info[i]).zfill(5)  # 转换为字符串并确保至少5位
        # 按照PHP代码的逻辑提取
        calday.append(int(info_str[0:1]))   # 第1个节气（第1位）
        calday.append(int(info_str[1:3]))   # 第2个节气（第2-3位）
        calday.append(int(info_str[3:4]))   # 第3个节气（第4位）
        calday.append(int(info_str[4:5]))   # 第4个节气（第5位）
    
    return calday[n - 1]

def to_ganzhi_year(year):
    """
    年份转换为干支纪年
    基于PHP的toGanZhiYear方法
    """
    gan_key = (year - 3) % 10
    zhi_key = (year - 3) % 12
    
    if gan_key == 0:
        gan_key = 10
    if zhi_key == 0:
        zhi_key = 12
    
    return TIANGAN[gan_key - 1] + DIZHI[zhi_key - 1]

def to_ganzhi(offset):
    """
    传入offset偏移量返回干支
    基于PHP的toGanZhi方法
    """
    return TIANGAN[offset % 10] + DIZHI[offset % 12]

def get_year_zhu(year, month, day):
    """
    年柱 - 以立春为界
    基于PHP的solar2lunar方法
    """
    li_chun = get_term(year, 3)  # 立春是第3个节气
    
    if month < 2 or (month == 2 and day < li_chun):
        # 在立春之前，用上一年
        return to_ganzhi_year(year - 1)
    else:
        # 在立春之后，用当年
        return to_ganzhi_year(year)

def get_month_zhu(year, month, day):
    """
    月柱 - 根据节气判断
    基于PHP的solar2lunar方法
    """
    # 当月的"节"（第一个节气）
    first_node = get_term(year, month * 2 - 1)
    
    # 依据12节气修正干支月
    gz_month = to_ganzhi((year - 1900) * 12 + month + 11)
    if day >= first_node:
        gz_month = to_ganzhi((year - 1900) * 12 + month + 12)
    
    return gz_month

def get_day_zhu(year, month, day):
    """
    日柱 - 基于公历日期计算
    基于PHP的solar2lunar方法
    """
    day_cyclical = get_diff_days(year, month, day) + 9
    return to_ganzhi(day_cyclical)

def get_hour_zhi(hour):
    """
    时支 - 对应JavaScript的hZhi()
    """
    if hour >= 23:
        sz = DIZHI0[11]
    elif hour >= 21:
        sz = DIZHI0[10]
    elif hour >= 19:
        sz = DIZHI0[9]
    elif hour >= 17:
        sz = DIZHI0[8]
    elif hour >= 15:
        sz = DIZHI0[7]
    elif hour >= 13:
        sz = DIZHI0[6]
    elif hour >= 11:
        sz = DIZHI0[5]
    elif hour >= 9:
        sz = DIZHI0[4]
    elif hour >= 7:
        sz = DIZHI0[3]
    elif hour >= 5:
        sz = DIZHI0[2]
    elif hour >= 3:
        sz = DIZHI0[1]
    elif hour >= 1:
        sz = DIZHI0[0]
    else:  # hour >= 0
        sz = DIZHI0[11]
    
    return sz

def get_hour_gan(day_gan, hour_zhi):
    """
    时干 - 对应JavaScript的hGan()
    """
    rg = day_gan
    sz = hour_zhi
    sz_index = DIZHI0.index(sz)
    
    # 五鼠遁口诀
    if rg == '甲' or rg == '己':
        sg = TIANGAN[(1 + sz_index) % 10]
    elif rg == '乙' or rg == '庚':
        sg = TIANGAN[(3 + sz_index) % 10]
    elif rg == '丙' or rg == '辛':
        sg = TIANGAN[(5 + sz_index) % 10]
    elif rg == '丁' or rg == '壬':
        sg = TIANGAN[(7 + sz_index) % 10]
    else:  # 戊或癸
        sg = TIANGAN[(9 + sz_index) % 10]
    
    return sg

def get_hour_zhu(day_gan, hour):
    """
    时柱
    """
    hour_zhi = get_hour_zhi(hour)
    hour_gan = get_hour_gan(day_gan, hour_zhi)
    return hour_gan + hour_zhi

def solar_to_ganzhi(year, month, day, hour=None):
    """
    公历转干支（年、月、日、时）
    结合PHP和JavaScript的精确实现
    返回: {'year': '甲子', 'month': '乙丑', 'day': '丙寅', 'hour': '丁卯'}
    """
    result = {
        'year': get_year_zhu(year, month, day),
        'month': get_month_zhu(year, month, day),
        'day': get_day_zhu(year, month, day)
    }
    
    if hour is not None:
        day_gan = result['day'][0]  # 日柱的天干
        result['hour'] = get_hour_zhu(day_gan, hour)
    else:
        result['hour'] = None
    
    return result
