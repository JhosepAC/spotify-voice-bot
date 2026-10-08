"""Optional wake-word gate (disabled by default).

When WAKE_ENABLED=false (default) this module is a no-op passthrough:
wait_for_wake() returns True immediately and no new dependency is needed.

When enabled it tries openwakeword (`pip install openwakeword onnxruntime`).
Only stock-model keywords work out of the box (e.g. "alexa", "hey_jarvis");
a custom "hey spotify" model must be trained and placed where
WAKE_MODEL_PATHS points. Missing library or models degrade gracefully
to always-listening with a one-line warning.
"""

import time

from config.settings import WAKE_ENABLED, WAKE_KEYWORDS


def _stock_model_names() -> list[str]:
    try:
        from openwakeword import utils

        return [m.replace(".onnx", "") for m in utils.MODELS]
    except Exception:
        return []


def wait_for_wake(timeout: float | None = None) -> bool:
    """
    Block until a wake word is heard. Returns True when listening may start.

    Always returns True immediately when the gate is disabled or when
    the optional dependency/models are unavailable.
    """
    if not WAKE_ENABLED:
        return True

    try:
        from openwakeword.model import Model
    except Exception:
        print("[Wake] openwakeword not installed; listening without wake word.")
        return True

    wanted = [w.strip().lower().replace(" ", "_") for w in WAKE_KEYWORDS if w.strip()]
    stock = set(_stock_model_names())
    usable = [w for w in wanted if w in stock]
    if not usable:
        print(f"[Wake] No usable stock models for {wanted}; listening directly.")
        return True

    import numpy as np
    import sounddevice as sd
    from config.settings import AUDIO_SAMPLE_RATE

    model = Model(wakeword_models=usable)
    print(f"[Wake] Waiting for {usable} ...")
    start = time.perf_counter()
    try:
        with sd.InputStream(
            samplerate=AUDIO_SAMPLE_RATE, channels=1, dtype="int16", blocksize=1280
        ) as stream:
            while True:
                if timeout is not None and time.perf_counter() - start > timeout:
                    return False
                chunk, _ = stream.read(1280)
                scores = model.predict(np.asarray(chunk).flatten())
                if any(scores[w] > 0.5 for w in usable):
                    model.reset()
                    return True
    except Exception as e:
        print(f"[Wake] Mic error ({e}); listening directly.")
        return True
