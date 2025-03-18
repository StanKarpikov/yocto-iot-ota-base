do_install:append () {
    rm "${D}${nonarch_base_libdir}/firmware/brcm/brcmfmac43455-sdio.raspberrypi,4-model-b.bin" 
    ln -s -r "${D}${nonarch_base_libdir}/firmware/cypress/cyfmac43455-sdio-standard.bin" "${D}${nonarch_base_libdir}/firmware/brcm/brcmfmac43455-sdio.raspberrypi,4-model-b.bin"
}