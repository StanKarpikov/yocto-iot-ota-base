DESCRIPTION = "Fake U-Boot provider"
PROVIDES += "u-boot virtual/bootloader"
RPROVIDES_${PN} += "u-boot virtual/bootloader"

LICENSE = "MIT"
MENDER_UBOOT_AUTO_CONFIGURE = "0"

inherit deploy

do_deploy() {
    :
}

addtask deploy after do_compile before do_build