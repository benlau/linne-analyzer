def slidingWindow(data,sampling,frameSize):
    # Sliding Window Paratitioning on a data set of frames
    frames = []
    size = len(data)
    i = 0
    half = frameSize / 2
    for s in sampling:
        start = s - half
        start = max([start,0])
        end = s + half
        end = min([end,size])
        frames.append(data[start:end])
    return frames

def frange(start,stop,step):
    # Range with step of floating point type
    r = start
    while r < stop:
        yield int(r)
        r = r + step
