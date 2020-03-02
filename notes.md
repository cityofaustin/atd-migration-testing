# TODO:
- drop estimate and sprints from migrated issues :/
- make sure you're gracefully handling znehub failes on dependency, epics, releases setting
- on last dry run, some product labels were not colored correctly. looks like they were created by default. that's not right.
- warehouse inventory project did not map to a product :/ < fixed
- download new label map!
- set "closed" state implemented. need to test!
- have to link epics, dependencies and releases to atd-data-tech issues :(
- will not link epics, dependencies, or releases to closed issues
- heyyy are you droppping project labels?? you need to append, not replace, i think
- close all migrated issues! have to do that before setting new pipelines!
- some issues may not be in zenhub—must ignore
- not sure if depency output works, since we're dropping nulls. need to test with actual created issues
- make sure all releases already exist. yeesh
- don't process issues with the "migrated" label
- filter out epics, pipelines not in our main workspace
- we're not going to fetch closed dependencies, ok??

## Labels
Update this sheet for the label mapping:
https://docs.google.com/spreadsheets/d/1pTum5oFfDpIo575zAYDPA_bdsEfoElpCO1-HzAU68wk/edit#gid=651251559


## TODO

### GITHUB
-[x] title 
-[x] body
-[x] assignee
-[x] old url
-[x] new url
-[x] milestone
-[x] comments
-[x] labels


### ZENHUB
- estimate // done
- epic // good to go except missing issues derp
- dependency // good to go except missing
- pipeline // need to set
- release // need to set



### PRELAUNCH CHECKLIST
- destination repo correct
- destination repo_id correct
- destination workspace correct
- assignments enabled
- test code removed from pipeline setter
- update source github issues enabled


download open atd-data-tech issues
then they'll be included in the processing
set their new_github_issue number to their issue number 
do not create/update/comment any of them?