"""平台配置"""

PLATFORM_CONFIG = {
    "DeepSeek 官方": {
        "url": "https://api.deepseek.com/chat/completions",
        "models": ["deepseek-chat", "deepseek-reasoner"],
        "key_hint": "sk-...",
        "note": "新用户送5000万Token"
    },
    "硅基流动": {
        "url": "https://api.siliconflow.cn/v1/chat/completions",
        "models": ["deepseek-ai/DeepSeek-V3", "deepseek-ai/DeepSeek-R1"],
        "key_hint": "sk-...",
        "note": "新用户送2000万Token"
    },
    "阿里云百炼": {
        "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "models": ["qwen-max", "qwen-plus"],
        "key_hint": "sk-...",
        "note": "按量付费"
    },
    "OpenAI": {
        "url": "https://api.openai.com/v1/chat/completions",
        "models": ["gpt-4o", "gpt-4o-mini"],
        "key_hint": "sk-...",
        "note": "需海外支付"
    }
}