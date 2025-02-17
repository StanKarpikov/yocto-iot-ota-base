# Guide

See <https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html>

## Initialise New Confguration

```bash
source poky/oe-init-build-env .
```

Change absolute paths to `${TOPDIR}`:

```ini
(...)
BBLAYERS ?= " \
  ${TOPDIR}/poky/meta \
  ${TOPDIR}/poky/meta-poky \
  ${TOPDIR}/poky/meta-yocto-bsp \
(...)
```

Workaround for Ubuntu 24.04

```bash
# Workaround for ubuntu issue [Allow bitbake to create user namespace](https://bugs.launchpad.net/ubuntu/+source/apparmor/+bug/2056555)
# Credit to Changqing Li (sandy-lcq), Karsten S. Opdal (karsten-s-opdal) and Ferry Toth (ftoth)

## Add Bitbake's AppArmor Profile to associate it with User Namespace profile
sudo tee /etc/apparmor.d/bitbake > /dev/null <<'EOF'
abi <abi/4.0>,
include <tunables/global>
profile bitbake /**/bitbake/bin/bitbake flags=(unconfined) {
        userns,
}
EOF

# Reload AppArmor Profile
sudo apparmor_parser -r /etc/apparmor.d/bitbake
```

## Show Dependencies

```bash
# Show Recipes
bitbake-layers show-recipes
# Then
bitbake -g core-image-minimal -u taskexp

# List packages to build
bitbake -g core-image-minimal && cat pn-buildlist | grep -ve "native" | sort | uniq
```

## Run

### Steps Before Running Build

```bash
source poky/oe-init-build-env .

export YOCTO_CACHE_DIR="."
# export SSTATE_DIR="$YOCTO_CACHE_DIR/sstate-cache"
# export TMPDIR="$YOCTO_CACHE_DIR/tmp"
export DL_DIR="$YOCTO_CACHE_DIR/downloads"
export BB_ENV_PASSTHROUGH_ADDITIONS="DL_DIR"

```

### Build

```bash

# Build
bitbake core-image-custom

# Run in Qemu
runqemu qemux86-64 nographic
```

## Debugging

### Check for Variable

```bash
bitbake -e core-image-custom | grep EXTRA_USERS_PARAMS
```
