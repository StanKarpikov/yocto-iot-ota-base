SUMMARY = "AWS IoT Base"
DESCRIPTION = "Collection of packages to connect devices to AWS IoT"
LICENSE = "MIT"

RDEPENDS:${PN} += " \
    python3-difflib \
    python3-asyncio \
    python3-xml \
"

ALLOW_EMPTY:${PN} = "1"