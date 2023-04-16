import sys
import os

CUSTOM_EOF = b'\x1f\x66\x69\x6c\x65\x2d\x68\x69\x64\x65\x72\x1f'
FILE_NAME_SEPARATOR = b'\x1c'


def printHeader():
    print("  _____ _ _            _   _ _     _           ")
    print(" |  ___(_) | ___      | | | (_) __| | ___ _ __ ")
    print(" | |_  | | |/ _ \_____| |_| | |/ _` |/ _ \ '__|")
    print(" |  _| | | |  __/_____|  _  | | (_| |  __/ |   ")
    print(" |_|   |_|_|\___|     |_| |_|_|\__,_|\___|_|   ")
    print("")
    print("")


def hide(camouflaged_file, secret_file, output_file):
    print('Hiding file ' + secret_file + ' in ' + camouflaged_file + '...')
    print('Output file: ' + output_file)

    secret_file_name = secret_file.split(os.sep)[-1]

    with open(camouflaged_file, 'rb') as camouflaged_file:
        camouflaged_data = camouflaged_file.read()

    with open(secret_file, 'rb') as secret_file:
        secret_data = secret_file.read()

    output_data = camouflaged_data + CUSTOM_EOF + \
        str.encode(secret_file_name) + FILE_NAME_SEPARATOR + secret_data

    with open(output_file, 'wb') as output_file:
        output_file.write(output_data)

    print('Done.')


def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        print(
            'Usage: python file-hider.py -c camouflaged_file -s secret_file -o output_file')
        print('Options:')
        print('  -c, --camouflaged-file: the file to hide the secret file in')
        print('  -s, --secret-file: the file to hide')
        print('  -o, --output-file: the output file')
        sys.exit()

    if len(sys.argv) != 7:
        print('Error: invalid number of arguments.')
        print('Use the -h or --help option for more information.')
        sys.exit()

    if '-c' in sys.argv:
        camouflaged_file_index = sys.argv.index('-c')
    elif '--camouflaged-file' in sys.argv:
        camouflaged_file_index = sys.argv.index('--camouflaged-file')
    if '-s' in sys.argv:
        secret_file_index = sys.argv.index('-s')
    elif '--secret-file' in sys.argv:
        secret_file_index = sys.argv.index('--secret-file')
    if '-o' in sys.argv:
        output_file_index = sys.argv.index('-o')
    elif '--output-file' in sys.argv:
        output_file_index = sys.argv.index('--output-file')

    camouflaged_file = sys.argv[camouflaged_file_index + 1]
    secret_file = sys.argv[secret_file_index + 1]
    output_file = sys.argv[output_file_index + 1]

    printHeader()
    hide(camouflaged_file, secret_file, output_file)
    print()
    print('Done.')


if __name__ == '__main__':
    main()
