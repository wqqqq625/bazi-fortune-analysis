"""
八字计算模块
计算天干地支、日主等信息
"""
from datetime import datetime
from lunar_calendar import solar_to_ganzhi, TIANGAN, DIZHI

# 导出analyze_2026_yunshi函数供app.py使用
__all__ = ['calculate_bazi', 'get_day_master', 'analyze_with_deepseek', 'analyze_2026_yunshi']

# 天干五行对应
TIANGAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

# 地支藏干（简化版）
DIZHI_CANGGAN = {
    '子': ['癸'], '丑': ['己', '癸', '辛'], '寅': ['甲', '丙', '戊'],
    '卯': ['乙'], '辰': ['戊', '乙', '癸'], '巳': ['丙', '戊', '庚'],
    '午': ['丁', '己'], '未': ['己', '丁', '乙'], '申': ['庚', '壬', '戊'],
    '酉': ['辛'], '戌': ['戊', '辛', '丁'], '亥': ['壬', '甲']
}

def calculate_bazi(dt):
    """
    计算八字（基于JavaScript Bazi函数的精确实现）
    dt: datetime对象（公历日期）
    返回: {'year': '甲子', 'month': '乙丑', 'day': '丙寅', 'hour': '丁卯'}
    """
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour if hasattr(dt, 'hour') else None
    
    # 使用精确的农历转换模块
    ganzhi = solar_to_ganzhi(year, month, day, hour)
    
    return ganzhi

def get_day_master(day_pillar):
    """
    获取日主信息
    day_pillar: 日柱，如 '甲子'
    返回: 日主信息字符串
    """
    if not day_pillar or len(day_pillar) < 2:
        return '未知'
    
    day_gan = day_pillar[0]
    day_zhi = day_pillar[1]
    
    wuxing = TIANGAN_WUXING.get(day_gan, '未知')
    
    # 天干名称
    gan_names = {
        '甲': '甲木', '乙': '乙木', '丙': '丙火', '丁': '丁火', '戊': '戊土',
        '己': '己土', '庚': '庚金', '辛': '辛金', '壬': '壬水', '癸': '癸水'
    }
    
    day_master_name = gan_names.get(day_gan, day_gan)
    
    return f"{day_master_name}（{day_pillar}）"

def analyze_with_ai(bazi, day_master, api_key=None):
    """
    使用AI分析八字，判断喜用神
    """
    if not api_key:
        # 如果没有API key，返回基础分析
        return generate_basic_analysis(bazi, day_master)
    
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        
        # 构建提示词
        prompt = f"""请作为专业的八字命理师，分析以下八字信息：

八字：{bazi['year']} {bazi['month']} {bazi['day']} {bazi['hour'] or '未知'}
日主（日柱）：{day_master}

请重点分析并明确回答：
1. 【日主】明确说明日主是什么（{day_master}），以及其五行属性
2. 【喜用神】详细分析并明确指出：
   - 喜神是什么（为什么）
   - 用神是什么（为什么）
   - 请用简洁明确的语言说明
3. 【忌神】说明忌神是什么
4. 【五行分析】简要说明八字中五行的强弱分布情况

请用中文回答，语言要专业、准确、易懂。重点突出日主和喜用神的分析。"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一位资深的中国传统命理学专家，精通八字命理分析。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"AI分析失败: {e}")
        return generate_basic_analysis(bazi, day_master)

def generate_basic_analysis(bazi, day_master):
    """
    生成基础分析（当AI不可用时）
    """
    day_gan = bazi['day'][0] if bazi.get('day') else ''
    wuxing = TIANGAN_WUXING.get(day_gan, '未知')
    
    analysis = f"""
【日主分析】
您的日主是{day_master}，五行属{wuxing}。

【八字信息】
年柱：{bazi['year']}
月柱：{bazi['month']}
日柱：{bazi['day']}
时柱：{bazi['hour'] or '未知'}

【基础分析】
由于未配置AI分析功能，这里提供基础信息。
要获得详细的喜用神分析，请配置API Key。

