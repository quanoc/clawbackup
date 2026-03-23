# Cline AI 编码助手架构图

## 架构总览

```mermaid
flowchart TB
    subgraph User["👤 用户层"]
        VSCode[VSCode 编辑器]
        ChatPanel[聊天面板]
        StatusBar[状态栏]
    end

    subgraph UI["🎨 UI Layer - 界面层"]
        ExtensionHost[扩展宿主进程]
        Webview[Webview 面板]
        CommandPalette[命令面板]
        Notifications[通知系统]
    end

    subgraph Core["⚙️ Core Engine - 核心引擎"]
        TaskScheduler[任务调度器]
        MessageRouter[消息路由器]
        StateManager[状态管理器]
        ErrorHandler[错误处理器]
    end

    subgraph LLM["🧠 LLM Interface - 模型接口"]
        APIWrapper[API 封装层]
        PromptManager[提示词管理器]
        TokenCounter[Token 计数器]
        ModelSelector[模型选择器]
        RateLimiter[速率限制器]
    end

    subgraph Context["📚 Context Manager - 上下文管理"]
        MemoryStore[记忆存储]
        ConversationHistory[对话历史]
        WorkspaceIndex[工作区索引]
        FileCache[文件缓存]
        EmbeddingEngine[嵌入引擎]
    end

    subgraph Tools["🛠️ Tool System - 工具系统"]
        FileSystem[文件系统工具]
        Terminal[终端工具]
        GitTools[Git 工具]
        NetworkTools[网络工具]
        SearchTools[搜索工具]
        CodeTools[代码分析工具]
    end

    subgraph Sandbox["🔒 Execution Sandbox - 执行沙箱"]
        CodeExecutor[代码执行器]
        SecurityPolicy[安全策略]
        ResourceLimits[资源限制]
        OutputCapture[输出捕获]
    end

    %% 用户到 UI 层
    VSCode --> ExtensionHost
    ChatPanel --> Webview
    StatusBar --> ExtensionHost

    %% UI 层到核心引擎
    ExtensionHost --> TaskScheduler
    Webview --> MessageRouter
    CommandPalette --> TaskScheduler
    Notifications --> StateManager

    %% 核心引擎内部流转
    TaskScheduler --> MessageRouter
    MessageRouter --> StateManager
    StateManager --> ErrorHandler

    %% 核心引擎到 LLM 接口
    TaskScheduler --> APIWrapper
    MessageRouter --> PromptManager
    StateManager --> TokenCounter
    APIWrapper --> ModelSelector
    APIWrapper --> RateLimiter

    %% 核心引擎到上下文管理
    StateManager --> MemoryStore
    TaskScheduler --> ConversationHistory
    WorkspaceIndex --> FileCache
    FileCache --> EmbeddingEngine

    %% 核心引擎到工具系统
    TaskScheduler --> FileSystem
    TaskScheduler --> Terminal
    TaskScheduler --> GitTools
    TaskScheduler --> NetworkTools
    TaskScheduler --> SearchTools
    TaskScheduler --> CodeTools

    %% 工具系统到执行沙箱
    CodeExecutor --> SecurityPolicy
    CodeExecutor --> ResourceLimits
    CodeExecutor --> OutputCapture
    Terminal --> CodeExecutor

    %% 数据回流
    APIWrapper -.->|响应 | TaskScheduler
    MemoryStore -.->|上下文 | PromptManager
    OutputCapture -.->|执行结果 | StateManager
    FileSystem -.->|文件内容 | Context
    GitTools -.->|版本信息 | Context

    %% 样式定义
    classDef userLayer fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
    classDef uiLayer fill:#fff4e1,stroke:#ff9900,stroke-width:2px
    classDef coreLayer fill:#f0f0f0,stroke:#333333,stroke-width:3px
    classDef llmLayer fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef contextLayer fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef toolLayer fill:#ffebee,stroke:#c62828,stroke-width:2px
    classDef sandboxLayer fill:#fff8e1,stroke:#f57f17,stroke-width:2px,stroke-dasharray: 5 5

    class User userLayer
    class UI uiLayer
    class Core coreLayer
    class LLM llmLayer
    class Context contextLayer
    class Tools toolLayer
    class Sandbox sandboxLayer
```

## 数据流详细图

