import subprocess
import re
import sys
import os
import time
import threading
import random
import keyboard
from colorama import Fore, Back, Style, init


init(autoreset=True)


original_mac = None
selected_interface = None
restore_in_progress = False


MANUFACTURER_OUIS = {
    "Intel": [
        "00:03:47", "00:04:23", "00:07:E9", "00:0C:F1", "00:0E:0C", 
        "00:0E:35", "00:12:F0", "00:13:02", "00:13:20", "00:13:CE", 
        "00:15:00", "00:15:17", "00:16:6F", "00:16:76", "00:16:EA", 
        "00:16:EB", "00:18:DE", "00:19:D1", "00:19:D2", "00:1B:21", 
        "00:1B:77", "00:1C:BF", "00:1C:C0", "00:1D:E0", "00:1D:E1", 
        "00:1E:64", "00:1E:65", "00:1E:67", "00:1F:3B", "00:1F:3C", 
        "00:20:7B", "00:21:5C", "00:21:5D", "00:21:6A", "00:21:6B", 
        "00:22:FA", "00:22:FB", "00:23:14", "00:23:15", "00:24:D6", 
        "00:24:D7", "00:26:C6", "00:26:C7", "00:27:0E", "00:27:10", 
        "00:28:F8", "00:28:F9", "00:28:FA", "00:2A:69", "00:2E:C4", 
        "00:3C:7D", "00:4D:7F", "04:D3:B0", "0C:8B:FD", "0C:D2:92", 
        "10:0B:A9", "10:F0:05", "18:3D:A2", "24:77:03", "28:16:AD", 
        "28:B2:BD", "30:3A:64", "34:13:E8", "34:DE:1A", "3C:A9:F4", 
        "3C:FD:FE", "40:25:C2", "44:85:00", "48:45:20", "48:51:B7", 
        "4C:34:88", "4C:79:BA", "4C:80:93", "4C:EB:42", "50:2D:A2", 
        "58:91:CF", "58:94:6B", "58:A8:39", "5C:51:4F", "5C:C5:D4", 
        "5C:E0:C5", "60:36:DD", "60:57:18", "64:80:99", "64:D4:DA", 
        "68:05:CA", "68:17:29", "68:5D:43", "70:1C:E7", "74:E5:0B", 
        "78:FF:57", "7C:2A:31", "7C:5C:F8", "7C:7A:91", "7C:B0:C2", 
        "80:19:34", "80:9B:20", "84:3A:4B", "84:A6:C8", "88:53:2E", 
        "8C:70:5A", "8C:A9:82", "90:49:FA", "90:E2:BA", "94:65:9C", 
        "98:4F:EE", "9C:4E:36", "A0:36:9F", "A0:88:B4", "A0:A8:CD", 
        "A4:34:D9", "A4:BF:01", "A4:C3:F0", "AC:2B:6E", "AC:72:89", 
        "AC:7B:A1", "AC:FD:CE", "B0:35:9F", "B4:96:91", "B4:B6:76", 
        "B8:03:05", "B8:81:98", "BC:0F:64", "BC:77:37", "C4:34:6B", 
        "C4:85:08", "C4:D9:87", "C8:21:58", "C8:34:8E", "C8:F7:33", 
        "CC:2F:71", "D0:57:4C", "D0:7E:35", "D8:FC:93", "DC:A9:71", 
        "E0:9D:31", "E4:42:A6", "E4:A7:A0", "E4:F8:9C", "E8:B1:FC", 
        "EC:0E:C4", "EC:3D:FD", "EC:EB:B8", "F0:27:65", "F0:42:1C", 
        "F4:06:69", "F4:8C:50", "F8:0F:41", "F8:16:54", "F8:59:71", 
        "F8:F2:1E", "FC:F8:AE"
    ],
    "Cisco": [
        "00:00:0C", "00:01:42", "00:01:43", "00:01:63", "00:01:64", 
        "00:01:96", "00:01:97", "00:01:C7", "00:01:C9", "00:02:16", 
        "00:02:17", "00:02:3D", "00:02:4A", "00:02:4B", "00:02:7D", 
        "00:02:7E", "00:02:B9", "00:02:BA", "00:02:FC", "00:02:FD", 
        "00:03:31", "00:03:32", "00:03:6B", "00:03:6C", "00:03:9F", 
        "00:03:A0", "00:03:E3", "00:03:E4", "00:03:FD", "00:03:FE", 
        "00:04:27", "00:04:28", "00:04:4D", "00:04:4E", "00:04:6D", 
        "00:04:6E", "00:04:9A", "00:04:9B", "00:04:C0", "00:04:C1", 
        "00:04:DD", "00:04:DE", "00:05:00", "00:05:01", "00:05:31", 
        "00:05:32", "00:05:5E", "00:05:5F", "00:05:73", "00:05:74", 
        "00:05:9A", "00:05:9B", "00:05:DC", "00:05:DD", "00:06:28", 
        "00:06:2A", "00:06:7C", "00:06:C1", "00:07:0D", "00:07:0E", 
        "00:07:4F", "00:07:50", "00:07:7D", "00:07:84", "00:07:85", 
        "00:07:B3", "00:07:B4", "00:07:EB", "00:07:EC", "00:08:20", 
        "00:08:21", "00:08:7C", "00:08:7D", "00:08:A3", "00:08:A4", 
        "00:08:C2", "00:08:E2", "00:08:E3", "00:09:11", "00:09:12", 
        "00:09:43", "00:09:44", "00:09:7B", "00:09:7C", "00:09:B6", 
        "00:09:B7", "00:09:E8", "00:09:E9", "00:0A:41", "00:0A:42", 
        "00:0A:8A", "00:0A:8B", "00:0A:B7", "00:0A:B8", "00:0A:F3", 
        "00:0A:F4", "00:0B:5F", "00:0B:60", "00:0B:85", "00:0B:86", 
        "00:0B:BE", "00:0B:BF", "00:0B:FC", "00:0B:FD", "00:0C:30", 
        "00:0C:31", "00:0C:41", "00:0C:85", "00:0C:86", "00:0C:CE", 
        "00:0C:CF", "00:0D:28", "00:0D:29", "00:0D:65", "00:0D:66", 
        "00:0E:38", "00:0E:39", "00:0E:83", "00:0E:84", "00:0E:D6", 
        "00:0E:D7", "00:0F:23", "00:0F:24", "00:0F:66", "00:0F:8F", 
        "00:0F:90", "00:0F:F7", "00:0F:F8", "00:10:07", "00:10:0B", 
        "00:10:0D", "00:10:11", "00:10:14", "00:10:1F", "00:10:29", 
        "00:10:2F", "00:10:54", "00:10:79", "00:10:7B", "00:10:A6", 
        "00:10:F6", "00:10:FF", "00:11:20", "00:11:21", "00:11:5C", 
        "00:11:5D", "00:11:92", "00:11:93", "00:11:BB", "00:11:BC", 
        "00:12:00", "00:12:01", "00:12:43", "00:12:44", "00:12:7F", 
        "00:12:80", "00:12:D9", "00:12:DA", "00:13:10", "00:13:19",
        "00:13:1A", "00:13:5F", "00:13:60", "00:13:97", "00:13:C3", 
        "00:13:C4", "00:14:1B", "00:14:69", "00:14:6A", "00:14:A8", 
        "00:14:A9", "00:14:F1", "00:14:F2", "00:15:2B", "00:15:2C", 
        "00:15:60", "00:15:62", "00:15:63", "00:15:C6", "00:15:C7", 
        "00:15:F9", "00:15:FA", "00:16:46", "00:16:47", "00:16:9C", 
        "00:16:9D", "00:16:C7", "00:16:C8", "00:17:0E", "00:17:0F", 
        "00:17:3B", "00:17:59", "00:17:5A", "00:17:94", "00:17:95", 
        "00:17:DF", "00:17:E0", "00:18:18", "00:18:19", "00:18:68", 
        "00:18:73", "00:18:74", "00:18:B9", "00:18:BA", "00:19:06", 
        "00:19:07", "00:19:2F", "00:19:30", "00:19:55", "00:19:56", 
        "00:19:A9", "00:19:AA", "00:19:E7", "00:19:E8", "00:1A:2F"
    ],
    "Apple": [
        "00:03:93", "00:05:02", "00:0A:27", "00:0A:95", "00:0D:93", 
        "00:0E:6D", "00:11:24", "00:13:1B", "00:14:51", "00:16:CB", 
        "00:17:F2", "00:19:E3", "00:1B:63", "00:1D:4F", "00:1E:52", 
        "00:1E:C2", "00:1F:5B", "00:1F:F3", "00:21:E9", "00:22:41", 
        "00:23:12", "00:23:32", "00:23:6C", "00:23:DF", "00:24:36", 
        "00:25:00", "00:25:4B", "00:25:BC", "00:26:08", "00:26:4A", 
        "00:26:B0", "00:26:BB", "00:30:65", "00:3E:E1", "00:50:E4", 
        "00:56:CD", "00:61:71", "00:6D:52", "00:C6:10", "00:D5:38", 
        "04:0C:CE", "04:15:52", "04:1E:64", "04:26:65", "04:48:9A", 
        "04:4B:ED", "04:52:F3", "04:54:53", "04:69:F8", "04:D3:CF", 
        "04:DB:56", "04:E5:36", "04:F1:3E", "04:F7:E4", "08:66:98", 
        "08:6D:41", "08:70:45", "08:74:02", "08:F4:AB", "0C:15:39", 
        "0C:30:21", "0C:3E:9F", "0C:4D:E9", "0C:51:01", "0C:74:C2", 
        "0C:77:1A", "0C:BC:9F", "0C:D7:4E", "10:1C:0C", "10:40:F3", 
        "10:41:7F", "10:93:E9", "10:9A:DD", "10:DD:B1", "18:34:51", 
        "18:65:90", "18:81:0E", "18:9E:FC", "18:AF:61", "18:E7:F4", 
        "18:EE:69", "1C:36:BB", "1C:5C:F2", "1C:91:48", "1C:9E:46", 
        "1C:AB:A7", "1C:E6:2B", "20:78:F0", "20:7D:74", "20:A2:E4", 
        "20:AB:37", "20:C9:D0", "24:1E:EB", "24:24:0E", "24:5B:A7", 
        "24:A0:74", "24:A2:E1", "24:AB:81", "24:E3:14", "24:F0:94", 
        "24:F5:A2", "28:37:37", "28:5A:EB", "28:6A:B8", "28:6A:BA", 
        "28:CF:DA", "28:CF:E9", "28:E0:2C", "28:E1:4C", "28:E7:CF", 
        "28:F0:76", "2C:1F:23", "2C:20:0B", "2C:33:61", "2C:AB:00", 
        "2C:B4:3A", "2C:BE:08", "2C:F0:A2", "2C:F0:EE", "30:10:E4", 
        "30:35:AD", "30:63:6B", "30:90:AB", "30:D9:D9", "30:F7:C5", 
        "34:08:BC", "34:12:98", "34:15:9E", "34:36:3B", "34:51:C9", 
        "34:A3:95", "34:AB:37", "34:C0:59", "34:E2:FD", "38:0F:4A", 
        "38:48:4C", "38:66:F0", "38:71:DE", "38:B5:4D", "38:C9:86", 
        "38:CA:DA", "3C:07:54", "3C:15:C2", "3C:2E:F9", "3C:2E:FF", 
        "3C:AB:8E", "3C:D0:F8", "3C:E0:72", "40:30:04", "40:33:1A", 
        "40:3C:FC", "40:4D:7F", "40:6C:8F", "40:98:AD", "40:A6:D9", 
        "40:B3:95", "40:D3:2D", "40:E2:30", "44:00:10", "44:2A:60", 
        "44:4C:0C", "44:2A:60", "44:4C:0C", "44:D1:FA", "44:FB:42"
    ],
    "Samsung": [
       "00:00:F0", "00:07:AB", "00:0D:AE", "00:12:47", "00:12:FB", 
        "00:13:77", "00:15:99", "00:15:B9", "00:16:32", "00:16:6B", 
        "00:16:DB", "00:17:C9", "00:17:D5", "00:18:AF", "00:1A:8A", 
        "00:1B:98", "00:1C:43", "00:1D:25", "00:1D:F6", "00:1E:7D", 
        "00:1F:CC", "00:1F:CD", "00:21:19", "00:21:4C", "00:21:D1", 
        "00:21:D2", "00:23:39", "00:23:3A", "00:23:99", "00:23:C2", 
        "00:23:D6", "00:23:D7", "00:24:54", "00:24:90", "00:24:91", 
        "00:24:E9", "00:25:38", "00:25:66", "00:25:67", "00:26:37", 
        "00:26:5D", "00:26:5F", "00:E0:64", "00:E3:B2", "04:18:0F", 
        "04:1B:BA", "04:FE:31", "08:08:C2", "08:21:EF", "08:37:3D", 
        "08:3D:88", "08:78:08", "08:8C:2C", "08:C6:B3", "08:EE:8B", 
        "08:FC:88", "08:FD:0E", "0C:14:20", "0C:71:5D", "0C:89:10", 
        "0C:A8:A7", "0C:B3:19", "0C:DF:A4", "10:0B:A9", "10:1D:C0", 
        "10:30:47", "10:3B:59", "10:77:B1", "10:D3:8A", "10:D5:42", 
        "14:1F:78", "14:32:D1", "14:49:E0", "14:56:8E", "14:5A:05", 
        "14:89:FD", "14:96:E5", "14:9F:3C", "14:A3:64", "14:BB:6E", 
        "14:F4:2A", "18:16:C9", "18:1E:B0", "18:21:95", "18:22:7E", 
        "18:26:66", "18:3A:2D", "18:3F:47", "18:46:17", "18:67:B0", 
        "18:83:31", "18:89:5B", "18:E2:C2", "1C:23:2C", "1C:3A:DE", 
        "1C:5A:3E", "1C:62:B8", "1C:66:AA", "1C:AF:05", "20:13:E0", 
        "20:2D:07", "20:55:31", "20:5D:47", "20:64:32", "20:6E:9C", 
        "20:D3:90", "20:D5:BF", "20:DB:AB", "24:4B:03", "24:4B:81", 
        "24:92:0E", "24:C6:96", "24:DB:AC", "24:DB:ED", "24:F5:AA", 
        "28:27:BF", "28:39:5E", "28:83:35", "28:98:7B", "28:BA:B5", 
        "28:CC:01", "28:D1:AF", "2C:0E:3D", "2C:44:01", "2C:AE:2B", 
        "2C:BA:BA", "30:07:4D", "30:19:66", "30:CD:A7", "30:D6:C9", 
        "30:F7:72", "34:14:5F", "34:23:BA", "34:2D:0D", "34:31:11", 
        "34:8A:7B", "34:AA:8B", "34:BE:00", "34:C3:AC", "38:01:95", 
        "38:0A:94", "38:0B:40", "38:16:D1", "38:2D:D1", "38:2D:E8", 
        "38:94:96", "38:94:ED", "38:AA:3C", "38:D4:0B", "38:EC:E4", 
        "3C:05:18", "3C:0E:23", "3C:5A:37", "3C:62:00", "3C:8B:FE", 
        "3C:A1:0D", "3C:BB:FD", "3C:F7:A4", "40:0E:85", "40:16:3B", 
        "40:D3:AE", "44:4E:1A", "44:6D:6C", "44:78:3E", "44:8F:17", 
        "44:F4:59", "48:13:7E", "48:27:EA", "48:44:F7", "48:49:C7", 
        "48:5A:3F", "48:C7:96", "4C:3C:16", "4C:A5:6D", "4C:BC:A5", 
        "4C:DD:31", "50:01:BB", "50:32:75", "50:3D:A1", "50:77:05", 
        "50:85:69", "50:92:B9", "50:9E:A7", "50:A4:C8", "50:B7:C3", 
        "50:C8:E5", "50:CC:F8", "50:F0:D3", "50:FC:9F", "54:40:AD", 
        "54:88:0E", "54:92:BE", "54:9B:12", "54:BD:79", "54:F2:01", 
        "54:FA:3E", "58:B1:0F", "58:C3:8B", "58:C5:CB", "5C:0A:5B", 
        "5C:2E:59", "5C:49:7D", "5C:51:81", "5C:51:88", "5C:96:9D", 
        "5C:99:60", "5C:A3:9D", "5C:B5:24", "5C:E8:EB", "5C:F6:DC", 
        "60:6B:BD", "60:77:71", "60:8F:5C", "60:A1:0A", "60:A4:D0", 
        "60:AF:6D", "60:C5:AD", "60:D0:A9", "60:F1:89", "60:F4:94", 
        "64:1C:AE", "64:6C:B2", "64:77:91", "64:B3:10", "64:B8:53"
    ],
    "AMD": [
        "00:0C:87", "00:1A:80", "00:11:18", "00:1A:67", "00:0F:20",
        "00:13:F6", "00:14:04", "00:0B:F0", "00:14:04", "00:1A:67",
        "18:A9:05", "18:9C:5D", "74:D0:2B", "7C:E0:5E", "BC:12:66",
        "BC:EE:7B", "C0:CB:38"
    ],
    "Nvidia": [
        "00:00:F4", "00:D3:E0", "00:03:01", "00:07:67", "00:08:78",
        "00:60:C0", "04:4B:80", "00:16:B2", "00:F3:F4", "00:4A:77",
        "00:AA:BB", "00:AB:B1", "00:AB:B2", "04:4B:80", "90:49:87",
        "D0:6F:3B", "FA:2F:67", "FC:D8:48", "EC:0E:C4", "F4:8C:50"
    ],
    "Dell": [
        "00:01:44", "00:06:5B", "00:08:74", "00:0B:DB", "00:0D:56",
        "00:0F:1F", "00:11:43", "00:12:3F", "00:13:72", "00:14:22",
        "00:15:C5", "00:16:F0", "00:18:8B", "00:19:B9", "00:1A:A0",
        "00:1C:23", "00:1D:09", "00:1E:4F", "00:1E:C9", "00:21:70",
        "00:21:9B", "00:22:19", "00:23:AE", "00:24:E8", "00:25:BD",
        "00:26:B9", "00:B0:D0", "08:00:20", "10:7D:1A", "14:B3:1F",
        "14:FE:B5", "18:03:73", "18:A9:9B", "24:B6:FD", "28:F1:0E",
        "34:17:EB", "40:5C:FD", "44:A8:42", "48:4D:7E", "50:9A:4C",
        "54:48:10", "54:9F:35", "5C:F9:DD", "64:00:6A", "74:86:7A",
        "78:2B:CB", "78:45:C4", "84:2B:2B", "8C:EC:4B", "A4:BA:DB",
        "B0:83:FE", "B4:E1:0F", "BC:30:5B", "C8:1F:66", "D0:67:E5",
        "D4:AE:52", "D4:BE:D9", "E0:DB:55", "F0:1F:AF", "F4:8E:38",
        "F8:BC:12", "F8:CA:B8", "F8:DB:88", "FC:15:B4"
    ],
    "Asus": [
        "00:0C:6E", "00:0E:A6", "00:11:2F", "00:11:D8", "00:13:D4",
        "00:15:F2", "00:17:31", "00:18:F3", "00:1B:FC", "00:1E:8C",
        "00:22:15", "00:23:54", "00:24:8C", "00:26:18", "08:60:6E",
        "10:BF:48", "10:C3:7B", "14:DA:E9", "14:EB:33", "1C:87:2C",
        "20:CF:30", "2C:4D:54", "30:5A:3A", "30:85:A9", "38:2C:4A",
        "38:D5:47", "40:16:7E", "48:5B:39", "50:46:5D", "54:04:A6",
        "58:11:22", "5C:AC:4C", "60:A4:4C", "60:F4:45", "70:4D:7B",
        "70:8B:CD", "74:D0:2B", "88:D7:F6", "90:E6:BA", "AC:22:0B",
        "AC:9E:17", "BC:AE:C5", "C8:60:00", "D0:17:C2", "D8:50:E6",
        "E0:3F:49", "E0:CB:4E", "F4:6D:04", "F8:0F:41", "FC:C2:3D"
    ],
    "Microsoft": [
        "00:03:FF", "00:12:5A", "00:15:5D", "00:17:FA", "00:1D:D8",
        "00:22:48", "00:25:AE", "00:50:F2", "28:18:78", "30:59:B7",
        "3C:83:75", "48:50:73", "4C:0B:BE", "50:1A:C5", "58:82:A8"
    ],
    "HP": [
        "00:01:E6", "00:01:E7", "00:02:A5", "00:04:EA", "00:08:02", 
        "00:08:83", "00:0B:CD", "00:0D:93", "00:0E:7F", "00:0E:B3", 
        "00:0F:20", "00:0F:61", "00:10:83", "00:10:E3", "00:11:0A"
    ],
    "TP-Link": [
        "00:19:E0", "00:1D:0F", "00:21:27", "00:23:CD", "00:25:86", 
        "00:27:19", "14:CC:20", "14:E6:E4", "14:CF:E2", "18:A6:F7", 
        "18:D6:C7", "1C:3B:F3", "1C:FA:68", "20:DC:E6", "24:69:68"
    ],
    "Razer": [
        "00:00:00", "18:65:90", "20:18:05", "2C:B4:3A", "3C:A3:15", 
        "6C:29:95", "7C:3A:5D", "94:9F:3E", "9C:1F:DD", "A0:EB:AA", 
        "AC:42:28", "C8:89:11", "F0:79:59", "F8:0F:41", "F8:FF:C2"
    ]
}

