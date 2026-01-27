import pygame
from UnipyEngine.Utils import Vector2
from typing import List

class KeyCode:
    # Lettres
    A = pygame.K_a; B = pygame.K_b; C = pygame.K_c; D = pygame.K_d; E = pygame.K_e
    F = pygame.K_f; G = pygame.K_g; H = pygame.K_h; I = pygame.K_i; J = pygame.K_j
    K = pygame.K_k; L = pygame.K_l; M = pygame.K_m; N = pygame.K_n; O = pygame.K_o
    P = pygame.K_p; Q = pygame.K_q; R = pygame.K_r; S = pygame.K_s; T = pygame.K_t
    U = pygame.K_u; V = pygame.K_v; W = pygame.K_w; X = pygame.K_x; Y = pygame.K_y
    Z = pygame.K_z

    # Chiffres (au-dessus du clavier)
    Alpha0 = pygame.K_0; Alpha1 = pygame.K_1; Alpha2 = pygame.K_2; Alpha3 = pygame.K_3
    Alpha4 = pygame.K_4; Alpha5 = pygame.K_5; Alpha6 = pygame.K_6; Alpha7 = pygame.K_7
    Alpha8 = pygame.K_8; Alpha9 = pygame.K_9

    # Pavé numérique
    Keypad0 = pygame.K_KP0; Keypad1 = pygame.K_KP1; Keypad2 = pygame.K_KP2
    Keypad3 = pygame.K_KP3; Keypad4 = pygame.K_KP4; Keypad5 = pygame.K_KP5
    Keypad6 = pygame.K_KP6; Keypad7 = pygame.K_KP7; Keypad8 = pygame.K_KP8
    Keypad9 = pygame.K_KP9
    KeypadPeriod = pygame.K_KP_PERIOD
    KeypadDivide = pygame.K_KP_DIVIDE
    KeypadMultiply = pygame.K_KP_MULTIPLY
    KeypadMinus = pygame.K_KP_MINUS
    KeypadPlus = pygame.K_KP_PLUS
    KeypadEnter = pygame.K_KP_ENTER
    KeypadEquals = pygame.K_KP_EQUALS

    # Touches de fonction
    F1 = pygame.K_F1; F2 = pygame.K_F2; F3 = pygame.K_F3; F4 = pygame.K_F4
    F5 = pygame.K_F5; F6 = pygame.K_F6; F7 = pygame.K_F7; F8 = pygame.K_F8
    F9 = pygame.K_F9; F10 = pygame.K_F10; F11 = pygame.K_F11; F12 = pygame.K_F12

    # Flèches
    UpArrow = pygame.K_UP
    DownArrow = pygame.K_DOWN
    LeftArrow = pygame.K_LEFT
    RightArrow = pygame.K_RIGHT

    # Contrôle
    Space = pygame.K_SPACE
    Return = pygame.K_RETURN
    Escape = pygame.K_ESCAPE
    Tab = pygame.K_TAB
    Backspace = pygame.K_BACKSPACE
    CapsLock = pygame.K_CAPSLOCK
    LeftShift = pygame.K_LSHIFT
    RightShift = pygame.K_RSHIFT
    LeftCtrl = pygame.K_LCTRL
    RightCtrl = pygame.K_RCTRL
    LeftAlt = pygame.K_LALT
    RightAlt = pygame.K_RALT

    # Symboles usuels
    Minus = pygame.K_MINUS
    Equals = pygame.K_EQUALS
    LeftBracket = pygame.K_LEFTBRACKET
    RightBracket = pygame.K_RIGHTBRACKET
    Semicolon = pygame.K_SEMICOLON
    Quote = pygame.K_QUOTE
    Backquote = pygame.K_BACKQUOTE
    Comma = pygame.K_COMMA
    Period = pygame.K_PERIOD
    Slash = pygame.K_SLASH
    Backslash = pygame.K_BACKSLASH

    # Spécial
    Insert = pygame.K_INSERT
    Delete = pygame.K_DELETE
    Home = pygame.K_HOME
    End = pygame.K_END
    PageUp = pygame.K_PAGEUP
    PageDown = pygame.K_PAGEDOWN
    PrintScreen = pygame.K_PRINTSCREEN
    ScrollLock = pygame.K_SCROLLOCK
    Pause = pygame.K_PAUSE
    NumLock = pygame.K_NUMLOCK

    # Multimedia (si dispo)
    #VolumeUp = pygame.K_VOLUMEUP
    #VolumeDown = pygame.K_VOLUMEDOWN
    #Mute = pygame.K_MUTE

class Input:
    _keys_down = set()
    _keys_up = set()
    _keys_held = set()
    _mouse_pos = (0, 0)
    _mouse_buttons = (False, False, False)

    @staticmethod
    def UpdateEvents(events: List[pygame.event.Event]) -> None:
        """Doit être appelée depuis Engine.Run() avec la liste pygame.event.get()."""
        Input._keys_down.clear()
        Input._keys_up.clear()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                Input._keys_down.add(event.key)
                Input._keys_held.add(event.key)
            elif event.type == pygame.KEYUP:
                Input._keys_up.add(event.key)
                if event.key in Input._keys_held:
                    Input._keys_held.remove(event.key)

            elif event.type == pygame.MOUSEMOTION:
                Input._mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Input._mouse_buttons = pygame.mouse.get_pressed()
            elif event.type == pygame.MOUSEBUTTONUP:
                Input._mouse_buttons = pygame.mouse.get_pressed()

    # --- API publique ---
    @staticmethod
    def GetKey(key: int) -> bool:
        """Retourne True tant que la touche est maintenue."""
        return key in Input._keys_held

    @staticmethod
    def GetKeyDown(key: int) -> bool:
        """Retourne True seulement sur la frame où la touche est pressée."""
        return key in Input._keys_down

    @staticmethod
    def GetKeyUp(key: int) -> bool:
        """Retourne True seulement sur la frame où la touche est relâchée."""
        return key in Input._keys_up

    @staticmethod
    def GetMousePosition() -> Vector2:
        return Vector2(*Input._mouse_pos)

    @staticmethod
    def GetMouseButton(button: int) -> bool:
        """0 = gauche, 1 = milieu, 2 = droit"""
        return Input._mouse_buttons[button]
