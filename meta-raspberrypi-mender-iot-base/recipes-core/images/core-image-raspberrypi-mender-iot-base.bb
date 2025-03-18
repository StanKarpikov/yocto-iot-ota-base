require recipes-core/images/core-image-minimal.bb

SUMMARY = "Minimal image for Raspberry Pi with Mender"
LICENSE = "MIT"

INHERIT += "rpi-update-firmware"

IMAGE_FEATURES:append = " read-only-rootfs"

IMAGE_INSTALL:append = " shadow-base mender-server-certificate"
IMAGE_INSTALL:remove = "sysvinit busybox-sysvinit"

# IMAGE_FSTYPES:pn-${INITRAMFS_IMAGE} = "${INITRAMFS_FSTYPES}"
#  tar.bz2 cpio.gz
IMAGE_FSTYPES:append = " sdimg"

INIT_MANAGER = "systemd"
VIRTUAL-RUNTIME_init_manager = "systemd"

DISTRO_FEATURES:append = " systemd usrmerge"
DISTRO_FEATURES_BACKFILL_CONSIDERED:append = "sysvinit"
VIRTUAL-RUNTIME_initscripts = "systemd-compat-units"
VIRTUAL-RUNTIME_login_manager = "shadow-base"
VIRTUAL-RUNTIME_dev_manager = "systemd"
ROOT_HOME ?= "/root"

MACHINE_WITH_CUDA = "0"

# TODO: Improve password security
inherit extrausers
EXTRA_USERS_PARAMS = "usermod -p '$(openssl passwd -6 root)' root;"
