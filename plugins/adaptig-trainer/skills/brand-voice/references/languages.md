# Writing for the client in their language

Talk to the trainer in the language they write to you in. Write what the client reads in
the client's language.

## Choosing the language

1. The trainer names it for this client: use that.
2. Otherwise, the `client language` in the trainer's saved details
   ([trainer-details.md](trainer-details.md)).
3. Otherwise, the language of the brief or notes they gave you.

When a step makes something the client reads (the proposal, the agenda, the post) and the
language is still unclear, offer the choice in the question you ask anyway: "English or
Traditional Chinese (Hong Kong)? Any other language works too." Do not make it a
separate round.

When the trainer does not read the language they asked for, say once that someone who
does should read it before it goes to the client.

## Traditional Chinese (Hong Kong)

- **Characters:** Traditional (繁體), Hong Kong usage and vocabulary: 電郵, 網上, 軟件, 資訊,
  課程, 導師, 同事. Never Simplified, never mainland or Taiwan usage when Hong Kong differs.
- **Register:** standard written Chinese (書面語) for the proposal, the agenda, worksheets
  and anything formal. Colloquial Cantonese (嘅, 咗, 啲, 係) only in a LinkedIn post, and
  only when the trainer asks for it.
- **Names stay in English:** Adaptig, Spark, Shift, Shape, and tool names such as
  ChatGPT, Copilot and Claude. Give the plain clause in Chinese at first mention, for
  example: Adaptig（一間 AI 應用培訓公司，由獨立導師教授其認可的工作坊）.
- **Money and dates:** HK$39,000 or 港元 39,000; 2026年12月10日; 上午10時 to 下午1時.
- **Punctuation:** full-width （，。：；！？）and 「」 for quotes.
- **Trainer details:** use the name and role the trainer gave, in the script they gave it.

## Files in another language

- The workshop pack renderer: set `"lang"` in the JSON (`"zh-Hant-HK"`, `"es"`…). It sets
  the page language, and with a Chinese tag it prints its own headings in Traditional
  Chinese.
- The one-pager and the social images: put the tag in the template's `{{LANG}}` slot.
- No Chinese font is bundled; the page uses the system's. On Linux (Cowork), run
  `fc-list :lang=zh-hk | head -1` before making a Chinese PDF or PNG. If nothing is
  listed, the characters would print as boxes: hand over the HTML and tell the trainer to
  open it on their own computer to print or screenshot it.
