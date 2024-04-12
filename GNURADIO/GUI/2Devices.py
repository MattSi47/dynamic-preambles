import curses
import socket
import threading
import sys
Device1= "Device 1"
Device2= "Device 2"
half_width = 0
half_height = 0
lin_total = 0

def instr(message, tag):
    if (tag + ": ") in message or (tag + "| ") in message:
        return True
    return False

def print_output(window, port, messages):
    global half_width
    global lin_total
    global Device1
    global Device2
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('localhost', port))
        
        if port == 52001:
            tag_loopback = Device1
        elif port == 52002:
            tag_loopback = Device2

        # Loop to continuously receive data
        while True:
            data, addr = s.recvfrom(1024)
            if data:
                # Add the new message to the message list
                messages.append(data.decode('utf-8'))

                # Clear the window
                window.clear()

                # Display the last three messages with decreasing opacity

                for i, message in enumerate(reversed(messages[-lin_total:])):
                    if i == 0:
                        if instr(message, tag_loopback):
                            window.addstr(1+i,1,"LOOPBACK", curses.A_BOLD|curses.color_pair(2))
                            window.addstr(1+i,1+len("LOOPBACK"),"--> ", curses.A_BOLD|curses.A_BLINK|curses.color_pair(2))
                            window.addstr(1+i,1+len("LOOPBACK--> "),message)
                        elif instr(message,"AP"):
                            window.addstr(1+i,1,">", curses.A_BLINK) 
                            window.addstr(1+i,2,message,curses.A_BOLD|curses.color_pair(3)) 
                        else:
                            window.addstr(1+i,1,">", curses.A_BLINK) 
                            window.addstr(1+i,2,message)
                    else:
                        if instr(message, tag_loopback):
                            window.addstr(1+i,1,"LOOPBACK--> ", curses.A_BOLD|curses.A_DIM|curses.color_pair(2))
                            window.addstr(1+i,1+len("LOOPBACK--> "),message, curses.A_DIM)
                        elif instr(message,"AP"):
                            window.addstr(1+i,1,message,curses.A_BOLD|curses.color_pair(3)|curses.A_DIM) 
                        else:
                            window.addstr(1+i,1,message, curses.A_DIM)
                    window.box()

                window.refresh()

    except Exception as e:
        window.clear()
        window.addstr("Error: " + str(e))
        window.refresh()


def main(stdscr,Name1,Name2):
    curses.curs_set(0)
    stdscr.clear()

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) 
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  


    # Split terminal horizontally
    global half_width  
    global half_height
    global lin_total
    height, width = stdscr.getmaxyx()
    half_width = width // 2
    half_height = height // 2

    top_win = curses.newwin(half_height, width, 0, 0)
    bottom_win = curses.newwin(half_height, width, half_height, 0)
    lin_total = half_height - 4
    top_txt = curses.newwin(half_height - 2, width - 2, 1, 1)
    bottom_txt = curses.newwin(half_height - 2, width - 2, half_height + 1, 1)

    global Device1
    global Device2

    top_win.addstr(0, (half_width - len(Device1)//2), Device1 + "\n", curses.A_STANDOUT|curses.A_BOLD)
    bottom_win.addstr(0, (half_width - len(Device2)//2), Device2 + "\n", curses.A_STANDOUT|curses.A_BOLD)
    top_win.refresh()
    bottom_win.refresh()

    top_txt.box()
    bottom_txt.box()
    top_txt.refresh()
    bottom_txt.refresh()


    messages_top = []  # List to store messages of port 52001
    messages_bottom = []  # List to store messages of port 52002

    thread1 = threading.Thread(target=print_output, args=(top_txt, 52001, messages_top))
    thread2 = threading.Thread(target=print_output, args=(bottom_txt, 52002, messages_bottom))

    # Start both threads
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 2Devices.py <Device 1 Name> <Device 2 Name>")
        sys.exit(1)
    
    Device1 = sys.argv[1]
    Device2 = sys.argv[2]

    curses.wrapper(main, Device1, Device2)