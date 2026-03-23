# Cline 项目架构可视化文档

> **创建时间**: 2026 年 3 月 13 日  
> **项目版本**: 3.72.0  
> **包含内容**: 整体架构图、核心模块图、连接节点图、模块详解

---

## 一、整体架构图

```svg
<svg viewBox="0 0 1200 900" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 渐变定义 -->
    <linearGradient id="webviewGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="controllerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f093fb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f5576c;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="coreGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4facfe;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#00f2fe;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="servicesGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#43e97b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#38f9d7;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="integrationGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#fa709a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#fee140;stop-opacity:1" />
    </linearGradient>
    
    <!-- 箭头标记 -->
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  
  <!-- 背景 -->
  <rect width="1200" height="900" fill="#f8f9fa"/>
  
  <!-- 标题 -->
  <text x="600" y="40" text-anchor="middle" font-size="24" font-weight="bold" fill="#333">
    Cline 整体架构
  </text>
  
  <!-- 用户层 -->
  <g transform="translate(400, 70)">
    <rect x="0" y="0" width="400" height="60" rx="8" fill="url(#webviewGrad)"/>
    <text x="200" y="35" text-anchor="middle" font-size="16" fill="white" font-weight="bold">
      👤 用户界面 (Webview - React)
    </text>
  </g>
  
  <!-- 箭头 1 -->
  <line x1="600" y1="130" x2="600" y2="160" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="610" y="150" font-size="12" fill="#666">Message Passing</text>
  
  <!-- Controller 层 -->
  <g transform="translate(350, 170)">
    <rect x="0" y="0" width="500" height="80" rx="8" fill="url(#controllerGrad)"/>
    <text x="250" y="30" text-anchor="middle" font-size="16" fill="white" font-weight="bold">
      🎮 Controller 层
    </text>
    <text x="250" y="55" text-anchor="middle" font-size="12" fill="white">
      消息处理 | 任务管理 | 状态同步
    </text>
  </g>
  
  <!-- 箭头 2 -->
  <line x1="600" y1="250" x2="600" y2="280" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- Core 层 -->
  <g transform="translate(350, 290)">
    <rect x="0" y="0" width="500" height="100" rx="8" fill="url(#coreGrad)"/>
    <text x="250" y="30" text-anchor="middle" font-size="16" fill="white" font-weight="bold">
      ⚙️ Core 核心层
    </text>
    <text x="250" y="55" text-anchor="middle" font-size="12" fill="white">
      Task | API Handler | Context | Storage
    </text>
    <text x="250" y="80" text-anchor="middle" font-size="12" fill="white">
      任务执行 | LLM 交互 | 上下文管理
    </text>
  </g>
  
  <!-- 箭头 3 -->
  <line x1="600" y1="390" x2="600" y2="420" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- Services 层 -->
  <g transform="translate(200, 430)">
    <rect x="0" y="0" width="800" height="120" rx="8" fill="url(#servicesGrad)"/>
    <text x="400" y="30" text-anchor="middle" font-size="16" fill="white" font-weight="bold">
      🔧 Services 服务层
    </text>
    <g transform="translate(50, 50)">
      <rect x="0" y="0" width="140" height="50" rx="5" fill="white" fill-opacity="0.3"/>
      <text x="70" y="30" text-anchor="middle" font-size="11" fill="white">MCP Hub</text>
      
      <rect x="160" y="0" width="140" height="50" rx="5" fill="white" fill-opacity="0.3"/>
      <text x="230" y="30" text-anchor="middle" font-size="11" fill="white">Browser</text>
      
      <rect x="320" y="0" width="140" height="50" rx="5" fill="white" fill-opacity="0.3"/>
      <text x="390" y="30" text-anchor="middle" font-size="11" fill="white">Terminal</text>
      
      <rect x="480" y="0" width="140" height="50" rx="5" fill="white" fill-opacity="0.3"/>
      <text x="550" y="30" text-anchor="middle" font-size="11" fill="white">Auth</text>
      
      <rect x="640" y="0" width="140" height="50" rx="5" fill="white" fill-opacity="0.3"/>
      <text x="710" y="30" text-anchor="middle" font-size="11" fill="white">Checkpoints</text>
    </g>
  </g>
  
  <!-- 箭头 4 -->
  <line x1="600" y1="550" x2="600" y2="580" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  
  <!-- Integrations 层 -->
  <g transform="translate(200, 590)">
    <rect x="0" y="0" width="800" height="120" rx="8" fill="url(#integrationGrad)"/>
    <text x="400" y="30" text-anchor="middle" font-size="16" fill="white" font-weight="bold">
      🔌 Integrations 集成层
    </text>
    <g transform="translate(50, 50)">
      <rect x="0" y="0" width="140" height="50" rx="5" fill="white" fill-opacity="0.3"/>
      <text x="70" y="30" text-anchor="middle" font-size="11" fill="white">VS Code API</text>
      
      <rect x="160" y="0" width="140" height="50" rx="5" fill="white" fill-opacity="0.3"/>
      <text x="230" y="30" text-anchor="middle" font-size="11" fill="white">File System</text>
      
      <rect x="320" y="0" width="140" height="50" rx="5" fill="white" fill-opacity="0.3"/>
      <text x="390" y="30" text-anchor="middle" font-size="11" fill="white">Terminal</text>
      
      <rect x="480" y="0" width="140" height="50" rx="5" fill="white" fill-opacity="0.3"/>
      <text x="550" y="30" text-anchor="middle" font-size="11" fill="white">Browser</text>
      
      <rect x="640" y="0" width="140" height="50" rx="5" fill="white" fill-opacity="0.3"/>
      <text x="710" y="30" text-anchor="middle" font-size="11" fill="white">LLM APIs</text>
    </g>
  </g>
  
  <!-- 外部连接 -->
  <g transform="translate(50, 750)">
    <text x="0" y="0" font-size="14" fill="#666" font-weight="bold">外部服务:</text>
    
    <g transform="translate(0, 30)">
      <rect x="0" y="0" width="150" height="40" rx="5" fill="#e0e0e0"/>
      <text x="75" y="25" text-anchor="middle" font-size="11" fill="#333">🤖 Claude/OpenAI</text>
      
      <rect x="170" y="0" width="150" height="40" rx="5" fill="#e0e0e0"/>
      <text x="245" y="25" text-anchor="middle" font-size="11" fill="#333">📁 本地文件系统</text>
      
      <rect x="340" y="0" width="150" height="40" rx="5" fill="#e0e0e0"/>
      <text x="415" y="25" text-anchor="middle" font-size="11" fill="#333">💻 终端/Shell</text>
      
      <rect x="510" y="0" width="150" height="40" rx="5" fill="#e0e0e0"/>
      <text x="585" y="25" text-anchor="middle" font-size="11" fill="#333">🌐 浏览器</text>
      
      <rect x="680" y="0" width="150" height="40" rx="5" fill="#e0e0e0"/>
      <text x="755" y="25" text-anchor="middle" font-size="11" fill="#333">🔌 MCP 服务器</text>
    </g>
  </g>
  
  <!-- 连接外部服务的虚线 -->
  <line x1="300" y1="710" x2="300" y2="745" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>
  <line x1="500" y1="710" x2="500" y2="745" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>
  <line x1="700" y1="710" x2="700" y2="745" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>
  <line x1="900" y1="710" x2="900" y2="745" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>
  <line x1="1100" y1="710" x2="1100" y2="745" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>
</svg>
```