def banner():
    print(f"""
    {Fore.CYAN}┌─────────────────────────────────────────────┐
    {Fore.CYAN}│             {Fore.RED}MAC GHOST PRO 3.0{Fore.CYAN}             │
    {Fore.CYAN}│              {Fore.GREEN}0xabcd Özel Tool{Fore.CYAN}              │
    {Fore.CYAN}│  {Fore.WHITE}Üretici MAC + Ethernet Seçimi + Ctrl+K{Fore.CYAN}   │
    {Fore.CYAN}└─────────────────────────────────────────────┘
    """)

def check_root():
    if os.geteuid() != 0:
        print(f"{Fore.RED}[-] Bu tool root yetkisi gerektirir!")
        print(f"{Fore.YELLOW}[*] 'sudo python3 mac_ghost_pro.py' komutu ile çalıştırın")
        sys.exit(1)

def get_interfaces():
    """Mevcut ağ arayüzlerini tespit et"""
    interfaces = []
    try:
        # ifconfig çıktısını al
        ifconfig_output = subprocess.check_output(["ifconfig"], text=True)
        # Regex ile arayüzleri bul
        interfaces = re.findall(r'^(\w+):', ifconfig_output, re.MULTILINE)
        return interfaces
    except subprocess.SubprocessError:
        print(f"{Fore.RED}[-] Ağ arayüzleri listelenirken hata oluştu!")
        return []

