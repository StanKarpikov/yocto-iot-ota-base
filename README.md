#

See https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html

Initialise build environment:

```bash
source poky/oe-init-build-env .
```

Change absolute paths to `${TOPDIR}`:

```
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
