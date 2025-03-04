# Custom Yocto Configuration for Jetson Orin NX with Mender

This configuration can be used as a basis for IoT projects for Jetson. It integrates with Mender and can be run in Qemu (however, without EFI for now).

> Note that the generated `sdimg` file contains the boot partition that is not used for flashing Jetson, but instead included for compatibility with Qemu. For production, use `INHERIT` in the distro configuration from `tegra-mender-setup` class instead of `tegra-mender-setup-iot-base`.

The test server certificate provided for convenience, it should be replaced for production and removed from git.

The devicetree overlay is not used at the moment and provided as a reference.

For general info about Yocto see <https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html>

## Preparation

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

## Run

### Steps Before Running Build

```bash
source tegra-demo-distro/layers/oe-init-build-env .

# The cache and downloads directory can be moved elsewhere, but the cache requires a Linux filesystem, NTFS doesn't work
export YOCTO_CACHE_DIR="."
# export SSTATE_DIR="$YOCTO_CACHE_DIR/sstate-cache"
# export TMPDIR="$YOCTO_CACHE_DIR/tmp"
export DL_DIR="$YOCTO_CACHE_DIR/downloads"
export BB_ENV_PASSTHROUGH_ADDITIONS="DL_DIR"
```

### Build

```bash

# Build
bitbake core-image-jetson-mender-iot-base
```

## Debugging and Useful Commands

### Show Dependencies

```bash
# Show Recipes
bitbake-layers show-recipes
# Then
bitbake -g core-image-minimal -u taskexp

# List packages to build
bitbake -g core-image-minimal && cat pn-buildlist | grep -ve "native" | sort | uniq
```

### Check for Variable

```bash
bitbake -e core-image-jetson-mender-iot-base | grep EXTRA_USERS_PARAMS
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

# Which package includes a file
oe-pkgdata-util find-path /boot/efi/bootaa64.efi
```

### Clean

```bash
bitbake world -c cleanall --continue
```

### Freeze Package Versions

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

### Check systemd services

```bash
SYSTEMD_COLORS=0 systemctl list-units --failed
```

## Running in Qemu

### Compile Qemu for Testing

To use the `user` mode network, compile Qemu from sources

```bash
git clone https://gitlab.com/qemu-project/qemu.git
cd qemu
./configure --target-list=aarch64-softmmu --enable-slirp
make
sudo make install
```

### Running a x86-64 Image

```bash
IMAGE=core-image-jetson-mender-iot-base
cd build/tmp/deploy/images/qemux86-64/
IMAGE="$IMAGE-qemux86-64.sdimg"; qemu-img resize -f raw "$IMAGE" 2G

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
    -drive file=$IMAGE-qemux86-64.sdimg,if=none,format=raw,id=sdimg_drive \
    -nic tap \
    -serial mon:stdio \
    -nographic
```

### Running an ARM64 Image

#### Boot using provided initrd and kernel

```bash
IMAGE=core-image-jetson-mender-iot-base
MACHINE=p3768-0000-p3767-0000

cd build/tmp/deploy/images/$MACHINE/
gunzip -kf tegra-minimal-initramfs-$MACHINE.cpio.gz
qemu-system-aarch64 \
    -m 2048 \
    -cpu cortex-a76 \
    -machine virt,highmem=off \
    -smp 1 \
    -device nvme,serial=deadbeef,drive=nvm \
    -drive file=$IMAGE-$MACHINE.sdimg,if=none,format=raw,id=nvm \
    -kernel Image \
    -initrd tegra-minimal-initramfs-$MACHINE.cpio \
    -append "root=/dev/nvme0n1p2 mminit_loglevel=4 console=ttyAMA0,115200 fbcon=map:0 nospectre_bhb video=efifb:off earlycon" \
    -nic user,model=virtio-net-pci \
    -serial mon:stdio \
    -nographic
```

#### Boot using EFI (TODO)

> This doesn't work at the moment, probably because the Jetson EFI binary expects more partitions in the image file

```bash
# get EFI EDK2 firmware from https://packages.debian.org/sid/qemu-efi-aarch64
# see https://www.kraxel.org/blog/2022/05/edk2-virt-quickstart/
dd of="QEMU_EFI-pflash.raw" if="/dev/zero" bs=1M count=64
dd of="QEMU_EFI-pflash.raw" if="AAVMF_CODE.no-secboot.fd" conv=notrunc
dd of="QEMU_VARS-pflash.raw" if="/dev/zero" bs=1M count=64
dd of="QEMU_VARS-pflash.raw" if="AAVMF_VARS.fd" conv=notrunc

MACHINE=p3768-0000-p3767-0000
IMAGE=core-image-jetson-mender-iot-base
SDIMAGE=$IMAGE-$MACHINE.sdimg
ESPIMAGE=tegra-espimage-$MACHINE.esp
qemu-system-aarch64 \
    -m 2048 \
    -cpu cortex-a76 \
    -machine virt,highmem=off,pflash0=code,pflash1=vars \
    -smp 8 \
    -device nvme,serial=aaaaaaa0,drive=nvm_boot \
    -drive file=esp.img,if=none,format=raw,id=nvm_boot \
    -device nvme,serial=aaaaaaa1,drive=nvm_main \
    -drive file=$SDIMAGE,if=none,format=raw,id=nvm_main \
    -device nvme,serial=aaaaaaa3,drive=nvm_1 \
    -drive file=boot.img,if=none,format=raw,id=nvm_1 \
    -device nvme,serial=aaaaaaa2,drive=nvm_2 \
    -drive file=initrd-flash.img,if=none,format=raw,id=nvm_2 \
    -drive if=none,id=code,format=raw,readonly=on,file=QEMU_EFI-pflash.raw \
    -drive if=none,id=vars,format=raw,file=QEMU_VARS-pflash.raw \
    -nic user,model=virtio-net-pci \
    -serial mon:stdio
```

### Build UEFI for Jetson

The following commands can be used to build an EFI binary for Jetson, however this doesn't fully work.
See https://forums.developer.nvidia.com/t/building-edk2-firmware-for-tegra-with-gcc-12-2/227757/5

```bash
mkdir edkrepo
cd edkrepo/
wget https://github.com/tianocore/edk2-edkrepo/releases/download/edkrepo-v2.1.2/edkrepo-2.1.2.tar.gz
tar xpvf edkrepo-2.1.2.tar.gz
python3.10 -m venv venv
sudo su
. ./venv/bin/activate
pip install setuptools
./install.py --verbose
edkrepo manifest-repos add nvidia https://github.com/NVIDIA/edk2-edkrepo-manifest.git main nvidi
edkrepo clone nvidia-uefi NVIDIA-Jetson jetson-r35.1
cd nvidia-uefi/
cat edk2-nvidia/Platform/NVIDIA/Jetson/Build.md 
apt install -y python3-virtualenv gcc-aarch64-linux-gnu
edk2-nvidia/Platform/NVIDIA/Jetson/build.sh
# If fails:
venv/bin/pip install setuptools

rm -r venv
python3.10 -m venv venv
/venv/bin/pip install --upgrade -r edk2/pip-requirements.txt
```
