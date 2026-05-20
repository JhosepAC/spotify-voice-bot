class ExecutionGuard:

    def should_execute(
        self,
        confidence,
        threshold=0.75
    ):
        """
        Validate execution threshold.
        """

        return confidence >= threshold