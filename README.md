# LalaBot
A discord bot that generates an inspiring quote and replies cheering up quotes when detect sad words. 
<br> 
Application is still using repl.it and UptimeRobot
<br>
[Source Code in Repl.it](https://replit.com/@akanijade/Lala-Bot#main.py)
[Add Bot to your Server](https://discord.com/api/oauth2/authorize?client_id=722716976186916886&permissions=8&scope=applications.commands%20bot)

## Help Box
Features a help box of what the bot can do
<br>
`/help`

## Quote
Generates an inspiring quote from an API
<br>
`/quote`

## Add Cheer Up Quotes
Add a new cheer up quote to the repl.it db database
<br>
`/new <quote>`

## Delete Cheer Up Quotes
Delete w cheer up quote to the repl.it db database by their index (starts from 0,1,2,..)
<br>
`/del [index]`

## List Cheer Up Quotes
List all the cheer up quotes in the repl.it db database
<br>
`/list`

## Testing
Replies with "ping pong!" if bot is working
<br>
`/test`

## Reponding
Check if bot will reply if it detects a sad word. It will mention whether the mode is on or not. 
<br>
`/responding`

## Slash
Not implemented yet, can received string and int

## Updates
+ has slash commands (quote, help, slash)
+ migrated to discord.py v2
+ fixed the loading images and thumbnails
+ fixed help box
+ added more cheer up quotes and sad words detection
+ added "add to server" button on profile page
+ request timeout (too many requests to API)




### Features to add
- using sentiment analysis to find negative tones in sentences
- adding a music feature again
- change the replying to sad words as slash commands
- adding more slash commands
- add buttons
- apply methods for all kinds of servers
- bot verification (if bot ever reaches 100 servers)
- check for disperancies with other packages that hasn't been udpated in lock file
- change deleting to a better efficient way instead of indexes
- fix that markoff package no longer has soft unicode
- guild/global commands do not delete after reboot (discord.py do not have a func yet to fix this, besides kicking the bot :stuck_out_tongue_closed_eyes:)
