"""
Mini-wrapper that exposes a tiny subset of PySimpleGUI's API but
implemented with tkinter + ttk (optionally ttkbootstrap for styling).

Exposes: Text, Button, Listbox, Multiline, popup, Window, WINDOW_CLOSED
Designed to support the project's existing UI files.
"""
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
try:
    import ttkbootstrap as tb
    from ttkbootstrap import Style
    _USE_TTB = True
except Exception:
    _USE_TTB = False

WINDOW_CLOSED = "__WINDOW_CLOSED__"


class Text:
    def __init__(self, text):
        self.type = "Text"
        self.text = text


class Button:
    def __init__(self, text):
        self.type = "Button"
        self.text = text


class Listbox:
    def __init__(self, values=None, size=None, key=None, enable_events=False):
        self.type = "Listbox"
        self.values = values or []
        self.size = size
        self.key = key
        self.enable_events = enable_events


class Multiline:
    def __init__(self, default_text="", size=(40, 10), disabled=False):
        self.type = "Multiline"
        self.default_text = default_text
        self.size = size
        self.disabled = disabled


def popup(msg, title="Mensaje"):
    root = tk._default_root
    if root is None:
        tmp = tk.Tk()
        tmp.withdraw()
        messagebox.showinfo(title, msg, parent=tmp)
        tmp.destroy()
    else:
        messagebox.showinfo(title, msg, parent=root)


class Window:
    def __init__(self, title, layout):
        # create root once
        if not hasattr(Window, "_root"):
            if _USE_TTB:
                Window._style = Style()
                Window._root = Window._style.master
            else:
                Window._root = tk.Tk()
            Window._root.withdraw()

        self._window = tk.Toplevel(Window._root)
        self._window.title(title)
        self._event_var = tk.StringVar(value="")
        self._elements = {}

        for r, row in enumerate(layout):
            frame = ttk.Frame(self._window)
            frame.grid(row=r, column=0, sticky="w", padx=6, pady=4)
            for elem in row:
                etype = getattr(elem, "type", None)
                if etype == "Text":
                    lbl = ttk.Label(frame, text=elem.text)
                    lbl.pack(side="left", padx=4)
                elif etype == "Button":
                    btn = ttk.Button(frame, text=elem.text, command=self._make_button_cmd(elem.text))
                    btn.pack(side="left", padx=4)
                    self._elements.setdefault("buttons", []).append(btn)
                elif etype == "Listbox":
                    height = elem.size[1] if elem.size else 6
                    listbox = tk.Listbox(frame, height=height, exportselection=False)
                    for v in elem.values:
                        listbox.insert(tk.END, v)
                    listbox.pack(side="left", padx=4)
                    key = elem.key or "-LIST-"
                    self._elements[key] = listbox
                elif etype == "Multiline":
                    h, w = elem.size[1], elem.size[0]
                    txt = scrolledtext.ScrolledText(frame, width=w, height=h)
                    txt.insert("1.0", elem.default_text)
                    if elem.disabled:
                        txt.configure(state="disabled")
                    txt.pack(side="left", padx=4)
                    self._elements.setdefault("multiline", []).append(txt)
                else:
                    pass

        self._window.protocol("WM_DELETE_WINDOW", self._on_close)
        self._closed = False

    def _make_button_cmd(self, text):
        def _cmd():
            self._event_var.set(text)

        return _cmd

    def _on_close(self):
        self._closed = True
        self._event_var.set(WINDOW_CLOSED)
        try:
            self._window.destroy()
        except Exception:
            pass

    def read(self):
        self._window.wait_variable(self._event_var)
        ev = self._event_var.get()
        values = {}
        for key, widget in self._elements.items():
            if isinstance(widget, tk.Listbox):
                sel = widget.curselection()
                values[key] = [widget.get(i) for i in sel] if sel else []
        self._event_var.set("")
        return ev, values

    def close(self):
        try:
            self._window.destroy()
        except Exception:
            pass
        self._closed = True


class _SGModule:
    Window = Window
    Text = Text
    Button = Button
    Listbox = Listbox
    Multiline = Multiline
    popup = staticmethod(popup)
    WINDOW_CLOSED = WINDOW_CLOSED


sg = _SGModule()
