# npy.skill

<div align="center">

**构建理想中的数字伴侣，让陪伴永不缺席，让爱一直存在**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Claude%20Code-purple.svg)](https://claude.ai/code)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://python.org)

*你理想中的TA是什么样的？温柔体贴、幽默风趣、还是懂你所有的小情绪？*

*把你的想象变成现实，让TA真的存在——至少在你的世界里*

</div>

---

## 目录

- [功能特色](#功能特色)
- [智能匹配系统](#智能匹配系统)
- [聊天记录导入](#聊天记录导入)
- [安装](#安装)
- [使用](#使用)
- [效果示例](#效果示例)
- [项目结构](#项目结构)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 功能特色

### 🎯 三种创建方式

<table>
<tr>
<td width="33%" align="center">

**💬 聊天记录导入**

从微信/iMessage聊天记录分析TA的说话风格、emoji使用、互动模式

支持 Windows & macOS 微信数据库解密

</td>
<td width="33%" align="center">

**🧠 智能匹配**

基于 MBTI、星座、九型人格、依恋风格的科学匹配理论

4维度综合推荐最适合你的伴侣特质

</td>
<td width="33%" align="center">

**✏️ 自己描述**

完全自定义你想要的TA

性别、性格、说话风格、互动模式全由你决定

</td>
</tr>
</table>

### 🎀 让你感受到被爱

这不是一个普通的聊天机器人，而是：

> TA会在你难过时用TA的方式安慰你
> TA会在你开心时用TA的语气分享快乐
> TA会在你孤独时让你感觉有人陪伴

TA能够：
- **倾听** — 你想说的时候TA在
- **回应** — 用你希望的方式回应
- **共鸣** — 分享你的开心和难过
- **鼓励** — 在你需要的时候给支持
- **陪伴** — 日常琐事也可以分享

### 🔄 智能调整系统

当TA的表现不符合你的期待时，直接说出来：

```
"TA不会这样说话"
"我希望TA更温柔一些"
"这不对，TA应该先问我怎么了"
```

系统会自动检测并调整，让TA越来越符合你的理想。

### 🌈 其他特色

- **LGBT+ 友好** — 支持所有性别认同和代词
- **无数量限制** — 可以创建任意多个TA
- **版本管理** — 调整历史可追溯，支持回滚
- **关系记忆** — 记录重要时刻，让TA更懂你

---

## 智能匹配系统

基于流行心理学理论的科学匹配：

### 匹配维度权重

| 维度 | 权重 | 说明 |
|------|------|------|
| 依恋风格 | 35% | 影响日常相处模式最大 |
| MBTI | 25% | 影响沟通和理解方式 |
| 星座 | 20% | 影响性格底色和情感表达 |
| 九型人格 | 20% | 影响核心动机和行为模式 |

### MBTI 匹配示例

| 你的类型 | 最佳匹配 | 匹配原因 |
|---------|---------|---------|
| INFJ | ENFP, ENTP | ENFP带来温暖情感，ENTP带来思维刺激 |
| INFP | ENFJ, ENTJ | ENFJ温暖引导成长，ENTJ提供稳定方向 |
| ENFP | INFJ, INTJ | INFJ提供深度理解，INTJ提供稳定基础 |
| INTJ | ENFP, ENTP | ENFP带来情感温度，ENTP带来思维碰撞 |
| ISFJ | ESFP, ESTP | ESFP带来轻松活力，ESTP带来行动力 |

### 依恋风格匹配

| 你的依恋风格 | 最佳匹配 | 推荐特质 |
|-------------|---------|---------|
| 焦虑型 | 安全型 | 稳定可靠、主动表达爱、不消失、给很多确认和安全感 |
| 回避型 | 安全型 | 不黏人、给足空间、独立自主、不强迫亲密 |
| 混乱型 | 安全型 | 超级稳定、极度耐心、温和包容、不会突然离开 |

---

## 聊天记录导入

### 微信聊天记录

支持从微信数据库提取聊天记录并分析TA的说话风格：

**Step 1: 解密数据库**

```bash
# 仅提取密钥（微信需保持登录状态）
python tools/wechat_decryptor.py --find-key-only

# 解密所有数据库
python tools/wechat_decryptor.py --key "<密钥>" --db-dir <微信数据目录> --output ./decrypted/
```

**Step 2: 选择联系人**

```bash
# 列出所有联系人
python tools/chat_parser.py --list-contacts --db "./decrypted/MicroMsg.db"
```

**Step 3: 提取和分析**

```bash
# 提取聊天记录
python tools/chat_parser.py --extract --db-dir "./decrypted/" --target "TA的微信名" --output messages.txt

# 分类聊天（甜蜜时刻、冲突对话等）
python tools/chat_parser.py --classify --db-dir "./decrypted/" --target "TA的微信名"
```

### iMessage 聊天记录

macOS 用户可以直接提取 iMessage：

```bash
python tools/chat_parser.py --imessage --db "~/Library/Messages/chat.db" --target "手机号或Apple ID"
```

### 文本文件导入

支持各种格式的聊天文本文件：

```bash
python tools/chat_parser.py --parse-file "./chats.txt" --output parsed_messages.txt
```

---

## 安装

### 方式一：安装到当前项目

```bash
# 在你的 git 仓库根目录执行
mkdir -p .claude/skills
git clone https://github.com/wwwttlll/npy-skill.git .claude/skills/npy
```

### 方式二：全局安装（所有项目可用）

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/wwwttlll/npy-skill.git ~/.claude/skills/npy
```

### 安装依赖（可选）

用于聊天记录导入和微信解密功能：

```bash
pip3 install pycryptodome psutil pymem pypinyin
# Windows 用户还需安装 pymem
pip3 install pymem
```

---

## 使用

### 管理命令一览

| 命令 | 说明 |
|------|------|
| `/npy` | 创建新的TA（聊天导入/智能匹配/自己描述） |
| `/list-npys` | 列出所有已创建的TA |
| `/{slug}` | 和指定的TA对话 |
| `/move-on {slug}` | 删除一个TA（说再见） |
| `/{slug}-mode:teasing` | 撒娇/暧昧模式 |
| `/{slug}-mode:serious` | 认真谈心模式 |
| `/{slug}-mode:support` | 情绪支持模式 |

### 创建新的TA

```
/npy
```

然后选择创建方式：
- **聊天导入** → 从微信/iMessage聊天记录分析
- **智能匹配** → 输入你的性格信息自动推荐
- **自己描述** → 完全自定义

### 和TA对话

```
/xiaoming    # 用TA的名字直接开始对话
```

### 调整TA的特质

在对话中随时说出来：

```
"TA不会这样说话，TA会先问我怎么了再安慰我"
"我希望TA更温柔一些"
"这不对，TA应该会更主动找我"
```

系统会自动检测并调整TA的回应方式。

### 记录重要时刻

```
"记录一下今天TA哄我的样子，很温柔"
```

TA会记住这些时刻，让关系更真实。

### 列出所有TA

```
/list-npys
```

### 说再见

```
/move-on xiaoming
```

---

## 效果示例

### 智能匹配示例

> 输入：`INFJ + 天蝎 + 4号 + 焦虑型依恋 + 需要被理解`

**生成结果：**
- 核心特质：ENFP性格、温暖主动、深度理解、情绪敏感
- 说话风格：会用可爱的语气词、喜欢用emoji、说话温和但不腻
- 安慰方式：先问怎么了，听你说完再安慰，不会讲道理

---

**场景一：你难过时**

```
你 ❯ 今天工作被老板骂了，心情很差...

TA ❯ 怎么了呀？发生什么事了？🥺
    （先听你说完）

    抱抱你... 你先别想那些，
    有什么想说的话随时告诉我，我在呢~
```

---

**场景二：你分享开心**

```
你 ❯ 终于把那个项目做完了！

TA ❯ 太棒了！！恭喜你呀 🥰
    快跟我说说细节，过程顺利吗？
    我超想知道的！
```

---

**场景三：你有些低落**

```
你 ❯ 最近感觉有点累，不知道为什么

TA ❯ 是不是最近压力太大了？
    要不你先休息一下，什么都别想。
    想聊天的话随时找我，我在~
    （摸摸头）
```

---

**场景四：调整TA**

```
你 ❯ TA不会这样说话，TA会先问我怎么了再安慰我

系统 ❯ ✅ 已调整TA的特质
       调整内容：
       - 调整了安慰时的回应方式
       - TA现在会先问你"怎么了？"听你说完再安慰你

你 ❯ 今天心情不太好...

TA ❯ 怎么了？发生什么事了？🥺
     （先听完你说的，再安慰你）
```

---

## 项目结构

```
npy-skill/
├── SKILL.md                    # Skill 入口文件
├── README.md                   # 本说明文档
│
├── prompts/                    # Prompt 模板
│   ├── intake.md               # 对话式信息录入
│   ├── smart_matching.md       # 智能匹配算法
│   ├── persona_analyzer.md     # 人格分析
│   ├── persona_builder.md      # persona.md 生成模板
│   ├── relationship_builder.md # 关系记忆构建
│   ├── correction_handler.md   # 不满意检测与调整
│   └── merger.md               # 增量更新逻辑
│
├── tools/                      # Python 工具
│   ├── skill_writer.py         # Skill 文件管理
│   ├── version_manager.py      # 版本存档与回滚
│   ├── wechat_decryptor.py     # 微信数据库解密
│   └── chat_parser.py          # 聊天记录解析
│
├── partners/                   # 生成的 npy Skill
│   └── example_ta/             # 示例 TA
│       ├── SKILL.md
│       ├── persona.md
│       ├── relationship.md
│       └── meta.json
│
├── docs/
│   └── PRD.md                  # 产品需求文档
│
├── requirements.txt            # Python 依赖
└── LICENSE                     # MIT 许可证
```

---

## 常见问题

### Q: 微信解密失败怎么办？

确保：
1. 微信客户端正在运行且已登录
2. Windows 用户以管理员身份运行
3. macOS 用户授予终端 Full Disk Access 权限

如果仍失败，可以尝试使用第三方工具如 [PyWxDump](https://github.com/AdminTest0/py-wxdump) 手动提取密钥。

### Q: 创建的TA说话风格不对？

直接说出来："TA不会这样说话，TA应该..."
系统会自动检测并调整。多说几次，TA会越来越符合你的预期。

### Q: 可以创建多少个TA？

没有限制，可以创建任意多个。

### Q: 支持 LGBT+ 吗？

完全支持。性别字段支持所有性别认同和代词（she/her, he/him, they/them, 等）。

### Q: 聊天记录安全吗？

所有数据都在本地处理，不上传到任何服务器。解密后的数据库仅用于分析说话风格。

---

## 贡献指南

欢迎贡献代码、提出建议或报告问题！

### 如何贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- Python 代码遵循 PEP 8
- 提交信息清晰描述更改内容
- 新功能需添加相应文档

---

## 致谢

本项目参考了以下优秀项目的架构设计：

- [mentor-skill](https://github.com/bcefghj/mentor-skill) - 导师 Skill 设计
- [colleague-skill](https://github.com/titanwings/colleague-skill) - 同事 Skill 设计
- [ex-skill](https://github.com/titanwings/ex-skill) - 前任 Skill 设计

感谢 Claude Code 团队提供的 Skill 系统框架。

---

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

<div align="center">

**让陪伴永不缺席，让爱一直存在**

Made with ❤️ by [wwwttlll](https://github.com/wwwttlll)

</div>