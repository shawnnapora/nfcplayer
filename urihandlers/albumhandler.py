import subprocess
from pathlib import Path


class AlbumHandler:
    Scheme = "nfcalbum"

    def __init__(self, base_path):
        self._base_path = Path(base_path).resolve()
        if not self._base_path.exists:
            raise Exception("provided base path does not exist")

    def handle_uris(self, uris):
        album_paths = []
        for uri in uris:
            self.validate_uri(uri)
            album_path = self._uri_path_to_real_path(uri)
            album_paths.append(album_path)
        self._play(album_paths)

    def validate_uri(self, uri):
        try:
            assert uri.netloc == '', "location"
            assert uri.params == '', "params"
            assert uri.query == '', "query"
            assert uri.fragment == '', "fragment"
        except AssertionError as error:
            raise Exception(f"uri may not have component {error}")

        # invoke and see if it throws
        self._uri_path_to_real_path(uri)

    @staticmethod
    def _play(album_paths):
        # strawberry is nice that it will run normally if not running, or if running
        # it acts as a remote for itself and promptly exits. So, we can just fire this
        # and forget about it. If this process exits, strawberry will continue running.
        invocation = ["strawberry", "-p", "-l"] + album_paths
        subprocess.Popen(invocation, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _uri_path_to_real_path(self, uri):
        album_path = (self._base_path / uri.path).resolve()

        # enforce both that the resolved path is in the form of artist/album and doesn't
        # escape from the base path with cute ".." tricks:
        idx = album_path.parents.index(self._base_path)
        if idx != 1:
            raise Exception(f"uri {uri.path} is not in the form 'Artist/Album'")

        if not album_path.exists():
            raise Exception(f"uri path {uri.path} does not exist in {self._base_path}.")

        return album_path.as_posix()
