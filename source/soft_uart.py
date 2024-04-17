# Example using PIO to create a UART TX interface

# ruff: noqa: F821 - @asm_pio decorator adds names to function scope

from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

UART_BAUD = 115200


@asm_pio(sideset_init=PIO.OUT_HIGH, out_init=PIO.OUT_HIGH, out_shiftdir=PIO.SHIFT_RIGHT)
def uart_tx():
    # fmt: off
    # Block with TX deasserted until data available
    pull()
    # Initialise bit counter, assert start bit for 8 cycles
    set(x, 7)  .side(0)       [7]
    # Shift out 8 data bits, 8 execution cycles per bit
    label("bitloop")
    out(pins, 1)              [6]
    jmp(x_dec, "bitloop")
    # Assert stop bit for 8 cycles total (incl 1 for pull())
    nop()      .side(1)       [6]
    # fmt: on


def create_soft_uart(pin: Pin):
    sm = StateMachine(
        0, uart_tx, freq=8 * UART_BAUD, sideset_base=pin, out_base=pin
    )
    sm.active(1)
    
    # We can print characters from each UART by pushing them to the TX FIFO
    def pio_uart_print(s):
        for b in s.encode("utf-8"):
            sm.put(b)
    return pio_uart_print
