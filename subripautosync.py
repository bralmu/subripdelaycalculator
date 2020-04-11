import sys
import os
import delaycalculator

def main():
    if len(sys.argv) != 4:
        print('Wrong number of arguments. Usage: subripautosync in_reference_file in_wrong_sync_file out_synced_file')
        exit()
    input_reference_file_path = str(sys.argv[1])
    input_wrong_sync_file_path = str(sys.argv[2])
    output_synced_file_path = str(sys.argv[3])
    delay_in_milliseconds = delaycalculator.calculate_delay(input_reference_file_path, input_wrong_sync_file_path)
    copy_wrong_to_output_command = 'cp ' + input_wrong_sync_file_path + ' ' + output_synced_file_path
    os.system(copy_wrong_to_output_command)
    shift_output_command = 'srt -i shift ' + str(delay_in_milliseconds) + 'ms ' + output_synced_file_path
    os.system(shift_output_command)


if __name__ == '__main__':
    main()