---

## 二、核心模块连接图

```svg
<svg viewBox="0 0 1400 1000" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 渐变 -->
    <linearGradient id="controllerGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f093fb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f5576c;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="taskGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4facfe;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#00f2fe;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="apiGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="mcpGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#43e97b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#38f9d7;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="toolGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#fa709a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#fee140;stop-opacity:1" />
    </linearGradient>
    
    <!-- 箭头 -->
    <marker id="arrowBlue" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#4facfe"/>
    </marker>
    <marker id="arrowRed" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#f5576c"/>
    </marker>
  </defs>
  
  <!-- 背景 -->
  <rect width="1400" height="1000" fill="#fafbfc"/>
  
  <!-- 标题 -->
  <text x="700" y="40" text-anchor="middle" font-size="24" font-weight="bold" fill="#333">
    Cline 核心模块与连接
  </text>
  
  <!-- Controller -->
  <g transform="translate(550, 80)">
    <rect x="0" y="0" width="300" height="80" rx="8" fill="url(#controllerGrad2)"/>
    <text x="150" y="35" text-anchor="middle" font-size="16" fill="white" font-weight="bold">
      🎮 Controller
    </text>
    <text x="150" y="60" text-anchor="middle" font-size="11" fill="white">
      消息处理 / 状态管理
    </text>
  </g>
  
  <!-- 向下连接 -->
  <line x1="700" y1="160" x2="700" y2="200" stroke="#4facfe" stroke-width="3" marker-end="url(#arrowBlue)"/>
  
  <!-- Task -->
  <g transform="translate(550, 200)">
    <rect x="0" y="0" width="300" height="80" rx="8" fill="url(#taskGrad)"/>
    <text x="150" y="35" text-anchor="middle" font-size="16" fill="white" font-weight="bold">
      ⚙️ Task
    </text>
    <text x="150" y="60" text-anchor="middle" font-size="11" fill="white">
      任务执行引擎
    </text>
  </g>
  
  <!-- Task 向左连接 API -->
  <line x1="550" y1="240" x2="400" y2="240" stroke="#4facfe" stroke-width="2" marker-end="url(#arrowBlue)"/>
  
  <!-- API Handler -->
  <g transform="translate(150, 200)">
    <rect x="0" y="0" width="220" height="80" rx="8" fill="url(#apiGrad)"/>
    <text x="110" y="35" text-anchor="middle" font-size="14" fill="white" font-weight="bold">
      🤖 API Handler
    </text>
    <text x="110" y="60" text-anchor="middle" font-size="11" fill="white">
      LLM 交互
    </text>
  </g>
  
  <!-- API 向上连接 LLM -->
  <line x1="260" y1="200" x2="260" y2="120" stroke="#667eea" stroke-width="2" stroke-dasharray="5,5"/>
  <g transform="translate(50, 80)">
    <rect x="0" y="0" width="200" height="40" rx="5" fill="#e8e8e8"/>
    <text x="100" y="25" text-anchor="middle" font-size="12" fill="#333">
      Claude / GPT / Gemini
    </text>
  </g>
  
  <!-- Task 向右连接 ToolExecutor -->
  <line x1="850" y1="240" x2="1000" y2="240" stroke="#4facfe" stroke-width="2" marker-end="url(#arrowBlue)"/>
  
  <!-- ToolExecutor -->
  <g transform="translate(1000, 200)">
    <rect x="0" y="0" width="220" height="80" rx="8" fill="url(#toolGrad)"/>
    <text x="110" y="35" text-anchor="middle" font-size="14" fill="white" font-weight="bold">
      🔧 ToolExecutor
    </text>
    <text x="110" y="60" text-anchor="middle" font-size="11" fill="white">
      工具执行协调器
    </text>
  </g>
  
  <!-- Task 向下连接 MCP -->
  <line x1="700" y1="280" x2="700" y2="350" stroke="#4facfe" stroke-width="2" marker-end="url(#arrowBlue)"/>
  
  <!-- MCP Hub -->
  <g transform="translate(550, 350)">
    <rect x="0" y="0" width="300" height="80" rx="8" fill="url(#mcpGrad)"/>
    <text x="150" y="35" text-anchor="middle" font-size="16" fill="white" font-weight="bold">
      🔌 MCP Hub
    </text>
    <text x="150" y="60" text-anchor="middle" font-size="11" fill="white">
      MCP 服务器管理
    </text>
  </g>
  
  <!-- MCP 向下连接外部 MCP -->
  <line x1="700" y1="430" x2="700" y2="480" stroke="#43e97b" stroke-width="2" stroke-dasharray="5,5"/>
  <g transform="translate(600, 480)">
    <rect x="0" y="0" width="200" height="40" rx="5" fill="#e8f8f0"/>
    <text x="100" y="25" text-anchor="middle" font-size="12" fill="#333">
      外部 MCP 服务器
    </text>
  </g>
  
  <!-- ToolExecutor 向下分支 -->
  <line x1="1110" y1="280" x2="1110" y2="350" stroke="#fa709a" stroke-width="2"/>
  
  <!-- 工具分支 -->
  <g transform="translate(850, 350)">
    <!-- File Tools -->
    <rect x="0" y="0" width="140" height="60" rx="5" fill="#fff0f5" stroke="#fa709a" stroke-width="2"/>
    <text x="70" y="25" text-anchor="middle" font-size="12" fill="#333" font-weight="bold">📁 File</text>
    <text x="70" y="45" text-anchor="middle" font-size="10" fill="#666">读写/创建/删除</text>
    
    <!-- Terminal -->
    <rect x="160" y="0" width="140" height="60" rx="5" fill="#fff0f5" stroke="#fa709a" stroke-width="2"/>
    <text x="230" y="25" text-anchor="middle" font-size="12" fill="#333" font-weight="bold">💻 Terminal</text>
    <text x="230" y="45" text-anchor="middle" font-size="10" fill="#666">命令执行</text>
    
    <!-- Browser -->
    <rect x="320" y="0" width="140" height="60" rx="5" fill="#fff0f5" stroke="#fa709a" stroke-width="2"/>
    <text x="390" y="25" text-anchor="middle" font-size="12" fill="#333" font-weight="bold">🌐 Browser</text>
    <text x="390" y="45" text-anchor="middle" font-size="10" fill="#666">导航/点击/截图</text>
  </g>
  
  <!-- Controller 向左连接 Webview -->
  <line x1="550" y1="120" x2="400" y2="120" stroke="#f5576c" stroke-width="2" marker-end="url(#arrowRed)"/>
  
  <!-- Webview -->
  <g transform="translate(150, 80)">
    <rect x="0" y="0" width="220" height="80" rx="8" fill="#e8e8e8"/>
    <text x="110" y="35" text-anchor="middle" font-size="14" fill="#333" font-weight="bold">
      💬 Webview
    </text>
    <text x="110" y="60" text-anchor="middle" font-size="11" fill="#666">
      React UI
    </text>
  </g>
  
  <!-- Controller 向右连接 State -->
  <line x1="850" y1="120" x2="1000" y2="120" stroke="#f5576c" stroke-width="2" marker-end="url(#arrowRed)"/>
  
  <!-- State Manager -->
  <g transform="translate(1000, 80)">
    <rect x="0" y="0" width="220" height="80" rx="8" fill="#f0f0f0"/>
    <text x="110" y="35" text-anchor="middle" font-size="14" fill="#333" font-weight="bold">
      💾 State Manager
    </text>
    <text x="110" y="60" text-anchor="middle" font-size="11" fill="#666">
      状态持久化
    </text>
  </g>
  
  <!-- Task 向下连接 Checkpoints -->
  <line x1="700" y1="280" x2="900" y2="350" stroke="#4facfe" stroke-width="2" stroke-dasharray="5,5"/>
  
  <!-- Checkpoints -->
  <g transform="translate(800, 430)">
    <rect x="0" y="0" width="200" height="60" rx="5" fill="#fff8dc" stroke="#daa520" stroke-width="2"/>
    <text x="100" y="25" text-anchor="middle" font-size="13" fill="#333" font-weight="bold">
      💾 Checkpoints
    </text>
    <text x="100" y="45" text-anchor="middle" font-size="11" fill="#666">
      工作区快照
    </text>
  </g>
  
  <!-- 图例 -->
  <g transform="translate(50, 550)">
    <text x="0" y="0" font-size="16" fill="#333" font-weight="bold">图例:</text>
    
    <rect x="0" y="20" width="20" height="20" fill="#f093fb"/>
    <text x="30" y="35" font-size="12" fill="#666">控制流</text>
    
    <rect x="120" y="20" width="20" height="20" fill="#4facfe"/>
    <text x="150" y="35" font-size="12" fill="#666">数据流</text>
    
    <rect x="240" y="20" width="20" height="20" fill="none" stroke="#666" stroke-dasharray="5,5"/>
    <text x="270" y="35" font-size="12" fill="#666">外部连接</text>
  </g>
</svg>
```

