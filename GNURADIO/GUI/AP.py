import curses
import socket
import threading
import sys
AP= "AP"
half_width = 0
half_height = 0
lin_total = 0

def instr(message, tag):
    if message.startswith(tag+"-"):
        return True
    return False
def phy(message, prefix):
    if message.startswith(prefix):
        return True
    return False

def print_output(window, port, messages):
    global half_width
    global lin_total
    tag_loopback = AP
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
                        elif phy(message, "Zigbee-"):
                            window.addstr(1+i,1,">", curses.A_BLINK) 
                            window.addstr(1+i,2,message[:len("Zigbee")],curses.A_BOLD|curses.color_pair(4))
                            window.addstr(1+i,2+len("Zigbee"),message[len("Zigbee"):],curses.color_pair(1))
                        elif phy(message, "Wifi-"):
                            window.addstr(1+i,1,">", curses.A_BLINK) 
                            window.addstr(1+i,2,message[:len("Wifi")],curses.A_BOLD|curses.color_pair(5))
                            window.addstr(1+i,2+len("Wifi"),message[len("Wifi"):],curses.color_pair(1))
                        else:
                            window.addstr(1+i,1,">", curses.A_BLINK) 
                            window.addstr(1+i,2,message)
                    else:
                        if instr(message, tag_loopback):
                            window.addstr(1+i,1,"LOOPBACK--> ", curses.A_BOLD|curses.A_DIM|curses.color_pair(2))
                            window.addstr(1+i,1+len("LOOPBACK--> "),message, curses.A_DIM)
                        elif phy(message, "Zigbee-"):
                            window.addstr(1+i,1,message[:len("Zigbee")],curses.A_BOLD|curses.color_pair(4)|curses.A_DIM)
                            window.addstr(1+i,1+len("Zigbee"),message[len("Zigbee"):],curses.color_pair(1)|curses.A_DIM)
                        elif phy(message, "Wifi-"):
                            window.addstr(1+i,1,message[:len("Wifi")],curses.A_BOLD|curses.color_pair(5)|curses.A_DIM)
                            window.addstr(1+i,1+len("Wifi"),message[len("Wifi"):],curses.color_pair(1)|curses.A_DIM)
                        else:
                            window.addstr(1+i,1,message, curses.A_DIM)
                    window.attron(curses.color_pair(3))
                    window.box()
                    window.attroff(curses.color_pair(3))

                window.refresh()
            

    except Exception as e:
        window.clear()
        window.addstr("Error: " + str(e))
        window.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) 
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)  
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)  

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


    win.addstr(0, (half_width - len(AP)//2), AP + "\n", curses.A_STANDOUT|curses.A_BOLD|curses.color_pair(3))
    win.refresh()


    txt.attron(curses.color_pair(3))
    txt.box()
    txt.attroff(curses.color_pair(3))
    txt.refresh()


    messages = []  # List to store messages of port 52001

    print_output(txt, 52001, messages)




if __name__ == "__main__":
    curses.wrapper(main)