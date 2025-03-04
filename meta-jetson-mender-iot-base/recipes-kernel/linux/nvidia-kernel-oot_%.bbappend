DEPENDS:append = " dtc-native"

FILESEXTRAPATHS:prepend := "${THISDIR}/linux-yocto:"
SRC_URI:append = " file://jetson-mender-iot-base-overlay.dts"

do_compile:append() {
    dtc -@ -O dtb -o ${B}/kernel-devicetree/generic-dts/dtbs/jetson-mender-iot-base-overlay.dtbo ${WORKDIR}/jetson-mender-iot-base-overlay.dts
}

do_sign_dtbs:append() {
    dtbo_file="${B}/kernel-devicetree/generic-dts/dtbs/jetson-mender-iot-base-overlay.dtbo"
    if [ -e "$dtbo_file" ]; then
        tegra_uefi_attach_sign "$dtbo_file"
    fi
}