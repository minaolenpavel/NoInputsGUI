import os
import subprocess
import pwd
import grp

app_dir = os.environ.get(
    "APPDIR",
    os.path.dirname(os.path.abspath(__file__))
)
def user_in_group(group_name: str) -> bool:
    user = pwd.getpwuid(os.getuid()).pw_name

    # check supplementary groups
    groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]

    # check primary group
    primary_gid = pwd.getpwnam(user).pw_gid
    primary_group = grp.getgrgid(primary_gid).gr_name

    return group_name in groups or group_name == primary_group

def is_installed() -> bool:
    binary_missing = not os.path.exists("/usr/bin/noinputs")
    rules_missing = not os.path.exists("/etc/udev/rules.d/99-noinputs.rules")
    not_in_group = not user_in_group("noinputs")

    if binary_missing or rules_missing or not_in_group:
        print("Installation is missing")
        return False
    else:
        return True
    
def install():
    subprocess.run([
        "pkexec",
        "sh",
        os.path.join(app_dir, "installer.sh"),
        app_dir
    ])