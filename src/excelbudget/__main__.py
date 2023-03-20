"testing."

from excelbudget.configure import post_setup_configuration, pre_setup_configuration
from excelbudget.state import setup_state


def main():
    "Entry point for the application script."
    pre_config = pre_setup_configuration()
    state = setup_state(pre_config)
    post_setup_configuration(state)


if __name__ == "__main__":
    main()
