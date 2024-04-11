import subprocess
import time
import sys
# import getopt


class HeadlessUploader:

    # separate the raw board search into a dictionary of usb devices
    def decode(self, data):
        lines = data.split('\n')
        result_dict = {}
        for i, line in enumerate(lines):
            if line.strip():
                result_dict[i] = line.strip().split('  ')
        for key in result_dict:
            result_dict[key] = [item for item in result_dict[key] if item.strip()]

        return result_dict

    # wait until a usb device matching the given board (self.board) is found and attempt to upload
    # .ino file (given by self.path)
    def upload_to_arduino(self):
        while self.not_found:
            check = subprocess.run(['arduino-cli', 'board', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            devices = self.decode(check.stdout.decode('utf-8'))

            for device_key in devices:
                for item in devices[device_key]:
                    if self.board in item:
                        port_name = devices[device_key][0]
                        compile_result = subprocess.run(['arduino-cli', 'compile', '--fqbn', self.board, self.path],
                                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        if compile_result.returncode == 0:
                            upload_result = subprocess.run(['arduino-cli', 'upload', '-p', port_name, '--fqbn', self.board, self.path],
                                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            if check.returncode == 0:
                                print(upload_result.stdout.decode('utf-8'))
                                print(f"Upload to: {port_name} was Successful!")
                                self.not_found = False
                            else:
                                print(upload_result.stderr.decode('utf-8'))
                                print(f"Upload to: {port_name} was Successful!")
                                self.not_found = False
        # TODO: Enable Interrupts on host device to avoid wasting resources
        time.sleep(10)

    def __init__(self, _path, _board='arduino:avr:uno'):
        self.not_found = True
        self.board = _board

        # TODO: check if the board platform core exists, if not download it
        #  arduino-cli core install <FQBN>
        #  arduino-cli core list <---- check for ID == <FQBN>

        self.path = _path

        # TODO: Check if the path is to a valid sketch folder

        self.upload_to_arduino()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        HeadlessUploader(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        HeadlessUploader(sys.argv[1])
    else:
        HeadlessUploader('HeadlessUploader')
