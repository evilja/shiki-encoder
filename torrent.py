
"magnet:?xt=urn:btih:a0848387b76f302984c44ab4dabfaec7b19bdd2c&dn=%5BErai-raws%5D%20Tougen%20Anki%20-%2012%20%5B480p%20CR%20WEB-DL%20AVC%20AAC%5D%5BMultiSub%5D%5B7807D287%5D&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"

from aiotorrent import Torrent, DownloadStrategy
async def get_torrent(a, b):
    torrent = Torrent(a)
    await torrent.init()
    await torrent.download(torrent.files[0], strategy=DownloadStrategy.SEQUENTIAL)