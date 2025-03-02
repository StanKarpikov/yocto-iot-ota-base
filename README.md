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
source tegra-demo-distro/layers/oe-init-build-env .

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

### Check Kernel Config

```bash
bitbake -c menuconfig virtual/kernel

# Or if a component doesn't support menuconfig in Yocto
bitbake mender-uboot -c devshell
```

### Check Which Recipy Includes a Package

```bash
bitbake-layers show-recipes | grep bluez
```

### Clean

```bash
bitbake world -c cleanall --continue
```

## Freeze Package Versions

```bash
bitbake -s > package-versions.txt
bitbake -e | grep ^SRCREV_ > srcrevs.txt
```

Add `PREFERRED_VERSION_<package>` and put in `frozen.conf`.

### OPKG Ipk Package Management

```bash
# For example gcc
bitbake gcc

bitbake package-index
```

### Running a x86-64 Image

```bash
cd build/tmp/deploy/images/qemux86-64/
gunzip --force core-image-custom-qemux86-64.sdimg.gz
IMAGE="core-image-custom-qemux86-64.sdimg"; qemu-img resize -f raw "$IMAGE" 2G

# sudo for the network adapter
sudo qemu-system-x86_64 \
    -m 1024 \
    -cpu IvyBridge \
    -machine q35,i8042=off \
    -smp 2 \
    -device sdhci-pci \
    -device sd-card,drive=sdimg_drive \
    -kernel bzImage-qemux86-64.bin \
    -append "root=/dev/mmcblk0p2 ro console=ttyS0" \
    -drive file=core-image-custom-qemux86-64.sdimg,if=none,format=raw,id=sdimg_drive \
    -nic tap \
    -serial mon:stdio \
    -nographic
```

### Running an ARM64 Image

/dev/nvme0n1p1   227G  121G   95G  57% /
/dev/nvme0n1p10   63M  110K   63M   1% /boot/efi

```bash
cd build/tmp/deploy/images/jetson-orin-nx/

sudo qemu-system-aarch64 \
    -m 2048 \
    -cpu cortex-a76 \
    -machine virt,highmem=off \
    -smp 8 \
    -device nvme,serial=deadbeef,drive=nvm \
    -drive file=core-image-custom-jetson-orin-nx.sdimg,if=none,format=raw,id=nvm \
    -kernel Image \
    -append "root=/dev/nvme0n1p2 ro mminit_loglevel=4 console=ttyAMA0,115200 firmware_class.path=/etc/firmware fbcon=map:0 nospectre_bhb video=efifb:off earlycon" \
    -nic user,model=virtio-net-pci \
    -serial mon:stdio \
    -nographic
```

```bash
SYSTEMD_COLORS=0 systemctl list-units --failed
```

### Compile Qemu for Testing

```bash
git clone https://gitlab.com/qemu-project/qemu.git
cd qemu
./configure --target-list=aarch64-softmmu --enable-slirp
make
sudo make install
```