---

## 三、数据流与工作流程图

```svg
<svg viewBox="0 0 1400 800" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="userGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="processGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f093fb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f5576c;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="llmGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4facfe;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#00f2fe;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="toolGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#43e97b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#38f9d7;stop-opacity:1" />
    </linearGradient>
    
    <marker id="flowArrow" markerWidth="12" markerHeight="10" refX="11" refY="5" orient="auto">
      <polygon points="0 0, 12 5, 0 10" fill="#667eea"/>
    </marker>
  </defs>
  
  <!-- 背景 -->
  <rect width="1400" height="800" fill="#f8f9fa"/>
  
  <!-- 标题 -->
  <text x="700" y="40" text-anchor="middle" font-size="24" font-weight="bold" fill="#333">
    Cline 工作流程
  </text>
  
  <!-- 1. 用户输入 -->
  <g transform="translate(100, 100)">
    <rect x="0" y="0" width="200" height="80" rx="8" fill="url(#userGrad)"/>
    <text x="100" y="35" text-anchor="middle" font-size="16" fill="white" font-weight="bold">
      1️⃣ 用户输入
    </text>
    <text x="100" y="60" text-anchor="middle" font-size="11" fill="white">
      "帮我创建 React 组件"
    </text>
  </g>
  
  <!-- 箭头 -->
  <line x1="300" y1="140" x2="350" y2="140" stroke="#667eea" stroke-width="3" marker-end="url(#flowArrow)"/>
  
  <!-- 2. 构建 Prompt -->
  <g transform="translate(350, 100)">
    <rect x="0" y="0" width="200" height="80" rx="8" fill="url(#processGrad)"/>
    <text x="100" y="35" text-anchor="middle" font-size="16" fill="white" font-weight="bold">
      2️⃣ 构建 Prompt
    </text>
    <text x="100" y="60" text-anchor="middle" font-size="11" fill="white">
      系统 Prompt + 上下文
    </text>
  </g>
  
  <!-- 箭头 -->
  <line x1="550" y1="140" x2="600" y2="140" stroke="#667eea" stroke-width="3" marker-end="url(#flowArrow)"/>
  
  <!-- 3. 调用 LLM -->
  <g transform="translate(600, 100)">
    <rect x="0" y="0" width="200" height="80" rx="8" fill="url(#llmGrad)"/>
    <text x="100" y="35" text-anchor="middle" font-size="16" fill="white" font-weight="bold">
      3️⃣ 调用 LLM
    </text>
    <text x="100" y="60" text-anchor="middle" font-size="11" fill="white">
      Claude / GPT / Gemini
    </text>
  </g>
  
  <!-- LLM 外部 -->
  <g transform="translate(600, 50)">
    <rect x="0" y="0" width="200" height="40" rx="5" fill="#e8f4f8" stroke="#4facfe" stroke-width="2"/>
    <text x="100" y="25" text-anchor="middle" font-size="12" fill="#333">
      🤖 外部 LLM API
    </text>
  </g>
  <line x1="700" y1="90" x2="700" y2="100" stroke="#4facfe" stroke-width="2" stroke-dasharray="5,5"/>
  
  <!-- 箭头 -->
  <line x1="800" y1="140" x2="850" y2="140" stroke="#667eea" stroke-width="3" marker-end="url(#flowArrow)"/>
  
  <!-- 4. 解析响应 -->
  <g transform="translate(850, 100)">
    <rect x="0" y="0" width="200" height="80" rx="8" fill="url(#processGrad)"/>
    <text x="100" y="35" text-anchor="middle" font-size="16" fill="white" font-weight="bold">
      4️⃣ 解析响应
    </text>
    <text x="100" y="60" text-anchor="middle" font-size="11" fill="white">
      文本 or 工具调用？
    </text>
  </g>
  
  <!-- 分支判断 -->
  <line x1="1050" y1="140" x2="1100" y2="140" stroke="#667eea" stroke-width="3"/>
  <line x1="1100" y1="140" x2="1100" y2="200" stroke="#667eea" stroke-width="2"/>
  <line x1="1100" y1="140" x2="1100" y2="80" stroke="#667eea" stroke-width="2"/>
  
  <!-- 文本响应 -->
  <g transform="translate(1100, 200)">
    <rect x="0" y="0" width="200" height="60" rx="5" fill="#fff8dc" stroke="#daa520" stroke-width="2"/>
    <text x="100" y="30" text-anchor="middle" font-size="14" fill="#333" font-weight="bold">
      📝 文本响应
    </text>
    <text x="100" y="50" text-anchor="middle" font-size="11" fill="#666">
      直接显示给用户
    </text>
  </g>
  
  <!-- 工具调用 -->
  <g transform="translate(1100, 20)">
    <rect x="0" y="0" width="200" height="60" rx="5" fill="#e8f8f0" stroke="#43e97b" stroke-width="2"/>
    <text x="100" y="30" text-anchor="middle" font-size="14" fill="#333" font-weight="bold">
      🔧 工具调用
    </text>
    <text x="100" y="50" text-anchor="middle" font-size="11" fill="#666">
      执行工具
    </text>
  </g>
  
  <!-- 工具调用向下 -->
  <line x1="1200" y1="50" x2="1250" y2="50" stroke="#43e97b" stroke-width="2" marker-end="url(#flowArrow)"/>
  
  <!-- 5. 执行工具 -->
  <g transform="translate(1250, 10)">
    <rect x="0" y="0" width="130" height="80" rx="5" fill="url(#toolGrad2)"/>
    <text x="65" y="30" text-anchor="middle" font-size="13" fill="white" font-weight="bold">
      5️⃣ 执行工具
    </text>
    <text x="65" y="50" text-anchor="middle" font-size="10" fill="white">File/Terminal/</text>
    <text x="65" y="65" text-anchor="middle" font-size="10" fill="white">Browser/MCP</text>
  </g>
  
  <!-- 工具列表 -->
  <g transform="translate(1250, 120)">
    <rect x="0" y="0" width="130" height="120" rx="5" fill="#f0f0f0" stroke="#666" stroke-width="1"/>
    <text x="65" y="20" text-anchor="middle" font-size="11" fill="#333" font-weight="bold">可用工具:</text>
    <text x="10" y="40" font-size="10" fill="#666">📁 ReadFile</text>
    <text x="10" y="60" font-size="10" fill="#666">✏️ WriteToFile</text>
    <text x="10" y="80" font-size="10" fill="#666">💻 ExecuteCommand</text>
    <text x="10" y="100" font-size="10" fill="#666">🌐 UseBrowser</text>
    <text x="10" y="120" font-size="10" fill="#666">🔌 CallMcpTool</text>
  </g>
  
  <!-- 工具执行后反馈 -->
  <line x1="1250" y1="90" x2="1250" y2="300" stroke="#43e97b" stroke-width="2"/>
  <line x1="1250" y1="300" x2="700" y2="300" stroke="#43e97b" stroke-width="2" stroke-dasharray="5,5"/>
  <line x1="700" y1="300" x2="700" y2="180" stroke="#43e97b" stroke-width="2" marker-end="url(#flowArrow)"/>
  
  <!-- 反馈标签 -->
  <text x="720" y="250" font-size="12" fill="#43e97b" font-weight="bold">
    ↩️ 结果反馈给 LLM
  </text>
  
  <!-- 循环标签 -->
  <g transform="translate(500, 220)">
    <rect x="0" y="0" width="150" height="50" rx="5" fill="#fff0f5" stroke="#f5576c" stroke-width="2"/>
    <text x="75" y="30" text-anchor="middle" font-size="12" fill="#f5576c" font-weight="bold">
      🔄 循环执行
    </text>
  </g>
  
  <!-- 6. 任务完成 -->
  <line x1="1050" y1="140" x2="1250" y2="140" stroke="#667eea" stroke-width="2"/>
  <line x1="1250" y1="140" x2="1250" y2="400" stroke="#667eea" stroke-width="2"/>
  
  <g transform="translate(1150, 400)">
    <rect x="0" y="0" width="200" height="80" rx="8" fill="#43e97b"/>
    <text x="100" y="35" text-anchor="middle" font-size="16" fill="white" font-weight="bold">
      6️⃣ 任务完成
    </text>
    <text x="100" y="60" text-anchor="middle" font-size="11" fill="white">
      显示结果 / 保存历史
    </text>
  </g>
  
  <!-- 底部说明 -->
  <g transform="translate(50, 550)">
    <text x="0" y="0" font-size="16" fill="#333" font-weight="bold">关键特性:</text>
    
    <rect x="0" y="20" width="20" height="20" fill="#667eea"/>
    <text x="30" y="35" font-size="12" fill="#666">用户批准每个步骤</text>
    
    <rect x="200" y="20" width="20" height="20" fill="#43e97b"/>
    <text x="230" y="35" font-size="12" fill="#666">自动创建快照</text>
    
    <rect x="400" y="20" width="20" height="20" fill="none" stroke="#666" stroke-dasharray="5,5"/>
    <text x="430" y="35" font-size="12" fill="#666">循环直到任务完成</text>
  </g>
</svg>
```

