do_install() {
    install -d -m 755 ${D}/${MENDER_BOOT_PART_MOUNT_LOCATION}/dtb

    for dtb_path in ${KERNEL_DEVICETREE}; do
        install -m 0644 ${DEPLOY_DIR_IMAGE}/devicetree/$(basename $dtb_path) ${D}/${MENDER_BOOT_PART_MOUNT_LOCATION}/dtb/
    done
}