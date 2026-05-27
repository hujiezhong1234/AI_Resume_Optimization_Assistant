"""AI 简历优化助手 - Gradio 版本"""

import gradio as gr
import requests
from io import BytesIO

from config import PLATFORM_CONFIG
from parsers.resume_parser import parse_resume


def call_ai(prompt, api_key, api_url, model):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    try:
        r = requests.post(api_url, headers=headers, json=payload, timeout=60)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        return f"❌ API 错误: {r.status_code}"
    except Exception as e:
        return f"❌ 异常: {str(e)}"


def smart_format_jd(raw_text):
    """智能格式化用户粘贴的 JD 文本"""
    if not raw_text:
        return ""

    text = raw_text.strip()

    if "【职位" in text or "【岗位" in text:
        return text

    lines = text.split('\n')
    title = ""
    company = ""

    for line in lines[:5]:
        if any(kw in line for kw in ["招聘", "急聘", "诚聘"]) and not title:
            title = line.strip()
        if any(kw in line for kw in ["公司", "集团", "科技"]) and len(line) < 30 and not company:
            company = line.strip()

    sections = []
    current_section = ""
    section_name = "职位描述"

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if any(line.startswith(kw) for kw in ["职位描述", "岗位职责", "工作内容", "任职要求", "岗位要求", "任职资格", "加分项", "福利待遇", "公司简介"]):
            if current_section:
                sections.append(f"【{section_name}】\n{current_section.strip()}")
            section_name = line.replace("：", "").replace(":", "").strip()
            current_section = ""
        else:
            current_section += line + "\n"

    if current_section:
        sections.append(f"【{section_name}】\n{current_section.strip()}")

    header = ""
    if title:
        header += f"【职位】{title}\n"
    if company:
        header += f"【公司】{company}\n"

    return header + "\n".join(sections) if sections else text


def analyze_resume(resume_file, jd_text, api_key, platform_name):
    """主分析函数"""
    if not api_key:
        return "❌ 请先输入 API Key"

    if not resume_file:
        return "❌ 请先上传简历"

    # 解析简历 - Gradio 返回的是文件路径 (NamedString)
    try:
        if isinstance(resume_file, str):
            # 是文件路径
            file_path = resume_file
            ext = file_path.split(".")[-1].lower()
            with open(file_path, 'rb') as f:
                resume_text = parse_resume(f, ext)
        else:
            # 是文件对象
            ext = resume_file.name.split(".")[-1].lower()
            resume_text = parse_resume(resume_file, ext)
    except Exception as e:
        return f"❌ 简历解析失败: {str(e)}"

    if not resume_text:
        return "❌ 简历解析失败，请检查文件格式"

    # 格式化 JD
    jd_formatted = smart_format_jd(jd_text)
    if not jd_formatted:
        return "❌ 请输入岗位 JD"

    # 调用 AI
    cfg = PLATFORM_CONFIG[platform_name]
    prompt = f"""你是一位资深 HR 总监 + 简历优化专家。请对以下简历进行专业诊断。

## 简历
{resume_text[:3500]}

## 岗位 JD
{jd_formatted[:2500]}

## 输出格式

### 🎯 匹配度评分
| 维度 | 得分 | 说明 |
|------|------|------|
| 总体匹配度 | XX/100 | ... |
| 硬性条件 | XX/100 | 学历、年限、技能证书 |
| 经验匹配 | XX/100 | 项目经验、行业背景 |
| 技能匹配 | XX/100 | 技术栈、工具掌握 |
| 潜力评估 | XX/100 | 成长性、学习能力 |

### ❌ 核心问题（Top 5）
1. **问题**：... | **影响**：... | **优先级**：🔴高/🟡中/🟢低
2. ...

### ✅ 逐条优化建议
1. **原文**：... → **改写**：...（说明为什么更好）
2. ...

### 🔑 关键词缺失
- JD 要求「XXX」→ 简历未体现 → 建议加入「XXX」部分

### 📈 量化成果改写示例
**原句**：负责用户增长
**优化后**：主导用户增长策略，通过 A/B 测试优化获客渠道，3 个月内 DAU 从 10万 提升至 25万（+150%），获客成本降低 40%

### 📝 优化后简历全文
[输出可直接复制使用的完整优化版简历，保持原有模块结构]
"""
    return call_ai(prompt, api_key, cfg["url"], cfg["models"][0])


