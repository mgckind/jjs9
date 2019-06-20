## JJS9

This is a small and in development wrapper for a front-end [JS9](https://github.com/ericmandel/js9) application which is a Javascript version of [DS9](http://ds9.si.edu/site/Home.html).

It can be used to create *any number* of JS9 Displays windows running locally, i.e., loading JavaScript in the same notebook of the client or it can load *any number* of JS9 Displays running from the server via socket.io communication.

Create as many instances needed and display a JS9 windows and functionalities. See [Demo](notebooks/Demo.ipynb) for example use.

### Installation

- Server Side: For now it requires a python server with [tornado](http://www.tornadoweb.org/en/stable/) running JS9 as a webpage and another [node](https://nodejs.org/en/) server running JS9 server-side helper. 
 
    - Installing python server: 
        - Clone [JS9](https://github.com/ericmandel/js9) from the original repository
        - Replace the file index.html with the index.html file from [jjs9](https://github.com/mgckind/jjs9)
        - Put the file js9_web.py from [jjs9](https://github.com/mgckind/jjs9) in the same directory as the js9 files and index.html
        - Choose an available port (the default is 8000) to run the JS9 python server with
          ```
          python js9_web.py
          ```
    - Installing node server:
        - Follow the instructions from JS9 [helper](https://github.com/ericmandel/js9/blob/master/help/helper.html)
        - js9Prefs.json is used to set the helper preferences. Change the helperport to an available port for the node server. This has to be different from the one used for the python server.
        - Start the node server-side helper with
          ```
          node js9Helper.js
          ``` 
- Client Side:
    To run the JS9 inside jupyter you'd also need [pyjs9](https://github.com/ericmandel/pyjs9) a nice python wrapper for the javascript functions in JS9. If you have JS9 server set up and a Jupyter notebook running on a local computer, you can start using jjs9 the following commands. All pyjs9 API's are compatible with jjs9.

    ```
    >>> import jjs9
    >>> jjs9.NewDiv()
    >>> J = jjs9.Js9Server(root='http://js9-server-running:my-port')
    >>> J.LoadProxy('url_fits_file.fits')
    >>> J.SetColorMap('red')
    >>> J.DelDiv()
    ```
    This opens a new JS9 iframe in a Jupyter notebook cell. Each NewDiv of JS9 requires a new socket connection with jjs9.Js9Server().
    
    
    Alternatively, there is an option without connecting to a JS9 remote server. This option is for users who only need the basic functionalities of JS9, or users who cannot connect to a remote JS9 server, or users who run Jupyter notebook remotely on a server. For now it needs the basic js and css files that contains everything. These can be found in [JS9](https://github.com/ericmandel/js9), in particular `js9-allinone.css` and `js9-allinone.js` need to be in same folder as the root of jupyter notebook. If JS9 does not load properly or Javascript gives error adding output, put these two files into /.jupyter/custom/ of the computer's home directory and rename them as custom.css and custom.js. Now if Jupyter notebook is restarted, JS9 should load with Js9Local.

    ```
    >>> import jjs9
    >>> jjs9.init_js9=True
    >>> J = jjs9.Js9Local(root='http://localhost:8888/')
    >>> J.NewDiv()
    >>> J.Load('local_file_in_server.fits')
    >>> J.SetColorMap('red')
    >>> J.DelDiv()
    ```
