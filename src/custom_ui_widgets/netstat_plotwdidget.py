from pyqtgraph import PlotWidget, DateAxisItem
import pyqtgraph as pg

pg.setConfigOption('background', '#F5F5F5')
pg.setConfigOption('foreground', 'k')

class NetStat_PlotWdidget(PlotWidget):

    def __init__(self, parent=None, background='default', plotItem=None, **kargs):
        super(NetStat_PlotWdidget, self).__init__(parent=parent, background=background, plotItem=plotItem, axisItems = {'bottom': DateAxisItem()}, **kargs)
