FILESEXTRAPATHS:prepend:mender-update-install := "${THISDIR}/files:"
SRC_URI:append:aarch64:mender-update-install = " file://02_mender_root_bootargs_grub.cfg;subdir=git"