提示：喜用神的判断需要综合分析八字中五行的强弱、生克关系等因素。
"""
    
    return analysis.strip()

def analyze_with_deepseek(bazi, day_master, nickname, gender, api_key=None):
    """
    使用 DeepSeek AI 分析八字，返回结构化结果
    返回格式：{
        'personalityAnalysis': '...',
        'currentSituation': '...',
        'coreAdvice': '...',
        'xiyongshen': '...',
        'avoid': '...',
        'summary': '...'
    }
    """
    if not api_key:
        return {
            'personalityAnalysis': f'{nickname}, your Day Master is {day_master}.',
            'currentSituation': 'API Key configuration required to get detailed analysis.',
            'coreAdvice': 'Please configure DeepSeek API Key.',
            'xiyongshen': '',
            'avoid': '',
            'summary': ''
        }
    
    try:
        from openai import OpenAI
        import httpx
        
        # DeepSeek API 配置
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
            http_client=httpx.Client()
        )
        
        # Build prompt - Request specific format analysis
        prompt = f"""As a professional Bazi (Four Pillars) fortune teller, analyze the following Bazi information. Use second-person conversation style and address the user as "{nickname}".

Bazi: {bazi['year']} {bazi['month']} {bazi['day']} {bazi['hour'] or 'Unknown'}
Day Master: {day_master}
Gender: {'Male' if gender == 'male' else 'Female'}

Please analyze in the following format using clear, conversational language that native English speakers can easily understand (avoid jargon and overly technical terms):

1. 【Personality Analysis】(First paragraph)
Use vivid metaphors to describe the user's personality traits, like "You are like a powerful, energetic river with immense vitality" style descriptions. Explain the Day Master, Five Elements attributes, and overall personality characteristics.

2. 【Current Situation】(Second paragraph)
Analyze the user's current situation, including aspects like energy, financial fortune, relationships, and any potential challenges.

3. 【Core Advice】(Third paragraph)
Explain what "converter" or key elements the user needs to improve their situation.

4. 【Favorable Elements Application】(Fourth paragraph, most important)
Explain in detail:
- What is the Favorable Element (most important, focus on strengthening this)
  - What it represents
  - How to strengthen it (career/skills, ways of doing things, other methods)
- What is the Useful Element (go with the flow)
  - What it represents
  - How to use it

5. 【Things to Avoid】(Fifth paragraph)
Explain what unfavorable elements are, and what should be avoided.

6. 【Summary】(Sixth paragraph)
Summarize the user's overall characteristics and recommendations concisely.

