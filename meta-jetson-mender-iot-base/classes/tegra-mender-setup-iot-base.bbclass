inherit tegra-mender-setup

# Boot partition size (override)
MENDER_BOOT_PART_SIZE_MB = "64"
# Boot partition (override)
MENDER_BOOT_PART = "${MENDER_STORAGE_DEVICE_BASE}1"

IMAGE_BOOT_FILES = ""