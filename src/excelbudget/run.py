import logging

import excelbudget.commands.generate as generate
import excelbudget.commands.update as update
import excelbudget.commands.validate as validate
import excelbudget.state as state

logger = logging.getLogger(__name__)


def run(state: state.State) -> None:
    """Runs a command.

    Args:
        state (State): The state.

    Raises:
        ValueError: If an invalid command is received.
    """
    cmd_name = state.args.cmd
    if cmd_name == "generate":
        cmd_cls = generate.Generate
    elif cmd_name == "update":
        cmd_cls = update.Update
    elif cmd_name == "validate":
        cmd_cls = validate.Validate
    else:
        raise ValueError(f"{cmd_name} is not a valid command")

    logger.info(f"Running the {cmd_name} command")
    cmd = cmd_cls(state)
    cmd.run()
