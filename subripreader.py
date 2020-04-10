import re


MAX_GROUPS_TO_READ = 100
MAX_TIME_TO_READ_IN_MILLISECONDS = 300000
INPUT_FILE_PATH = 'input1.srt'


def main():
    process_file(INPUT_FILE_PATH)


def process_file(input_file_path):
    subtitle_input_file = open_input_file(input_file_path)
    time_array = load_input_file(subtitle_input_file)
    close_input_file(subtitle_input_file)
    return time_array


def open_input_file(input_file_path):
    subtitle_input_file = open(input_file_path, 'r', errors='replace')
    return subtitle_input_file


def load_input_file(subtitle_input_file):
    start_end_times_list = get_start_end_times(subtitle_input_file)
    time_array = create_time_array(start_end_times_list)
    return time_array


def get_start_end_times(subtitle_input_file):
    start_end_times_list = []
    current_start_time_ms = 0
    current_end_time_ms = 0
    group_counter = 0
    for line in subtitle_input_file:
        if is_a_time_line(line) and group_counter < MAX_GROUPS_TO_READ:
            (current_start_time_ms, current_end_time_ms) = get_times(line)
            if current_start_time_ms < MAX_TIME_TO_READ_IN_MILLISECONDS:
                start_end_times_list.append((current_start_time_ms, current_end_time_ms))
                group_counter += 1
            else:
                break            
    return start_end_times_list


def create_time_array(start_end_times_list):
    time_array = [.0] * int(MAX_TIME_TO_READ_IN_MILLISECONDS / 1000)
    for time_pair in start_end_times_list:
        start_time = time_pair[0]
        end_time = time_pair[1]
        initial_affected_index = int(start_time / 1000)
        last_affected_index = int(end_time / 1000)
        for index in range(initial_affected_index, last_affected_index + 1):
            if index != initial_affected_index and index != last_affected_index:
                time_array[index] += 1
            elif index == initial_affected_index and index != last_affected_index:
                time_array[index] += ((index + 1) * 1000 - start_time) / 1000
            elif index != initial_affected_index and index == last_affected_index:
                time_array[index] += (end_time - index * 1000) / 1000
            else:
                time_array[index] += (end_time - start_time) / 1000
    return time_array

def is_a_time_line(line):
    matches = re.search('\d\d:\d\d:\d\d.+\s-->\s\d\d:\d\d:\d\d', line)
    line_is_time_line = matches is not None
    return line_is_time_line


def get_times(line):
    start_time_milliseconds = 0
    end_time_milliseconds = 0
    matches = re.findall('\d\d:|\d\d,\d{1,4}', line)
    start_hour = int(matches[0][:2])
    start_minute = int(matches[1][:2])
    start_second = float(matches[2].replace(',', '.'))
    end_hour = int(matches[3][:2])
    end_minute = int(matches[4][:2])
    end_second = float(matches[5].replace(',', '.'))
    start_time_milliseconds = int(start_second * 1000 + start_minute * 60000 + start_hour * 3600000)
    end_time_milliseconds = int(end_second * 1000 + end_minute * 60000 + end_hour * 3600000)
    return(start_time_milliseconds, end_time_milliseconds)
    

def close_input_file(subtitle_input_file):
    subtitle_input_file.close()


if __name__ == '__main__':
    main()
