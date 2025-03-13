SUMMARY = "AWS IoT Base"
DESCRIPTION = "Collection of packages to connect devices to AWS IoT"
LICENSE = "CLOSED"

RDEPENDS:${PN} += " \
    aws-iot-device-client \
"

ALLOW_EMPTY:${PN} = "1"