# PR: Quinoa 主题 - 侧边栏 UI 优化

## 📋 变更概述

优化最近文章组件（recent_posts）的样式和布局，提升阅读体验。

## ✨ 改进内容

### 1. 简化布局
- 移除缩略图显示，采用纯文本列表
- 减少视觉干扰，更专注于内容
- 统一使用 `no-thumbnail` 模式

### 2. 标题优化
- 自动去除数字前缀（如 "1. 文章标题" → "文章标题"）
- 标题文字溢出时显示省略号
- Hover 时标题轻微右移（3px），增加交互感

### 3. 美化元信息
- **分类标签**: 圆角背景，浅灰色，hover 变浅蓝
- **日期格式**: MM-DD 格式，斜体显示
- **布局**: Flexbox 左右分布，清晰对齐

### 4. 交互优化
- 列表项 hover 时浅灰背景
- 边框分隔线，最后一项无边框
- 平滑过渡动画（0.2s）

### 5. 其他
- 更新网易云音乐播放器 ID

## 📊 效果对比

### 之前
```
[缩略图]  1. AI 日报 2026-03-14
         AI 日报 · 2026-03-14
```

### 现在
```
AI 日报 2026-03-14
[AI 日报]                         03-14
```

## 🔧 修改文件

### `layout/widget/recent_posts.ejs`
- 移除缩略图相关代码
- 简化标题处理逻辑
- 添加 `.item-meta` 容器
- 优化日期格式

### `source/css/_partial/sidebar.styl`
- 重构 `no-thumbnail` 样式
- 添加 hover 效果
- 美化分类标签样式
- 优化间距和字体大小

### `layout/base/base.ejs`
- 更新音乐播放器 ID

## 🎨 样式细节

```stylus
// 列表项
li
    padding: 8px 0
    border-bottom: 1px solid #f0f0f0
    &:hover
        background-color: #f9f9f9

// 标题
.item-title a
    font-size: 14px
    white-space: nowrap
    text-overflow: ellipsis
    &:hover
        color: color-link
        transform: translateX(3px)

// 分类标签
.item-category a
    background-color: #f5f5f5
    padding: 2px 6px
    border-radius: 3px
    &:hover
        background-color: #e8f4ff

// 日期
.item-date
    color: #bbb
    font-size: 11px
    font-style: italic
```

## 📱 响应式

- 自适应侧边栏宽度
- 文字溢出自动省略
- 移动端友好

## 🧪 测试

- ✅ 最近文章组件正常显示
- ✅ 分类链接正常跳转
- ✅ Hover 效果流畅
- ✅ 无控制台错误

## 📸 截图

（待补充）

---

**分支**: `feature/sidebar-ui-improvements`  
**影响范围**: 侧边栏最近文章组件  
**向后兼容**: 是（仅样式优化）
