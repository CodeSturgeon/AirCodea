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

The code of the project was recently re-written, switching the update mechanism from raw HTTP calls to PhantomJS automation. This was mainly to get around the [tab deletion bug](https://bitbucket.org/TwoLivesLeft/core/issue/267/air-code-deletes-all-tabs-but-main) and frequent Codea crashes the raw calls triggered. However it does give the added ability to detect syntax problems.

Sadly the switch to PhantomJS hasn't helped much with the crash problems.
