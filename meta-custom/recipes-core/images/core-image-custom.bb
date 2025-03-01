require recipes-demo/images/demo-image-base.bb

SUMMARY = "Minimal image with BusyBox"
LICENSE = "MIT"

# TODO: Activate this in fstab
IMAGE_FEATURES:append = " read-only-rootfs"

IMAGE_INSTALL:append = " shadow-base mender-server-certificate nvidia-kernel-oot-devicetrees"
IMAGE_INSTALL:remove = "sysvinit busybox-sysvinit cuda-samples kernel-module-nvme"

IMAGE_FSTYPES = "ext4 sdimg tar.bz2 cpio.gz"

# TODO: Remove systemd
INIT_MANAGER = "systemd"
VIRTUAL-RUNTIME_init_manager = "systemd"

DISTRO_FEATURES:append = " systemd usrmerge"
DISTRO_FEATURES_BACKFILL_CONSIDERED:append = "sysvinit"
VIRTUAL-RUNTIME_initscripts = "systemd-compat-units"
VIRTUAL-RUNTIME_login_manager = "shadow-base"
VIRTUAL-RUNTIME_dev_manager = "systemd"
ROOT_HOME ?= "/root"

# Can save 10MB, but required for the USB to function
# BAD_RECOMMENDATIONS:append = "udev-hwdb"

MENDER_FEATURES_DISABLE:append = " mender-growfs-data"

inherit extrausers
EXTRA_USERS_PARAMS = "usermod -p '$(openssl passwd -6 root)' root;"
