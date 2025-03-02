FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

PACKAGE_ARCH = "${MACHINE_ARCH}"

SRC_URI:append = " \
    file://nvme_compiled_in.cfg \
"
