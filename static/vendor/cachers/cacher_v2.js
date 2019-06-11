var Cacher = function(url, progressid) {
    this.url = url;
    this.name = murmurhash(url, 7) + '_' + url.split('/').pop();
    this.progressid = progressid;
};

function log(text) {console.log(text);}

Cacher.prototype = {
    url: '',
    name: '',
    size: 0,
    checkedSize: 0,
    encodedurl: '',

    cache: function(cb) {
        var myThis = this;
        if (!this.url) {
            this.closeProgress();
            cb(null);
            return;
        }
        this.checkSize(function(back) {
            myThis.closeProgress();
            if(cb instanceof Error) {
                handleError();
                cb(null);
            } else {
                cb(back);
            }
        });
    },

    //Gets the size of specified url
    checkSize: function(cb) {
        var myThis = this;
        var xhr = new XMLHttpRequest();
        xhr.open("HEAD", this.url, true);
        xhr.onreadystatechange = function() {
            if (this.readyState == this.DONE) {
                myThis.size = parseInt(xhr.getResponseHeader("Content-Length"));
                log(myThis.name + ' size back: ' + myThis.size);
                myThis.checkIfCached(cb);
            }
        };
        xhr.send();
    },
    //gets remote file and writes it to the local storage
    getFile: function(entry, cb) {
        var myThis = this;
        if (this.url != '' && this.url != undefined) {
            if (this.size != this.checkedSize) {
                this.getRemoteFile(this.url, function(blobber) {
                    if(blobber) {
                        myThis.writeToFile(entry, blobber, myThis.getFileURL, cb);
                    } else {
                        cb(null);
                    }
                });
            } else {
                cb(null);
            }
        } else {
            cb(null);
        }
    },
    //Loads Media from remote source
    getRemoteFile: function(url, cb) {
        var myThis = this;
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.responseType = 'blob';
        xhr.addEventListener("progress", function(evt){
            if (evt.lengthComputable){
              var percentComplete = evt.loaded / evt.total;
                if (window.opener && window.opener.document) {
                    window.opener.$('#' + myThis.progressid).css('width', (percentComplete*100)+'%').attr('aria-valuenow', percentComplete*100);
                }
            }
        }, false);
        xhr.send();
        xhr.onload = function() {
            if (xhr.status !== 200) {
                //alert('Unexpected status code ' + xhr.status + ' for ' + url);
                cb(xhr.response);
                return false;
            }
            cb(xhr.response);
        };
    },
    //Checks if media already is cached
    checkIfCached: function(cb) {
        var myThis = this;
        if(this.size == 0) {
            cb(null);
            return;
        }
        window.fileSystem.root.getFile(myThis.name, {}, function(entry) {
            entry.getMetadata(function(metadata) {
                myThis.checkedSize = metadata.size;
                if (myThis.size != myThis.checkedSize) {
                    log('Size diff, creating file: ' + myThis.name);
                    myThis.createFile(myThis.name, cb);
                } else {
                    log('Already cached ' + myThis.url);
                    myThis.getFileURL(myThis.name, cb);
                }
            });
        }, function(error) {
            log('Cached file not found, creating: ' + myThis.name);
            myThis.createFile(myThis.name, cb);
        });
    },
    //Creates file on the filesystem
    createFile: function(path, cb) {
        var myThis = this;
        window.fileSystem.root.getFile(path, { create: true },
            function(fileEntry) {
                //log(fileEntry);
                log('Created file: ' + fileEntry.fullPath);
                myThis.getFile(fileEntry, cb);
            }, cb);
    },
    //Writes media to file
    writeToFile: function(entry, blob, cb, cb2) {
        var myThis = this;
        entry.createWriter(function(fileWriter) {
            fileWriter.onwriteend = function() {
                log('Wrote to file ' + entry.fullPath);
                cb(entry.fullPath, cb2);

            };
            fileWriter.onerror = function(e) {
                log('Write failed: ' + e.toString());
            };
            // Create a new Blob and write it to file
            fileWriter.write(blob);
        }, cb);
    },
    //creates uri encoded path
    getFileURL: function(path, cb) {
        var myThis = this;
        window.fileSystem.root.getFile(path, {}, function(fileEntry) {
            var url = fileEntry.toURL();
            myThis.encodedurl = url;
            cb(myThis.encodedurl);
        }, cb);

    },
    closeProgress: function() {
        if (window.opener && window.opener.document) {
            window.opener.$('#' + this.progressid).parents(':eq(2)').hide();
        }
    }

};



