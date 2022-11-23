# -*- coding: utf-8 -*-
# Copyright (c) 2020, KarjaKAK
# All rights reserved.

import subprocess
from sys import platform as plat


def ctlight():
    # Check for system theme mode

    thm = None
    if plat.startswith("win"):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        thm = subprocess.run(
            [
                "powershell.exe",
                '(Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize").SystemUsesLightTheme',
            ],
            startupinfo=startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
    else:
        thm = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

    match thm := thm.stdout:
        case thm if "Dark" in thm:
            return False
        case thm if thm.replace("\n", "") == "0":
            return False
        case _:
            return True


if __name__ == "__main__":
    print(ctlight())
