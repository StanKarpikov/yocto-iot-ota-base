require recipes-demo/images/demo-image-base.bb

SUMMARY = "Minimal image with BusyBox"
LICENSE = "MIT"

# TODO: Activate this in fstab
IMAGE_FEATURES:append = " read-only-rootfs"

IMAGE_INSTALL:append = " shadow-base mender-server-certificate nvidia-kernel-oot-devicetrees pstree"
IMAGE_INSTALL:remove = "sysvinit busybox-sysvinit cuda-samples"

IMAGE_FSTYPES:append = " sdimg tar.bz2 cpio.gz"
IMAGE_FSTYPES:tegra = " sdimg tegraflash mender dataimg"
IMAGE_FSTYPES:pn-tegra-minimal-initramfs:tegra = "${INITRAMFS_FSTYPES}"
IMAGE_FSTYPES:pn-tegra-initrd-flash-initramfs:tegra = "${TEGRA_INITRD_FLASH_INITRAMFS_FSTYPES}"

# TODO: Remove systemd
INIT_MANAGER = "systemd"
VIRTUAL-RUNTIME_init_manager = "systemd"

DISTRO_FEATURES:append = " systemd usrmerge"
DISTRO_FEATURES_BACKFILL_CONSIDERED:append = "sysvinit"
VIRTUAL-RUNTIME_initscripts = "systemd-compat-units"
VIRTUAL-RUNTIME_login_manager = "shadow-base"
VIRTUAL-RUNTIME_dev_manager = "systemd"
ROOT_HOME ?= "/root"

inherit extrausers
EXTRA_USERS_PARAMS = "usermod -p '$(openssl passwd -6 root)' root;"