def validate_mac(mac):
    """MAC adresi formatını doğrula"""
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    if re.match(pattern, mac):
        return True
    return False

def get_current_mac(interface):
    """Mevcut MAC adresini al"""
    try:
        ifconfig_output = subprocess.check_output(["ifconfig", interface], text=True)
        mac_search = re.search(r'ether\s+(\S+)', ifconfig_output)
        
        if mac_search:
            return mac_search.group(1)
        else:
            return None
    except subprocess.SubprocessError:
        return None

def change_mac(interface, new_mac):
    """MAC adresini değiştir"""
    print(f"{Fore.YELLOW}[*] {interface} arayüzü için MAC adresini değiştirme: {new_mac}")
    
    try:
        # İlk önce arayüzü devre dışı bırak
        subprocess.check_output(["ifconfig", interface, "down"])
        
        # MAC adresini değiştir
        subprocess.check_output(["ifconfig", interface, "hw", "ether", new_mac])
        
        # Arayüzü tekrar etkinleştir
        subprocess.check_output(["ifconfig", interface, "up"])
        
        return True
    except subprocess.SubprocessError as e:
        print(f"{Fore.RED}[-] MAC adresi değiştirilirken hata: {e}")
        return False

def restore_original_mac():
    """Orijinal MAC adresine geri dön"""
    global restore_in_progress, original_mac, selected_interface
    
    if restore_in_progress or not original_mac or not selected_interface:
        return
    
    restore_in_progress = True
    print("\n" + "="*50)
    print(f"{Fore.RED}[!] CTRL+K algılandı! Orijinal MAC adresine dönülüyor...")
    
    if change_mac(selected_interface, original_mac):
        current_mac = get_current_mac(selected_interface)
        if current_mac == original_mac:
            print(f"{Fore.GREEN}[+] Başarıyla orijinal MAC adresine dönüldü: {original_mac}")
        else:
            print(f"{Fore.RED}[-] Orijinal MAC adresine dönüş başarısız! Mevcut MAC: {current_mac}")
    
    print("="*50)
    restore_in_progress = False

