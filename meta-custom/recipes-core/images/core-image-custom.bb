require recipes-demo/images/demo-image-base.bb

SUMMARY = "Minimal image with BusyBox"
LICENSE = "MIT"

# TODO: Activate this in fstab
IMAGE_FEATURES += "read-only-rootfs"

IMAGE_INSTALL += " shadow-base mender-server-certificate"
IMAGE_INSTALL:remove = "sysvinit busybox-sysvinit"

# rpi-sdimg
# IMAGE_FSTYPES = "ext4 sdimg.gz tar.bz2 cpio.gz"
IMAGE_FSTYPES = "ext4 tar.bz2 cpio.gz"

# TODO: Remove systemd
INIT_MANAGER = "systemd"
VIRTUAL-RUNTIME_init_manager = "systemd"

DISTRO_FEATURES:append = " systemd usrmerge"
DISTRO_FEATURES_BACKFILL_CONSIDERED:append = "sysvinit"
VIRTUAL-RUNTIME_initscripts = "systemd-compat-units"
VIRTUAL-RUNTIME_login_manager = "shadow-base"
VIRTUAL-RUNTIME_dev_manager = "systemd"
# systemd hardcodes /root in its source codes, other values are not offically supported
ROOT_HOME ?= "/root"
# VIRTUAL-RUNTIME_init_manager = "busybox"
#VIRTUAL-RUNTIME_initscripts = "initscripts"
# VIRTUAL-RUNTIME_login_manager = "busybox"
# VIRTUAL-RUNTIME_initscripts = "systemd-compat-units"

# BAD_RECOMMENDATIONS += "udev-hwdb"

ARTIFACTIMG_FSTYPE = "ext4"

# Total storage size of the device
MENDER_STORAGE_TOTAL_SIZE_MB = "1024"

# Root filesystem size (active/passive partitions)
MENDER_ROOTFS_PART_A_SIZE_MB = "512"
MENDER_ROOTFS_PART_B_SIZE_MB = "512"

# Boot partition size
MENDER_BOOT_PART_SIZE_MB = "64"

# Data partition (remaining space)
MENDER_DATA_PART_SIZE_MB = "448"

MENDER_STORAGE_DEVICE_BASE = '/dev/mmcblk0p'

MENDER_BOOT_PART = "${MENDER_STORAGE_DEVICE_BASE}1"
MENDER_DATA_PART = "${MENDER_STORAGE_DEVICE_BASE}4"
MENDER_ROOTFS_PART_A = "${MENDER_STORAGE_DEVICE_BASE}2"
MENDER_ROOTFS_PART_B = "${MENDER_STORAGE_DEVICE_BASE}3"

MENDER_FEATURES_DISABLE:append = " mender-growfs-data"

inherit extrausers
EXTRA_USERS_PARAMS = "usermod -p '$(openssl passwd -6 root)' root;"
