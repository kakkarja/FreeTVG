# -*- coding: utf-8 -*-
# Copyright (c) 2020, KarjaKAK
# All rights reserved.

import psutil


# For mdh:
# "com.apple.WebKit.Networking", "com.apple.WebKit.WebContent"


class PidStore:
    def __init__(self, *procs) -> None:
        self.procs = procs
        self.l1 = set()
        self.l2 = set()

    def collect(self):
        container = self.l1 if not self.l1 else self.l2
        for proc in psutil.process_iter(["pid", "name"]):
            if proc.info["name"] in self.procs:
                container.add(proc.info["pid"])

    def _xor_remain(self):
        if self.l1 and self.l2 and self.l1 != self.l2:
            return self.l1 ^ self.l2
        else:
            return self.l1

    def terminate(self):
        procs = self._xor_remain()
        for proc in procs:
            psutil.Process(proc).kill()

    def avail(self):
        if self.l1:
            return True
        else:
            return False


PROCS = PidStore()
