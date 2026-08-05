# 🖼️ Bing 每日壁纸自动下载

> 基于 GitHub Actions，每天自动抓取 Bing 中国版每日壁纸（UHD 超高清版本），并提交到本仓库归档保存。

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-2088FF?logo=github-actions&logoColor=white)](https://github.com/jccm66/bing-pic/actions)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Update](https://img.shields.io/badge/Update-Daily-FF6B6B?logo=bing&logoColor=white)](#)

---

## ✨ 功能特性

- 🔄 **全自动运行**：每天北京时间凌晨 2 点自动下载当日 Bing 壁纸，无需人工干预
- 🖼️ **超高清下载**：自动获取 UHD（3840×2160）版本，而非默认的 1080P 版本
- 📦 **自动归档**：下载的图片自动提交到仓库 `Bing_Picture/` 目录，按日期+标题命名，方便历史检索
- 🆓 **零成本部署**：完全基于 GitHub Actions 免费额度，无需服务器
- 🌐 **中国版 Bing**：抓取 `cn.bing.com` 的每日图片，符合国内用户审美
- 📋 **元数据保留**：文件名包含日期和标题，便于检索和管理

---

## 🔧 工作原理

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  GitHub Actions │ ──▶ │   main.py 运行    │ ──▶ │  下载 UHD 壁纸   │
│  定时触发(UTC)   │     │  在 Ubuntu runner │     │  并 commit 到仓库 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                                                  │
        │                                                  ▼
        │           ┌──────────────────────────────────────┐
        └─────────▶ │  Bing_Picture/YYYYMMDD_标题.jpg       │
                    │  （永久保存在 GitHub 仓库中）           │
                    └──────────────────────────────────────┘
```

1. **定时触发**：GitHub Actions 在 UTC 18:00（即北京时间次日 02:00）触发 workflow
2. **环境准备**：自动检出仓库代码，并配置 Python 3.11 运行环境
3. **下载壁纸**：`main.py` 调用 Bing 官方 API，获取当日壁纸信息，并将链接转换为 UHD 版本下载
4. **自动提交**：workflow 自动将新下载的图片 `git commit` 并 `git push` 到仓库

---

## 📁 项目结构

```
bing-pic/
├── .github/
│   └── workflows/
│       └── bing-daily.yml     # GitHub Actions 自动化配置文件
├── Bing_Picture/              # 下载的壁纸自动保存目录（运行后自动生成）
│   └── YYYYMMDD_标题.jpg
├── main.py                    # 主程序：下载 Bing 每日壁纸
└── README.md                  # 项目说明文档
```

---

## 🚀 快速开始

本项目无需本地环境，Fork 后即可使用。

### 方式一：直接使用本仓库

如果你已经 clone / 拥有本仓库，无需任何额外操作，每天凌晨 2 点会自动运行。

### 方式二：Fork 到自己的账号

1. 点击本仓库右上角的 **Fork** 按钮，将仓库复制到你的 GitHub 账号下
2. 进入你 Fork 后的仓库，点击 **Actions** 标签页
3. 如果出现提示，点击 **"I understand my workflows, go ahead and enable them"** 启用 workflow
4. 完成！每天北京时间凌晨 2 点会自动下载壁纸到你的仓库

### 手动触发一次（用于测试）

1. 进入仓库的 **Actions** 标签页
2. 在左侧选择 **Bing Daily Picture** workflow
3. 点击右侧的 **Run workflow** 按钮 → 再次点击绿色的 **Run workflow**
4. 等待约 30 秒，任务完成后即可在 `Bing_Picture/` 目录看到当日壁纸

---

## ⏰ 自动化运行说明

自动化配置文件位于 [.github/workflows/bing-daily.yml](.github/workflows/bing-daily.yml)。

| 项目             | 值                          |
| ---------------- | --------------------------- |
| 触发方式         | `schedule` + `workflow_dispatch` |
| 运行时间（cron） | `0 18 * * *`（UTC 18:00）   |
| 对应北京时间     | 次日 02:00                  |
| 运行环境         | `ubuntu-latest`             |
| Python 版本      | 3.11                        |
| 所需权限         | `contents: write`（用于自动提交） |

> ⚠️ **关于运行时间**：GitHub Actions 的 `schedule` 触发不保证精准准时，在高负载时段可能会有几分钟到十几分钟的延迟，但每天都会执行一次。

---

## 🛠️ 自定义配置

### 修改下载图片数量

编辑 [main.py](main.py) 第 6 行的 API URL，将 `n=1` 改为你想要的天数（最多 8 天）：

```python
# 下载最近 3 天的壁纸
API_URL = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=3"
```

### 修改运行时间

编辑 [.github/workflows/bing-daily.yml](.github/workflows/bing-daily.yml) 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 18 * * *'   # UTC 18:00 = 北京时间 02:00
```

常见时区换算（北京时间 = UTC + 8）：

| 北京时间 | UTC 时间    | cron 表达式       |
| -------- | ----------- | ----------------- |
| 00:00    | 16:00（前） | `0 16 * * *`      |
| 02:00    | 18:00（前） | `0 18 * * *`      |
| 06:00    | 22:00（前） | `0 22 * * *`      |
| 08:00    | 00:00       | `0 0 * * *`       |
| 12:00    | 04:00       | `0 4 * * *`       |

### 使用国际版 Bing

将 [main.py](main.py) 中的 `cn.bing.com` 替换为 `www.bing.com` 即可获取国际版壁纸。

---

## ❓ 常见问题

<details>
<summary><b>壁纸文件名出现乱码怎么办？</b></summary>

GitHub Actions 的 Ubuntu runner 默认使用 UTF-8 编码，通常不会出现乱码。如果文件名包含特殊字符，`main.py` 会自动过滤仅保留字母、数字、空格、连字符和下划线。
</details>

<details>
<summary><b>为什么有时候定时任务没有运行？</b></summary>

GitHub 对 60 天内无活动的仓库会自动暂停定时 workflow。只需在仓库中做任意一次提交（例如修改 README），或手动触发一次 workflow 即可重新激活。
</details>

<details>
<summary><b>仓库图片太多会有问题吗？</b></summary>

GitHub 建议单仓库容量控制在 1GB 以内。每张 UHD 壁纸约 1-3MB，一年约 365-1000 张，约 0.5-3GB。建议每年清理一次旧壁纸，或只保留精选壁纸。如需长期大量存储，建议改用对象存储（如七牛云、阿里云 OSS）。
</details>

<details>
<summary><b>下载的图片分辨率是多少？</b></summary>

`main.py` 会自动将默认的 1920×1080 链接替换为 UHD 版本（通常为 3840×2160），适合作为 4K 显示器壁纸使用。
</details>

---

## 📝 技术细节

- **语言**：Python 3（仅使用标准库，无第三方依赖）
- **API**：Bing 官方 `HPImageArchive.aspx` 接口
- **网络请求**：`urllib.request`（自带 User-Agent 模拟，避免被识别为爬虫）
- **文件命名**：`{startdate}_{title}.jpg`，自动过滤非法字符
- **CI/CD**：GitHub Actions（cron 定时 + workflow_dispatch 手动触发）

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议，可自由使用、修改和分发。

> ⚠️ **注意**：Bing 每日壁纸的版权归 Microsoft 及图片原作者所有，本项目仅用于个人学习和技术研究，请勿用于商业用途。

---

## 🙏 致谢

- [Microsoft Bing](https://cn.bing.com/) - 提供每日精美壁纸
- [GitHub Actions](https://github.com/features/actions) - 提供免费的 CI/CD 服务

---

<sub>📅 最后更新：2026-08-05</sub>
