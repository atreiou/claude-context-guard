# COMMENTS.md — User's Verbatim Comments Log
# THIS FILE IS SACRED. EVERY COMMENT THE USER MAKES MUST BE LOGGED HERE VERBATIM WITH TIMESTAMP
# FAILURE TO PRESERVE USER COMMENTS IS AS DANGEROUS AS DELETING CORE FILES
#
# PURPOSE: Safety net against context loss. Comments stay here until they've been fully actioned
# (turned into decisions in DECISIONS.md, tasks in TASK_REGISTRY.md, or file changes).
# Once actioned, comments can be removed. This file ensures a fresh session can
# understand the user's actual intent, not just what was done.
#
# Format: Timestamp | Session | Verbatim comment
# Claude MUST append to this file every time the user provides direction, feedback, or decisions

---

## Session 6 — 2026-03-27/28

> [2026-03-27] "the repo version should be blank and consumer grade and neutral at all times — that should be a rule: including any private info, or any plans about the development of CCG, would be considered a bad failure of professionalism as anyone checking out the codebase in the opensource repo, would see it as a mistake, or see things they shouldn't." — Rob on public repo hygiene. **Actioned:** D-005.

> [2026-03-27] "your job in this conversation is to write in improvements and bug fixes, then push to the public repo clean, and then update all other instances in the root /software folder — I don't want to keep having to ask you to do that." — Rob on CCG update workflow. **Actioned:** D-007.

> [2026-03-27] "This name: 'CCG gold standard' creeped into the work at some point, but it makes no sense as CCG keeps improving — please remove all instances of the term 'gold standard' from everywhere." — Rob on terminology. **Actioned:** D-006.

> [2026-03-27] "Proceed with the standard ID, but also add the emoji ticks as they look cool and are nice to scan for quickly when you don't want to be reading." — Rob on task registry format. **Actioned:** D-008.

> [2026-03-27] "Standardise it because it keeps causing issues — previous git references don't matter as we've not even really started making Lilu." — Rob on moving Lilu safeguard files to root. **Actioned:** S6-009.

> [2026-03-27] "And there should be 5 projects with CCG in them now — not 4" — Rob flagging Dev Base was missed from CCG sync. **Actioned:** S6-007 extended to include Dev Base.

> [2026-03-28] "CCG should be able to track itself as there are two versions — the local version which we work on which should have CCG within it, and the public repo that should not, it should be clean obviously" — Rob on CCG self-tracking. **Actioned:** S6-011.

> [2026-03-28] "is it possible to review your own plans and actions and try to populate CCG's own CCG instance? Don't worry too much if not, not too important as long as it is running from now on." — Rob on reconstructing history. **Actioned:** S6-011, history reconstructed from git log and plans.

> [2026-03-28] "we are done here for a while" — Rob considers CCG mostly complete. Future work is bug fixes and improvements as they come up from real-world usage.

## Session 7 — 2026-03-28

> [2026-03-28] "Just go to work on the skill, no need to state that 'The /end skill has disable-model-invocation so I'll follow its steps manually.'" — Rob on not narrating skill execution. **Actioned:** S7-001, rule added to /end SKILL.md.

> [2026-03-28] "can you add a rule to the /end skill to specifically avoid any such comments please. Just run the skill like you would with any others - it is assumed you will do it properly so there is no need to inform the user that you're doing it properly lol." — Rob confirming the no-narration rule. **Actioned:** S7-001.

> [2026-03-28] "it honestly looks like the skills aren't being set as skills anywhere, just taken as suggestions to do manually - you keep doing that. They should be set as proper skills - when I type '/' they do not show up on most projects meaning they are not invokeable skills - please fix this." — Rob on skills not showing in / menu. **Actioned:** S7-002.

> [2026-03-28] "I've just saved all 5 of my projects, and the summary to the /end skill was different in every one - that should be a standardised format also." — Rob on inconsistent /end format. **Actioned:** S7-002.

> [2026-03-28] Re: disable-model-invocation — another Claude identified this flag as the cause. **Actioned:** S7-002, set to false on all skills.

> [2026-03-28] "I have chosen 'bypass permission' - you should not be having to ask me if you can edit an .md file [...] you're asking me for permissions on literally every fucking tool" — Rob frustrated by excessive permission prompts. **Actioned:** Noted, set defaultMode: acceptEdits in settings.local.json.

