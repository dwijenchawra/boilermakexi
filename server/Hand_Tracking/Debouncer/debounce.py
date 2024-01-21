import functools
import threading
import time

def debounce(delay, none_state=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Use nonlocal to modify the inner function's closure variable
            nonlocal last_returned_value, debounce_timer

            # Acquire the lock before accessing shared variables
            with lock:
                # If the timer is active and within the delay, return the last known state
                current_time = time.time()
                if debounce_timer is not None and (current_time - debounce_timer) < delay:
                    return last_returned_value

                # Call the actual function and store the result
                result = func(*args, **kwargs)
                last_returned_value = result

                # Set up the debounce timer
                debounce_timer = current_time

            return result

        # Initialize decorator-specific variables
        debounce_timer = None
        last_returned_value = None
        lock = threading.Lock()

        return wrapper

    return decorator
