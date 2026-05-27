"""岗位 JD 抓取"""

import re
import requests
from urllib.parse import urlparse


def fetch_jd_from_url(url):
    """从招聘网站链接抓取 JD 内容"""
    if not url or not url.startswith('http'):
        return None, "请输入有效的网址"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.encoding = 'utf-8'
        html = resp.text

        # BOSS 直聘
        if 'zhipin.com' in url:
            return _parse_boss(html)
        # 智联招聘
        elif 'zhaopin.com' in url:
            return _parse_zhaopin(html)
        # 前程无忧
        elif '51job.com' in url:
            return _parse_51job(html)
        # 拉勾
        elif 'lagou.com' in url:
            return _parse_lagou(html)
        else:
            # 通用抓取：尝试提取页面中最大的文本块
            return _generic_extract(html), "通用抓取（可能不完整，建议手动粘贴）"

    except Exception as e:
        return None, f"抓取失败: {str(e)}"


def _parse_boss(html):
    """解析 BOSS 直聘页面"""
    # 职位名称
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html)
    title = title_match.group(1) if title_match else ""

    # 职位描述（BOSS 的 JD 通常在 job-sec-text 或类似 class 中）
    desc_patterns = [
        r'<div[^>]*class="[^"]*job-sec-text[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*class="[^"]*job-description[^"]*"[^>]*>(.*?)</div>',
        r'<div[^>]*class="[^"]*detail-content[^"]*"[^>]*>(.*?)</div>',
    ]

    desc = ""
    for pattern in desc_patterns:
        match = re.search(pattern, html, re.DOTALL)
        if match:
            desc = match.group(1)
            break

    # 清理 HTML 标签
    desc = re.sub(r'<[^>]+>', '', desc)
    desc = re.sub(r'\s+', ' ', desc).strip()

    # 公司信息
    company_match = re.search(r'<a[^>]*ka="job-detail-company[^"]*"[^>]*>(.*?)</a>', html)
    company = company_match.group(1) if company_match else ""
    company = re.sub(r'<[^>]+>', '', company)

    full_jd = f"【职位】{title}\n【公司】{company}\n\n【职位描述】\n{desc}"
    return full_jd, "BOSS直聘抓取成功"


def _parse_zhaopin(html):
    return _generic_extract(html), "智联招聘抓取成功"


def _parse_51job(html):
    return _generic_extract(html), "前程无忧抓取成功"


def _parse_lagou(html):
    return _generic_extract(html), "拉勾网抓取成功"


def _generic_extract(html):
    """通用提取：找页面中最长的连续文本段落"""
    # 移除 script/style
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)

    # 提取所有文本
    text = re.sub(r'<[^>]+>', '\n', text)
    lines = [l.strip() for l in text.split('\n') if len(l.strip()) > 10]

    # 找最长的连续段落
    if lines:
        return '\n'.join(lines[:50])  # 取前50行
    return ""