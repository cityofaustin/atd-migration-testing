# TODO:
- Do we have all the repos??
- filter out epics, pipelines not in our main workspace
- get closed issues that are in epics
- comments?
- setting of dependencies?
- what about linked PRs?
- validate/lookup milestones
- create special "migrated" label
- how to handle miletsones that don't exist in dest?
- you're nulling out assignees for testing! 
- you can't apply the migrated label to migrated labels because they won't have the "product" labels???

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


## fields
- title
- body
- assignee
- estimate
- epic
- old url
- new url
- milestone
- pipeline
- release
- attachements?