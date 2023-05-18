import sys
import subprocess

def print_help():
    print("Usage:")
    print("  create <snapshot-name>")
    print("  remove <snapshot-name> | all")
    print("  list")
    print("  roll <snapshot-name>")
    print("  logrotate")

def create_snapshot(snapshot_name):
    zfs_command = f"zfs snapshot sa_pool/data@{snapshot_name}"
    subprocess.run(["sudo", "zsh", "-c", zfs_command])

def remove_snapshot(snapshot_name):
    if snapshot_name == "all":
        zfs_command = "zfs list -H -o name -t snapshot | xargs -I {} sudo zfs destroy {}"
    else:
        zfs_command = f"zfs destroy sa_pool/data@{snapshot_name}"
    subprocess.run(["sudo", "zsh", "-c", zfs_command])

def list_snapshots():
    zfs_command = "zfs list -H -o name -t snapshot"
    output = subprocess.check_output(["sudo", "zsh", "-c", zfs_command]).decode().strip()
    snapshots = output.split("\n")
    for snapshot in snapshots:
        print(snapshot.split("@")[1])

def rollback_snapshot(snapshot_name):
    zfs_command = f"zfs rollback -r sa_pool/data@{snapshot_name}"
    subprocess.run(["sudo", "zsh", "-c", zfs_command])

def logrotate_zfs():
    logrotate_command = "logrotate -f /etc/logrotate.d/fakelog"
    subprocess.run(["sudo", "zsh", "-c", logrotate_command])

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "help":
        print_help()
        return

    command = sys.argv[1]
    if command == "create":
        if len(sys.argv) < 3:
            print("Error: Please provide a snapshot name.")
            return
        snapshot_name = sys.argv[2]
        create_snapshot(snapshot_name)
    elif command == "remove":
        if len(sys.argv) < 3:
            print("Error: Please provide a snapshot name or 'all'.")
            return
        snapshot_name = sys.argv[2]
        remove_snapshot(snapshot_name)
    elif command == "list":
        list_snapshots()
    elif command == "roll":
        if len(sys.argv) < 3:
            print("Error: Please provide a snapshot name.")
            return
        snapshot_name = sys.argv[2]
        rollback_snapshot(snapshot_name)
    elif command == "logrotate":
        logrotate_zfs()
    else:
        print(f"Error: Unknown command '{command}'")

if __name__ == "__main__":
    main()
