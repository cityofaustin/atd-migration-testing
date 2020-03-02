# Notes

### PRELAUNCH CHECKLIST

- destination repo correct?
- destination repo_id correct?
- destination workspace correct?
- assignments enabled?
- test code removed from pipeline setter?
- update source github issues enabled?

- i think we need to create labels with the "new" action....they might not exist on issues but will soon need to
- test epic foo
- test attachments
- make sure you're gracefully handling zenhub fails on dependency, epics, releases
- on last dry run, some product labels were not colored correctly. looks like they were created by default. how is that possible?
- close all migrated issues BEFORE setting new pipelines (because, positions)
- some issues may not be in zenhub—-must ignore
- make sure all releases already exist. yeesh
- don't process issues with the "migrated" label
- filter out epics, pipelines not in our main workspace
- we're not going to fetch closed dependencies, ok??

## Labels
Update this sheet for the label mapping:
https://docs.google.com/spreadsheets/d/1pTum5oFfDpIo575zAYDPA_bdsEfoElpCO1-HzAU68wk/edit#gid=651251559

## TODO

### GITHUB
- title  [done]
- body [done]
- assignee [done]
- old url [done]
- new url [done]
- milestone [done]
- comments [done]
- labels [done]


### ZENHUB
- estimate [done]
- epics [retest w/ new existing-issue logic]
- dependency [done]
- pipeline [done]
- release [staged/ need to set]