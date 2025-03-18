FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI += " \
    file://enable_sdhci.cfg \
"

KERNEL_FEATURES:append = " enable_sdhci.cfg"