---

## 四、核心模块详解

### 4.1 Controller 模块 🎮

**位置**: `src/core/controller/`  
**代码量**: ~41KB  
**核心文件**: `index.ts`

#### 职责
- Webview 消息处理中枢
- Task 生命周期管理
- 状态同步到 Webview
- MCP Hub 管理
- 认证和账户管理

#### 核心方法
```typescript
class Controller {
  // 初始化任务
  async initTask(taskId: string): Promise<void>
  
  // 执行动作
  async executeAction(action: string, data?: any): Promise<void>
  
  // 取消任务
  async cancelTask(): Promise<void>
  
  // 清除任务
  async clearTask(): Promise<void>
  
  // 同步状态到 Webview
  async postStateToWebview(): Promise<void>
}
```

#### 连接关系
```
Webview ←→ Controller ←→ Task
                ↓
          State Manager
                ↓
           MCP Hub
```

---

### 4.2 Task 模块 ⚙️

**位置**: `src/core/task/`  
**代码量**: ~148KB  
**核心文件**: `index.ts`, `ToolExecutor.ts`

#### 职责
- AI 任务执行引擎
- LLM 对话管理
- 工具调用协调
- 检查点创建/恢复

#### 核心流程
```typescript
class Task {
  async startTask(prompt: string): Promise<void> {
    // 1. 构建 Prompt
    // 2. 调用 LLM
    // 3. 解析响应
    // 4. 执行工具
    // 5. 反馈结果
    // 6. 循环直到完成
  }
}
```