Please respond in English using clear, engaging language that avoids overly technical terminology. Focus on explaining the favorable elements and their applications. Make sure your English is natural and fluent for native speakers."""

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are an expert in traditional Chinese Bazi (Four Pillars) fortune telling. You excel at explaining complex metaphysical concepts in clear, engaging English that native speakers can easily understand. Always respond in fluent, natural English."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content.strip()
        
        # 解析 AI 返回的内容，提取各个部分
        result = parse_ai_response(ai_response, nickname)
        
        return result
        
    except Exception as e:
        print(f"DeepSeek AI分析失败: {e}")
        import traceback
        traceback.print_exc()
        return {
            'personalityAnalysis': f'{nickname}, your Day Master is {day_master}.',
            'currentSituation': f'AI analysis temporarily unavailable: {str(e)}',
            'coreAdvice': 'Please try again later.',
            'xiyongshen': '',
            'avoid': '',
            'summary': ''
        }

def parse_ai_response(text, nickname):
    """
    解析 AI 返回的文本，提取各个部分
    """
    result = {
        'personalityAnalysis': '',
        'currentSituation': '',
        'coreAdvice': '',
        'xiyongshen': '',
        'avoid': '',
        'summary': ''
    }
    
    # Try to split by markers
    sections = {
        'personalityAnalysis': ['Personality Analysis', 'Personality', 'First paragraph', '1.', '性格特点分析', '性格特点', '第一段'],
        'currentSituation': ['Current Situation', 'Current', 'Second paragraph', '2.', '当前状况分析', '当前状况', '第二段'],
        'coreAdvice': ['Core Advice', 'Advice', 'Third paragraph', '3.', '核心建议', '第三段'],
        'xiyongshen': ['Favorable Elements', 'Favorable', 'Application', 'Fourth paragraph', '4.', '喜用神应用', '喜用神', '第四段'],
        'avoid': ['Things to Avoid', 'Avoid', 'Fifth paragraph', '5.', '需要避免的', '避免', '第五段'],
        'summary': ['Summary', 'Sixth paragraph', '6.', '总结', '第六段']
    }
    
    # 简单的文本分割逻辑
    lines = text.split('\n')
    current_section = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 检查是否是新的章节标题
        found_section = None
        for section_key, keywords in sections.items():
            for keyword in keywords:
                if keyword in line and len(line) < 50:  # 标题通常较短
                    found_section = section_key
                    break
            if found_section:
                break
        
        if found_section:
            # 保存之前的内容
            if current_section and current_content:
                result[current_section] = '\n'.join(current_content).strip()
            current_section = found_section
            current_content = []
        else:
            # 添加到当前章节
            if current_section:
                current_content.append(line)
            else:
                # 如果没有找到章节，默认添加到第一个
                if not result['personalityAnalysis']:
                    current_section = 'personalityAnalysis'
                    current_content.append(line)
    
    # 保存最后一个章节
    if current_section and current_content:
        result[current_section] = '\n'.join(current_content).strip()
    
    # 如果没有成功分割，将整个文本按段落分配
    if not any(result.values()):
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        if len(paragraphs) >= 1:
            result['personalityAnalysis'] = paragraphs[0]
        if len(paragraphs) >= 2:
            result['currentSituation'] = paragraphs[1]
        if len(paragraphs) >= 3:
            result['coreAdvice'] = paragraphs[2]
        if len(paragraphs) >= 4:
            result['xiyongshen'] = paragraphs[3]
        if len(paragraphs) >= 5:
            result['avoid'] = paragraphs[4]
        if len(paragraphs) >= 6:
            result['summary'] = paragraphs[5]
    
    # 确保所有字段都有内容
    if not result['personalityAnalysis']:
        result['personalityAnalysis'] = text[:500]  # 至少返回前500字
    
    return result

def analyze_2026_yunshi(bazi, day_master, nickname, api_key=None):
    """
    分析2026年丙午年运势
    返回运势分析文本
    """
    if not api_key:
        return f'{nickname}, 2026 is the Bingwu Year. API Key configuration required to get detailed fortune analysis.'
    
    try:
        from openai import OpenAI
        import httpx
        
        # DeepSeek API 配置
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
            http_client=httpx.Client()
        )
        
        # Build prompt
        prompt = f"""As a professional Bazi (Four Pillars) fortune teller, analyze the following user's fortune for 2026 (Bingwu Year). Use second-person conversation style and address the user as "{nickname}".

User's Bazi: {bazi['year']} {bazi['month']} {bazi['day']} {bazi['hour'] or 'Unknown'}
Day Master: {day_master}

2026 is the Bingwu Year (Heavenly Stem: Bing Fire, Earthly Branch: Wu Fire).

Please analyze:
1. The impact of 2026 Bingwu Year on the user's Bazi
2. Overall fortune trends (career, wealth, relationships, health, etc.)
3. Things to pay attention to
4. Suitable activities and directions

Please use clear, conversational English in second-person style so the user can clearly understand their 2026 fortune. Make the language engaging and interesting, avoiding overly technical terms. Ensure your English is natural and fluent for native speakers."""

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are an expert in traditional Chinese Bazi (Four Pillars) fortune telling and annual fortune analysis. You excel at explaining complex metaphysical concepts in clear, engaging English that native speakers can easily understand. Always respond in fluent, natural English."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"2026年运势分析失败: {e}")
        import traceback
        traceback.print_exc()
        return f'{nickname}, 2026 is the Bingwu Year. Fortune analysis temporarily unavailable, please try again later.'

