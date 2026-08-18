import subprocess
import sys


def run(command, input_text=None):
    subprocess.run(
        [sys.executable, "-m", "outreach", command],
        input=input_text,
        text=True,
        check=True,
    )


def main():
    # Scan LinkedIn posts
    run("scan")

    # Show pending jobs
    run("list")

    # Automatically approve and send all eligible emails
    run("approve", input_text="y\n")


if __name__ == "__main__":
    main()