#### 连接关系
```
Controller → Task → API Handler → LLM
                 ↓
          ToolExecutor
                 ↓
      File/Terminal/Browser/MCP
```

---

### 4.3 API Handler 模块 🤖

**位置**: `src/core/api/`  
**代码量**: ~22KB  
**核心文件**: `index.ts`

#### 职责
- 与 LLM 提供商交互
- 流式响应处理
- Token 计数和成本追踪
- 自动重试机制

#### 支持的提供商
```typescript
enum ApiProvider {
  anthropic = "anthropic",      // Claude
  openrouter = "openrouter",    // OpenRouter
  openai = "openai",            // GPT
  gemini = "gemini",            // Gemini
  bedrock = "bedrock",          // AWS Bedrock
  azure = "azure",              // Azure OpenAI
  vertex = "vertex",            // GCP Vertex
  // ... 20+ 提供商
}
```

#### 连接关系
```
Task → API Handler → LLM Provider
                ↓
          Token/Cost Tracking
```

---

### 4.4 ToolExecutor 模块 🔧

**位置**: `src/core/task/tools/`  
**代码量**: ~24KB  
**核心文件**: `ToolExecutor.ts`, `ToolExecutorCoordinator.ts`

#### 职责
- 工具调用验证
- 用户审批流程
- 工具执行协调
- 结果捕获和反馈