> [2026-03-28] "Your stupid project folder keeps causing issues when we're upgrading because it seems to be setup different to all the other instances of CCG" — Rob on Dev Base projects.ts having safeguardPath: "templates" for CCG instead of root. **Actioned:** S7-003, removed override.

> [2026-03-28] "why is that skill not showing as an actionable skill? Why is this shit still not working properly!?" — Rob on /end still not appearing in "/" menu after fixes. **Cause:** skill cache loads at conversation start; mid-session changes to disable-model-invocation don't take effect until next conversation.

> [2026-03-28] "True - it's working now" — Rob confirming all 5 skills now appear in "/" menu in a new conversation. **Actioned:** S7-002 verified working.

## Session 8 — 2026-03-30

> [2026-03-30] "Obviously this is a bug - there should be explicit instructions in that skill to cease all work and record it for the next session." — Rob on /end executing plans instead of just archiving them. **Actioned:** S8-001, save-only rule added.

> [2026-03-30] "when you sync to all instances per D-007, what other instances are you referring to? You do realise that you should scan the /software folder as there may be new projects each time you do that?" — Rob on dynamic instance discovery. **Actioned:** Sync now scans /Software/ dynamically.

> [2026-03-30] "do you realise that all of the work I am asking you to do is specific to the CCG project and all your saves and everything should be in there only, unless I ask you to push to the other instances? That is the reason you are in the main parent folder, so you can access the CCG instances in all the other folders too" — Rob clarifying /Software/ is the working dir for access, CCG is the actual project. **Actioned:** Memory saved (feedback_ccg_is_home_project.md).

> [2026-03-30] "I'm so sick of agreeing to plans but then having to constantly give you permission to simply cd, read and write, move and delete etc" — Rob on permission prompts. **Actioned:** S8-002, settings.local.json cleaned up to Bash(*) + acceptEdits.

> [2026-03-31] "The multiple agents issue is still persisting - other projects are confusing plans" — Rob reporting plans leaking between projects via shared ~/.claude/plans/. **Actioned:** S8-003.

> [2026-03-31] "Be careful not to push anything to the public repo that exposes anything private or specific to everything else remember!" — Rob reminding about public repo hygiene during sync. **Actioned:** Verified commit `ef431a9` contains only generic skill instructions.

> [2026-03-31] "CCG Gap: /audit results are ephemeral. The audit report is only shown in conversation and lost when context compresses or the session ends. It should be saved to something like activity/audits/ with a timestamp, so there's a history of audit results over time." — Rob (via Dev Base bug report). **Actioned:** S8-004.

## Session 9 — 2026-04-01

> [2026-04-01] "Please act on the following error report: CCG Bug Report: Pre-Compaction Hook Not Firing" — Rob submitted bug report stating PreCompact is not a valid hook event. **Actioned:** Investigation found PreCompact IS valid but hooks have no decision control — script rewritten to directly back up files. S9-001.

> [2026-04-01] "Yes please enter plan mode and investigate" — Rob confirming investigation after discovering the bug report's root cause was wrong. **Actioned:** S9-001.

> [2026-04-01] "List the projects you have just synced to?" — Rob checking sync coverage. **Actioned:** Listed all 5 consumer projects.

> [2026-04-01] "Cool - please double check that the public repo is clean of private info and anything that has nothing to do with the version a new user would need." — Rob requesting public repo hygiene audit. **Actioned:** Full scan, confirmed clean.

> [2026-04-01] "I just hit a rate limit again with no warning - we should include that because it is highly likely that that also disrupts context right? What happens?" — Rob requesting rate limit protection. **Actioned:** S9-002, RATE LIMIT AWARENESS section added to templates/CLAUDE.md.

> [2026-04-01] "Yes please." — Confirming rate limit section should be added. **Actioned:** S9-002.

> [2026-04-01] "Ok so is the public repo completely up-to-date and all other instances, including both in Lilu, synced?" — Rob checking final sync state. **Actioned:** Found Lilu templates/CLAUDE.md was missed, fixed in S9-005.

## Session 10 — 2026-04-04

> [2026-04-04] "Ok can you set a scheduled task for that time +5 minutes, to publish it please." — Rob on scheduling JourneyKits publish for after 24h cooldown. **Actioned:** Scheduled task `publish-context-guard` created for 2026-04-05 18:45 UTC.

> [2026-04-04] "No the public repo should not have any of this new stuff in it - that repo is for CCG on its own, this new 'kit' is for journeykits.ai only - perhaps you can clean up the local folder to make this clear, and add a note a few notes in the system so none of it gets pushed to other instances in other projects either." — Rob on kit files being local-only. **Actioned:** kit.md, publish_kit.py, kit_bundle.json excluded via .git/info/exclude; memory note saved.

