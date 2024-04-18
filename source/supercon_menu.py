import machine
import joystick
from menu import *   # bad habit but makes our menu definition nice
from vos_state import vos_state
import vectoros
import colors
import random


def runsketch(_arg):
    """
    Run the demo sketch
    """
    vos_state.show_menu=False     # get the menu of the way
    vectoros.launch_task('sketch')
    return EXIT


def planets(_arg):
    """
    Run the planets sketch
    """

    vos_state.show_menu=False     # get the menu of the way
    vectoros.launch_task('planets')  # launch
    return EXIT


def dynamic_sound_text():
    return " Sound Off" if machine.Pin(22).value() else " Sound On"


def toggle_sound(_arg):
    ## toggle sound here
    machine.Pin(22, machine.Pin.OUT).toggle()
    return CONT


def run_lissajous(_arg):
    """
    Run the main vector scope demo.
    """

    vos_state.show_menu = False
    vos_state.gc_suspend = True
    vectoros.launch_task("lissajous")
    # we never come back, vectorscope
    return EXIT


def run_life(arg):
    vos_state.show_menu = False
    vectoros.launch_task("life", arg)
    return EXIT


def run_robot(_arg):
    vos_state.show_menu=False
    vectoros.launch_task('run_robot')
    return EXIT


def reboot(arg):
    if arg==False:
        vectoros.reset()
    else:
        vectoros.soft_reset()


def abcd(key):
    """
    Handle slots
    """

    if vos_state.show_menu:
        vos_debug.debug_print(vos_debug.DEBUG_LEVEL_INFO, f"Menu key {key}")
        kdict = {
            keyleds.KEY_A: 'A',
            keyleds.KEY_B: 'B',
            keyleds.KEY_C: 'C',
            keyleds.KEY_D: 'D',
        }
        await vectoros.launch_vecslot("slot" + kdict[key])


# I really didn't want this to be async but it seems like do_menu must have an await
# and run rarely returns when you have a lot going on
async def vos_main():
    # you do NOT have to use with here
    # but if you don't you have to worry about the menu controller's joystick instance going out of scope yourself
    # or just make everything global -- the menu is smart enough to not listen to events when it is not active
    # note: m_back and m_exit were imported from menu
    ## Start with sound off
    machine.Pin(22, machine.Pin.OUT).toggle()

    screen=vectoros.get_screen()
    splashes = ["splash_europe.jpg", "splash_2024.jpg", "splash_wrencher.jpg"]
    screen.jpg(random.choice(splashes))
    await asyncio.sleep_ms(1000)

    while True: # since this is the main menu, we don't really every quit
        print("creating slotkey")
        keyboardcb.KeyboardCB(abcd,keyleds.KEY_ABCD)

        with Menu(
            clear_after=True,
            fg_color=colors.PHOSPHOR_DARK,
            bg_color=colors.PHOSPHOR_BG,
            cursor_bg=colors.PHOSPHOR_BG,
            cursor_fg=colors.PHOSPHOR_BRIGHT,
        ) as amenu:
            ## name in menu, command to run, return value?
            demo_submenu = [
                ["  Planets", planets, 0],
                ["  Sketch", runsketch, 0],
                ["  Back", m_exit, None],
            ]
            life_submenu = [
                ["  Pulsar", run_life, "pulsar"],
                ["  Beacon", run_life, "beacon"],
                ["  Glider", run_life, "glider"],
                ["  GosperGliderGun", run_life, "gosper_glider_gun"],
                ["  Back", m_exit, None],
            ]
            mainmenu = [
                [" Lissajous", run_lissajous, None],
                [" Demos", SUBMENU, demo_submenu],
                [" Run Robot", run_robot, None],
                [" Life", SUBMENU, life_submenu],
                [dynamic_sound_text, toggle_sound, None],
                [" Reboot", reboot, False],
            ]

            # comment next line for default font
            amenu.set_font("*")   # set default vector font
            await amenu.do_menu(mainmenu)

        vos_debug.debug_print(vos_debug.DEBUG_LEVEL_INFO, f"Menu waiting {vos_state.show_menu}")

        while vos_state.show_menu == False:   # wait until we have to be seen again
            await asyncio.sleep_ms(0)


def main():
    asyncio.run(vos_main())
    # this never runs


if __name__=="__main__":
    import vectoros
    vectoros.run()