#### 可用工具
| 工具 | 功能 | 需审批 |
|------|------|--------|
| **ReadFile** | 读取文件 | ❌ 否 |
| **WriteToFile** | 写入文件 | ✅ 是 |
| **ExecuteCommand** | 执行命令 | ✅ 是 |
| **UseBrowser** | 浏览器操作 | ✅ 是 |
| **CallMcpTool** | MCP 工具 | ✅ 是 |
| **SearchFiles** | 文件搜索 | ❌ 否 |

#### 连接关系
```
Task → ToolExecutor → Tool Validator
                 ↓
            User Approval
                 ↓
      File/Terminal/Browser
```

---

### 4.5 MCP Hub 模块 🔌

**位置**: `src/services/mcp/`  
**代码量**: ~59KB  
**核心文件**: `McpHub.ts`, `McpOAuthManager.ts`

#### 职责
- MCP 服务器管理
- 工具发现注册
- OAuth 认证处理
- 流式 HTTP 重连

#### 核心方法
```typescript
class McpHub {
  // 添加服务器
  async addServer(config: McpServerConfig): Promise<void>
  
  // 移除服务器
  async removeServer(name: string): Promise<void>
  
  // 调用工具
  async callTool(server: string, tool: string, params: any): Promise<any>
  
  // 列出工具
  async listTools(): Promise<McpTool[]>
}
```

