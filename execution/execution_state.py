class ExecutionState:

    def __init__(self):

        self.executed = False

        self.last_command = None

    def mark_executed(
        self,
        command
    ):
        """
        Mark command executed.
        """

        self.executed = True

        self.last_command = command

    def reset(self):
        """
        Reset execution state.
        """

        self.executed = False

        self.last_command = None