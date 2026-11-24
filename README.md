# Adaptig trainer plugin

A Claude plugin for Adaptig trainers. Six commands help you win a client, write the proposal, price and prepare the workshop, share it, and tell us what to improve.

## Install

**Claude Code.** In a Claude Code session, run these two lines:

```
/plugin marketplace add https://github.com/adaptig/trainer-plugin.git
/plugin install adaptig-trainer@adaptig
```

Then run `/reload-plugins`, or restart Claude Code.

**Claude Desktop.** Go to **Customize > Plugins > Add > Add marketplace**, paste `adaptig/trainer-plugin`, and install **adaptig-trainer**. Use it in **Cowork** or the **Code** tab. It also works in a normal chat, but there it can't save files.

You don't need a GitHub account.

## The six commands

| Command | What you get |
|---|---|
| `/adaptig-trainer:win-client` | The message that gets you the meeting, then a proposal you can send |
| `/adaptig-trainer:proposal` | A proposal from your meeting notes or the client's brief, at your price, ready to send |
| `/adaptig-trainer:price-workshop` | What you pay Adaptig for the seats and what you keep at your price |
| `/adaptig-trainer:prep-workshop` | A timed plan, exercises from the client's own work, participant sheets and a one-page handout |
| `/adaptig-trainer:share-workshop` | A LinkedIn post before or after the workshop, and a referral ask |
| `/adaptig-trainer:feedback` | Tells Adaptig what worked, what didn't, or what you want next |

Type `/adaptig` and pick one, or just say what you need. You set your own price; the plugin never invents one. `price-workshop` shows what you keep at it.

## What Adaptig counts

In Claude Code, Cowork and the Code tab of Claude Desktop, the plugin records each time you run one of its commands or skills. It sends the command or skill name, the app, the time and an ID made at random on your computer the first time, kept in `~/.adaptig/installer-id`. It never sends your prompts, files, clients or anything you write. Every message is also written, exactly as sent, to `~/.adaptig/trainer-usage.log`. In a normal Claude Desktop chat nothing is counted.

The counts go to Adaptig's own database. We use them only to see which commands help and which to fix or drop. To have yours deleted, send `/adaptig-trainer:feedback` with the ID from `~/.adaptig/installer-id`. To switch it off, create an empty file at `~/.adaptig/no-usage`, or ask Claude to "switch off Adaptig usage counting".

## Updates

To get new versions automatically: open `/plugin`, go to **Marketplaces**, select **adaptig**, and turn on auto-update. To update by hand: `/plugin marketplace update adaptig`.

## Licence

The skills and code are MIT licensed. The Adaptig name, logo, shapes and brand are Adaptig's and are not covered by that licence.
