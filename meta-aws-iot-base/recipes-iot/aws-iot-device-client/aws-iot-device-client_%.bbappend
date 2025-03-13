BBAPPEND_DIR := "${THISDIR}"
FILESEXTRAPATHS:prepend = "${BBAPPEND_DIR}/files:"
SRC_URI += " \
    file://aws-iot-device-client.json \
    file://AmazonRootCA1.pem \
    file://device.pem.crt \
    file://private.pem.key \
"

do_install:append() {
    install -d ${D}/etc/aws_cert
    install -d ${D}/etc/.aws-iot-device-client
    chmod -R 700 ${D}/etc/aws_cert
    chmod -R 700 ${D}/etc/.aws-iot-device-client
    install -m 0644 ${WORKDIR}/AmazonRootCA1.pem ${D}/etc/aws_cert/
    install -m 0644 ${WORKDIR}/device.pem.crt ${D}/etc/aws_cert/
    install -m 0600 ${WORKDIR}/private.pem.key ${D}/etc/aws_cert/

    install -m 0755 ${WORKDIR}/aws-iot-device-client.json \
                  ${D}/etc/.aws-iot-device-client/aws-iot-device-client.json
}