def handle_keyboard():
    """Ctrl+K tuş kombinasyonunu dinle"""
    keyboard.add_hotkey('ctrl+k', restore_original_mac)
    keyboard.wait()

def generate_full_mac(oui):
    """OUI'dan tam bir MAC adresi oluştur"""
    # Son 3 okteti rastgele oluştur
    random_hex = [format(random.randint(0, 255), '02x') for _ in range(3)]
    # OUI + rastgele oluşturulan son 3 oktet
    full_mac = f"{oui}:{':'.join(random_hex)}"
    return full_mac

def show_manufacturers():
    """Tüm üreticileri göster"""
    print(f"\n{Fore.CYAN}[+] MAC adresi üreticileri:")
    for i, manufacturer in enumerate(MANUFACTURER_OUIS.keys(), 1):
        print(f"{Fore.WHITE}    {i}. {manufacturer}")

def select_manufacturer():
    """Kullanıcıdan üretici seçmesini iste"""
    manufacturers = list(MANUFACTURER_OUIS.keys())
    
    show_manufacturers()
    
    while True:
        try:
            choice = int(input(f"\n{Fore.YELLOW}[?] Üretici numarasını seçin: "))
            if 1 <= choice <= len(manufacturers):
                selected_manufacturer = manufacturers[choice-1]
                return selected_manufacturer
            else:
                print(f"{Fore.RED}[-] Geçersiz seçim! Lütfen listedeki bir numarayı girin.")
        except ValueError:
            print(f"{Fore.RED}[-] Lütfen bir sayı girin!")

