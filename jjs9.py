from __future__ import print_function
"""
JS9 wrapper to be used in Jupyter/IPython notebooks

Matias Carrasco Kind
"""
__author__ = 'Matias Carrasco Kind'
import uuid
import json
from astropy import wcs
from astropy.io import fits

def libinit(root=None):
    """
    Initialization function needed to load javascript libraries and css styles into the notebook.

    Parameters:
    -----------
    root : root url where main path for the notebook is running
    """
    #root = 'http://localhost:8888/files/'
    req = """
    require.config({
      paths: {
          js9: '%sjs9-allinone',
      }
    });
    """ % root
    css = """
    <link rel="stylesheet" type="text/css" href="%sjs9-allinone.css">
    """ % root
    init = """
    require(['js9'], function(){
        console.log('Loaded');     
    });
    """
    get_ipython().run_cell_magic('javascript', '', req)
    get_ipython().run_cell_magic('html', '', css)
    get_ipython().run_cell_magic('javascript', '', init)

class Js9(object):
    """Jupyter Notebbok wrapper around JS9 class object"""
    def __init__(self):
        """
        Initiate the class with an unique id unless is manually parsed

        Parameters:
        -----------
        wid : Id to be use for the JS9 display. Default a unique id is created
        """
        self.created = False
        self.wid = uuid.uuid4().hex
        self.url = None
        self.wcs_world2pix = None
        self.wcs_pix2world = None

    def DelDiv(self):
        """
        Delete current div for this class
        """
        if self.created:
            self.CloseImage()
            command = """$('#{}').remove();""".format(self.wid)
            get_ipython().run_cell_magic('javascript', '', command)
            self.created = False
            self.wid = uuid.uuid4().hex


    def NewDiv(self, width='80%', height='512px'):
        """
        Creates a new div to be added to the notebook cell

        Parameters:
        -----------

        width :  width of the displayed window in css style (string). Default is 
                 80% of the screen
        height : height of the displayed window in css style (string). Default is 
                 512px of the screen
        
        """
        if self.created:
            self.DelDiv()
        print('Display id = {}JS9'.format(self.wid))
        command = """
        "<div id='{0}' ><div class='JS9Menubar' data-width='512px' data-height='54px' id='{0}JS9Menubar'></div><div class='JS9' data-width='{1}' data-height='{2}' id='{0}JS9'></div></div>"
        """.format(self.wid, width, height)
        js_command = "element.append({});".format(command)
        get_ipython().run_cell_magic('javascript', '', js_command)
        get_ipython().run_cell_magic('javascript', '', "JS9.AddDivs('{}JS9');".format(self.wid))
        self.created = True

    def Load(self, url, **kwargs):
        """
        Loads a FITS file into the display created.

        Parameters:
        -----------
        url : Path to file (can be locally)

        Extra arguments in form of a dictionary used by the JS9 javascript object JS9.Load()
        """
        opts = ''
        self.url = url
        if not 'wcsunits' in kwargs:
            kwargs['wcsunits'] = 'degrees'
        if not 'scaleclipping' in kwargs:
            kwargs['scaleclipping'] = 'zscale'
        if len(kwargs) > 0:
            opts = json.dumps(kwargs)+','
        fmt = dict(url=self.url, kw=opts, wid=self.wid)
        command = "JS9.Load('{url}',{kw}{{display:'{wid}JS9'}});".format(**fmt)
        try:
            hdulist = fits.open(url)
            temp_wcs = wcs.WCS(hdulist[0].header)
            self.wcs_world2pix = temp_wcs.wcs_world2pix
            self.wcs_pix2world = temp_wcs.wcs_pix2world
            hdulist.close()
        except:
            pass
        get_ipython().run_cell_magic('javascript', '', command)

    def CloseImage(self):
        """
        Close current image
        """
        command = "JS9.CloseImage({{display:'{wid}JS9'}});".format(wid=self.wid)
        get_ipython().run_cell_magic('javascript', '', command)

    def SetColorMap(self, colormap, contrast=None, bias=None):
        """
        Set color map of currently displayed image

        Parameters:
        -----------

        colormap: colormap name
        contrast: contrast value (range: 0 to 10)
        bias: bias value (range 0 to 1)
        """
        extra = ''
        if contrast is not None:
            extra += '%f,' % contrast
        if bias is not None:
            extra  += '%f,' % bias
        fmt = dict(wid=self.wid,cmap=colormap, extra=extra)
        command = "JS9.SetColormap('{cmap}', {extra} {{display:'{wid}JS9'}});".format(**fmt)
        get_ipython().run_cell_magic('javascript', '', command)

        

    def AddRegions(self, **kwargs):
        """
        Add Regions to JS9 display using same syntax as JS9.AddRegions.
        This uses astropy.wcs to do the coordinates transformations
        """
        n_objs = 0
        objs = []
        # default shape is circle
        if not 'shape' in kwargs:
            kwargs['shape'] = ['circle']
        for k in kwargs.keys():
            n_objs = max(n_objs, len(kwargs[k]))
        for j in range(n_objs):
            temp = {}
            for k in kwargs.keys():
                try:
                    temp[k] = kwargs[k][j]
                except IndexError:
                    if k == 'shape':
                        temp[k] = 'circle'
            objs.append(temp)
        all_objs = json.dumps(objs)
        command = "JS9.AddRegions({objs}, {{display:'{id}JS9'}})".format(objs=all_objs, id=self.wid)
        get_ipython().run_cell_magic('javascript', '', command)


