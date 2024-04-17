# A little slideshow you can customize
## Images need to be in true color / jpg
## Example conversion: convert Death_Star.jpg -resize 240x240 -type TrueColor thats_no_moon.jpg

import screennorm
import keyboardcb
import keyleds
import vectoros
import timer
import gc
import asyncio
from vos_state import vos_state
import colors
from soft_uart import create_soft_uart
from machine import Pin


screen=screennorm.ScreenNorm()   # get the screen
exit_flag=False   # don't exit
soft_uart = None


# Joystick
# Up is delay up, Down is delay down
# Right is next, and Left toggles the pause flag
def rob_joycb(key):
    print("rob_joycb")
    if (key==keyleds.JOY_UP):
        print("UP")
        soft_uart("UP")
    if (key==keyleds.JOY_DN):
        print("DOWN")
        soft_uart("DOWN")
    if (key==keyleds.JOY_RT):
        print("RIGHT")
        soft_uart("RIGHT")
    if (key==keyleds.JOY_LF):
        print("LEFT")
        soft_uart("LEFT")

    
def menu(key):						# menu -bail out
    global exit_flag
    exit_flag=True


async def vos_main():
    global exit_flag, current_slide, tid, timer_rate, soft_uart
    screen.jpg("robot.jpg")
    soft_uart = create_soft_uart(Pin(28))
    
    # we treat the joystick like any other key here
    keys=keyboardcb.KeyboardCB({
        keyleds.KEY_MENU: menu,
        keyleds.JOY_UP: rob_joycb,
        keyleds.JOY_DN: rob_joycb,
        keyleds.JOY_RT: rob_joycb,
        keyleds.JOY_LF: rob_joycb
    })

    # do nothing... everything is on keyboard and timer
    while exit_flag==False:
        await asyncio.sleep_ms(500)
# stop listening for keys
    keys.detach()
    exit_flag=False  # next time

    vos_state.show_menu=True  # tell menu to wake up
  
def main():
    asyncio.run(vos_main());

# if __name__=="__main__":
#      main()


if __name__=="__main__":
    import vectoros
    vectoros.run()
