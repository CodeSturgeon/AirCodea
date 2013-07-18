# Air Codea
_Because I really just want to use vim & git_

Air Codea is a command line sync tool for use with the Air Code feature of Codea.


## Commands

### Pull
Pull file from Codea overwriting content

### Push
Push file to Codea overwriting content
(Note you cannot make new files like this)

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
