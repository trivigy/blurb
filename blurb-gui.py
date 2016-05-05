#!/usr/bin/python

import sys
import cairo
import gtk
import pango


def transparent_expose(widget, event):
    cr = widget.window.cairo_create()
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.set_source_rgba(0, 0, 0, 0.8)
    cr.region(gtk.gdk.region_rectangle(event.area))
    cr.fill()
    cr.set_operator(cairo.OPERATOR_OVER)
    return False


def main(argc, argv):
    win = gtk.Window()
    box = gtk.HBox()
    win.add(box)

    label = gtk.Label("This is some text that will be read by a computer.")
    label.modify_font(pango.FontDescription("bold 22"))
    label.set_line_wrap(True)
    box.pack_start(label, expand=True, fill=True)

    win.set_decorated(False)
    win.set_app_paintable(True)
    win.set_keep_above(True)
    # win.set_position(gtk.WIN_POS_CENTER)

    screen = win.get_screen()
    rootwin = win.get_screen().get_root_window()
    x, y, _ = rootwin.get_pointer()
    monitor_num = screen.get_monitor_at_point(x, y)
    pos = screen.get_monitor_geometry(monitor_num)
    win.resize(pos[2], 1)
    print pos

    rgba = screen.get_rgba_colormap()
    win.set_colormap(rgba)

    win.connect("delete-event", gtk.main_quit)
    win.connect("expose-event", transparent_expose)
    win.show_all()
    gtk.main()


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
