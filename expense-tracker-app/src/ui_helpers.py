import time, sys

# animated countdown
def animated_countdown(duration_seconds, message):
    spinner_symbols = ["⡿", "⣟", "⣯", "⣷", "⣾", "⣽", "⣻", "⢿"]
    start_time = time.monotonic()
    index = 0

    while True:
        elapsed = time.monotonic() - start_time
        remaining = max(0, int(duration_seconds - elapsed + 0.999))

        if remaining == 0:
            break

        symbol = spinner_symbols[index % len(spinner_symbols)]
        index += 1

        sys.stdout.write(f"\r{symbol} {message} ({remaining}s remaining)")
        sys.stdout.flush()

        time.sleep(0.1)

    # Clear the animation line
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()

    print("Try Again✓")