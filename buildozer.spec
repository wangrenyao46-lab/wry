[app]

# (str) Title of your application
title = 发饰店积分系统

# (str) Package name
package.name = shop_points

# (str) Package domain (needed for android/ios packaging)
package.domain = org.shop.points

# (source.dir) Source code directory.
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,db

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy==2.2.0

# (str) Supported orientation
orientation = portrait

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (str) Android NDK version (comment out because we set path below)
# android.ndk = 23b

# (str) Android NDK directory (use the manually downloaded one)
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r23b

# (int) Android SDK version
android.sdk_version = 33

# (bool) Accept Android SDK license agreements
android.accept_sdk_license = True

# (str) Android arch to build for
android.archs = arm64-v8a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warnings
warn_on_root = 1

# (str) Path to build artifact storage
# build_dir = ./.buildozer

# (str) Path to build output
# bin_dir = ./bin
