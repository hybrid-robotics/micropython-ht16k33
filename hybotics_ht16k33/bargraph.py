# SPDX-FileCopyrightText: 2018 Carter Nelson  for Adafruit Industries
# SPDX-FileCopyrightText: Dale Weber 2021
#
# SPDX-License-Identifier: MIT

"""
`hybotics_ht16k33.bargraph`
===========================

* Authors: Carter Nelson for Adafruit Industries

* Ported to Micropython by Dale Weber <hybotics.wy@gmail.com>
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/hybotics/Hybotics_Micropython_HT16K33.git"

from hybotics_ht16k33.ht16k33 import HT16K33


class Bicolor24(HT16K33):
    """Bi-color 24-bar bargraph display."""

    LED_OFF = 0
    LED_RED = 1
    LED_GREEN = 2
    LED_YELLOW = 3

    def __getitem__(self, key):
        # map to HT16K33 row (x) and column (y), see schematic
        x = key % 4 + 4 * (key // 12)
        y = key // 4 - 3 * (key // 12)
        # construct the color value and return it
        return self._pixel(x, y) | self._pixel(x + 8, y) << 1

    def __setitem__(self, key, value):
        # map to HT16K33 row (x) and column (y), see schematic
        x = key % 4 + 4 * (key // 12)
        y = key // 4 - 3 * (key // 12)
        # conditionally turn on red LED
        self._pixel(x, y, value & 0x01)
        # conditionally turn on green LED
        self._pixel(x + 8, y, value >> 1)

    def fill(self, color):
        """Fill the whole display with the given color."""
        what_it_was = self.auto_write
        self.auto_write = False
        for i in range(24):
            self[i] = color
        self.show()
        self.auto_write = what_it_was
