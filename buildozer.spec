[app]

# (str) Title of your application
title = 发饰店积分系统

# (str) Package name
package.name = shop_points

# (str) Package domain (needed for android/ios packaging)
package.domain = org.shop.points

# (source.dir) Source code directory. The left dot will be replaced
# with an appropriate path depending on the platform used, such as
# dist, build and bin, etc.
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,db

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.2.0,pyjnius

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android SDK version to use
android.sdk_version = 33

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
# android.ndk_path = /path/to/android-ndk

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
# android.sdk_path = /path/to/android-sdk

# (bool) Indicate if the intention is to build for a remote server
# android.skip_update = False

# (bool) Accept Android SDK license agreements
android.accept_sdk_license = True

# (str) Android NDK version to use
android.ndk_version = 25b

# (list) Pattern to whitelist for the whole project
#android.whitelist = lib-dynload/termios.so

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (bool) Indicate if the screen should stay on
# android.flags = fullscreen

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will be disabled
# android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
# android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file for custom backup agent declaration within the manifest
# android.backup_tokens = @xml/backup_tokens

# (str) XML file for client secrets (see the Google API documentation)
# android.secrets = @xml/client_secrets

# (bool) Copy library instead of making a libpymodules.so
# android.copy_libs = 1

# (int) overrides automatic versionCode generation in buildozer.spec
# android.version_code = 1

# (list) pattern matched against the current device abis to select build arch
# android.accept_abilist = armeabi-v7a, arm64-v8a

# (bool) Copy library instead of making a libpymodules.so
# android.copy_libs = 1

# (bool) Use the ANDROID_SDK_ROOT environment variable
# android.use_legacy_toolchain = False

# (bool) Enable AndroidX support
# android.enable_androidx = True

#
# Python for android (p4a) specific
#

# (str) python for android git repo URL
# p4a.url = https://github.com/kivy/python-for-android

# (str) python for android branch to use, defaults to master
# p4a.branch = develop

# (str) python for android git specific commit to use, defaults to HEAD, must be within --p4a.branch
# p4a.commit = HEAD

# (str) python for android directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) The bootstrap to use. Leave empty to let python-for-android choose.
# p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
# p4a.port = 5000


#
# iOS specific
#

# (bool) Whether or not to sign the code
# ios.sign = True

# (str) Path to the codesign key
# ios.codesign_identity = Apple Developer

# (str) Filename of .p12 key. Match ios.key_filename + .p12
# ios.p12_filename = ./ios/Certificate.p12

# (str) Filename of .mobileprovision file
# ios.provisioning_profile_filename = ./ios/BuildDistribution.mobileprovision

# (str) Path to directory to store the files
# ios.executables_dir = executables/

# Keystore
# [app:module_selection]
# android.accept_sdk_license = True


#
# [buildozer]
#

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warnings (0 = off, 1 = on (default))
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. where to put the built APK, IPA or so)
# bin_dir = ./bin

#
# List as sections
#

# You can define p4a.local_recipes to override them with completely custom
# versions of the recipes. p4a.local_recipes should point to a directory
# containing your recipes as subdirectories. Any recipe overrides here will
# override p4a's recipes for the given dependencies.

# p4a.local_recipes = ./recipes

# p4a.depends = sqlite3,pycrypto
# p4a.depends = sqlite3

#
# Android API level
#

# p4a.bootstrap = sdl

# Android logcat filtering
# android.logcat_filters = *:S python:D