#### 连接关系
```
Controller → MCP Hub → MCP Server 1
                   → MCP Server 2
                   → MCP Server N
```

---

### 4.6 Checkpoints 模块 💾

**位置**: `src/integrations/checkpoints/`  
**代码量**: ~10KB  
**核心文件**: `CheckpointManager.ts`

#### 职责
- 工作区快照创建
- 快照对比
- 快照恢复
- 增量快照优化

#### 使用场景
```typescript
// 创建快照
await checkpoints.save({
  workspaceState: getWorkspaceSnapshot(),
  taskState: task.getCurrentState(),
  timestamp: Date.now()
})

// 对比差异
const diff = await checkpoints.compare(checkpointId)

// 恢复快照
await checkpoints.restore(checkpointId)
```

#### 连接关系
```
Task → Checkpoints → File System
              ↓
         Snapshot Storage
```

---

### 4.7 State Manager 模块 📦

**位置**: `src/core/storage/`  
**代码量**: ~15KB  
**核心文件**: `StateManager.ts`

#### 职责
- 状态持久化
- 状态同步
- 迁移管理
- 错误恢复

#### 核心特性
- ✅ 防抖持久化（避免频繁写入）
- ✅ 内存缓存（快速读取）
- ✅ 错误恢复（持久化失败不中断）
- ✅ 外部同步（多实例同步）

