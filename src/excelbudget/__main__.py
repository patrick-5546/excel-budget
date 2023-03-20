from excelbudget.configure import post_state_configuration, pre_state_configuration
from excelbudget.run import run
from excelbudget.state import setup_state


def main():
    "Entry point for the application script."
    pre_config = pre_state_configuration()
    state = setup_state(pre_config)
    post_state_configuration(state)
    run(state)


if __name__ == "__main__":
    main()
