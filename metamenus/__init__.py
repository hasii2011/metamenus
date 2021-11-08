#
#
#

from wx.lib.newevent import NewCommandEvent

try:
    # noinspection PyUnresolvedReferences
    import unidecode
    use_unidecode = True
except ModuleNotFoundError:
    use_unidecode = False

# Events -----------------------------------------------------------------------

(MenuExBeforeEvent, EVT_BEFOREMENU) = NewCommandEvent()
(MenuExAfterEvent,  EVT_AFTERMENU)  = NewCommandEvent()
