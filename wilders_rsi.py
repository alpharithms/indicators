def wilders_rsi(data: typing.List[float or int], window_length: int,
                use_rounding: bool = True) -> typing.List[typing.Any]:
    """
    A manual implementation of Wells Wilder's RSI calculation as outlined in
    his 1978 book "New Concepts in Technical Trading Systems" which makes
    use of the α-1 Wilder Smoothing Method of calculating the average
    gains and losses across trading periods.

    @author: https://github.com/alphazwest

    Args:
        data: List[float or int] - a collection of floating point values
        window_length: int-  the number of previous periods used for RSI calculation
        use_rounding: bool - option to round calculations to the nearest 2 decimal places
    Returns:
        A list object with len(data) + 1 members where the first is a header as such:
             ['date', 'close', 'gain', 'loss', 'avg_gain', 'avg_loss', 'rsi']
    """

    # Define a rounding function based on argument
    do_round = lambda x: round(x, 2) if use_rounding else x  # noqa: E731

    # Define containers
    gains: typing.List[float]       = []
    losses: typing.List[float]      = []
    window: typing.List[float]      = []

    # Define convenience variables
    prev_avg_gain: float or None    = None
    prev_avg_loss: float or None    = None

    # Define output container with header
    output: typing.List[typing.Any] = [
        ['date', 'close', 'gain', 'loss', 'avg_gain', 'avg_loss', 'rsi']
    ]
    for i, price in enumerate(data):

        # Skip first row but remember price
        if i == 0:
            window.append(price)
            output.append([i+1, price, 0, 0, 0, 0, 0])
            continue

        # Calculate price difference with previous period
        difference = do_round(wilder_data[i] - wilder_data[i - 1])

        # Record positive differences as gains, negative as losses
        if difference > 0:
            gain = difference
            loss = 0
        elif difference < 0:
            gain = 0
            loss = abs(difference)
        else:
            gain = 0
            loss = 0
        gains.append(gain)
        losses.append(loss)

        # Don't calculate averages until n-periods data available
        if i < window_length:
            window.append(price)
            output.append([i+1, price, gain, loss, 0, 0, 0])
            continue

        # Calculate Average for first gain as SMA
        if i == window_length:
            avg_gain = sum(gains) / len(gains)
            avg_loss = sum(losses) / len(losses)

        # Use WSM after initial window-length period
        else:
            avg_gain = (prev_avg_gain * (window_length - 1) + gain) / window_length
            avg_loss = (prev_avg_loss * (window_length - 1) + loss) / window_length

        # Round for precision
        avg_gain = do_round(avg_gain)
        avg_loss = do_round(avg_loss)

        # Keep in memory
        prev_avg_gain = avg_gain
        prev_avg_loss = avg_loss

        # Calculate RS
        rs = do_round(avg_gain / avg_loss)

        # Calculate RSI
        rsi = do_round(100 - (100 / (1 + rs)))

        # Remove oldest values
        window.append(price)
        window.pop(0)
        gains.pop(0)
        losses.pop(0)

        # Save Data
        output.append([i+1, price, gain, loss, avg_gain, avg_loss, rsi])

    return output
