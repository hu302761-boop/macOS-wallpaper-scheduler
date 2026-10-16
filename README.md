# macOS Wallpaper Scheduler

一个本地运行的 macOS 壁纸调度器，根据工作日、法定节假日和时间段选择壁纸。

## 功能

- 工作日按时间段切换壁纸
- 周末和节假日使用独立规则
- 跨午夜时间段
- `--dry-run` 预览当前会选择的壁纸，不修改系统
- 使用 macOS `launchd` 每小时运行
- 所有规则保存在 JSON 配置中，不依赖网络服务

## 快速开始

```bash
cp config.example.json config.json
# 修改 config.json 中的图片路径、节假日和时间段
python3 wallpaper_scheduler.py --config config.json --dry-run
python3 wallpaper_scheduler.py --config config.json
```

配置中的星期使用 ISO 规则：`1` 表示周一，`7` 表示周日。时间段采用 `[start, end)`，例如 `19:00` 到 `10:00` 表示跨午夜时段。

## launchd

将 `com.hu.wallpaper-scheduler.plist.example` 复制到 `~/Library/LaunchAgents/`，把其中的项目路径替换为本机绝对路径，然后执行：

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.hu.wallpaper-scheduler.plist
```

定时脚本和图片不要放在 `Documents` 或桌面等受 macOS 隐私保护的目录中。建议使用 `~/Library/Application Support/WallpaperScheduler/`。

## 项目边界

这是基于原项目已确认需求重新实现的可公开版本。原项目的旧源码和图片不在当前电脑上，因此仓库不包含个人壁纸资产，也不宣称与旧文件逐字一致。
