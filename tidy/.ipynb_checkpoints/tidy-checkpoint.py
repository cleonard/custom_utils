"""Shim for htmltidy binary

Method:

- Create a temp file and write html to it
- Run subprocess to call htmltidy modifying file in place
- Read file and return tidy markup
"""

import os
import re
import shlex
import subprocess

# Get working dir (location of this module) and process ID
# for creating temp file names
cwd = re.search(r"^.+/", __file__).group()
pid = os.getpid()


def tidy(html):
    """Standard tidying"""
    cmd = "tidy -m {}"
    markup = _run(cmd, html)
    return markup


def pretty(html):
    """Pretty-printed tidying with indention"""
    config = os.path.join(cwd, "pretty.config")
    cmd = " ".join(["tidy", "-config", config, "-m", "{}"])
    markup = _run(cmd, html)
    return markup


def compressed(html):
    """Compressed tidying minimizing whitespace"""
    cmd = "tidy -m {}"
    markup = _run(cmd, html)
    markup = re.sub(r"\n", "", markup)
    markup = re.sub(r" +", " ", markup)
    return markup


def _run(cmd, html):
    """Base method to run htmltidy"""

    # Create temp file
    temp_file_name = f"_tmp_{pid}.txt"
    temp_file = os.path.join(cwd, temp_file_name)

    # Write html to temp file
    with open(temp_file, "w") as tf:
        tf.write(html)

    # Format cmd with temp_file and run
    args = shlex.split(cmd.format(temp_file))
    run = subprocess.run(args)

    # Read html from temp_file
    with open(temp_file) as tf:
        markup = tf.read()

    # Delete temp_file
    os.remove(temp_file)

    return markup


def tidy_help():
    """Return this module's help text"""
    help_file = os.path.join(cwd, "tidy_help.txt")
    with open(help_file) as hf:
        help_text = hf.read()
    return help_text