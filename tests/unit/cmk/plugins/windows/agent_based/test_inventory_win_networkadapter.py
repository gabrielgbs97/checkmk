#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


import pytest

from cmk.agent_based.v2 import InventoryResult, StringTable, TableRow
from cmk.plugins.windows.agent_based.inventory_win_networkadapter import (
    inventory_win_networkadapter,
    parse_win_networkadapter,
)


@pytest.mark.parametrize(
    "string_table, expected_result",
    [
        ([], []),
        (
            [
                ["AdapterType", " Ethernet 802.3"],
                ["DeviceID", " 7"],
                ["MACAddress", " 08", "00", "27", "9C", "F8", "39"],
                ["Name", " Intel(R) PRO/1000 MT-Desktopadapter 2"],
                ["NetworkAddresses", ""],
                ["ServiceName", " E1G60"],
                ["Speed", " 1000000000"],
                ["Address", " 192.168.178.26"],
                ["Subnet", " 255.255.255.0"],
                ["DefaultGateway", " 192.168.178.1"],
                ["AdapterType", " Ethernet 802.3"],
                ["DeviceID", " 7"],
                ["MACAddress", " 08", "00", "27", "9C", "F8", "39"],
                ["Name", " Intel(R) PRO/1000 MT-Desktopadapter 1"],
                ["NetworkAddresses", ""],
                ["ServiceName", " E1G60"],
                ["Speed", " 1000000000"],
                ["Address", " 192.168.178.26"],
                ["Subnet", " 255.255.255.0"],
                ["DefaultGateway", " 192.168.178.1"],
            ],
            [
                TableRow(
                    path=["hardware", "nwadapter"],
                    key_columns={
                        "name": " Intel(R) PRO/1000 MT-Desktopadapter 1",
                    },
                    inventory_columns={
                        "type": " Ethernet 802.3",
                        "macaddress": " 08:00:27:9C:F8:39",
                        "speed": 1000000000,
                        "gateway": " 192.168.178.1",
                        "ipv4_address": ", 192.168.178.26",
                        "ipv6_address": None,
                        "ipv4_subnet": "255.255.255.0",
                        "ipv6_subnet": None,
                    },
                    status_columns={},
                ),
                TableRow(
                    path=["hardware", "nwadapter"],
                    key_columns={
                        "name": " Intel(R) PRO/1000 MT-Desktopadapter 2",
                    },
                    inventory_columns={
                        "type": " Ethernet 802.3",
                        "macaddress": " 08:00:27:9C:F8:39",
                        "speed": 1000000000,
                        "gateway": " 192.168.178.1",
                        "ipv4_address": ", 192.168.178.26",
                        "ipv6_address": None,
                        "ipv4_subnet": "255.255.255.0",
                        "ipv6_subnet": None,
                    },
                    status_columns={},
                ),
            ],
        ),
    ],
)
def test_inventory_win_networkadapter(
    string_table: StringTable, expected_result: InventoryResult
) -> None:
    assert (
        list(inventory_win_networkadapter(parse_win_networkadapter(string_table)))
        == expected_result
    )
