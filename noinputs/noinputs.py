#!/usr/bin/env python3

import argparse
import math
import os
import re
import sys
from contextlib import closing
from threading import Event
from typing import Any, Callable

import evdev
from evdev import ecodes

class DefaultArgs:
    all_devs = True
    multi = False

args = DefaultArgs()


def printe(*args: Any, **kwargs: Any) -> None:
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


class InputDevice(evdev.InputDevice):  # type: ignore
    basename: str

    bustype: str
    vendor: str
    product: str
    hex_version: str

    venprod: str

    _str: str

    def __init__(self, dev: str):
        super().__init__(dev)
        self.basename = os.path.basename(self.path)

        self.bustype = f"{self.info.bustype:04x}"
        self.vendor = f"{self.info.vendor:04x}"
        self.product = f"{self.info.product:04x}"
        self.hex_version = f"{self.info.version:04x}"

        self.venprod = f"{self.vendor}:{self.product}"

        self.id = f"{self.basename.removeprefix('event')}"
        self._str = f'{self.id:}\t{{{self.venprod}}}\t"{self.name}"'

    def match(self, search: str) -> bool:
        return (
            self.basename == f"event{search}"
            or self.venprod == search
            or re.fullmatch(search, self.name) is not None
        )

    def set_inhibit(self, value: bool) -> None:
        with open(
            f"/sys/class/input/{self.basename}/device/inhibited", "w"
        ) as f:
            f.write("01"[value])

    def get_inhibit(self) -> bool:
        with open(
            f"/sys/class/input/{self.basename}/device/inhibited", "r"
        ) as f:
            return f.read(1) == "1"

    def toggle_inhibit(self) -> None:
        self.set_inhibit(not self.get_inhibit())

    def __str__(self) -> str:
        return self._str


EV_FILTER = [
    ecodes.EV_KEY,  # Keyboards
    ecodes.EV_REL,  # Mice
    ecodes.EV_ABS,  # Gamepads/Tablets
]


def check_ev_caps(dev: InputDevice) -> bool:
    if args.all_devs:
        return True

    caps = dev.capabilities().keys()
    return any(x in EV_FILTER for x in caps)


def list_devices(*search: str) -> None:
    devices = []
    for dev in find_devices(*search):
        print(f"{'X' if dev.get_inhibit() else ' '} {dev}")
        devices.append(dev)
        dev.close()
    return devices


def find_devices(*search: str) -> list[InputDevice]:
    devs: list[InputDevice] = []

    for device in evdev.list_devices():
        dev = InputDevice(device)

        if not check_ev_caps(dev):
            dev.close()
            continue

        if not search:
            devs.append(dev)
            continue

        for s in search:
            if dev.match(s):
                devs.append(dev)
                break
        else:
            dev.close()

    return devs


def act_check(f: Callable[[list[InputDevice]], None]) -> Callable[[str], None]:
    """
    Function decorator that wraps functions that take InputDevice lists to
    effectively take search queries instead. Sanity checks included.
    """

    def func(*search: str) -> None:
        if not search:
            arg_parser.error("Provide device name or id")

        devs = find_devices(*search)
        if len(devs) == 0:
            sys.exit("No devices found")

        if len(devs) > 1 and not args.multi:
            printe("Found devices:")
            for dev in devs:
                printe(" ", dev)
            printe("\nWon't act on multiple devices! Pass -m to do it anyway.")
            sys.exit(1)

        f(devs)

    return func


@act_check
def grab_devices(devs: list[InputDevice]) -> None:
    printe(f"Grabbing:")
    for dev in devs:
        printe(" ", dev)
        dev.grab()

    try:
        Event().wait()
    except KeyboardInterrupt:
        for dev in devs:
            dev.close()


@act_check
def inhibit_devices(devs: list[InputDevice]) -> None:
    printe(f"Inhibiting:")
    for dev in devs:
        dev.set_inhibit(True)
        printe(" ", dev)


@act_check
def uninhibit_devices(devs: list[InputDevice]) -> None:
    printe(f"Uninhibiting:")
    for dev in devs:
        dev.set_inhibit(False)
        printe(" ", dev)


@act_check
def toggle_inhibit(devs: list[InputDevice]) -> None:
    printe(f"Toggling:")
    for dev in devs:
        dev.toggle_inhibit()
        printe(" ", dev)


@act_check
def generate_udev_rule(devs: list[InputDevice]) -> None:
    if sys.stdout.isatty():
        # Only print "sudo" if it's being used right now
        sudo = os.environ.get("SUDO_COMMAND", "") and "sudo "

        printe(
            "Put the text under 8< into a .rules file in /etc/udev/rules.d/",
            "This can be done manually or with tee. E.g.:",
            f"{sudo}{' '.join(sys.argv)} | {sudo}tee /etc/udev/rules.d/99-noinputs.rules",
            "-- 8< ----------",
            sep="\n",
        )

    for dev in devs:
        print(
            'ACTION=="add"',
            'SUBSYSTEM=="input"',
            'ATTRS{inhibited}=="0"',
            f'ATTRS{{id/bustype}}=="{dev.bustype}"',
            f'ATTRS{{id/vendor}}=="{dev.vendor}"',
            f'ATTRS{{id/product}}=="{dev.product}"',
            f'ATTRS{{id/version}}=="{dev.hex_version}"',
            f'ATTRS{{name}}=="{dev.name}"',
            'ATTR{inhibited}="1"',
            sep=", ",
        )


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="list and inhibit input devices"
    )

    arg_parser.add_argument(
        "-a",
        "--alldevs",
        action="store_true",
        dest="all_devs",
        help="""do not filter devices by capabilities. Show and search through
        all devices; not just mice, keyboards, and gamepads""",
    )

    arg_parser.add_argument(
        "-m",
        "--multiple",
        action="store_true",
        dest="multi",
        help="""allow grabbing/inhibiting multiple devices at once""",
    )

    arg_parser.add_argument(
        "-l",
        "--list",
        action="store_const",
        dest="act",
        const=list_devices,
        help="list devices. Acts as dry run, if [device] is provided",
    )

    arg_parser.add_argument(
        "-g",
        "--grab",
        action="store_const",
        dest="act",
        const=grab_devices,
        help="grab device and hang around",
    )

    arg_parser.add_argument(
        "-i",
        "--inhibit",
        action="store_const",
        dest="act",
        const=inhibit_devices,
        help="inhibit device",
    )

    arg_parser.add_argument(
        "-u",
        "--uninhibit",
        action="store_const",
        dest="act",
        const=uninhibit_devices,
        help="uninhibit device",
    )

    arg_parser.add_argument(
        "-t",
        "--toggle",
        action="store_const",
        dest="act",
        const=toggle_inhibit,
        help="toggle inhibit state",
    )

    arg_parser.add_argument(
        "--gen-udev-rule",
        action="store_const",
        dest="act",
        const=generate_udev_rule,
        help="generate udev rule to auto-inhibit device",
    )

    arg_parser.add_argument(
        "device",
        nargs="*",
        default="",
        help="""
        device's numeric id, vendor:product, or a regular expressions used to
        match against the entire name. E.g. "Mouse" would only match devices
        named exactly that, while ".*Mouse.*" would match anything with the word
        in the name.
        """,
    )

    args = arg_parser.parse_args()

    if os.getuid() != 0:
        sys.exit("Insufficient permissions. Need root!")
    elif args.act:
        args.act(*args.device)
    else:
        arg_parser.print_help()
