# The trainer's details: asked once, then remembered

A proposal, an agenda or a post carries the trainer's name, role and contact details.
Ask for them once, save them on the trainer's own computer, and never ask again.

## The file

```
# My Adaptig trainer details
name: Alex Example
role: Adaptig Certified Trainer
contact: alex@example.com · +852 5555 0000 · example.com
client language: English
currency: HKD
```

Each line is what the trainer gave, in their words. `role` says "Adaptig Certified
Trainer" only when the trainer says they are certified. `client language` is the default
for client documents (see [languages.md](languages.md)); a client who reads another
language still gets their own. `currency` is the one they charge clients in.

Where it lives:

- **Claude Code, or the Code tab of Claude Desktop:** `~/.adaptig/trainer-profile.md`.
- **Cowork:** the home folder there is wiped after the session. When the home folder is
  under `/sessions/`, save the file as `adaptig-trainer-profile.md` in the folder the
  trainer connected (under `/sessions/<id>/mnt/`), and tell them that is where it is.
  Read both places before asking.
- **A chat with no file access:** you cannot save it. Ask once in the conversation and
  reuse the answers to its end. Then give the trainer the five lines and suggest they
  paste them into their Claude settings (Settings > Profile, personal preferences), so
  every new chat has them.

The file stays on the trainer's computer. The plugin's usage counter never reads it, and
nothing in it is sent to Adaptig.

## Read it first

Before you write anything that carries the trainer's name, read the file. When it has a
name, a role and contact details, use them and do not ask. Say once, in one short line at
the end of the reply: "Used your saved details. Say 'change my details' to update them."

## Ask at the end, not at the start

When the file is missing or incomplete, do the work first: the full text of the proposal,
agenda or post, with the sender lines left out. Then, at the end of that same reply, ask
for the missing details in one message, together with any other question the step has
(such as the fee). Never open a step with a form.

> To sign this and make the designed file, I need a few details. I'll save them on your
> computer so I never ask again:
> 1. Your name, as clients should see it
> 2. Your role (for example "Adaptig Certified Trainer", if you are certified)
> 3. The contact details to show clients: email, phone, website, any you like
> 4. The language you usually write to clients in: English, Traditional Chinese
>    (Hong Kong), or another
> 5. The currency you charge in

When they answer, save the file (make the folder if needed), finish the step, and say in
one line where the file is. If they skip a detail, leave it out of the document and do
not ask again in this conversation.

## Change or forget

"Change my details", "my phone number changed", "update my role": show the saved lines,
change what they named, save. "Forget my details": delete the file and say so.

## Never

- Put a client's name or anything about a client in this file.
- Invent or tidy up a detail the trainer did not give.
- Print a placeholder such as "[Your name]" in a client document.