```mermaid
sequenceDiagram
    participant U as 👤 用户
    participant UI as 🎨 UI Layer
    participant CE as ⚙️ Core Engine
    participant CM as 📚 Context Manager
    participant LLM as 🧠 LLM Interface
    participant TS as 🛠️ Tool System
    participant SB as 🔒 Execution Sandbox

    Note over U,SB: 完整任务执行流程

    U->>UI: 输入指令<br/>(自然语言)
    UI->>CE: 解析后的任务请求
    
    rect rgb(240, 240, 240)
        Note right of CE: 任务解析阶段
        CE->>CM: 获取相关上下文
        CM-->>CE: 返回工作区信息<br/>对话历史
        CE->>CE: 任务分解与规划
    end

    rect rgb(232, 245, 233)
        Note right of CE: LLM 调用阶段
        CE->>LLM: 构建提示词 + 上下文
        LLM->>LLM: Token 计数与优化
        LLM->>LLM: 调用模型 API
        LLM-->>CE: 返回模型响应<br/>(含工具调用意图)
    end

    rect rgb(255, 235, 237)
        Note right of CE: 工具执行阶段
        alt 需要执行工具
            CE->>TS: 分发工具调用
            TS->>SB: 安全执行代码
            SB-->>TS: 返回执行结果
            TS-->>CE: 返回工具输出
        else 无需工具
            CE->>CE: 直接处理响应
        end
    end

    rect rgb(243, 229, 245)
        Note right of CE: 结果整合阶段
        CE->>CM: 更新对话历史
        CE->>CM: 更新记忆存储
        CE->>CE: 整合所有结果
    end

    CE->>UI: 发送最终响应
    UI->>U: 展示结果<br/>(代码/文本/操作)

    Note over U,SB: 流程结束，等待下一指令
```

## 组件详细架构

```mermaid
flowchart LR
    subgraph UI_Components["UI Layer 组件详情"]
        UI1[任务输入框]
        UI2[代码预览面板]
        UI3[工具调用日志]
        UI4[进度指示器]
        UI5[配置面板]
    end

    subgraph Core_Components["Core Engine 组件详情"]
        C1[意图识别模块]
        C2[任务队列]
        C3[依赖解析器]
        C4[执行协调器]
        C5[结果聚合器]
    end

    subgraph LLM_Components["LLM Interface 组件详情"]
        L1[API 客户端集群]
        L2[提示词模板库]
        L3[响应解析器]
        L4[流式处理器]
        L5[降级策略]
    end

    subgraph Context_Components["Context Manager 组件详情"]
        M1[短期记忆]
        M2[长期记忆]
        M3[向量数据库]
        M4[文件 watcher]
        M5[符号索引]
    end

    subgraph Tool_Components["Tool System 组件详情"]
        T1[文件读/写/搜索]
        T2[shell 命令执行]
        T3[git 操作封装]
        T4[HTTP 请求工具]
        T5[代码解析器]
        T6[测试运行器]
    end

    subgraph Sandbox_Components["Execution Sandbox 组件详情"]
        S1[Docker 容器]
        S2[权限检查]
        S3[超时控制]
        S4[资源监控]
        S5[输出过滤]
    end

    UI_Components --> Core_Components
    Core_Components --> LLM_Components
    Core_Components --> Context_Components
    Core_Components --> Tool_Components
    Tool_Components --> Sandbox_Components

    classDef detail fill:#ffffff,stroke:#666666,stroke-width:1px
    class UI_Components,Core_Components,LLM_Components,Context_Components,Tool_Components,Sandbox_Components detail
```

## 安全架构

```mermaid
flowchart TB
    subgraph SecurityLayers["安全防御层"]
        L1["第一层：输入验证"]
        L2["第二层：意图审查"]
        L3["第三层：沙箱隔离"]
        L4["第四层：权限控制"]
        L5["第五层：审计日志"]
    end

    User((用户)) --> L1
    L1 -->|通过 | L2
    L2 -->|安全 | L3
    L3 -->|隔离执行 | L4
    L4 -->|记录 | L5

    L1 -.->|拒绝 | User
    L2 -.->|危险操作 | User

    subgraph Protection["保护机制"]
        P1[命令白名单]
        P2[路径限制]
        P3[网络访问控制]
        P4[资源配额]
        P5[敏感操作确认]
    end

    L3 --> P1
    L3 --> P2
    L4 --> P3
    L4 --> P4
    L2 --> P5

    classDef security fill:#ffebee,stroke:#c62828,stroke-width:2px
    class SecurityLayers,Protection security
```

## 渲染说明

### 在线渲染

1. **Mermaid Live Editor** (推荐)
   - 访问：https://mermaid.live/
   - 复制上方任意代码块粘贴即可实时预览
   - 支持导出 PNG/SVG

2. **GitHub/GitLab**
   - 在 Markdown 文件中直接使用 ```mermaid 代码块
   - 平台会自动渲染

### 本地渲染

1. **VSCode 扩展**
   ```bash
   # 安装 Mermaid 预览扩展
   # 扩展 ID: bierner.markdown-mermaid
   ```

2. **Node.js CLI**
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   mmdc -i input.mmd -o output.png
   ```

3. **Python**
   ```bash
   pip install mermaid
   # 使用 Python 脚本渲染
   ```

### 文件位置

- 本架构图已保存至：`/home/admin/.openclaw/workspace/cline-architecture.md`
- 可单独提取各代码块保存为 `.mmd` 文件

---

**架构特点总结：**

✅ **层次清晰**：6 大核心组件分层明确，职责单一  
✅ **数据流向**：双向箭头标注数据回流路径  
✅ **安全优先**：独立的安全架构和沙箱设计  
✅ **可扩展**：模块化设计便于添加新工具和能力  
✅ **生产就绪**：包含错误处理、速率限制、资源监控等生产特性
