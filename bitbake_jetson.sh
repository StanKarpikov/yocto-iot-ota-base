source tegra-demo-distro/layers/oe-init-build-env .

# The cache and downloads directory can be moved elsewhere, but the cache requires a Linux filesystem, NTFS doesn't work
if [ -z "$YOCTO_CACHE_DIR" ]; then
  export YOCTO_CACHE_DIR="."
fi
# export SSTATE_DIR="$YOCTO_CACHE_DIR/sstate-cache"
# export TMPDIR="$YOCTO_CACHE_DIR/tmp"
export DL_DIR="$YOCTO_CACHE_DIR/downloads"

export MACHINE="p3768-0000-p3767-0000"
export DISTRO="distro-jetson-mender-iot-base"
export JETSON_LAYERS_ENABLED=1
export RASPBERRYPI_LAYERS_ENABLED=0
export BB_ENV_PASSTHROUGH_ADDITIONS="DL_DIR JETSON_LAYERS_ENABLED MACHINE DISTRO"

bitbake core-image-jetson-mender-iot-base