#!/usr/bin/env node

/**
 * Wiki发布Skill
 * 
 * 功能：自动化发布文章到Wiki系统
 * 
 * 流程：
 * 1. 检查并clone clawbackup仓库
 * 2. 切换到wiki/project分支
 * 3. 检查并安装hexo和pnpm
 * 4. 安装项目依赖
 * 5. 参考指定文章结构创建markdown文档
 * 6. 执行hexo生成和部署
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const path = require('path');

const execAsync = promisify(exec);

// 配置
const CONFIG = {
  repoUrl: 'git@github.com:quanoc/clawbackup.git',
  workDir: '/root/.openclaw/workspace/dev-projects',
  projectName: 'clawbackup',
  branch: 'wiki/project',
  deployBranch: 'page',
  referenceArticle: 'source/_posts/analysis/tw93-agent-article.md',
  targetDir: 'source/_posts/analysis'
};

class WikiPublisher {
  constructor() {
    this.projectPath = path.join(CONFIG.workDir, CONFIG.projectName);
    this.logs = [];
  }

  async log(message, level = 'info') {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] [${level}] ${message}`;
    this.logs.push(logEntry);
    console.log(logEntry);
  }

  async checkAndCloneRepo() {
    await this.log('Step 1: 检查并clone仓库');
    
    try {
      await fs.access(this.projectPath);
      await this.log('仓库已存在，跳过clone');
    } catch {
      await this.log('仓库不存在，开始clone...');
      try {
        await execAsync(`cd ${CONFIG.workDir} && git clone ${CONFIG.repoUrl}`, { timeout: 60000 });
        await this.log('Clone成功');
      } catch (error) {
        await this.log(`Clone失败: ${error.message}`, 'error');
        throw error;
      }
    }
    
    // 检查主题目录
    await this.checkAndCloneTheme();
    
    return true;
  }

  async checkAndCloneTheme() {
    await this.log('Step 1.5: 检查主题目录');
    
    const themePath = path.join(this.projectPath, 'themes', 'Quinoa');
    
    try {
      // 检查主题目录是否存在且有内容
      const files = await fs.readdir(themePath);
      const hasContent = files.filter(f => f !== '.gitkeep').length > 0;
      
      if (hasContent) {
        await this.log('主题目录已有内容，跳过clone');
        return true;
      }
    } catch {
      // 目录不存在，需要创建
      await this.log('主题目录不存在');
    }
    
    // Clone主题
    await this.log('开始clone主题...');
    try {
      await execAsync(
        `cd ${this.projectPath}/themes && rm -rf Quinoa && git clone https://github.com/quanoc/hexo-theme-Quinoa.git Quinoa`,
        { timeout: 60000 }
      );
      await this.log('主题clone成功');
      return true;
    } catch (error) {
      await this.log(`主题clone失败: ${error.message}`, 'error');
      // 主题失败不阻断流程，继续执行
      return true;
    }
  }

  async switchBranch() {
    await this.log('Step 2: 切换分支');

    try {
      await execAsync(`cd ${this.projectPath} && git checkout ${CONFIG.branch}`, { timeout: 30000 });
      await this.log(`已切换到 ${CONFIG.branch} 分支`);

      // Pull 最新代码
      await this.log('拉取最新代码...');
      const sshConfigPath = path.join(this.projectPath, 'ssh_config');
      const env = {
        ...process.env,
        GIT_SSH_COMMAND: `ssh -F ${sshConfigPath} -o StrictHostKeyChecking=no`
      };
      await execAsync(`cd ${this.projectPath} && git pull origin ${CONFIG.branch}`, {
        timeout: 30000,
        env
      });
      await this.log('已拉取最新代码');
      return true;
    } catch (error) {
      await this.log(`切换分支或拉取失败: ${error.message}`, 'error');
      throw error;
    }
  }

  async checkAndInstallTools() {
    await this.log('Step 3: 检查并安装工具');
    
    // 检查pnpm
    try {
      await execAsync('which pnpm');
      await this.log('pnpm已安装');
    } catch {
      await this.log('安装pnpm...');
      await execAsync('npm install -g pnpm', { timeout: 120000 });
      await this.log('pnpm安装完成');
    }

    // 检查hexo
    try {
      await execAsync('which hexo');
      await this.log('hexo已安装');
    } catch {
      await this.log('安装hexo-cli...');
      const pnpmHome = '/root/.local/share/pnpm';
      process.env.PNPM_HOME = pnpmHome;
      process.env.PATH = `${pnpmHome}:${process.env.PATH}`;
      await execAsync('pnpm setup', { timeout: 30000 });
      await execAsync('pnpm install -g hexo-cli', { timeout: 120000 });
      await this.log('hexo-cli安装完成');
    }

    return true;
  }

  async installDependencies() {
    await this.log('Step 4: 安装项目依赖');
    
    try {
      const pnpmHome = '/root/.local/share/pnpm';
      process.env.PNPM_HOME = pnpmHome;
      process.env.PATH = `${pnpmHome}:${process.env.PATH}`;
      
      await execAsync(`cd ${this.projectPath} && pnpm install`, { timeout: 120000 });
      await this.log('依赖安装完成');
      return true;
    } catch (error) {
      await this.log(`依赖安装失败: ${error.message}`, 'error');
      throw error;
    }
  }

  async checkEnvironment() {
    await this.log('Step 5: 检查环境是否就绪');
    
    try {
      // 检查是否可以启动hexo server
      const pnpmHome = '/root/.local/share/pnpm';
      process.env.PNPM_HOME = pnpmHome;
      process.env.PATH = `${pnpmHome}:${process.env.PATH}`;
      
      // 简单检查hexo命令是否可用
      await execAsync(`cd ${this.projectPath} && hexo version`, { timeout: 10000 });
      await this.log('Hexo环境就绪');
      return true;
    } catch (error) {
      await this.log(`环境检查失败: ${error.message}`, 'error');
      throw error;
    }
  }

  async readReferenceStructure() {
    await this.log('Step 6: 读取参考文章结构');
    
    try {
      const referencePath = path.join(this.projectPath, CONFIG.referenceArticle);
      const content = await fs.readFile(referencePath, 'utf-8');
      
      // 解析Front Matter
      const frontMatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
      if (frontMatterMatch) {
        const frontMatter = frontMatterMatch[1];
        await this.log('成功读取参考文章结构');
        return { frontMatter, fullContent: content };
      } else {
        throw new Error('无法解析参考文章结构');
      }
    } catch (error) {
      await this.log(`读取参考文章失败: ${error.message}`, 'error');
      throw error;
    }
  }

  async createArticle(title, content, metadata = {}) {
    await this.log('Step 7: 创建文章');
    
    try {
      // 读取参考结构
      const reference = await this.readReferenceStructure();
      
      // 生成文件名
      const date = new Date();
      const dateStr = date.toISOString().split('T')[0];
      const abbrlink = metadata.abbrlink || title.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
      const filename = `${abbrlink}.md`;
      
      // 构建Front Matter
      const frontMatter = `---
title: ${title}
toc: true
abbrlink: ${abbrlink}
date: ${dateStr} 00:00:00
updated: ${dateStr} ${date.toTimeString().split(' ')[0]}
author: ${metadata.author || 'OpenClaw Team'}
tags:
${metadata.tags ? metadata.tags.map(tag => `  - ${tag}`).join('\n') : '  - Wiki'}
categories:
${metadata.categories ? metadata.categories.map(cat => `  - ${cat}`).join('\n') : '  - 技术架构'}
---

${content}`;
      
      // 写入文件
      const targetPath = path.join(this.projectPath, CONFIG.targetDir, filename);
      await fs.writeFile(targetPath, frontMatter, 'utf-8');
      
      await this.log(`文章已创建: ${targetPath}`);
      return targetPath;
    } catch (error) {
      await this.log(`创建文章失败: ${error.message}`, 'error');
      throw error;
    }
  }

  async clean() {
    await this.log('Step 8: Hexo清理');
    
    try {
      const pnpmHome = '/root/.local/share/pnpm';
      process.env.PNPM_HOME = pnpmHome;
      process.env.PATH = `${pnpmHome}:${process.env.PATH}`;
      
      const { stdout, stderr } = await execAsync(`cd ${this.projectPath} && hexo clean`, { timeout: 60000 });
      await this.log('Hexo清理完成');
      if (stdout) await this.log(stdout);
      if (stderr) await this.log(stderr, 'warn');
      return true;
    } catch (error) {
      await this.log(`Hexo清理失败: ${error.message}`, 'error');
      // 清理失败不阻断流程，继续执行
      return true;
    }
  }

  async generate() {
    await this.log('Step 9: Hexo生成');
    
    try {
      const pnpmHome = '/root/.local/share/pnpm';
      process.env.PNPM_HOME = pnpmHome;
      process.env.PATH = `${pnpmHome}:${process.env.PATH}`;
      
      const { stdout, stderr } = await execAsync(`cd ${this.projectPath} && hexo g`, { timeout: 120000 });
      
      // 分析输出
      const warnings = stderr.match(/WARN.*/g) || [];
      const errors = stderr.match(/ERROR.*/g) || [];
      
      await this.log(`Hexo生成完成`);
      await this.log(`生成文件数: ${(stdout.match(/INFO  Generated:/g) || []).length}`);
      await this.log(`警告数: ${warnings.length}`);
      await this.log(`错误数: ${errors.length}`);
      
      if (warnings.length > 0) {
        await this.log('警告详情:', 'warn');
        for (const warn of warnings.slice(0, 5)) {
          await this.log(`  ${warn}`, 'warn');
        }
        if (warnings.length > 5) {
          await this.log(`  ... 还有 ${warnings.length - 5} 个警告`, 'warn');
        }
      }
      
      if (errors.length > 0) {
        await this.log('错误详情:', 'error');
        for (const err of errors) {
          await this.log(`  ${err}`, 'error');
        }
        throw new Error(`Hexo生成失败，发现 ${errors.length} 个错误`);
      }
      
      // 检查关键文件是否生成
      const requiredFiles = ['index.html', 'atom.xml'];
      for (const file of requiredFiles) {
        try {
          await fs.access(path.join(this.projectPath, 'public', file));
          await this.log(`✓ 关键文件已生成: ${file}`);
        } catch {
          await this.log(`✗ 关键文件缺失: ${file}`, 'error');
        }
      }
      
      return true;
    } catch (error) {
      await this.log(`Hexo生成失败: ${error.message}`, 'error');
      throw error;
    }
  }

  async deploy() {
    await this.log('Step 10: Hexo部署');

    try {
      const pnpmHome = '/root/.local/share/pnpm';
      process.env.PNPM_HOME = pnpmHome;
      process.env.PATH = `${pnpmHome}:${process.env.PATH}`;

      // 使用项目目录下的 SSH 密钥配置
      const sshConfigPath = path.join(this.projectPath, 'ssh_config');

      // 检查 ssh_config 是否存在
      try {
        await fs.access(sshConfigPath);
        await this.log(`使用项目 SSH 配置: ${sshConfigPath}`);
      } catch {
        await this.log('警告: 未找到项目 ssh_config，将使用默认 SSH 配置', 'warn');
      }

      // 通过 GIT_SSH_COMMAND 指定 SSH 配置
      const env = {
        ...process.env,
        GIT_SSH_COMMAND: `ssh -F ${sshConfigPath} -o StrictHostKeyChecking=no`
      };

      const { stdout, stderr } = await execAsync(`cd ${this.projectPath} && hexo d`, {
        timeout: 120000,
        env
      });

      await this.log('Hexo部署完成');
      if (stdout) await this.log(stdout);
      if (stderr) await this.log(stderr, 'warn');
      return true;
    } catch (error) {
      await this.log(`Hexo部署失败: ${error.message}`, 'error');
      throw error;
    }
  }

  async run(options = {}) {
    await this.log('=== Wiki发布流程开始 ===');
    
    try {
      // 环境准备
      await this.checkAndCloneRepo();
      await this.switchBranch();
      await this.checkAndInstallTools();
      await this.installDependencies();
      await this.checkEnvironment();
      
      // 如果提供了文章内容，创建文章
      if (options.title && options.content) {
        await this.createArticle(options.title, options.content, options.metadata);
      }
      
      // 生成和部署
      await this.clean();
      await this.generate();
      await this.deploy();
      
      await this.log('=== Wiki发布流程完成 ===');
      return { success: true, logs: this.logs };
    } catch (error) {
      await this.log(`流程失败: ${error.message}`, 'error');
      return { success: false, logs: this.logs, error: error.message };
    }
  }
}

