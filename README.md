# Index

- [Installation](#installation)
- [Rules](#Rules)
- Commands:
  - [Time](#Time)
  - [Who](#Who)
  - [Play](#Play)
  - [What is](#What-is)
  - [Wheather](#Wheather)
  - [Whatsapp](#Whatsapp)
  - [Tell](#Tell)
  - [News](#News)

# installation

## Recommendations

- Use linux(MacOS too) for better experience
- Configure adb with your phone for phone speicific features like whatsapp message. You can read more about this [here.](https://developer.android.com/studio/command-line/adb). (I will suggest you use wireless configuration)
- Have a stable internet connection. (Ofcourse you need internet but a good quality one too.)
- Have a good quality microphone. (Not actually needed but will give you better experience)

## Step 1: Clone this repo.

Then `cd` into it.

```bash
cd V.O.A
```

## Step 2: Run follwing command to complete set up

### For Windows

```bash
python configure.py
```

### For Linux and MacOS

```bash
python3 configure.py
```

## Step 3: Run follwing to check

### For Windows

```bash
python main.py
```

### For Linux and MacOS

```bash
python3 main.py
```

If a window pops up then write `veronika test`, if you here anything setup is successful.

# Rules

- `[word]` means it's optional
- `{word}` means it's compulsory word
- `(word 1 | word 2 | ... | word n)` means one of the word
- #<sentance 1> <-> #<sentance 2> means both can be used in any order. i.e. sentance 1, sentance 2 == sentance 2, sentance 1

# Time

- veronika time (Tells you time)
- veronika date (Tells you date)
- veronika timestamp (Tells you current timestamp )

# Who

- veronika who [am] i (Tells you your name)
- veronika who is `<someone>` (Tells you about someone)

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

# News

- veronika `news` (Tells you news from google, not gurenteed to working perfectly fine)

## TODO

- [x] Whatsapp-group configuration, so we can send message to groups too.
- [ ] Fix what is, still awaiting