def show_manufacturer_ouis(manufacturer):
    """Seçilen üreticinin OUI'larını göster"""
    ouis = MANUFACTURER_OUIS[manufacturer]
    print(f"\n{Fore.GREEN}[+] {manufacturer} üreticisinin OUI (ilk 3 oktet) listesi:")
    
    # OUI listesini 5'li gruplar halinde yazdır
    for i in range(0, len(ouis), 5):
        group = ouis[i:i+5]
        print(f"{Fore.WHITE}    {', '.join(group)}")
    
    # Örnek tam MAC adresleri oluştur
    print(f"\n{Fore.CYAN}[+] {manufacturer} için örnek MAC adresleri:")
    for _ in range(3):
        random_oui = random.choice(ouis)
        full_mac = generate_full_mac(random_oui)
        print(f"{Fore.WHITE}    {full_mac}")

def main():
    global original_mac, selected_interface
    
    banner()
    check_root()
    
    # Mevcut ağ arayüzlerini al
    interfaces = get_interfaces()
    
    if not interfaces:
        print(f"{Fore.RED}[-] Hiçbir ağ arayüzü bulunamadı!")
        sys.exit(1)
    
    # Arayüzleri kategorize et
    eth_interfaces = [iface for iface in interfaces if iface.startswith('e')]
    wlan_interfaces = [iface for iface in interfaces if iface.startswith('w')]
    lo_interfaces = [iface for iface in interfaces if iface == 'lo']
    other_interfaces = [iface for iface in interfaces if not (iface in eth_interfaces or iface in wlan_interfaces or iface in lo_interfaces)]
    
    # Kategorileri göster
    print(f"\n{Fore.CYAN}[+] Mevcut ağ arayüzleri:")
    
    if eth_interfaces:
        print(f"{Fore.GREEN}    Ethernet Arayüzleri:")
        for i, iface in enumerate(eth_interfaces, 1):
            print(f"{Fore.WHITE}    {i}. {iface}")
    
    if wlan_interfaces:
        print(f"{Fore.GREEN}    Kablosuz Arayüzleri:")
        for i, iface in enumerate(wlan_interfaces, 1):
            print(f"{Fore.WHITE}    {len(eth_interfaces) + i}. {iface}")
    
    if lo_interfaces:
        print(f"{Fore.GREEN}    Loopback Arayüzleri:")
        for i, iface in enumerate(lo_interfaces, 1):
            print(f"{Fore.WHITE}    {len(eth_interfaces) + len(wlan_interfaces) + i}. {iface}")
    
    if other_interfaces:
        print(f"{Fore.GREEN}    Diğer Arayüzler:")
        for i, iface in enumerate(other_interfaces, 1):
            print(f"{Fore.WHITE}    {len(eth_interfaces) + len(wlan_interfaces) + len(lo_interfaces) + i}. {iface}")
    
    # Tüm arayüzleri tek listede birleştir
    all_interfaces = eth_interfaces + wlan_interfaces + lo_interfaces + other_interfaces
    
    # Arayüz seçimi
    while True:
        try:
            choice = int(input(f"\n{Fore.YELLOW}[?] Değiştirmek istediğiniz arayüzün numarasını girin: "))
            if 1 <= choice <= len(all_interfaces):
                selected_interface = all_interfaces[choice-1]
                
                # Seçilen arayüzün tipini kontrol et
                if selected_interface.startswith('w') and not eth_interfaces:
                    print(f"{Fore.YELLOW}[!] Kablosuz arayüz seçtiniz. Ağınız kablosuz olabilir.")
                elif selected_interface == 'lo':
                    print(f"{Fore.YELLOW}[!] Loopback arayüzü seçtiniz. Bu genellikle önerilmez.")
                
                break
            else:
                print(f"{Fore.RED}[-] Geçersiz seçim! Lütfen listedeki bir numarayı girin.")
        except ValueError:
            print(f"{Fore.RED}[-] Lütfen bir sayı girin!")
    
    # Mevcut MAC adresini kaydet
    original_mac = get_current_mac(selected_interface)
    if original_mac:
        print(f"{Fore.GREEN}[+] {selected_interface} arayüzünün orijinal MAC adresi: {original_mac}")
    else:
        print(f"{Fore.RED}[-] {selected_interface} arayüzünün MAC adresi alınamadı!")
        print(f"{Fore.RED}[-] Bu arayüz MAC değiştirmeyi desteklemiyor olabilir.")
        sys.exit(1)
    
    # Klavye dinleyicisini başlat
    keyboard_thread = threading.Thread(target=handle_keyboard, daemon=True)
    keyboard_thread.start()
    
    print(f"\n{Fore.CYAN}[*] Not: İstediğiniz zaman {Fore.RED}[CTRL+K]{Fore.CYAN} tuşlarına basarak orijinal MAC adresine dönebilirsiniz.")
    
    # Üretici seçimi
    selected_manufacturer = select_manufacturer()
    print(f"{Fore.GREEN}[+] Seçilen üretici: {selected_manufacturer}")
    
    # Seçilen üreticinin OUI'larını göster
    show_manufacturer_ouis(selected_manufacturer)
    
    # Kullanıcıdan MAC adresi al
    print(f"\n{Fore.YELLOW}[?] Yeni MAC adresini girin (örn: {random.choice(MANUFACTURER_OUIS[selected_manufacturer])}:XX:XX:XX):")
    while True:
        new_mac = input(f"{Fore.WHITE}>>> ")
        
        if validate_mac(new_mac):
            # MAC'in ilk 3 okteti üreticiye ait mi kontrol et
            oui = new_mac.split(':', 3)[0] + ':' + new_mac.split(':', 3)[1] + ':' + new_mac.split(':', 3)[2]
            if oui in MANUFACTURER_OUIS[selected_manufacturer]:
                break
            else:
                print(f"{Fore.RED}[-] Girdiğiniz MAC adresi {selected_manufacturer} üreticisine ait değil!")
                print(f"{Fore.YELLOW}[*] Lütfen şu OUI'lardan birini kullanın: {', '.join(MANUFACTURER_OUIS[selected_manufacturer][:3])}...")
                print(f"{Fore.YELLOW}[?] MAC adresini tekrar girin veya rasgele {selected_manufacturer} MAC adresi için 'R' yazın:")
        elif new_mac.upper() == 'R':
            # Rasgele bir MAC adresi oluştur
            random_oui = random.choice(MANUFACTURER_OUIS[selected_manufacturer])
            new_mac = generate_full_mac(random_oui)
            print(f"{Fore.YELLOW}[*] Rasgele MAC adresi oluşturuldu: {new_mac}")
            break
        else:
            print(f"{Fore.RED}[-] Geçersiz MAC adresi formatı! Doğru format: XX:XX:XX:XX:XX:XX")
            print(f"{Fore.YELLOW}[?] MAC adresini tekrar girin veya rasgele {selected_manufacturer} MAC adresi için 'R' yazın:")
    
    # MAC adresini değiştir
    if change_mac(selected_interface, new_mac):
        # Değişikliği doğrula
        new_current_mac = get_current_mac(selected_interface)
        if new_current_mac == new_mac:
            print(f"{Fore.GREEN}[+] MAC adresi başarıyla değiştirildi: {new_current_mac}")
        else:
            print(f"{Fore.RED}[-] MAC adresi değiştirilemedi! Mevcut MAC: {new_current_mac}")
    else:
        print(f"{Fore.RED}[-] MAC adresi değiştirme işlemi başarısız oldu!")
    
    print(f"\n{Fore.CYAN}[*] Tool çalışmaya devam ediyor. {Fore.RED}CTRL+K{Fore.CYAN} kombinasyonu ile orijinal MAC'e dönebilirsiniz.")
    print(f"{Fore.CYAN}[*] Çıkmak için {Fore.RED}CTRL+C{Fore.CYAN} tuşlarına basın.")
    
    try:
        # Ana thread'i açık tut
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[*] Program sonlandırılıyor...")
        sys.exit(0)

if __name__ == "__main__":
    main()
