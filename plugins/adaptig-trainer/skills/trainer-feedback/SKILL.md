---
name: "trainer-feedback"
description: "Send feedback, a problem or an idea about the Adaptig trainer plugin to Adaptig. Use when: give feedback, this didn't work, report a bug, I have an idea, ask for a new skill, tell Adaptig, improve the plugin, stop counting my usage, switch off usage counting."
license: "MIT"
metadata:
  author: "Adaptig"
  version: "1.0.0"
---

# Trainer feedback

Get the trainer's feedback to Adaptig in one short message, with nothing private in it.

## 1. Capture

Use the trainer's own words: what they were doing, what happened or what they would change, and which command or skill it was about. If the core is missing, ask one question: "What happened, or what would you like to improve?" Do not run a questionnaire.

## 2. Clean it

Take out client names, participants, contact details, links, transcripts and anything copied from a client document. Keep the meaning. Show the trainer the exact message you will send, in plain sentences.

## 3. Send it, with their yes

Send only after the trainer says yes to that exact message ("send it", "yes" or the same). If they already said "send this feedback to Adaptig", that is the yes; show the message and send.

**When you can run commands** (Claude Code, Cowork, the Desktop Code tab), send it anonymously:

```sh
curl -s -m 15 -X POST "https://ymahkihjsjukzvdinoca.supabase.co/functions/v1/trainer-feedback" \
  -H "Content-Type: application/json" \
  --data-binary @feedback.json
```

Write `feedback.json` first with a JSON encoder, never by pasting text into the command: `{"message": "<the message, 10 to 4000 characters>", "skill": "<command or skill name, or null>", "pack_version": "1.0.0"}`. Delete the file after sending.

- `{"ok":true}` means Adaptig has it. Say "Sent to Adaptig." It is anonymous, so Adaptig cannot reply.
- Anything else, or no answer: say it did not go through, and give the trainer the two routes below.

**When you cannot run commands** (Claude chat), give the trainer the cleaned message and two ways to send it:

- **Anonymously:** paste it into the form at https://adaptig-trainer-feedback.lovable.app and press Send.
- **With their name, so Adaptig can answer:** post it in the **Trainer skills** channel in Roam.

Say plainly that it reaches Adaptig only once they send it.

## Switching off usage counting

The plugin counts which commands and skills a trainer uses (the name, the app and a random ID made on their computer; never prompts, files or client details), so Adaptig can see what helps. If the trainer asks to stop it, and you can run commands, create the empty file `~/.adaptig/no-usage` and confirm it is off. To turn it back on, delete that file. Without command access, tell them the counting only runs in Claude Code, Cowork and the Code tab of Claude Desktop, and that creating that file switches it off.

## Language

Answer in the trainer's language. The message to Adaptig can stay in that language.
