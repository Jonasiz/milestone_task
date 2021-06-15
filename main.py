import argparse

from demo_modes import main, main_interactive


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Choose demo mode')

    valid_modes = ['plain', 'interactive']
    parser.add_argument('--mode', default='interactive', choices=valid_modes)
    args = parser.parse_args()

    if args.mode == 'interactive':
        main_interactive()
    else:
        main()