> [2026-04-04] "Triple check the public repo - it should have CCG files ONLY" — Rob demanding public repo cleanliness verification. **Actioned:** Verified git ls-files shows only CCG project files.

> [2026-04-04] Agent bug report: "/start and /save skills don't commit or push — only /end does. When sessions end via context overflow, /end never runs, so work accumulates uncommitted." — Reported from seeko-child project with 2,060+ uncommitted lines across 4 sessions.

> [2026-04-04] "Please implement option 3 - both makes most sense. If the start skill notices work has been done but nothing has been committed since before it, then it can safely assume a session ended any way other than with the end skill, and it can run its own assessment, cross reference, and commit and push. The save skill should absolutely have commit and push, it's literally the whole point of it - to create a save point!" — Rob directing fix for /start and /save. **Actioned:** S10-003.

> [2026-04-04] Two new projects added to consumer list: seeko-child (via Socials.club parent), Waypoint AR. "Those are two new projects that should be kept on the project list for updates from now on [...] Lilu has two versions of CCG - buildtime, and runtime, but I believe both are now the full version so push to both equally." **Actioned:** Memory updated with full consumer list.

> [2026-04-04] "Ok cool - so if the public repo of CCG has now been restored, does that effect the Journey Kit from earlier?" — Rob checking if stale merge affected the kit bundle. **Actioned:** Rebuilt kit_bundle.json with updated skills.

> [2026-04-04] "You don't need to make a plan for this, it's simple, just do it please" / "You're out of plan mode, please just complete my previous request" — Rob wanting direct execution for simple tasks. **Actioned:** Skipped plan mode, executed directly.

## Session 11 — 2026-04-05

> [2026-04-05] "Session log and task registry can just keep the last 3, no need for 5, but make sure to include the ability to actually go reference the older files in case there is confusion or something seems to be missing." — Rob on pagination design. **Actioned:** D-014, changed from 5 to 3 sessions.

> [2026-04-05] "Decisions and comments - if they are something that has been done and actioned, they can be moved to an archive that doesn't get read unless specifically instructed or is part of a debugging cross reference - don't delete anything just move it off the list to be read automatically." — Rob on DECISIONS/COMMENTS archival strategy. **Actioned:** D-014.

> [2026-04-05] "I don't see how the start skill is the right place to do this - it should be on save or end as that is when the agent definitely has full context and can make the best decisions." — Rob on when pagination should run. **Actioned:** D-014, moved from /start to /save and /end.

> [2026-04-05] "In comments - archive any questions that are just curiosities, not necessarily comments about the project itself." — Rob on COMMENTS archival. **Actioned:** D-014, curiosity questions added to archive criteria.

> [2026-04-05] "/start reads only current files, notes archive existence, and checks archives before flagging DROPPED tasks - then what is the point in having them archived if the start skill is going to read the archives anyway!? No - it should not do that, it should only check archives if explicitly asked to, or if there is confusion or it feels something is missing." — Rob on /start not auto-reading archives. **Actioned:** D-015, fixed /start to not auto-read.

> [2026-04-05] "I think reviewing archives and cross-referencing should be left for the audit skill." — Rob on where archive cross-referencing belongs. **Actioned:** D-015.

> [2026-04-05] "Also, is the readme for the repos - especially the open source public one, being kept up-to-date with all of these improvements? But obviously not as 'improvements' but as 'features.'" — Rob on README maintenance. **Actioned:** S11-005, README updated with all features.

> [2026-04-05] "You shouldn't be having to ask me to give you permission to edit files!? That's a really simple and necessary task and you are set to 'bypass permissions' - please check your config and make sure it is actually set to bypass permissions, this is fucking annoying having to give you permission to do the same thing over and over." — Rob on permission prompts. **Noted:** Config verified correct (defaultMode: bypassPermissions, skipDangerousModePermissionPrompt: true). The prompts are from Claude Code's platform-level safety layer, not the config.

> [2026-04-05] "Obviously don't bother updating anything until after you've added the new page feature to help keep context bloat down due to extended records." — Rob on prioritising pagination before syncing. **Actioned:** Pagination implemented first, then all syncs.

> [2026-04-05] "Ok great, now update the Journey.AI kit ready for upload later this evening please." — Rob requesting kit bundle rebuild. **Actioned:** S11-008.
