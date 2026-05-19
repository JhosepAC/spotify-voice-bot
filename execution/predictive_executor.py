from execution.execution_guard import (
    ExecutionGuard
)

from execution.execution_state import (
    ExecutionState
)

from execution.command_confidence import (
    calculate_confidence
)

from commands.router import (
    route_command
)


class PredictiveExecutor:

    def __init__(self):

        self.guard = (
            ExecutionGuard()
        )

        self.state = (
            ExecutionState()
        )

    def try_execute(
        self,
        partial_text,
        intent,
        entities
    ):
        """
        Try predictive execution.
        """

        if self.state.executed:
            return None

        confidence = (
            calculate_confidence(

                partial_text,

                intent,

                entities
            )
        )

        can_execute = (
            self.guard.should_execute(
                confidence
            )
        )

        if not can_execute:
            return None

        response = route_command(
            intent,
            entities
        )

        self.state.mark_executed(
            partial_text
        )

        return response

    def reset(self):
        """
        Reset execution pipeline.
        """

        self.state.reset()