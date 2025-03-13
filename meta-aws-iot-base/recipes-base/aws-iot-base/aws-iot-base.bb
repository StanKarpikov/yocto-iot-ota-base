SUMMARY = "AWS IoT Base"
DESCRIPTION = "Collection of packages to connect devices to AWS IoT"
LICENSE = "CLOSED"

RDEPENDS:${PN} += " \
    aws-iot-device-client \
"

FILESEXTRAPATHS:prepend = "${THISDIR}/files:"
SRC_URI = " \
    file://aws_config.json \
    file://AmazonRootCA1.pem \
    file://device.pem.crt \
    file://private.pem.key \
"

do_install() {
    install -d ${D}/etc/aws
    install -d ${D}/etc/cert
    install -m 0644 ${WORKDIR}/aws_config.json ${D}/etc/aws/
    install -m 0644 ${WORKDIR}/AmazonRootCA1.pem ${D}/etc/cert/
    install -m 0644 ${WORKDIR}/device.pem.crt ${D}/etc/cert/
    install -m 0644 ${WORKDIR}/private.pem.key ${D}/etc/cert/
}

FILES:${PN} = " /etc/aws/aws_config.json \
                /etc/cert/"

ALLOW_EMPTY:${PN} = "1"