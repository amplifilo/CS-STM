# PLOTTING

import holoviews as hv
from holoviews import opts
from holoviews.core import Store
from holoviews.util.settings import list_backends

# More advanced Holoviews options usage contained here:
# http://holoviews.org/_modules/holoviews/core/options.html

def get_hv_opts(opts_set):

    if len(list_backends()) == 0:
        import warnings
        warnings.warn('Need to activate extension.', Warning)
        return

    use_backend = lambda lst : any(i == Store.current_backend for i in lst)

    # put raster separately; separate defaults
    if opts_set == 'Image':
        if use_backend(['bokeh', 'matplotlib']):
            opts_  = [opts.Image(cmap='coolwarm', xaxis=None, yaxis=None,\
                                 frame_width=200, frame_height=200),
                      opts.Raster(cmap='coolwarm', xlabel='', ylabel='',\
                                 frame_width=200, frame_height=200),
                      opts.Layout(shared_axes=False)]
            opts.defaults(*opts_)
            print(f'Default opts set: {opts_}')

# LOADING DATA

def load_stm_data(samples=None):
    import deepdish
    
    fpath = r"maksymovych_STM_data.h5"
    dct = deepdish.io.load(fpath)

    # sort by size
    dct = dict(sorted([(k,v) for k,v in dct.items()], key=lambda x:x[1].shape))
    
    # make into list if not
    if samples == None:
        return dct
    else:
        if type(samples) != list:
            samples = list(samples)
        return {k:dct[k] for k in samples}


# IMAGE OPERATIONS

def stretch_img(img, min_val=0, max_val=1):

    '''
    Rescale an array linearly between a min and max val.
    '''
    
    min_ = img.min()
    max_ = img.max()

    a = (max_val - min_val) / (max_ - min_)
    b = -a * min_ + min_val

    return a * img + b

def stretchncenter(img, min_val=0, max_val=1):
    import numpy as np
    img = stretch_img(img, min_val, max_val)
    img = img - np.mean(img)
    return img