/**
 * JS Implementation of MurmurHash3 (r136) (as of May 20, 2011)
 *
 * @author <a href="mailto:gary.court@gmail.com">Gary Court</a>
 * @see http://github.com/garycourt/murmurhash-js
 * @author <a href="mailto:aappleby@gmail.com">Austin Appleby</a>
 * @see http://sites.google.com/site/murmurhash/
 *
 * @param {string} key ASCII only
 * @param {number} seed Positive integer only
 * @return {number} 32-bit positive integer hash
 */

function murmurhash(key, seed) {
    var remainder, bytes, h1, h1b, c1, c1b, c2, c2b, k1, i;

    remainder = key.length & 3; // key.length % 4
    bytes = key.length - remainder;
    h1 = seed;
    c1 = 0xcc9e2d51;
    c2 = 0x1b873593;
    i = 0;

    while (i < bytes) {
        k1 =
            ((key.charCodeAt(i) & 0xff)) |
            ((key.charCodeAt(++i) & 0xff) << 8) |
            ((key.charCodeAt(++i) & 0xff) << 16) |
            ((key.charCodeAt(++i) & 0xff) << 24);
        ++i;

        k1 = ((((k1 & 0xffff) * c1) + ((((k1 >>> 16) * c1) & 0xffff) << 16))) & 0xffffffff;
        k1 = (k1 << 15) | (k1 >>> 17);
        k1 = ((((k1 & 0xffff) * c2) + ((((k1 >>> 16) * c2) & 0xffff) << 16))) & 0xffffffff;

        h1 ^= k1;
        h1 = (h1 << 13) | (h1 >>> 19);
        h1b = ((((h1 & 0xffff) * 5) + ((((h1 >>> 16) * 5) & 0xffff) << 16))) & 0xffffffff;
        h1 = (((h1b & 0xffff) + 0x6b64) + ((((h1b >>> 16) + 0xe654) & 0xffff) << 16));
    }

    k1 = 0;

    switch (remainder) {
        case 3:
            k1 ^= (key.charCodeAt(i + 2) & 0xff) << 16;
        case 2:
            k1 ^= (key.charCodeAt(i + 1) & 0xff) << 8;
        case 1:
            k1 ^= (key.charCodeAt(i) & 0xff);

            k1 = (((k1 & 0xffff) * c1) + ((((k1 >>> 16) * c1) & 0xffff) << 16)) & 0xffffffff;
            k1 = (k1 << 15) | (k1 >>> 17);
            k1 = (((k1 & 0xffff) * c2) + ((((k1 >>> 16) * c2) & 0xffff) << 16)) & 0xffffffff;
            h1 ^= k1;
    }

    h1 ^= key.length;

    h1 ^= h1 >>> 16;
    h1 = (((h1 & 0xffff) * 0x85ebca6b) + ((((h1 >>> 16) * 0x85ebca6b) & 0xffff) << 16)) & 0xffffffff;
    h1 ^= h1 >>> 13;
    h1 = ((((h1 & 0xffff) * 0xc2b2ae35) + ((((h1 >>> 16) * 0xc2b2ae35) & 0xffff) << 16))) & 0xffffffff;
    h1 ^= h1 >>> 16;

    return h1 >>> 0;
}
