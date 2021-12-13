# CHANGELOG
### Deebee Bot
+ **0.1**: simple text based bot created with manual emote reply
+ **0.2_01**: added emote lookup class for emote reply automation
+ **0.2_02**: changed emote lookup class to simple method
+ **0.2_03**: added error reporting when emote not found
+ **0.3**: overhaul with entire code: simplified the conditional statements
+ **0.4**: added weather command see Weather app updates
+ **1.0**: successfuly migrated commands to `discord.ext.commands` API
+ **1.1**: added `roll` command to roll dice.
+ **1.2**: changed how message reaction worked
+ **1.2_01**: made `weather`, and `keep_alive` modules optional
+ **1.3**: added Discord Interactions
+ **1.3_01**: added `days-before-xmas` daily countdown till christmas
+ **1.3_02**: added if-else for `days-before-xmas` for less than or equal to 35 days
+ **1.3_03**: added `ext.commands` error handlers
+ **1.3_04**: major overhaul to the `roll` command
#
### Weather app
+ **0.1**: simple app to pull weather images, then convert to video
+ **0.2**: added daily weather report starting from `00.00` to `20.00`
+ **0.2_01**: changed timezone from `UTC` to `Asia/Manila`
+ **0.2_02**: changed time loop from `1 hour` to `5 minutes`
+ **0.2_03**: reverted back to `1 hour` from `5 minutes`
+ **0.3**: added 2-hour interval mid-day in addition to 4-hour interval daily
+ **0.3_01**: code cleanup and absolute timing for 2-hour interval
+ **0.3_02**: fixed weather loop clean up routine
#
### Web Server
+ **0.1**: added redirect to uptimerobot monitor
+ **0.2**: added SimpleLogin module pointing to Discord WebHook form
+ **0.3**: added URL redirection
+ **0.4**: migrated all redirect to [reloc.tk](https://www.reloc.tk/ "https://www.reloc.tk/")
+ **1.0**: site shows simple page to invite bot
#
### Virus Scanning
A Passive virus scan with the help of VirusTotal API. Alerts the channel if and only if an attachment or link has/is a malware.
+ To do
+ Development links: [Official VirusTotal API for Python](https://github.com/VirusTotal/vt-py/ "vt-py")
+ **0.1**: added file scanning

#
#

# FUTURE PLANS
### Currently Doing
+ ~~Main Mission: I need context! - Find out how SlashContext works.~~
+ ~~Figure out how to make discord file attachment link readable by VirusTotal~~
+ ~~Get discord file attachment hashes~~
  + ~~Submit the file hashes to VirusTotal~~
### To Do
###### **_Expand items on To Do list. Be more concise._**
+ Change how file input is sent (discord file links don't work -> Need premium)
+ Implement attachment virus scanning with VirusTotal API
  + Additionally, Link malware scanning
# 
### Halted
+ Integrate Himawari-8 weather images
  + add `entire day` capability
    + use https://www.data.jma.go.jp/mscweb/data/himawari/list_r2w.html for image data
+ Integrate word definition lookup
  + ~~use PyDictionary~~ ~~Research for alternatives~~
  + [spaCy](https://spacy.io/ "spaCy") is an open source natural language processing

#
#

# URL Redirects
###### Migrated
+ [reloc.tk/webhook/](https://www.reloc.tk/webhook/ "https://www.reloc.tk/webhook/") - Discord WebHook documentation
+ [reloc.tk/ms-safemode/](https://www.reloc.tk/ms-safemode/ "https://www.reloc.tk/ms-safemode/") - Microsoft SafeMode instructions
+ [reloc.tk/ms-hiddenfiles/](https://www.reloc.tk/ms-hiddenfiles/ "https://www.reloc.tk/ms-hiddenfiles/") - Microsoft enable hidden files instructions
+ [reloc.tk/ms-restorepoint/](https://www.reloc.tk/ms-restorepoint/ "https://www.reloc.tk/ms-restorepoint/") - Tutorial for how to create restore points in windows
+ [reloc.tk/ms-scanrepair/](https://www.reloc.tk/ms-scanrepair/ "https://www.reloc.tk/ms-scanrepair/") - Possible reasons for persistent start-up auto repair
+ [reloc.tk/win10-kms/](https://www.reloc.tk/win10-kms/ "https://www.reloc.tk/win10-kms/") - Windows 10 KMS licenses