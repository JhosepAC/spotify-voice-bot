from execution.predictive_executor import (
    PredictiveExecutor
)


class ExecutionManager:

    def __init__(self):

        self.executor = (
            PredictiveExecutor()
        )

    def process_prediction(
        self,
        partial_text,
        prediction
    ):
        """
        Process realtime prediction.
        """

        if not prediction.intent:
            return None

        response = (
            self.executor.try_execute(

                partial_text,

                prediction.intent,

                prediction.entities
            )
        )

        return response

    def reset(self):
        """
        Reset execution manager.
        """

        self.executor.reset()