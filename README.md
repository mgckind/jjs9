## JJS9

This is a small and in development wrapper for a front-end [JS9](https://github.com/ericmandel/js9) application which is a Javascript version of [DS9](http://ds9.si.edu/site/Home.html).

It can be used to create *any number* of JS9 Displays windows running locally, i.e., loading JavaScript in the same notebook of the client or it can load *any number* of JS9 Displays running from the server via socket.io communication.

Create as many instances needed and display a JS9 windows and functionalities. See [Demo](notebooks/Demo.ipynb) for example use.

### Requirements

- Server Side: For now it requires to have a Js9 node server running somewhere (instructions to follow) and  the tornado interface to run JS9 application and API as well. The js file and instructions are in the original repository  [JS9](https://github.com/ericmandel/js9)

    ```
    python js9_web.py
    node Js9Helper.js
    ``` 
    To run the JS9 inside jupyter you'd also need [pyjs9](https://github.com/ericmandel/pyjs9) a nice python wrapper for the javascript functions in JS9.

    ```
    >>> import jjs9
    >>> J = jjs9.Js9Server(root='http://js9-server-running:my-port')
    >>> J.NewDiv()
    >>> J.LoadProxy('url_fits_file.fits')
    >>> J.SetColorMap('red')
    >>> J.DelDiv()
    ```
    Will open a new window 

- Client Side: For now it needs the basic js and css files that contains everything, these can be found in [JS9](https://github.com/ericmandel/js9), in particular `js9-allinone.css` and `js9-allinone.js` need to be in same folder as the root of jupyter notebook. This will change soon

    ```
    >>> import jjs9
    >>> J = jjs9.Js9Local(root='http://localhost:8888/files/')
    >>> J.NewDiv()
    >>> J.Load('local_file_in_server.fits')
    >>> J.SetColorMap('red')
    >>> J.DelDiv()

