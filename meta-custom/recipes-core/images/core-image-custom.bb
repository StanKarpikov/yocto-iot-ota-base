require recipes-core/images/core-image-minimal.bb

SUMMARY = "Minimal image with BusyBox"
LICENSE = "MIT"

# IMAGE_FEATURES = "read-only-rootfs"

IMAGE_INSTALL += " shadow-base mender-server-certificate"

IMAGE_FSTYPES = "ext4"

INIT_MANAGER = "systemd"
VIRTUAL-RUNTIME_init_manager = "systemd"
VIRTUAL-RUNTIME_initscripts = ""

BAD_RECOMMENDATIONS += "udev-hwdb"

inherit extrausers
EXTRA_USERS_PARAMS = "usermod -p '$(openssl passwd -6 root)' root;"
