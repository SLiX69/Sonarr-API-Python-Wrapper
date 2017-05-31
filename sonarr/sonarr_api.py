# -*- coding: utf-8 -*-

import requests


class SonarrAPI(object):

    def __init__(self, host_url, api_key):
        """Constructor requires Host-URL and API-KEY"""
        self.host_url = host_url
        self.api_key = api_key


    # ENDPOINT CALENDAR
    def get_calendar(self):
        # optional params: start (date) & end (date)
        """Gets upcoming episodes, if start/end are not supplied episodes airing today and tomorrow will be returned"""
        res = self.request_get("{}/calendar".format(self.host_url))
        return res.json()


    # ENDPOINT COMMAND
    def command(self):
        pass



    # ENDPOINT DISKSPACE
    def get_diskspace(self):
        """Return Information about Diskspace"""
        res = self.request_get("{}/diskspace".format(self.host_url))
        return res.json()


    # ENDPOINT EPISODE
    def get_episodes_by_series_id(self, series_id):
        """Returns all episodes for the given series"""
        res = self.request_get("{}/episode?seriesId={}".format(self.host_url, series_id))
        return res.json()

    def get_episode_by_episode_id(self, episode_id):
        """Returns the episode with the matching id"""
        res = self.request_get("{}/episode/{}".format(self.host_url, episode_id))
        return res.json()

    def upd_episode(self, data):
        #TEST THIS
        """Update the given episodes, currently only monitored is changed, all other modifications are ignored"""
        '''NOTE: All parameters (you should perform a GET/{id} and submit the full body with the changes,
        as other values may be editable in the future.'''
        res = self.request_put("{}/episode".format(self.host_url, data))
        return res.json()


    # ENDPOINT EPISODE FILE
    def get_episode_files_by_series_id(self, series_id):
        """Returns all episode files for the given series"""
        res = self.request_get("{}/episodefile?seriesId={}".format(self.host_url, series_id))
        return res.json()

    # TEST THIS
    def get_episode_file_by_episode_id(self, episode_id):
        """Returns the episode file with the matching id"""
        res = self.request_get("{}/episodefile/{}".format(self.host_url, episode_id))
        return res.json()

    # TEST THIS
    def rem_episode_file_by_episode_id(self, episode_id):
        """Delete the given episode file"""
        res = self.request_del("{}/episodefile/{}".format(self.host_url, episode_id))
        return res.json()


    # ENDPOINT HISTORY
    # DOES NOT WORK
    def get_history(self):
        """Gets history (grabs/failures/completed)"""
        res = self.request_get("{}/history".format(self.host_url))
        return res.json()


    # ENDPOINT WANTED MISSING
    # DOES NOT WORK
    def get_wanted_missing(self):
        """Gets missing episode (episodes without files)"""
        res = self.request_get("{}/wanted/missing/".format(self.host_url))
        return res.json()


    # ENDPOINT QUEUE
    def get_queue(self):
        """Gets current downloading info"""
        res = self.request_get("{}/queue".format(self.host_url))
        return res.json()


    # ENDPOINT PROFILE
    def get_quality_profiles(self):
        """Gets all quality profiles"""
        res = self.request_get("{}/profile".format(self.host_url))
        return res.json()


    # ENDPOINT RELEASE


    # ENDPOINT RELEASE/PUSH


    # ENDPOINT ROOTFOLDER
    def get_root_folder(self):
        """Returns the Root Folder"""
        res = self.request_get("{}/rootfolder".format(self.host_url))
        return res.json()


    # ENDPOINT SERIES
    def get_series(self):
        """Return all series in your collection"""
        res = self.request_get("{}/series".format(self.host_url))
        return res.json()

    def get_series_by_series_id(self, series_id):
        """Return the series with the matching ID or 404 if no matching series is found"""
        res = self.request_get("{}/series/{}".format(self.host_url, series_id))
        return res.json()

    def get_series_to_add(self, tvdbId):
        """Searches for new shows on trakt and returns Series object to add"""
        res = self.request_get("{}/series/lookup?term={}".format(self.host_url, 'tvdbId:' + str(tvdbId)))
        s_dict = res.json()[0]

        # get root folder path
        root = self.get_root_folder()[0]['path']
        add_json = {
            'title': s_dict['title'],
            'seasons': s_dict['seasons'],
            'path': root + s_dict['title'],
            'qualityProfileId': 4,         # 4 = 1080p, not sure how to determine id from sn.get_quality_profiles())
            'seasonFolder': True,
            'monitored': True,
            'tvdbId': tvdbId,
            'images': s_dict['images'],
            'titleSlug': s_dict['titleSlug'],
            "addOptions": {
                          "ignoreEpisodesWithFiles": True,
                          "ignoreEpisodesWithoutFiles": True
                        }
                    }

        return add_json

    def add_series(self, tvdvId):
        """Add a new series to your collection"""
        series_to_add = self.get_series_to_add(tvdbId=tvdvId)
        res = self.request_post("{}/series".format(self.host_url), data=series_to_add)
        return res.json()

    def upd_series(self, data):
        """Update an existing series"""
        res = self.request_put("{}/series".format(self.host_url), data)
        return res.json()

    def rem_series(self, series_id, rem_files=False):
        """Delete the series with the given ID"""
        # File deletion does not work
        data = {
            # 'id': series_id,
            'deleteFiles': 'true'
        }
        res = self.request_del("{}/series/{}".format(self.host_url, series_id), data)
        return res.json()


    # ENDPOINT SERIES LOOKUP
    def lookup_series(self, query):
        """Searches for new shows on trakt"""
        res = self.request_get("{}/series/lookup?term={}".format(self.host_url, query))
        return res.json()


    # ENDPOINT SYSTEM-STATUS
    def get_system_status(self):
        """Returns the System Status"""
        res = self.request_get("{}/system/status".format(self.host_url))
        return res.json()



    # REQUESTS STUFF
    def request_get(self, url, data={}):
        """Wrapper on the requests.get"""
        headers = {
            'X-Api-Key': self.api_key
        }
        res = requests.get(url, headers=headers, json=data)
        return res

    def request_post(self, url, data):
        """Wrapper on the requests.post"""
        headers = {
            'X-Api-Key': self.api_key
        }
        res = requests.post(url, headers=headers, json=data)
        return res

    def request_put(self, url, data):
        """Wrapper on the requests.put"""
        headers = {
            'X-Api-Key': self.api_key
        }
        res = requests.put(url, headers=headers, json=data)
        return res

    def request_del(self, url, data):
        """Wrapper on the requests.delete"""
        headers = {
            'X-Api-Key': self.api_key
        }
        res = requests.delete(url, headers=headers, json=data)
        return res
