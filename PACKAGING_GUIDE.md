# 发饰店积分系统 - APK 打包指南

## 📋 一、环境准备

### 系统需求
- **操作系统**：Windows、Mac 或 Linux
- **Python**：3.7 以上版本
- **内存**：至少 4GB RAM
- **磁盘**：至少 10GB 空闲空间

### 1.1 安装必要工具

#### Windows 用户：
```bash
# 1. 安装 Python 依赖
pip install buildozer cython

# 2. 安装 Java Development Kit (JDK)
# 下载 JDK 11 或更新版本
# https://www.oracle.com/java/technologies/downloads/

# 3. 设置环境变量
# 在系统环境变量中添加 JAVA_HOME
# 示例：C:\Program Files\Java\jdk-11.0.0
```

#### Mac 用户：
```bash
# 1. 安装 Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 安装依赖
brew install python3 openjdk
pip3 install buildozer cython

# 3. 设置 Java 环境
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
```

#### Linux 用户 (Ubuntu/Debian)：
```bash
# 1. 安装依赖包
sudo apt-get update
sudo apt-get install -y build-essential git python3-dev python3-pip openjdk-11-jdk

# 2. 安装 Python 工具
pip3 install buildozer cython

# 3. 设置 Java 环境
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

---

## 🔧 二、项目配置

### 2.1 项目结构

确保你的项目目录如下：
```
wry/
├── buildozer.spec          # 构建配置文件
├── main.py                 # 主应用程序
└── points_system.db        # 数据库文件（可选，运行时生成）
```

### 2.2 验证配置

检查 `buildozer.spec` 中的关键配置：

```ini
# 应用信息
title = 发饰店积分系统
package.name = shop_points
package.domain = org.shop.points
version = 1.0

# 依赖
requirements = python3,kivy==2.2.0,pyjnius

# Android 配置
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk_version = 33
android.archs = arm64-v8a
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET
```

---

## 🚀 三、打包步骤

### 3.1 初始化构建

在项目目录中打开终端，运行：

```bash
# 第一次运行会自动下载 Android SDK、NDK 等（需要较长时间）
buildozer android debug
```

**首次构建预计耗时：30-60 分钟**（取决于网络速度）

### 3.2 监听构建过程

构建过程会在终端输出日志，监听以下关键信息：

```
# 正常进度指示
# - "Downloading Android NDK..."
# - "Building Python for android..."
# - "Building APK..."
# - "[100%] ... creating the APK"

# 完成标志
# "APK created successfully at: bin/shop_points-1.0-debug.apk"
```

### 3.3 常见构建问题

| 错误信息 | 解决方案 |
|---------|--------|
| `Java not found` | 检查 JAVA_HOME 环境变量 |
| `SDK license not accepted` | 在 buildozer.spec 中设置 `android.accept_sdk_license = True` |
| `Out of memory` | 增加 JVM 内存：`export GRADLE_OPTS="-Xmx4096m"` |
| `Network timeout` | 检查网络连接，重新运行构建命令 |
| `Permission denied` | 确保项目文件夹有读写权限 |

---

## 📱 四、生成的 APK 文件

构建成功后，APK 文件位置：

```
bin/shop_points-1.0-debug.apk   # Debug 版本（用于测试）
```

### 4.1 安装 APK 到手机

#### 方式一：通过 USB 连接（推荐）
```bash
# 1. 连接 Android 手机并启用 USB 调试
# 2. 运行以下命令
adb install bin/shop_points-1.0-debug.apk

# 3. 等待安装完成
# "Success" 表示安装成功
```

#### 方式二：直接复制到手机
1. 将 APK 文件传输到手机
2. 使用文件管理器打开 APK
3. 点击"安装"

---

## 🔐 五、Release 版本构建

用于正式发布到应用商店：

### 5.1 生成密钥库

```bash
# 首次生成（只需一次）
keytool -genkey -v -keystore shop_points.keystore -keyalg RSA -keysize 2048 -validity 10000

# 按提示输入密码和应用信息
```

### 5.2 配置 buildozer.spec

```ini
# 添加以下配置
android.release_artifact = aab
android.keystore = 1
android.keystore_path = /path/to/shop_points.keystore
android.keystore_alias = shop_points
```

### 5.3 构建 Release 版本

```bash
buildozer android release
```

生成文件：
```
bin/shop_points-1.0-release-unsigned.apk
```

---

## 🧹 六、清理与维护

### 清理构建文件

```bash
# 清理所有构建文件（重新构建时使用）
buildozer android clean

# 清理构建缓存
rm -rf .buildozer
```

### 更新依赖

如需升级 Kivy 版本：
```bash
# 在 buildozer.spec 中修改
requirements = python3,kivy==2.3.0,pyjnius

# 然后重新构建
buildozer android clean
buildozer android debug
```

---

## 📊 七、性能优化建议

### 7.1 APK 大小优化

当前 APK 大小约：**50-80 MB**

```ini
# buildozer.spec 中的优化配置
android.logcat_filters = *:S python:D
p4a.strip_libraries = 1
```

### 7.2 运行时优化

编辑 `buildozer.spec`：
```ini
# 禁用不需要的功能
android.features = android.hardware.touchscreen
```

---

## 🐛 八、调试与日志

### 实时查看日志

```bash
# 连接手机后查看 logcat
adb logcat | grep python

# 保存日志到文件
adb logcat > app_log.txt
```

### 常见运行时错误

| 错误 | 原因 | 解决方案 |
|------|------|--------|
| 应用崩溃 | 缺少权限 | 检查 `android.permissions` 配置 |
| 数据库错误 | 路径问题 | 使用 `context.getFilesDir()` |
| 界面显示异常 | 屏幕适配 | 调整 Kivy 的 `Window.size` |

---

## 📞 九、常见问题 FAQ

### Q: 首次构建需要多长时间？
**A:** 首次构建会下载 SDK/NDK，通常需要 30-60 分钟。后续构建只需 5-10 分钟。

### Q: 可以在 Python 3.11 上构建吗？
**A:** 建议使用 Python 3.8-3.10。3.11+ 的支持还在完善中。

### Q: 如何修改应用图标？
**A:** 在 buildozer.spec 中添加：
```ini
android.icon = %(source_dir)s/data/icon.png
```

### Q: 支持实时更新吗？
**A:** 建议通过应用市场更新。如需热更新，需集成第三方框架。

### Q: 数据库文件会丢失吗？
**A:** SQLite 数据库存储在应用私有目录，卸载应用时会丢失。建议定期导出备份。

---

## ✅ 十、上线检查清单

发布前请确认：

- [ ] 应用在多部测试手机上运行正常
- [ ] 所有功能已测试
- [ ] 没有明显的崩溃或错误
- [ ] 隐私政策已准备
- [ ] 版本号已更新
- [ ] 应用图标已准备

---

## 📞 支持与反馈

如遇到问题，请参考：
- [Buildozer 官方文档](https://buildozer.readthedocs.io/)
- [Kivy 官方文档](https://kivy.org/doc/stable/)
- [Python for Android](https://python-for-android.readthedocs.io/)

---

**打包成功！祝你的应用运营顺利！🎉**
