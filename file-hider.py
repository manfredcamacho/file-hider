import sys
import os

CUSTOM_EOF = b'\x1f\x66\x69\x6c\x65\x2d\x68\x69\x64\x65\x72\x1f'
FILE_NAME_SEPARATOR = b'\x1c\x73\x70\x6C\x69\x74\x1c'
PREFIX_RECOVERED_FILE = 'recovered_'


def printHeader():
    print("  _____ _ _            _   _ _     _           ")
    print(" |  ___(_) | ___      | | | (_) __| | ___ _ __ ")
    print(" | |_  | | |/ _ \_____| |_| | |/ _` |/ _ \ '__|")
    print(" |  _| | | |  __/_____|  _  | | (_| |  __/ |   ")
    print(" |_|   |_|_|\___|     |_| |_|_|\__,_|\___|_|   ")
    print("")
    print("")


def printHelp():
    print(
        f'Usage: python3 {sys.argv[0]} -c camouflaged_file -s secret_file -o output_file')
    print()
    print('Options for hide files:')
    print('  -c, --camouflaged-file: the file to hide the secret file in')
    print('  -s, --secret-file: the file to hide')
    print('  -o, --output-file: the output file')
    print()
    print('Options for recover files:')
    print('  -r, --recover-file: The camouflaged file to recover files from.')
    print('  -d, --destination: The destination folder to recover files to. (optional)')
    print()
    print()


def printInvalidArguments():
    print('Error: invalid number of arguments.')
    print('Use the -h or --help option for more information.')


def get_file_name(file_path):
    return file_path.split(os.sep)[-1]


def hide_file(camouflaged_file, secret_file, output_file):
    print('Hiding file ' + secret_file + ' in ' + camouflaged_file + '...')
    print('Output file: ' + output_file)

    secret_file_name = get_file_name(secret_file)

    with open(camouflaged_file, 'rb') as camouflaged_file:
        camouflaged_data = camouflaged_file.read()

    with open(secret_file, 'rb') as secret_file:
        secret_data = secret_file.read()

    output_data = camouflaged_data + CUSTOM_EOF + \
        str.encode(secret_file_name) + FILE_NAME_SEPARATOR + secret_data

    with open(output_file, 'wb') as output_file:
        output_file.write(output_data)


def recover_files(camouflaged_file_name, destination_folder):

    print('Recovering files from ' + camouflaged_file_name + '...')

    with open(camouflaged_file_name, 'rb') as camouflaged_file:
        camouflaged_data = camouflaged_file.read()

    if CUSTOM_EOF not in camouflaged_data:
        print('Error: no secret file found in ' + camouflaged_file_name + '.')
        return

    camouflaged_data = camouflaged_data.split(CUSTOM_EOF)

    print('Found ' + str(len(camouflaged_data) - 1) + ' secret file(s).')
    print('Destination folder: ' + destination_folder)
    print()

    print('Recovering original camouflaged file ...')
    with open(PREFIX_RECOVERED_FILE + get_file_name(camouflaged_file_name), 'wb') as recover_camouflaged_file:
        recover_camouflaged_file.write(camouflaged_data[0])

    for i in range(len(camouflaged_data) - 1):
        secret_file = camouflaged_data[i + 1].split(FILE_NAME_SEPARATOR)
        secret_file_name = PREFIX_RECOVERED_FILE + \
            secret_file[0].decode('utf-8')
        secret_file_data = secret_file[1]

        print('Recovering file ' + secret_file_name + '...')

        with open(secret_file_name, 'wb') as secret_file_name:
            secret_file_name.write(secret_file_data)


def get_destination_index():
    if '-d' in sys.argv:
        return sys.argv.index('-d')
    elif '--destination' in sys.argv:
        return sys.argv.index('--destination')
    else:
        return -1


def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        printHelp()
        sys.exit()

    if '-c' in sys.argv or '--camouflaged-file' in sys.argv:
        if ('-s' not in sys.argv and '--secret-file' not in sys.argv) or ('-o' not in sys.argv and '--output-file' not in sys.argv) or len(sys.argv) != 7:
            printInvalidArguments()
            sys.exit()

        argument = '-c' if '-c' in sys.argv else '--camouflaged-file'
        camouflaged_file_index = sys.argv.index(argument)
        argument = '-s' if '-s' in sys.argv else '--secret-file'
        secret_file_index = sys.argv.index(argument)
        argument = '-o' if '-o' in sys.argv else '--output-file'
        output_file_index = sys.argv.index(argument)

        camouflaged_file = sys.argv[camouflaged_file_index + 1]
        secret_file = sys.argv[secret_file_index + 1]
        output_file = sys.argv[output_file_index + 1]
        printHeader()
        hide_file(camouflaged_file, secret_file, output_file)

    elif '-r' in sys.argv or '--recover-file' in sys.argv:
        if len(sys.argv) != 3:
            printInvalidArguments()
            sys.exit()
        argument = '-r' if '-r' in sys.argv else '--recover-file'
        camouflaged_file_index = sys.argv.index(argument)
        camouflaged_file = sys.argv[camouflaged_file_index + 1]

        destination_folder = os.getcwd()
        if ('-d' in sys.argv or '--destination-folder' in sys.argv):
            argument = '-d' if '-d' in sys.argv else '--destination-folder'
            destination_index = sys.argv.index(argument)
            isDirectory = os.path.isdir(sys.argv[destination_index + 1])
            if (isDirectory):
                destination_folder = sys.argv[destination_index + 1]
            else:
                print('Error: destination is not a directory.')
                sys.exit()

        printHeader()
        recover_files(camouflaged_file, destination_folder)

    else:
        printInvalidArguments()
        sys.exit()

    print()
    print('Done.')


if __name__ == '__main__':
    main()
