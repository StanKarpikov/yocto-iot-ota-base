require recipes-core/images/core-image-minimal.bb

SUMMARY = "Minimal image with BusyBox"
LICENSE = "MIT"

IMAGE_FEATURES = ""

IMAGE_INSTALL += " shadow-base"

inherit extrausers
EXTRA_USERS_PARAMS = "usermod -p '$(openssl passwd -6 root)' root;"
