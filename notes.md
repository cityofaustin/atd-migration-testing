# TODO:
- it would seem that the atd-monorepo-testing is not ready to accept labels via api
- not sure if depency output works, since we're dropping nulls. need to test with actual created issues
- make sure all releases already exist. yeesh
- close source issues?
- don't process issues with the "migrated" label
- Do we have all the repos??
- filter out epics, pipelines not in our main workspace
- get closed issues that are in epics
- comments?
- we're not going to fetch closed dependencies, ok??
- what about linked PRs?
- validate/lookup milestones
- how to handle miletsones that don't exist in dest?
- you're nulling out assignees for testing! 
- need to warn folks that they're going to get a shitload of notifications

## Labels
Update this sheet for the label mapping:
https://docs.google.com/spreadsheets/d/1pTum5oFfDpIo575zAYDPA_bdsEfoElpCO1-HzAU68wk/edit#gid=651251559


FLOW:
- add missing labels
- and that all labels are mapped to products
- only open issues!? no. migrate closed. - what about epics with closed issues???
- get all issues and zenhub data
- write to JSON
- create all issues in github (milestones, labels, assignees, title, body, state)
- each time issue is created:
    - close/link to new issues/apply "migrated" label
    - write to JSON
- convert issues to epics
- add issues to epics
- move issuses to pipeline
- set a special migrated label!


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
- estimate // need to set
- epic // need to create
- dependency // need to create
- pipeline // need to set
- release // need to set