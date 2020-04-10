import subripreader


def main():
    (time_array_a, time_array_b) = calculate_time_arrays('input1.srt', 'input2.srt')
    (delays, matching_factors) = calculate_matching_factors_for_several_delays(time_array_a, time_array_b)
    best_case_index = search_best_case(delays, matching_factors)
    delay_estimation_in_milliseconds = estimate_delay_in_milliseconds(delays, matching_factors, best_case_index)
    print('Subtitle is delayed', delay_estimation_in_milliseconds, 'ms from the reference.')
    
        
def calculate_time_arrays(reference_file_path, delayed_file_path):
    time_array_a = subripreader.process_file(reference_file_path)
    time_array_b = subripreader.process_file(delayed_file_path)
    return (time_array_a, time_array_b)
    

def calculate_matching_factors_for_several_delays(time_array_a, time_array_b):
    delays = []
    matching_factors = []
    for current_delay_seconds in range (int(len(time_array_a) / -2), int(len(time_array_a) / 2)):
        current_matching_factor = calculate_matching_factor(time_array_a, time_array_b, current_delay_seconds)
        delays.append(current_delay_seconds)
        matching_factors.append(current_matching_factor)
    return (delays, matching_factors)


def calculate_matching_factor(time_array_a, time_array_b, delay_seconds: int):
    matching_factor = .0
    for index in range (0, len(time_array_a) - abs(delay_seconds)):
        if delay_seconds >= 0:
            matching_factor += 1 - abs(time_array_a[index] - time_array_b[index + delay_seconds])
        else:
            matching_factor += 1 - abs(time_array_a[index - delay_seconds] - time_array_b[index])
    matching_factor = matching_factor / (len(time_array_a) - delay_seconds)
    return matching_factor


def search_best_case(delays, matching_factors):
    best_case_index = 0
    best_matching_factor = .0
    for current_index in range (0, len(delays)):
        if matching_factors[current_index] > best_matching_factor:
            best_matching_factor = matching_factors[current_index]
            best_case_index = current_index
    return best_case_index


def estimate_delay_in_milliseconds(delays, matching_factors, best_case_index):
    calculated_delay_in_milliseconds = delays[best_case_index] * 1000    
    if best_case_index != 0 and best_case_index != len(delays):
        left_neighbor_matching_factor = matching_factors[best_case_index - 1]
        right_neighbor_matching_factor = matching_factors[best_case_index + 1]
        calculated_delay_compensation = (right_neighbor_matching_factor - left_neighbor_matching_factor) / 2
        calculated_delay_in_milliseconds += calculated_delay_compensation * 1000
    return int(calculated_delay_in_milliseconds)


if __name__ == '__main__':
    main()
