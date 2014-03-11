__author__ = 'Joe Linn'

import pylastica.request
import pylastica.client
import pylastica.exception


class Snapshot(object):
    """
    @see http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html
    """

    def __init__(self, client):
        """
        @param client: a pylastica Client object
        @type client: pylastica.client.Client
        """
        super(Snapshot, self).__init__()
        if not isinstance(client, pylastica.client.Client):
            raise TypeError("client must be a Client object: %r" % client)
        self._client = client

    def register_repository(self, name, repository_type, settings=None):
        """
        Create a snapshot repository
        @param name: the name of the repository
        @type name: str
        @param repository_type: the repository type ("fs" for file system)
        @type repository_type: str
        @param settings: Additional repository settings. If type "fs" is used, the "location" setting must be provided.
        @type settings: dict
        @return:
        @rtype: pylastica.response.Response
        """
        data = {"type": repository_type}
        if settings is not None:
            if not isinstance(settings, dict):
                raise TypeError("settings must be a dict: %r" % settings)
            data["settings"] = settings
        return self.request(name, pylastica.request.Request.PUT, data)

    def get_repository(self, name):
        """
        Retrieve a repository record by name
        @param name: the name of the desired repository
        @type name: str
        @return:
        @rtype: dict
        """
        response = self.request(name)
        if not response.is_ok() and response.status == 404:
            raise pylastica.exception.NotFoundException("repository '%s' does not exist." % name)
        return response.data[name]

    def get_repositories(self):
        """
        Retrieve all repository records
        @return:
        @rtype: dict
        """
        return self.request("_all").data

    def create_snapshot(self, repository, name, options=None, wait_for_completion=False):
        """
        Create a new snapshot
        @param repository: the name of the repository in which this snapshot should be stored
        @type repository: str
        @param name: the name of this snapshot
        @type name: str
        @param options: optional settings for this snapshot
        @type options: dict
        @param wait_for_completion: if True, the request will not return until the snapshot operation is complete
        @type wait_for_completion: bool
        @return:
        @rtype: pylastica.response.Response
        """
        query = None
        if wait_for_completion:
            query = {"wait_for_completion": "true"}
        return self.request("%s/%s" % (repository, name), pylastica.request.Request.PUT, options, query)

    def get_snapshot(self, repository, name):
        """
        Retrieve data regarding a specific snapshot
        @param repository: the name of the repository from which to retrieve the snapshot
        @type repository: str
        @param name: the name of the desired snapshot
        @type name: str
        @return:
        @rtype: dict
        """
        response = self.request("%s/%s" % (repository, name))
        if not response.is_ok() and response.status == 404:
            raise pylastica.exception.NotFoundException("snapshot '%s' in repository '%s' does not exist." % (name, repository))
        return response.data['snapshots'][0]

    def get_all_snapshots(self, repository):
        """
        Retrieve data regarding all snapshots in the given repository
        @param repository: the repository name
        @type repository: str
        @return:
        @rtype: pylastica.response.Response
        """
        return self.request("%s/_all" % repository).data

    def delete_snapshot(self, repository, name):
        """
        Delete a snapshot
        @param repository: the repository in which the snapshot resides
        @type repository: str
        @param name: the name of the snapshot to be deleted
        @type name: str
        @return:
        @rtype: pylastica.response.Response
        """
        return self.request("%s/%s" % (repository, name), pylastica.request.Request.DELETE)

    def restore_snapshot(self, repository, name, options=None, wait_for_completion=False):
        """
        Restore a snapshot
        @param repository: the name of the repository
        @type repository: str
        @param name: the name of the snapshot
        @type name: str
        @param options: options for the restore operation
        @type options: dict
        @param wait_for_completion: if True, the HTTP request will not return until the restore operation is complete
        @type wait_for_completion: bool
        @return:
        @rtype: pylastica.response.Response
        """
        query = None
        if wait_for_completion:
            query = {"wait_for_completion": "true"}
        return self.request("%s/%s/_restore" % (repository, name), pylastica.request.Request.POST, options, query)

    def request(self, path, method=pylastica.request.Request.GET, data=None, query=None):
        """
        Perform a snapshot request
        @param path: the URL
        @type path: str
        @param method: the HTTP method
        @type method: str
        @param data: request body data
        @type data: dict
        @param query: query string parameters
        @type query: dict
        @return:
        @rtype: pylastica.response.Response
        """
        return self._client.request("/_snapshot/%s" % path, method, data, query)