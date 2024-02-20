from config import fps

def convert_to_time(indices):
    time_ranges = []
    start_index = indices[0]

    for i in range(1, len(indices)):
        if indices[i] != indices[i-1] + 1:
            end_index = indices[i-1]
            start_time = convert_index_to_time(start_index)
            end_time = convert_index_to_time(end_index)
            time_range = f"{start_time}~{end_time}"
            time_ranges.append(time_range)
            start_index = indices[i]

    # 처리되지 않은 마지막 구간 처리
    end_index = indices[-1]
    start_time = convert_index_to_time(start_index)
    end_time = convert_index_to_time(end_index)
    time_range = f"{start_time}~{end_time}"
    time_ranges.append(time_range)

    return time_ranges

def convert_index_to_time(index):
    total_seconds = index / fps
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"