#### 连接关系
```
Controller → State Manager → Global State
                       → Workspace State
                       → File Storage
```

---

### 4.8 Browser 模块 🌐

**位置**: `src/services/browser/`  
**代码量**: ~8KB  
**核心文件**: `BrowserService.ts`

#### 职责
- 启动无头浏览器
- 页面导航
- 元素交互（点击/输入）
- 截图和日志捕获

#### Computer Use 能力
```typescript
class BrowserService {
  async navigate(url: string): Promise<void>
  async click(selector: string): Promise<void>
  async type(selector: string, text: string): Promise<void>
  async screenshot(): Promise<string>
  async getConsoleLogs(): Promise<string>
}
```

#### 连接关系
```
ToolExecutor → Browser → Chrome/Chromium
                    ↓
              Screenshots/Logs
```

---

### 4.9 Terminal 模块 💻

**位置**: `src/integrations/terminal/`  
**代码量**: ~12KB  
**核心文件**: `TerminalManager.ts`

#### 职责
- Shell 命令执行
- 输出捕获
- 长时间进程监控
- VS Code Shell 集成

#### 安全机制
```typescript
// 命令执行前
const approval = await userApprove(command)
if (!approval) {
  throw new Error("User denied")
}

// 执行命令
const result = await executeCommand(command)
```

#### 连接关系
```
ToolExecutor → Terminal → Shell
                    ↓
              Output/Exit Code
```

---

## 五、模块间通信协议

### 5.1 Webview ↔ Controller

**协议**: VS Code Message Passing  
**格式**: JSON-RPC

```typescript
// Webview → Controller
webview.postMessage({
  type: "action",
  action: "startTask",
  data: { prompt: "..." }
})

// Controller → Webview
webview.postMessage({
  type: "state",
  state: { ... }
})
```

---

### 5.2 Controller ↔ Task

**协议**: 直接方法调用  
**格式**: TypeScript 类方法

```typescript
// Controller 创建 Task
this.task = new Task({
  apiHandler,
  toolExecutor,
  checkpoints
})

// Task 执行
await this.task.startTask(prompt)
```

---

### 5.3 Task ↔ API Handler

**协议**: 流式 API 调用  
**格式**: Stream Response

```typescript
// Task 调用 API
const stream = apiHandler.createMessage({
  messages,
  systemPrompt
})

// 处理流式响应
for await (const chunk of stream) {
  yield chunk
}
```

---

### 5.4 Task ↔ ToolExecutor

**协议**: 工具调用协议  
**格式**: Tool Call Schema

```typescript
// Task 请求工具调用
const result = await toolExecutor.execute({
  tool: "write_to_file",
  params: { path: "...", content: "..." },
  requiresApproval: true
})
```

---

### 5.5 gRPC 内部通信

**协议**: gRPC + Protocol Buffers  
**位置**: `proto/`

```protobuf
// proto 定义示例
service ClineService {
  rpc SendMessage (MessageRequest) returns (MessageResponse);
  rpc StreamResponse (StreamRequest) returns (stream StreamResponse);
}
```

---

## 六、总结

### 架构优势

| 优势 | 说明 |
|------|------|
| **分层清晰** | Webview → Controller → Core → Services |
| **模块化** | 各模块职责明确，易于维护 |
| **可扩展** | MCP 协议支持插件扩展 |
| **安全性** | 人工审批 + 快照恢复 |
| **多模型** | 支持 20+ 模型提供商 |

---

### 核心数据流

```
用户 → Webview → Controller → Task → API → LLM
                                    ↓
                              ToolExecutor
                                    ↓
                          File/Terminal/Browser/MCP
                                    ↓
                              结果反馈 → LLM
                                    ↓
                              循环直到完成
```

---

### 关键设计模式

| 模式 | 应用位置 | 说明 |
|------|---------|------|
| **Observer** | Webview ↔ Controller | 状态同步 |
| **Strategy** | API Handler | 多模型支持 |
| **Command** | ToolExecutor | 工具调用 |
| **Memento** | Checkpoints | 快照恢复 |
| **Factory** | API Provider | 提供商创建 |

---

**文档创建时间**: 2026 年 3 月 13 日  
**包含内容**: 3 个 SVG 架构图 + 核心模块详解 + 通信协议说明

---

*注：架构图为 SVG 格式，可在支持 SVG 的 Markdown 阅读器中直接查看，或保存为 .svg 文件用浏览器打开。*
