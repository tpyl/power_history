#!/usr/bin/env python3

import sys, tty, termios, shutil

def getch():
    """
    Reads one character from stdin, with no echo
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try: 
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def filter_candidates(candidates: list, usr_input: str):
    """
    Return entries in candidates that contain usr_input as substring, ordered by the index
    where the substring is found. Duplicates are removed. For matches where the index of 
    the substring is the same, original order (time) is kept.
    """
    with_dups = list(sorted(filter(lambda x: usr_input in x, candidates), key=lambda x: x.find(usr_input)))
    seen = set()
    return [x for x in with_dups if not (x in seen or seen.add(x))]


def printe(s:str, end="\n"):
    """
    Print to stderr
    """
    sys.stderr.write(s + end)

def move_up(n: int):
    """
    Moves the cursor up by n lines
    """
    printe("\x1B[%dA"%n, end="")

def clear(n: int):
    """
    Clears out n lines, returns the cursor to starting line
    """
    for i in range(n):
        printe("\x1B[K")
    move_up(n)


if __name__ == "__main__":
    # Load command history, latest command at the top of the list
    cmds = list(reversed([line.strip() for line in open('/home/timo/.bash_history')]))

    prev_candidates = 0
    if len(sys.argv) > 1:
        term_width = int(sys.argv[1])
    else:
        term_width = shutil.get_terminal_size().columns
    selected = 0
    input_buf = []
    move_up(1)
    printe("\x1B[K")

    while True:
        # Print current input buffer in green
        printe("\x1B[K\r\x1B[32;1m%s\x1B[0m" % ''.join(input_buf))

        # Find matching commands from history
        candidates = filter_candidates(cmds, ''.join(input_buf))

        # Clip selected command to bounds
        selected = max(0, min(len(candidates) -1, selected))
        start_idx = max(0, selected-3);
        end_idx = min(len(candidates), start_idx + 6)

        # Clear out previously printed alternatives
        clear(prev_candidates)

        # Print out current alternatives
        prev_candidates = end_idx - start_idx
        for idx in range(start_idx, end_idx):
            if idx == selected:
                printe("\x1B[46m%s\x1B[0m\x1B[K" % candidates[idx][:term_width])
            else:
                printe(candidates[idx][:term_width] + "\x1B[K")

        # Return cursor to starting position
        move_up(prev_candidates + 1)
        sys.stderr.flush()

        ch = getch()

        if ch=='\r':
            clear(prev_candidates + 1)
            printe(candidates[selected])
            print(candidates[selected])
            sys.exit(0)
        elif ord(ch) == 127:
            input_buf = input_buf[:-1]
            # TODO: Attempt to preserve selected location
            selected = 0
        elif ord(ch) == 27:
            code = getch()
            if ord(code) == 91:
                code = getch()
            # Down arrow
            if ord(code) == 66:
                selected += 1
            # Up arrow1
            elif ord(code) == 65:
                selected -= 1
            else:
                clear(prev_candidates+1)
                sys.exit(-1)
        elif ch.isprintable():
            input_buf.append(ch)
            # TODO: Attempt to preserve selected location
            selected = 0
