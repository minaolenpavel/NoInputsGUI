# noinputs

#### A simple script to list and temporarily disable input devices.

This script attempts to provide experience similar to that of `xinput`
while being Wayland compatible.

```
$ sudo noinputs.py --list
  [0]   {0000:0001}     "Power Button"
  [1]   {0000:0001}     "Power Button"
  [5]   {046D:C092}     "Logitech G102 LIGHTSYNC Gaming Mouse"
  [6]   {046D:C092}     "Logitech G102 LIGHTSYNC Gaming Mouse Keyboard"
  [19]  {0000:0000}     "Eee PC WMI hotkeys"
  [10]  {2333:6666}     "ydotoold virtual device"
  [2]   {046D:C328}     "Logitech USB Keyboard"
  [3]   {046D:C328}     "Logitech USB Keyboard Consumer Control"
  [4]   {046D:C328}     "Logitech USB Keyboard System Control"
X [11]  {30FA:0301}     "USB OPTICAL MOUSE "
$ sudo noinputs.py -t 11
Toggling:
  [11]  {30FA:0301}     "USB OPTICAL MOUSE "
```

### Features:

-   Select devices using numeric id, vendor:product or regular expression
-   List device
    > Inhibited devices are marked with X  
    > Acts as dry-run, if a list of devices is provided
-   Inhibit devices
    > The devices will be disabled until they're re-enabled,
    > re-plugged or the machine reboots
-   Toggle inhibition of devices
-   Grab devices
    > The devices will be disabled while the program is running
-   Generate udev rules to auto-inhibit unwanted devices automatically

---

The utility requires superuser permissions to work.
To avoid having to type the password every time, a sudoers configuration file
can be added.

For example:

```
# /etc/sudoers.d/noinputs

%wheel ALL=(root) NOPASSWD:/usr/bin/noinputs
```

will allow any member of the group "wheel" to use the utility without password
verification.

### Installation:

[Available on AUR](https://aur.archlinux.org/packages/noinputs-git) for
Arch Linux based systems.

Manual installation:

-   Place `noinputs.py` in `/usr/local/bin` and mark it as executable
    ```sh
    # As root
    cp noinputs.py /usr/local/bin/noinputs
    chmod +x /usr/local/bin/noinputs
    ```
-   Install evdev library for python:
    | | |
    |-|-|
    | **Arch Linux** & friends | `pacman -S python-evdev` |
    | **Ubuntu, Debian** & friends | `apt install python3-evdev` |
    | **Fedora** & friends | `dnf install python3-evdev` |
    | **Alpine** | `apk add py3-evdev` |
    For other distros see [repology](https://repology.org/project/python:evdev/versions)

-   Use it as usual. E.g.:
    ```sh
    sudo noinputs -l # List input devices
    ```
