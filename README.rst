Lights Out
==========

| Lights out! Guerrilla radio! Turn that s*** up!
|    - Rage Against the Machine

Lights Out is a tool to convert radio station online playlists into Spotify playlists.

Usage
-----

You can install Lights Out using pip::

    $ pip install lightsout

Before you can use Lights Out for the first time, you'll need to register an
application with Spotify. To do this, visit `the Spotify Developer portal`_
and provide some application details. In return, you'll get two credentials:
a ``SPOTIFY_CLIENT_ID`` and a ``SPOTIFY_CLIENT_SECRET``.

.. note:

    When you register your application, you'll be prompted for a Redirect URL.
    Use ``http://localhost:8888`` - this shouldn't work in a browser, but that
    doesn't matter.

.. _the Spotify Developer portal: https://developer.spotify.com/my-applications/#!/applications/create]

Then, create a file called ``.lightsoutrc`` in your home directory. This file
should contain your two Spotify credentials::

    SPOTIFY_CLIENT_ID='<your credentials here>'
    SPOTIFY_CLIENT_SECRET='<your credentials here>'

Substitute your own credentials as appropriate.

Then, you can run Lights Out::

    $ lightsout -u <your Spotify username>

Substitute your own spotify username as appropriate.


If this is the first time you have run Lights Out, you'll be redirected to
a browser, prompted to log into your Spotify account, and authorize your
application. This will redirect to the ``localhost:8888`` URL you specified
as the redirect URL for your application. Your browser won't be able to load
this page - but that's OK - all you need is the URL. Copy the URL, and
paste it into the console window where Lights Out is running.

Once you've done this, Lights Out will pull down the data for the playlist,
search Spotify for tracks matching the songs on the playlist, and construct a
Spotify playlist for those songs.

Options
-------

There are a number of options you can also pass to ``lightsout``:

* You can specify a station other than ``doublej`` using the ``-s`` option::

    $ lightsout -u <your Spotify username> -s triplej

  See ``--help`` for the list of available channels

* You can specify the starting date/time for the playlist search with the
  ``-d`` option. If you specified::

    $ lightsout -u <your Spotify username> -d '2016-05-01T10:30:00+0800'

  the search would be for 10:30 AM, May 1 2016, AWST.

* You can specify the size of the playlist window. By default, searches will be for 24 hours,
  but you can specify any length in hours with the ``-l`` option. For example::

    $ lightsout -u <your Spotify username> -l 4

  would generate a 4 hour playlist.

* You can specify that you want to append to an existing playlist using the
  ``-p`` option::

    $ lightsout -u <your Spotify username> -p 7wkac9khk9ssablyH9kRsC

  You can find the list of existing playlists by specifying ``LIST`` as the playlist::

    $ lightsout -u <your Spotify username> -p LIST

* If you want to maintain a perpetual playlist (a playlist that is replaced,
  rather than appended to), you can specify that playlist using the ``-P``
  option::

    $ lightsout -u <your Spotify username> -p 7wkac9khk9ssablyH9kRsC

  If you want to update a perpetual playlist, but *not* append to an existing
  playlist, you can specify ``-p NONE`` in addition to ``-P``::

    $ lightsout -u <your Spotify username> -p NONE -P 7wkac9khk9ssablyH9kRsC


Extending Lights Out
--------------------

Lights out currently has support for the following stations:

* ABC Australia

  * Double J

  * Triple J

  * Unearthed

  * ABC Classic

  * ABC Classic 2

  * ABC Jazz

  * ABC Country

  * ABC Extra

To add a new station station, you need to add a single function to
``lightsout/backends.py``. This function takes two arguments: a start
datetime and an end datetime. The function must return a list of
dictionaries, each dictionary describing a single track::

    [
        {'track': 'Paranoid Android', 'artist': 'Radiohead', 'album': 'OK Computer'},
        {'track': 'mogwai fear satan', 'artist': 'Mogwai', 'album': 'Young Team'},
        {'track': 'Brennisteinn', 'artist': 'Sigur Rós', 'album': 'Kveikur'},
        ...
    ]
