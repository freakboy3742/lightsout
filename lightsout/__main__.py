from __future__ import print_function, absolute_import, unicode_literals

import argparse
from datetime import datetime, timedelta, tzinfo
import os.path
import sys

import spotipy
import spotipy.util as util

from .backends import BACKENDS


class AWST(tzinfo):
    """AWST"""
    def __repr__(self):
        return "AWST"

    def utcoffset(self, dt):
        return timedelta(hours=8)

    def tzname(self, dt):
        return "AWST"

    def dst(self, dt):
        return timedelta(hours=8)


def get_creds():
    try:
        creds = {}
        with open(os.path.expanduser('~/.lightsoutrc')) as source_file:
            exec(source_file.read(), creds, creds)
    except Exception as e:
        print("""
Couldn't find your Spotify credentials.

You need to create a file called ".lightsoutrc" in your home directory. This
file must have the following content:

    SPOTIFY_CLIENT_ID='<YOUR CLIENT ID>'
    SPOTIFY_CLIENT_SECRET='<YOUR CLIENT SECRET>'

Substituting your own ID and secret as appropriate. To get a client ID and
secret, visit:

    https://developer.spotify.com/my-applications/#!/applications/create

        """)
        sys.exit(1)

    return creds


def date_time(input):
    return datetime.strptime(input, '%Y-%m-%dT%H:%M:%S%z')


def add_to_playlist(sp, username, track_ids, playlist_id, perpetual_id):
    if playlist_id != 'NONE':
        print("Adding %d tracks to playlist '%s'... " % (len(track_ids), playlist_id), end='')
        sys.stdout.flush()
        sp.user_playlist_add_tracks(username, playlist_id, track_ids)
        print("Done.")
    if perpetual_id:
        print("Adding %d tracks to perpetual playlist... " % len(track_ids), end='')
        sys.stdout.flush()
        sp.user_playlist_add_tracks(username, perpetual_id, track_ids)
        print("Done.")
    print()


def main():
    parser = argparse.ArgumentParser(
        prog='lightsout',
        description='Converts online radio playlist data to playable Spotify playlists.'
    )

    parser.add_argument(
        '-d', '--date',
        help='The date/time to start the playlist (e.g., 2016-05-01T08:00:00+0800 for 8 AM, May 1 2016, AWST). Defaults to yesterday, 8AM AWST.',
        type=date_time,
        default=(datetime.today() - timedelta(hours=24)).replace(hour=8, minute=0, second=0, microsecond=0, tzinfo=AWST())
    )
    parser.add_argument(
        '-l', '--length',
        help='The length of the window to scrape in hours.',
        type=int,
        default=24
    )
    parser.add_argument(
        '-u', '--username',
        help='Your spotify username',
        required=True
    )
    parser.add_argument(
        '-p', '--playlist',
        help='The Spotify playlist ID to add tracks to (NEW creates a new playlist, LIST to show existing playlists).',
        default="NEW"
    )
    parser.add_argument(
        '-P', '--perpetual',
        help='The ID of the perpetual playlist to update.',
    )
    parser.add_argument(
        '-n', '--name',
        help='The name for your Spotify playlist',
    )
    parser.add_argument(
        '-s', '--station',
        dest='station',
        help='The station to scrape',
        choices=BACKENDS.keys(),
        default='doublej'
    )

    creds = get_creds()

    args = parser.parse_args()

    token = util.prompt_for_user_token(
        username=args.username,
        scope='playlist-modify-public',
        client_id=creds['SPOTIFY_CLIENT_ID'],
        client_secret=creds['SPOTIFY_CLIENT_SECRET'],
        redirect_uri='http://localhost:8888/callback'
    )
    sp = spotipy.Spotify(auth=token)

    if args.playlist.lower() == 'list':
        # Retrieve the list of playlists.
        playlists = sp.user_playlists(args.username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == args.username:
                print('%s: %s (%s tracks)' % (
                    playlist['id'],
                    playlist['name'],
                    playlist['tracks']['total'])
                )

    else:
        # Normal query
        print("Searching for songs on %s for %s hours starting %s..." % (
            BACKENDS[args.station]['name'],
            args.length,
            args.date.strftime("%d %b, %Y %H:%M %Z")
        ))
        songs = BACKENDS[args.station]['query'](start=args.date, end=args.date + timedelta(hours=args.length))
        print("Found %s songs." % len(songs))
        print()

        if args.playlist == 'NEW':
            if args.name:
                playlist_name = args.name
            else:
                playlist_name = '%s playlist for %s' % (
                    BACKENDS[args.station]['name'],
                    args.date.strftime('%d %b, %Y')
                )
            print("Creating playlist '%s'... " % playlist_name, end='')
            sys.stdout.flush()
            result = sp.user_playlist_create(args.username, playlist_name, public=True)
            print("%s." % result['id'])
            playlist_id = result['id']
        else:
            playlist_id = args.playlist

        if args.perpetual:
            print("Flushing perpetual playlist... ", end='')
            sys.stdout.flush()
            perpetual_id = args.perpetual
            sp.user_playlist_replace_tracks(args.username, perpetual_id, [])
            print("Done.")

        track_ids = []
        for i, song in enumerate(songs):
            try:
                song['index'] = i + 1
                print("%(index)s: Searching for '%(title)s' by '%(artist)s' (from '%(album)s')... " % song, end='')
                sys.stdout.flush()
                result = sp.search("artist:%(artist)s album:%(album)s track:%(title)s" % song, type="track")
                if result['tracks']['total'] > 0:
                    print("%s" % result['tracks']['items'][0]['id'])
                    track_ids.append(result['tracks']['items'][0]['id'])
                else:
                    print("No match found.")
                    print("... searching without album title... " % song, end='')
                    sys.stdout.flush()
                    result = sp.search("artist:%(artist)s track:%(title)s" % song, type="track")
                    if result['tracks']['total'] > 0:
                        print("%s" % result['tracks']['items'][0]['id'])
                        track_ids.append(result['tracks']['items'][0]['id'])
                    else:
                        print("No match found.")

                # Every 10 tracks found, flush to the playlist.
                if len(track_ids) == 10:
                    add_to_playlist(sp, args.username, track_ids, playlist_id, perpetual_id)
                    track_ids = []
            except Exception as e:
                print("Unexpected error: %s" % e)

        if track_ids:
            add_to_playlist(sp, args.username, track_ids, playlist_id, perpetual_id)


if __name__ == '__main__':
    main()
