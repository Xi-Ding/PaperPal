# PaperPal: Localized Academic Reader 📚

> **Stop switching tabs. Start deep reading.**  
> PaperPal 是一个专为科研人员设计的英文学术论文阅读助手，通过语义级分块与术语保护技术，构建流畅的本地化阅读体验。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Framework: Tauri](https://img.shields.io/badge/Framework-Tauri-FFC131.svg)](https://tauri.app/)
[![Stability: Stable](https://img.shields.io/badge/Stability-Production--Ready-green.svg)]()

---

## 🌟 核心特性

- **🎯 术语保护引擎 (Term-Locking)**: 自动识别并保留高频学术术语（如 *eccentric contraction*），防止 LLM 将专业词汇误译为生活化表达。
- **🧱 语义级文档切分 (Semantic Chunking)**: 拒绝机械的 Token 计数。基于逻辑段落进行分块，确保 LLM 始终掌握完整的上下文论证。
- **🧠 意图感知 QA (Intent-Aware Interaction)**:
  - **局部提问**: 聚焦当前选中段落及其相邻语义块。
  - **全局提问**: 自动检索 *Abstract*、*Introduction* 与 *Conclusion*，提供全局视野。
- **⚡ 沉浸式 UI**: 基于 Tauri 构建，极低资源占用，支持 Markdown 渲染与公式预览。

## 🏗️ 技术架构

项目采用两阶段串联架构：

1. **预处理阶段**: 
   - `Marker-OCR` -> 格式化 Markdown
   - `Structure-Analyzer` -> 语义层级分块
2. **交互阶段**:
   - `Router` -> 识别问题意图 (Local vs Global)
   - `RAG-Lite` -> 动态上下文拼接
   - `Inference` -> 本地(Ollama/vLLM) 或 云端 API

## 🚀 快速开始

### 环境要求
- Python 3.9+
- Node.js & Rust (仅限开发 Tauri 前端)

### 安装配置
```bash
# 克隆仓库
git clone https://github.com/your-username/PaperPal.git
cd PaperPal

# 安装后端依赖
pip install -r requirements.txt

# 运行后端服务
python backend_service.py
```

## 📅 路线图 (Roadmap)
- [x] 基于 Marker 的 PDF 高精度转换
- [x] 意图分类路由器
- [ ] Zotero 插件集成
- [ ] 多模态图表理解支持
- [ ] 本地向量数据库存储

## 📄 开源协议
本项目采用 [MIT License](LICENSE) 协议。
