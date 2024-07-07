CSRCS += ui.c
CSRCS += ui_comp.c
CSRCS += ui_comp_containercmd.c
CSRCS += ui_comp_containerdistencelabel.c
CSRCS += ui_comp_containertimelabel.c
CSRCS += ui_comp_hook.c
CSRCS += ui_events.c
CSRCS += ui_font_CmdFont.c
CSRCS += ui_font_IconFont.c
CSRCS += ui_font_SubCmdFont.c
CSRCS += ui_helpers.c
CSRCS += ui_Surface.c

DEPPATH += --dep-path $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/custom
VPATH += :$(LVGL_DIR)/$(LVGL_DIR_NAME)/src/custom

CFLAGS += "-I$(LVGL_DIR)/$(LVGL_DIR_NAME)/src/custom"
