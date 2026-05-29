[app]

title = Majestic EMS Tablet
package.name = majestictablet
package.domain = org.majesticrp

source.dir = .
source.include_exts = py,png,jpg,kv,json

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license = True

android.permissions = INTERNET

[buildozer]

log_level = 2
warn_on_root = 1
