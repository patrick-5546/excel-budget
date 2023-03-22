"""Xlbudget: a personal bookkeeping assistant."""

from .configure import configure_argument_parser, configure_logger


def main():
    "Entry point for the application script."
    parser = configure_argument_parser()
    args = parser.parse_args()
    configure_logger(args.log_level)

    cmd = args.init(args)
    cmd.run()
