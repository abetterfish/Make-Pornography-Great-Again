"""
Frank Hrach
DownloadManager.py
"""

import urllib
import os
import QueuedFile
import threading

class DownloadManager(object):
    """
    Download the supplied url and saves it to the supplied path
    """
    #maxDownloads
    #currentDownloads;
    #run
    #queue

    def __init__(self, event):
        self.max_downloads = 4
        self.current_downloads = 0
        self.queue = []
        self.should_run = True
        self.event = event


    def enqueue_file(self, url, file_name, extension, destination):
        """
        Adds a file to the queue
        """
        self.queue.append(
            QueuedFile.QueuedFile(url, file_name, extension, destination))

    def start_downloader(self):
        """
        Manages 4 downloads with a queue.
        Should be started as a thread
        """

        # run until main thread says it should no longer run
        while self.should_run:

            if self.current_downloads >= self.max_downloads:
                thread = threading.Thread(target=download, args=self.queue.pop())
            else:
                # wait until download thread notifies all
                self.event.wait()


def download(queued_file, event):
    """
    Downloads
    """
    path = os.path.join(queued_file.destination, queued_file.file_name \
        + "." + queued_file.extension)

    # download only if the file does not already exist
    if not os.path.exists(path):
        urllib.urlretrieve(queued_file.url + queued_file.file_name \
            + queued_file.extension, path)

    # Notify the controller that we have finished
    event.notifyAll()