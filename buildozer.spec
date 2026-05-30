[app]
title = 发饰店积分系统
package.name = shop_points
package.domain = org.shop.points
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0
requirements = python3,kivy==2.2.0
orientation = portrait
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET
android.api = 33
android.minapi = 21
# 不在这里指定 NDK 版本，通过环境变量 ANDROIDNDK 传递
android.sdk_version = 33
android.accept_sdk_license = True
android.archs = arm64-v8a
android.enable_androidx = True
log_level = 2
warn_on_root = 1
