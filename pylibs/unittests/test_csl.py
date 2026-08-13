#!/usr/bin/env python3
# Copyright (c) 2023-2024, The OTNS Authors.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
import logging
import unittest
from typing import Dict

from OTNSTestCase import OTNSTestCase
from otns.cli import errors, OTNS


class CslTests(OTNSTestCase):



    def testCslReenable(self):
        ns = self.ns

        print("ABTIN - ABTIN ######################################################################################")

        # setup a Parent Router with SSED Child
        ns.add("router", 100, 100)
        ns.go(10)
        nodeid = ns.add("ssed", 200, 100)
        ns.node_cmd(nodeid, "csl period 288000")
        ns.go(10)
        self.assertFormPartitions(1)


        if False:
            print("ABTIN Parent pings SSED FIRST")

            for n in range(0, 15):
                ns.ping(1, 2, datasize=n + 10)
                ns.go(5)
            self.assertPings(ns.pings(), 15, max_delay=3000, max_fails=1)

            print("ABTIN Parent pings SSED FIRST PASSED!!!!")

        print("ABTIN SSED pings parent (only 1 now) !!!!!!!!")

        # SSED pings parent
        for n in range(0, 1):
            ns.ping(2, 1, datasize=n + 10)
            ns.go(5)
        self.assertPings(ns.pings(), 1, max_delay=3000, max_fails=1)

        print("ABTIN SSED pings parent ALL GOOD")

        # parent pings SSED

        print("ABTIN Parent pings SSED (only one now also)")

        for n in range(0, 1):
            ns.ping(1, 2, datasize=n + 10)
            ns.go(5)

        self.assertPings(ns.pings(), 11, max_delay=3000, max_fails=1)

        print("ABTIN-------------------------------------------------------------------------------------------")

        for k in range(0, 4):
            # disable CSL
            ns.node_cmd(nodeid, "csl period 0")
            ns.go(1)

            # SSED pings parent
            for n in range(0, 15):
                ns.ping(2, 1, datasize=n + 10)
                ns.go(5)
            self.assertPings(ns.pings(), 15, max_delay=3000, max_fails=1)

            # re-enable CSL
            ns.node_cmd(nodeid, "csl period 144000")
            ns.go(1)

            # SSED pings parent
            for n in range(0, 15):
                ns.ping(2, 1, datasize=n + 10)
                ns.go(5)
            self.assertPings(ns.pings(), 15, max_delay=3000, max_fails=1)

            # parent pings SSED
            for n in range(0, 15):
                ns.ping(1, 2, datasize=n + 10)
                ns.go(5)
            self.assertPings(ns.pings(), 15, max_delay=3000, max_fails=1)


if __name__ == '__main__':
    unittest.main()
