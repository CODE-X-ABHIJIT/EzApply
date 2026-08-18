import subprocess


def run(command, input_text=None):

    subprocess.run(
        command,
        input=input_text,
        text=True,
        check=True,
    )


# ------------------------------------------------------------
# Scan all LinkedIn posts
# ------------------------------------------------------------

run(
    [
        "python",
        "-m",
        "outreach",
        "scan",
    ]
)


# ------------------------------------------------------------
# Show jobs found
# ------------------------------------------------------------

run(
    [
        "python",
        "-m",
        "outreach",
        "list",
    ]
)


# ------------------------------------------------------------
# Automatically approve and send
# ------------------------------------------------------------

run(
    [
        "python",
        "-m",
        "outreach",
        "approve",
    ],
    input_text="y\n",
)