# ========== Gradio 界面 ==========
with gr.Blocks(title="AI 简历优化助手", theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # 🎯 AI 简历优化助手
    ### 上传简历 + 粘贴岗位 JD，AI 帮你精准匹配、直达 Offer
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## ⚙️ 配置")
            platform = gr.Dropdown(
                choices=list(PLATFORM_CONFIG.keys()),
                value="硅基流动",
                label="API 平台"
            )
            api_key = gr.Textbox(
                label="API Key",
                placeholder="sk-...",
                type="password"
            )

            gr.Markdown("## 📄 简历上传")
            resume_file = gr.File(
                label="支持 PDF / Word",
                file_types=[".pdf", ".docx"]
            )

            gr.Markdown("## 🎯 岗位 JD")

            with gr.Tab("粘贴 JD 文本"):
                jd_input = gr.Textbox(
                    label="岗位描述",
                    placeholder="""从招聘网站复制粘贴 JD 内容到这里...

支持自动识别以下格式：
- 职位描述 / 岗位职责 / 任职要求
- 加分项 / 福利待遇 / 公司简介

💡 提示：BOSS 直聘、拉勾等网站请直接复制页面文字""",
                    lines=12
                )
                format_btn = gr.Button("✨ 智能格式化", variant="secondary", size="sm")
                jd_preview = gr.Textbox(
                    label="格式化预览",
                    lines=6,
                    interactive=False
                )

                def on_format(text):
                    return smart_format_jd(text)

                format_btn.click(on_format, inputs=jd_input, outputs=jd_preview)

            with gr.Tab("从链接抓取（实验性）"):
                gr.Markdown("""
                ⚠️ **注意**：BOSS 直聘、拉勾等网站有反爬机制，直接抓取通常失败。
                
                **推荐做法**：
                1. 打开招聘页面
                2. `Ctrl+A` 全选 → `Ctrl+C` 复制
                3. 切换到「粘贴 JD 文本」标签页粘贴
                """)

                jd_url = gr.Textbox(
                    label="招聘链接",
                    placeholder="https://www.zhipin.com/job/..."
                )
                scrape_btn = gr.Button("🔍 尝试抓取", variant="secondary")
                scrape_result = gr.Textbox(
                    label="抓取结果",
                    lines=5,
                    interactive=False
                )

                def try_scrape(url):
                    if not url:
                        return "请输入链接"
                    try:
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                        }
                        r = requests.get(url, headers=headers, timeout=10)
                        if "安全验证" in r.text or "验证码" in r.text:
                            return "❌ 该网站需要验证码，请手动复制 JD 文本"
                        if len(r.text) < 500:
                            return "❌ 抓取内容为空，请手动复制"
                        return "⚠️ 抓取到内容但可能不完整，建议手动复制确保准确"
                    except Exception as e:
                        return f"❌ 抓取失败: {str(e)}"

                scrape_btn.click(try_scrape, inputs=jd_url, outputs=scrape_result)

        with gr.Column(scale=2):
            gr.Markdown("## 📊 分析结果")
            analyze_btn = gr.Button("🚀 开始 AI 深度分析", variant="primary", size="lg")

            result_output = gr.Markdown(
                value="点击上方按钮开始分析..."
            )

            gr.Markdown("""
            ---
            💡 **使用提示**：
            - 简历建议 1-2 页，重点突出量化成果
            - JD 越详细，AI 分析越精准
            - 分析结果中的「优化后简历全文」可直接复制使用
            """)

    analyze_btn.click(
        analyze_resume,
        inputs=[resume_file, jd_input, api_key, platform],
        outputs=result_output
    )


if __name__ == "__main__":
    demo.launch()