// 命令行接口
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  const publisher = new WikiPublisher();
  
  switch (command) {
    case 'setup':
      // 仅环境准备
      await publisher.checkAndCloneRepo();
      await publisher.switchBranch();
      await publisher.checkAndInstallTools();
      await publisher.installDependencies();
      await publisher.checkEnvironment();
      console.log('\n✅ 环境准备完成');
      break;
      
    case 'clean':
      // 仅清理
      await publisher.clean();
      console.log('\n✅ 清理完成');
      break;
      
    case 'create':
      // 创建文章
      const title = args[1] || '新文章';
      const contentFile = args[2];
      let content = '';
      
      if (contentFile) {
        content = await fs.readFile(contentFile, 'utf-8');
      } else {
        content = args.slice(2).join(' ') || '文章内容';
      }
      
      await publisher.createArticle(title, content);
      console.log('\n✅ 文章创建完成');
      break;
      
    case 'generate':
      // 仅生成
      await publisher.generate();
      console.log('\n✅ 生成完成');
      break;
      
    case 'deploy':
      // 仅部署
      await publisher.deploy();
      console.log('\n✅ 部署完成');
      break;
      
    case 'full':
      // 完整流程
      const articleTitle = args[1];
      const articleContentFile = args[2];
      let articleContent = '';
      
      if (articleContentFile) {
        articleContent = await fs.readFile(articleContentFile, 'utf-8');
      }
      
      const result = await publisher.run({
        title: articleTitle,
        content: articleContent
      });
      
      if (result.success) {
        console.log('\n✅ 发布成功');
      } else {
        console.log('\n❌ 发布失败');
        process.exit(1);
      }
      break;
      
    default:
      console.log('用法:');
      console.log('  node wiki-publisher.js setup                    - 环境准备');
      console.log('  node wiki-publisher.js clean                    - Hexo清理');
      console.log('  node wiki-publisher.js create "标题" "内容"      - 创建文章');
      console.log('  node wiki-publisher.js generate                 - Hexo生成');
      console.log('  node wiki-publisher.js deploy                   - Hexo部署');
      console.log('  node wiki-publisher.js full "标题" [内容文件]    - 完整发布流程');
      console.log('');
      console.log('示例:');
      console.log('  node wiki-publisher.js setup');
      console.log('  node wiki-publisher.js full "MLOps自动化" ./content.md');
  }
}

// 导出模块
module.exports = WikiPublisher;

// 如果直接运行
if (require.main === module) {
  main().catch(console.error);
}