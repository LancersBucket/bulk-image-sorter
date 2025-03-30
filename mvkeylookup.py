"""Convert string characters to dearpygui mvKey_* constants."""
import dearpygui.dearpygui as dpg

# Mapping characters to mvKey_* values
__CHAR_TO_MVKEY__ = {
    "0": dpg.mvKey_0, "1": dpg.mvKey_1, "2": dpg.mvKey_2, "3": dpg.mvKey_3, "4": dpg.mvKey_4,
    "5": dpg.mvKey_5, "6": dpg.mvKey_6, "7": dpg.mvKey_7, "8": dpg.mvKey_8, "9": dpg.mvKey_9,

    "a": dpg.mvKey_A, "b": dpg.mvKey_B, "c": dpg.mvKey_C, "d": dpg.mvKey_D, "e": dpg.mvKey_E,
    "f": dpg.mvKey_F, "g": dpg.mvKey_G, "h": dpg.mvKey_H, "i": dpg.mvKey_I, "j": dpg.mvKey_J,
    "k": dpg.mvKey_K, "l": dpg.mvKey_L, "m": dpg.mvKey_M, "n": dpg.mvKey_N, "o": dpg.mvKey_O,
    "p": dpg.mvKey_P, "q": dpg.mvKey_Q, "r": dpg.mvKey_R, "s": dpg.mvKey_S, "t": dpg.mvKey_T,
    "u": dpg.mvKey_U, "v": dpg.mvKey_V, "w": dpg.mvKey_W, "x": dpg.mvKey_X, "y": dpg.mvKey_Y,
    "z": dpg.mvKey_Z
}

def string_to_mvkey(char: str) -> int:
    """ Convert a string character to mvKey_* constant """
    return __CHAR_TO_MVKEY__.get(char.lower(), None)

def mvkey_to_string(mvkey: int) -> str:
    """ Convert mvKey_* constant to string character """
    for char, key in __CHAR_TO_MVKEY__.items():
        if key == mvkey:
            return char
    return None
