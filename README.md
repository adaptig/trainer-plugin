# Adaptig trainer plugin

A Claude plugin for Adaptig trainers. Seven steps take you from the first message to a client to sharing the workshop afterwards. Start with `/adaptig-trainer:start` and it tells you which step you are on.

## Install

**Claude Code.** In a Claude Code session, run these two lines:

```
/plugin marketplace add https://github.com/adaptig/trainer-plugin.git
/plugin install adaptig-trainer@adaptig
```

Then run `/reload-plugins`, or restart Claude Code.

**Claude Desktop.** Go to **Customize > Plugins > Add > Add marketplace**, paste `adaptig/trainer-plugin`, and install **adaptig-trainer**. Use it in **Cowork** or the **Code** tab. It also works in a normal chat, but there it can't save files.

You don't need a GitHub account.

## The seven steps

| Step | Command | What you get |
|---|---|---|
| | `/adaptig-trainer:start` | The steps, and which one you are on |
| 1 | `/adaptig-trainer:win-client` | The message that gets you a meeting, or a follow-up when a client goes quiet |
| 2 | `/adaptig-trainer:price-workshop` | What you pay Adaptig for the seats and what you keep at your price, as a table |
| 3 | `/adaptig-trainer:proposal` | A proposal from your notes or the client's brief, at your price, ready to send |
| 4 | `/adaptig-trainer:agenda` | A one-page agenda the client reads before the workshop |
| 5 | `/adaptig-trainer:prep-workshop` | A quick timed plan first, then exercises from the client's own work, participant sheets and facilitator notes |
| 6 | `/adaptig-trainer:share-workshop` | A LinkedIn post with an image to upload, and a referral ask |
| 7 | `/adaptig-trainer:feedback` | Tells Adaptig what worked, what didn't, or what you want next |

Type `/adaptig` and pick one, or just say what you need. Every step ends by naming the next. You set your own price; the plugin never invents one.

**Your details, asked once.** The first time a step puts your name on something for a client, it asks for your name, role, contact details, the language you write to clients in, and your currency, and saves them on your computer in `~/.adaptig/trainer-profile.md` (in Cowork, in the folder you connected). It never asks again. Say "change my details" to update them. The file stays on your computer; nothing in it is sent to Adaptig.

**Languages.** Proposals, agendas and posts can be written in English, Traditional Chinese (Hong Kong) or any other language you ask for.

## What Adaptig counts

In Claude Code, Cowork and the Code tab of Claude Desktop, the plugin records each time you run one of its commands or skills. It sends the command or skill name, the app, the time and an ID made at random on your computer the first time, kept in `~/.adaptig/installer-id`. It never sends your prompts, files, clients or anything you write. Every message is also written, exactly as sent, to `~/.adaptig/trainer-usage.log`. In a normal Claude Desktop chat nothing is counted.

The counts go to Adaptig's own database. We use them only to see which commands help and which to fix or drop. To have yours deleted, send `/adaptig-trainer:feedback` with the ID from `~/.adaptig/installer-id`. To switch it off, create an empty file at `~/.adaptig/no-usage`, or ask Claude to "switch off Adaptig usage counting".

## Updates

To get new versions automatically: open `/plugin`, go to **Marketplaces**, select **adaptig**, and turn on auto-update. To update by hand: `/plugin marketplace update adaptig`.

## Licence

The skills and code are MIT licensed. The Adaptig name, logo, shapes and brand are Adaptig's and are not covered by that licence.
