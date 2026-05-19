BLOCKED_COMMANDS = [
    "rm -rf",
    "rm -f",
    "mkfs",
    "dd if",
    "shutdown",
    "reboot",
    "> /dev/sda",
    "chmod 777",
    "curl | bash",
    "wget | bash",
]

def is_safe(command):
    for blocked in BLOCKED_COMMANDS:
        if blocked in command:
            print(f"BLOCKED: '{command}' contains dangerous pattern '{blocked}'")
            return False
    return True