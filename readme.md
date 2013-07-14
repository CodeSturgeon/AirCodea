# Air Codea
_Because I really just want to use vim & git_

Air Codea is a command line sync tool for use with the Air Code feature of Codea.


## Commands

### Pull
Pull file from Codea overwriting content

### Push
Push file to Codea overwirting content
(Note you cannot make new files like this)

### Sync (Default)
Try to judge which way the files should go. If in doubt do nothing.


## Config
INI style file

    [connection]
    ip = <IP given by Codea>
    port = <Port given by Codea>
    project = <Project this folder syncs with>
