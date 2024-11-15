import math
import struct
import requests

name = str("output_durations.bin")
tx = bool(1)


def decode_duration(code):

    duration = 0
    for char in code:
        if char == "f":
            duration += 4
        elif char == "c":
            duration += 2
        elif char == "e":
            duration += 3
        else:
            duration += 1
    return duration


def parse_signal_data(input_file, binary_output_file):

    multiplier = 4
    max_pause_value = 65535
    lines = []

    with open(input_file, "r") as f:
        lines = f.readlines()

    with open(binary_output_file, "wb") as binary_file:
        for i, line in enumerate(lines):
            if "[Pause:" in line:
                try:
                    code, pause_part = line.split("[Pause:")
                    pause_str = "".join(filter(str.isdigit, pause_part))
                    pause = int(pause_str) - 7

                    high_duration = decode_duration(code.strip())
                    high_duration = math.floor(high_duration * multiplier)
                    pause = math.floor(pause * multiplier)

                    if pause > max_pause_value:
                        if i == len(lines) - 1:
                            pause = 1
                        else:
                            pause = max_pause_value

                    binary_file.write(struct.pack("<HH", high_duration, pause))

                except Exception as e:
                    print(f"string processing error: {line.strip()}. error: {e}")


def upload_file_and_generate_signal(file_path):
    upload_url = "http://sigi.local/upload"

    with open(file_path, "rb") as file:
        files = {"datafile": file}
        upload_response = requests.post(upload_url, files=files)

        if upload_response.status_code == 200:
            print("successfully!")

            generate_signal_url = "http://sigi.local/start?file=output_durations.bin"
            generate_response = requests.get(generate_signal_url)

            if generate_response.status_code == 200:
                print("Signal successfully generated!")
            else:
                print("Error when generating signal.")
        else:
            print("Error uploading file.")


def main():
    input_file = "input.txt"

    parse_signal_data(input_file, name)
    print(f"Data saved in {name}")


if tx == 1:
    upload_file_and_generate_signal(name)


if __name__ == "__main__":
    main()
