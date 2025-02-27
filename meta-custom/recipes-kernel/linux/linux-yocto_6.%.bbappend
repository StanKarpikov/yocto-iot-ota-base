FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

PACKAGE_ARCH = "${MACHINE_ARCH}"

SRC_URI:append = " \
    file://nvme_compiled_in.cfg \
"

# SRC_URI += "file://custom-overlay.dts;subdir=git/arch/${ARCH}/boot/dts/nvidia"

# KERNEL_DEVICETREE:append = " nvidia/custom-overlay.dtbo"
