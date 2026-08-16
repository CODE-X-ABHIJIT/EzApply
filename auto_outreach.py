import subprocess


subprocess.run(
    ["python", "-m", "outreach", "scan"],
    check=True,
)

subprocess.run(
    ["python", "-m", "outreach", "list"],
    check=True,
)

subprocess.run(
    ["python", "-m", "outreach", "approve"],
    input="y\n",
    text=True,
    check=True,
)