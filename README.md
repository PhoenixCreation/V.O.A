# Index

- [Rules](#Rules)
- [Play](#Play)
- [What is](#What-is)
- [Wheather](#Wheather)
- [Whatsapp](#Whatsapp)
- [Tell](#Tell)

# Rules

- `[word]` means it's optional
- `{word}` means it's compulsory word
- `(word 1 | word 2 | ... | word n)` means one of the word
- #<sentance 1> <-> #<sentance 2> means both can be used in any order. i.e. sentance 1, sentance 2 == sentance 2, sentance 1

# Play

- veronika play [the] `radio` (will start a radio on gaana.com)
- veronika play [song] `<song_name>` (will play the song on youtube)
- veronika play `<anything>` (plays the provided thing on youtube)

# What is

- veronika what is `<topic>` (will give you brief info on topic)

# Wheather

- veronika `weather` [(of | in) `<city>`] [ (on | at) ('tommorow' | date)]
- (if city is not provided then it will give weather of surat)
- (if city is provided then it will give weather of city )

# Whatsapp

> `WARNING`: You need to configure adb of your phone first. If you don't know how then check online, you will find better soltions then I can Explain.

- veronika send whatsapp [message] {that} `<message>` {to} `<user>`
- veronika send whatsapp [message] {to} `<user>` {that} `<message>`
- All above (sends message to person using adb configuration of your phone)

# Tell

- veronika tell [me a] what is `<topic>` (same as what is `<topic>`)
- veronika tell [me a] joke (tells you a joke)

## TODO

- [ ] Whatsapp-group configuration, so we can send message to groups too.
