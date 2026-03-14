# NoInputs-GUI

<p align="center">
  <!-- Replace with your project logo -->
  <img src="logo.png" alt="NoInputs GUI Logo" width="200"/>
</p>

A **simple Linux GUI tool** that allows users to **temporarily disable and re-enable input devices** such as **mice, keyboards, and other input peripherals**.

This tool is designed specifically for **Wayland environments**, where traditional tools like `xinput` do not work.

`NoInputs-GUI` is based on the original CLI project **noinputs**, providing a **graphical interface** for easier device management.

---

## Features

- 🖱️ **List all input devices**
- ⛔ **Disable (inhibit) input devices**
- 🔁 **Re-enable disabled devices**

---

## Current Status

⚠️ **Stable Beta**

- Tested only on:
  - **Arch Linux**
  - **CachyOS**

Other distributions may work but are **currently untested**.

---

## Wayland Only

This project targets **Wayland users**.

For **X11 users**, tools such as:

- `xinput`
- `xinput disable`
- other X11 utilities

already provide similar functionality.

`NoInputs-GUI` exists to fill this **missing functionality under Wayland**.

---

## Installation

Currently, the application is **not available in the Arch repositories**.

Installation is done by downloading the binary from the **GitHub Releases** page.

### 1. Download the latest release

Go to the **Releases** section of this repository and download the archive.

### 2. Extract the archive

```
unzip noinputs-0.1.0.zip 
```

Inside the archive you will find 

```
noinputs_gui.bin
```

### 3. Make it executable

```bash
chmod +x NoInputs-GUI.bin
```

### 4. Run it

```bash
./NoInputs-GUI.bin
```

### 5. Create a shortcut

For conveniency, I would advise to create a desktop shortcut or a symbolic link to launch it where it's convenient for you.

### 6. Installation

The first time you run the program, you will be prompted to "install" the program, it will run the `installer.sh` script available in the source code. It will essentially create an udev rule so the program can access your devices. 
However the program will prompt you everytime you want to disable a device.


## Example Usage

Once launched, the GUI will:
- List all available input devices
- Allow you to select a device
- Disable or re-enable it with a button

Disabled devices remain inhibited until:
- they are re-enabled
- the device is unplugged
- the system reboots

## Credits

[The original project provides](https://gitlab.com/S410/noinputs) the underlying concept and functionality for Wayland input inhibition.

## Contributing

Feedback, bug reports, and suggestions are appreciated.

I won't allow any contribution to this repository for safety measures, but you are welcome to fork it and reuse my code as you please. But take into consideration I am not responsible for anything happening with the source code outside of this repository.

If you encounter issues, please open an Issue on this repository.

## License 

The project is under the GNU GPL-3.0 License as is the original project. 

See the `LICENSE` for details.