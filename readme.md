# Air Codea
_Because I really just want to use vim & git_

Air Codea is a command line sync tool for use with the Air Code feature of Codea.


## Commands

### Pull
Pull file from Codea overwriting content

_NOTE: 'all' will sync all known files_

### Push
Push file to Codea overwriting content

_NOTE: you cannot make new files like this_

_NOTE: 'all' will sync all known files_

### Sync (Default)
Try to judge which way the files should go. If in doubt do nothing.

First list the files that Codea knows of, then:
- If the file is not downloaded, pull the file
- Get the last known hash of the file, if we don't have one, skip the file
- If the file is not changed locally or remotely, skip the file
- If the file is not changed locally but it remotely, pull the file
- If the file is changed locally and not remotely, push the file
- The file is in conflict, skip the file

Conflicts and unknown hashes are easy solved with a manual Push/Pull of the file.


## Config
INI style file.

    [connection]
    ip = <IP given by Codea>
    port = <Port given by Codea>
    project = <Project this folder syncs with>

Note that hashes are saved in this file automatically.


## Issues

The air code server is a bit buggy. There are times when Codea will delete files (O_O) when you use air code. For whatever reason AirCodea trips that bug more frequently than using a browser. Keep this in mind when pushing and syncing. I keep things checked in to git at pretty much all times to mitigate the issue.
