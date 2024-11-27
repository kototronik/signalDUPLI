import math
import struct
import requests
import argparse

def decode_duration(code):
    """Converts a string of characters (f, c, e, digits) into microseconds."""
    duration = 0
    for char in code:
        if char == 'f':
            duration += 4
        elif char == 'c':
            duration += 2
        elif char == 'e':
            duration += 3
        else:
            duration += 1
    return duration

def parse_signal_data(input_file, binary_output_file):
    """Reads data from the input file, calculates durations, and writes to a binary output file."""
    multiplier = 4  # Multiplier for conversion
    max_pause_value = 65535  # Maximum allowable value for a pause (e.g., for a 16-bit number)
    
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
        
        with open(binary_output_file, 'wb') as binary_file:
            for i, line in enumerate(lines):
                if '[Pause:' in line:
                    try:
                        code, pause_part = line.split('[Pause:')
                        pause_str = ''.join(filter(str.isdigit, pause_part))
                        pause = int(pause_str) - 7
                        
                        # Calculate high_duration and apply the multiplier
                        high_duration = decode_duration(code.strip())
                        high_duration = math.floor(high_duration * multiplier)
                        pause = math.floor(pause * multiplier)
                        
                        # Check for maximum value
                        if pause > max_pause_value:
                            if i == len(lines) - 1:  # Check if the line is the last one
                                pause = 1
                            else:
                                pause = max_pause_value

                        # Write data to the binary file
                        binary_file.write(struct.pack('<HH', high_duration, pause))
                    
                    except Exception as e:
                        print(f"Error processing line: {line.strip()}. Error: {e}")
    except FileNotFoundError:
        print(f"The file {input_file} was not found.")
    except Exception as e:
        print(f"Error processing the file: {e}")

def upload_file_and_generate_signal(file_path):
    """Uploads the file to a server and starts signal generation."""
    upload_url = "http://sigi.local/upload"
    
    try:
        with open(file_path, 'rb') as file:
            files = {'datafile': file}
            upload_response = requests.post(upload_url, files=files)
            
            if upload_response.status_code == 200:
                print("File uploaded successfully!")

                # Request to generate the signal
                generate_signal_url = f"http://sigi.local/start?file={file_path}"
                generate_response = requests.get(generate_signal_url)
                
                if generate_response.status_code == 200:
                    print("Signal generated successfully!")
                else:
                    print(f"Error generating the signal: {generate_response.status_code}")
            else:
                print(f"Error uploading the file: {upload_response.status_code}")
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except requests.RequestException as e:
        print(f"Error communicating with the server: {e}")

def main():
    """Main program: processes data, writes to a file, and uploads to the server."""
    parser = argparse.ArgumentParser(description="Process and upload signal data.")
    parser.add_argument(
        '-i', '--input', 
        type=str, 
        default='input.txt', 
        help="Input file with signal data (default: 'input.txt')"
    )
    parser.add_argument(
        '-o', '--output', 
        type=str, 
        default='output_durations.bin', 
        help="Output binary file name (default: 'output_durations.bin')"
    )
    parser.add_argument(
        '-ns', '--no-send', 
        action='store_true', 
        help="Disable file upload to the server (enabled by default)."
    )
    
    args = parser.parse_args()
    
    print(f"Processing file: {args.input}")
    parse_signal_data(args.input, args.output)
    print(f"Data saved to {args.output}")
    
    if not args.no_send:
        print("Uploading file to the server...")
        upload_file_and_generate_signal(args.output)
    else:
        print("Upload disabled. Processing complete.")

if __name__ == '__main__':
    main()
