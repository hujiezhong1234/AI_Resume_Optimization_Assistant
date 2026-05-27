# 🎯 AI 简历优化助手

> 上传简历 + 粘贴岗位 JD，AI 帮你精准匹配、直达 Offer

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Gradio](https://img.shields.io/badge/Gradio-4.x-orange)](https://gradio.app)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ 功能亮点

| 功能 | 说明 |
|------|------|
| 📄 **智能简历解析** | 支持 PDF / Word 格式，自动提取文本内容 |
| 🎯 **JD 智能格式化** | 自动识别职位描述、任职要求、加分项等模块 |
| 🔗 **JD 链接抓取** | 支持 BOSS 直聘、智联、前程无忧、拉勾等网站（实验性） |
| 🤖 **多平台 AI 支持** | DeepSeek / 硅基流动 / 阿里云百炼 / OpenAI 一键切换 |
| 📊 **五维匹配评分** | 总体匹配度、硬性条件、经验匹配、技能匹配、潜力评估 |
| ✍️ **逐条优化建议** | 原文改写对比，量化成果示例，可直接复制使用 |
| 🔑 **关键词缺失检测** | 自动对比 JD 要求与简历内容，提示缺失关键词 |

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/ai-resume-optimizer.git
cd ai-resume-optimizer
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

> **依赖说明**：
> - `gradio` — Web 界面框架
> - `PyPDF2` — PDF 文本提取
> - `python-docx` — Word 文档解析
> - `requests` — API 调用与网页抓取

### 3. 配置 API Key

在界面中选择 AI 平台并输入对应的 API Key：

| 平台 | 申请地址 | 备注 |
|------|---------|------|
| DeepSeek 官方 | [platform.deepseek.com](https://platform.deepseek.com) | 新用户送 5000 万 Token |
| 硅基流动 | [siliconflow.cn](https://siliconflow.cn) | 新用户送 2000 万 Token |
| 阿里云百炼 | [bailian.aliyun.com](https://bailian.aliyun.com) | 按量付费 |
| OpenAI | [platform.openai.com](https://platform.openai.com) | 需海外支付 |

### 4. 启动应用

```bash
python app.py
```

访问 `http://localhost:7860` 即可使用。

## 📸 使用流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  上传简历    │ ──▶ │  粘贴 JD    │ ──▶ │  AI 分析    │
│ (PDF/Word)  │     │  或粘贴链接  │     │  生成报告   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 分析输出示例

#### 🎯 匹配度评分
| 维度 | 得分 | 说明 |
|------|------|------|
| 总体匹配度 | 78/100 | 整体较为匹配，有优化空间 |
| 硬性条件 | 85/100 | 学历、年限符合要求 |
| 经验匹配 | 75/100 | 项目经验相关度中等 |
| 技能匹配 | 80/100 | 技术栈基本覆盖 |
| 潜力评估 | 72/100 | 成长性良好 |

#### ✅ 逐条优化建议
- **原文**：负责用户增长  
  **改写**：主导用户增长策略，通过 A/B 测试优化获客渠道，3 个月内 DAU 从 10 万提升至 25 万（+150%），获客成本降低 40%

#### 📝 优化后简历全文
AI 生成可直接复制使用的完整优化版简历，保持原有模块结构。

## 📁 项目结构

```
.
├── app.py              # Gradio 主应用入口
├── config.py           # AI 平台配置（API 地址、模型列表）
├── resume_parser.py    # 简历解析模块（PDF/Word）
├── jd_scraper.py       # 招聘网站 JD 抓取模块
├── requirements.txt    # 依赖列表
└── README.md           # 项目说明
```

### 模块说明

| 文件 | 职责 |
|------|------|
| `app.py` | Gradio 界面、用户交互、AI 调用编排 |
| `config.py` | 集中管理多平台 API 配置，方便扩展新平台 |
| `resume_parser.py` | 封装 PDF 和 Word 的文本提取逻辑 |
| `jd_scraper.py` | 针对主流招聘网站的反爬与解析策略 |

## 🔧 进阶配置

### 添加新的 AI 平台

在 `config.py` 中新增配置项：

```python
PLATFORM_CONFIG = {
    # ... 现有配置
    "自定义平台": {
        "url": "https://api.example.com/v1/chat/completions",
        "models": ["model-name"],
        "key_hint": "your-key-prefix",
        "note": "备注说明"
    }
}
```

### 自定义 Prompt

编辑 `app.py` 中 `analyze_resume` 函数的 `prompt` 变量，可调整：
- 评分维度与权重
- 优化建议的详细程度
- 输出格式与语言风格

## ⚠️ 注意事项

1. **JD 抓取限制**：BOSS 直聘、拉勾等网站有反爬机制，建议直接复制页面文字粘贴
2. **API 安全**：API Key 仅在本地浏览器输入，不会上传到任何第三方服务器
3. **隐私保护**：简历内容仅用于当前次 AI 分析，不会被存储或记录
4. **文件大小**：建议上传 1-2 页的简历，过长的文件可能影响解析效果

## 🛣️ 路线图

- [ ] 支持更多简历格式（TXT、HTML、图片 OCR）
- [ ] 历史分析记录与对比
- [ ] 简历模板推荐与一键导出
- [ ] 批量 JD 对比分析
- [ ] 面试题库生成（基于 JD 与简历）

## 🤝 贡献指南

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 打开 Pull Request

## 📄 许可证

本项目基于 [MIT](LICENSE) 许可证开源。

## 🙏 致谢

- [Gradio](https://gradio.app) — 让机器学习 demo 构建变得简单
- [DeepSeek](https://deepseek.com) / [硅基流动](https://siliconflow.cn) — 提供高性价比的大模型 API

---

> 💡 **求职小贴士**：简历建议 1-2 页，重点突出量化成果；JD 越详细，AI 分析越精准。

<p align="center">Made with ❤️ for job seekers</p>
