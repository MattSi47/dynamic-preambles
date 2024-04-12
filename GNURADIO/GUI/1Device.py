import curses
import socket
import threading
import sys
Device1= "Device 1"
half_width = 0
half_height = 0
lin_total = 0

def instr(message, tag):
    if (tag + ": ") in message or (tag + "| ") in message:
        return True
    return False
def APCheck():
    if ("AP-") in message:
        return True
    return False

def print_output(window, port, messages):
    global half_width
    global lin_total
    global Device1
    tag_loopback = Device1
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('localhost', port))
        

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
                        elif APCheck():
                            window.addstr(1+i,1,">", curses.A_BLINK) 
                            window.addstr(1+i,2,message,curses.A_BOLD|curses.color_pair(3)) 
                        else:
                            window.addstr(1+i,1,">", curses.A_BLINK) 
                            window.addstr(1+i,2,message)
                    else:
                        if instr(message, tag_loopback):
                            window.addstr(1+i,1,"LOOPBACK--> ", curses.A_BOLD|curses.A_DIM|curses.color_pair(2))
                            window.addstr(1+i,1+len("LOOPBACK--> "),message, curses.A_DIM)
                        elif APCheck():
                            window.addstr(1+i,1,message,curses.A_BOLD|curses.color_pair(3)|curses.A_DIM) 
                        else:
                            window.addstr(1+i,1,message, curses.A_DIM)
                    window.box()

                window.refresh()
            

    except Exception as e:
        window.clear()
        window.addstr("Error: " + str(e))
        window.refresh()


def main(stdscr,Name1):
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

    win = curses.newwin(height, width, 0, 0)
    lin_total = height - 4
    txt = curses.newwin(height - 2, width - 2, 1, 1)


    global Device1

    win.addstr(0, (half_width - len(Device1)//2), Device1 + "\n", curses.A_STANDOUT|curses.A_BOLD)
    win.refresh()


    txt.box()
    txt.refresh()


    messages = []  # List to store messages of port 52001

    print_output(txt, 52001, messages)




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 1Device.py <Device Name>")
        sys.exit(1)
    
    Device1 = sys.argv[1]

    curses.wrapper(main, Device1)
