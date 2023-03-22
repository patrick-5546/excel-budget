"""Xlbudget: a personal bookkeeping assistant."""

from .configure import setup


def main():
    "Entry point for the application script."
    args = setup()
    cmd = args.init(args)
    cmd.run()
