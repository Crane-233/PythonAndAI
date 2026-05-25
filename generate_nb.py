import json

# 定义标准的 Jupyter Notebook 结构
notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 📘 Day 1 课件：高级推导式与 JSON 解析深度通关\n",
    "---\n",
    "### 🎯 今日学习目标\n",
    "1. 掌握列表/字典/集合推导式的条件嵌套，写出高效且优雅的 Pythonic 代码。\n",
    "2. 彻底搞懂 `json.loads()`、`json.dumps()` 及其在处理大模型多层嵌套输出时的核心技巧。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## ✍️ 第一部分：高级推导式（Comprehensions）\n",
    "推导式不仅是为了“少写几行代码”，更重要的是它在 Python 底层经过了优化，执行速度比普通的 `for` 循环追加（`.append()`）更快。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 1. 列表推导式与条件嵌套\n",
    "* **语法公式：** `[表达式 for 变量 in 可迭代对象 if 条件]`\n",
    "* **双重条件（If-Else 转换）：** `[值1 if 条件 else 值2 for 变量 in 可迭代对象]`"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 基础示例：提取偶数的平方\n",
    "squares = [x**2 for x in range(10) if x % 2 == 0]\n",
    "print(\"基础偶数平方:\", squares)\n",
    "\n",
    "# 高级示例：根据分数打标签（If-Else 必须放在 for 前面）\n",
    "scores = [55, 85, 92, 60, 45]\n",
    "status = [\"Pass\" if s >= 60 else \"Fail\" for s in scores]\n",
    "print(\"分数标签结果:\", status)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2. 嵌套循环推导式（二维矩阵扁平化）\n",
    "在大模型返回的段落或多层级数据时，经常需要将二维列表压平。其推导式嵌套顺序与传统 for 循环的顺序完全一致。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "matrix = [[1, 2, 3], [4, 5], [6, 7, 8]]\n",
    "\n",
    "# 扁平化操作\n",
    "flatten = [num for row in matrix for num in row]\n",
    "print(\"扁平化后的列表:\", flatten)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 3. 字典推导式（Dictionary Comprehensions）\n",
    "在大模型开发中，常用于快速过滤、清洗或反转 API 返回的 key-value 映射。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 示例：过滤掉温度低于 20 度的城市，并统一把名字大写\n",
    "weather_data = {\"Hong Kong\": 26, \"Beijing\": 15, \"London\": 12, \"Tokyo\": 22}\n",
    "\n",
    "warm_cities = {city.upper(): temp for city, temp in weather_data.items() if temp >= 20}\n",
    "print(\"过滤后的温暖城市:\", warm_cities)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 📦 第二部分：JSON 模块深度解析\n",
    "大模型（LLM）在调用工具或进行结构化输出时，本质上都是在传输 **JSON 字符串**。Python 的 `json` 模块就是沟通大模型与本地系统的桥梁。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 1. 工业级避坑：处理中文乱码与美化打印\n",
    "直接使用 `json.dumps()` 会导致中文变成 unicode 编码（如 `\\u667a\\u80fd`）。必须加上 `ensure_ascii=False` 来保持中文呈现。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "\n",
    "ai_response = {\"status\": \"success\", \"agent_name\": \"智能客服\", \"skills\": [\"查天气\", \"算数学\"]}\n",
    "\n",
    "# ❌ 错误示范\n",
    "bad_json = json.dumps(ai_response)\n",
    "print(\"❌ 错误示范输出 (中文变成编码):\\n\", bad_json, \"\\n\")\n",
    "\n",
    "#  正确示范：ensure_ascii=False 保持中文，indent=4 实现美化缩进\n",
    "good_json = json.dumps(ai_response, ensure_ascii=False, indent=4)\n",
    "print(\" 正确示范输出:\\n\", good_json)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 🛠️ 第三部分：今日实战小项目\n",
    "### 📝 项目需求描述\n",
    "大模型在完成一次“长文本分析任务”后，给你返回了如下一段复杂的、多层嵌套的 JSON 字符串。\n",
    "你需要利用**字典推导式**和 **JSON 解析**，精准提取出所有 **“属于用户 (user) 且 发言字数大于 10 个字”** 的对话内容，并将结果规范化打印。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "\n",
    "# 原始数据\n",
    "raw_llm_output = \"\"\"\n",
    "{\n",
    "    \"session_id\": \"chat_cmpl_12345\",\n",
    "    \"metadata\": {\"location\": \"Hong Kong\", \"topic\": \"AI Agent\"},\n",
    "    \"conversations\": [\n",
    "        {\"role\": \"user\", \"text\": \"你好！\", \"timestamp\": 1716631200},\n",
    "        {\"role\": \"assistant\", \"text\": \"你好！请问有什么我可以帮您的？\", \"timestamp\": 1716631205},\n",
    "        {\"role\": \"user\", \"text\": \"我想了解一下如何用 Python 搭建一个多智能体系统，能给我一个大纲吗？\", \"timestamp\": 1716631220},\n",
    "        {\"role\": \"assistant\", \"text\": \"没问题，我们可以分为四个阶段...\", \"timestamp\": 1716631240},\n",
    "        {\"role\": \"user\", \"text\": \"听起来不错，谢谢。\", \"timestamp\": 1716631250}\n",
    "    ]\n",
    "}\n",
    "\"\"\"\n",
    "\n",
    "# 请在下方编写你的清洗逻辑代码：\n",
    "# 1. 将 JSON 字符串解析为字典\n",
    "# 2. 提取 conversations 列表\n",
    "# 3. 使用字典推导式完成过滤（要求：role 为 user 且 text 长度 > 10）\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 💡 项目参考答案\n",
    "可以展开下方代码块检查自己的实现是否正确。"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. 解析数据\n",
    "data = json.loads(raw_llm_output)\n",
    "\n",
    "# 2. 核心挑战：使用推导式一步到位过滤数据\n",
    "cleaned_chat = {\n",
    "    msg[\"timestamp\"]: msg[\"text\"] \n",
    "    for msg in data[\"conversations\"] \n",
    "    if msg[\"role\"] == \"user\" and len(msg[\"text\"]) > 10\n",
    "}\n",
    "\n",
    "# 3. 美化输出\n",
    "print(\"--- 清洗后的有效用户发言 ---\")\n",
    "print(json.dumps(cleaned_chat, ensure_ascii=False, indent=4))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 🦾 今日课后思考题\n",
    "如果大模型返回的 `raw_llm_output` 字符串首尾不小心带了 \\`\\`\\`json 和 \\`\\`\\` 这样的 Markdown 标记（这是大模型经常犯的毛病），直接用 `json.loads()` 会报错。你该用什么 Python 字符串方法先把这些杂质“剥离”掉？\n",
    "\n",
    "*提示：可以去自学了解一下字符串的 `.strip()`、`.replace()` 或 `.removeprefix()` 方法。*"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

# 用 Python 原生写入文件，保证标准的 UTF-8 编码和严丝合缝的 JSON 格式
with open("Day1_Masterclass.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, ensure_ascii=False, indent=1)

print("🎉 成功！'Day1_Masterclass.ipynb' 已安全生成，现在你可以用 VS Code 或 Jupyter 顺利打开它了！")