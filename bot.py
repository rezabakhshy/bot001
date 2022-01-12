from telethon import TelegramClient, Button, events

import uuid, os, sqlite3, psycopg2

api_id=13893053
api_hash="f586d92837b0f6eebcaa3e392397f47c"
bot_token = '2136835913:AAFp2UmOaw-qdLwrGtgCni4D0JlgD2_bU4o'
owners = open('owners.txt', 'r').read().splitlines()
admins = open('admins.txt', 'r').read().splitlines()

con = psycopg2.connet(database='', user='', password='', host='', port=None) #sqlite3.connect('database.db')
cur = con.cursor()

cur.execute('CREATE TABLE musics VALUES (id text, msgid text, name text, artist text);')
cur.execute('CREATE TABLE starts VALUES (id text;')
con.commit()

c = 0
c2 = 0

for i in owners: owners[c] = int(i); c += 1
for i in admins: admins[c2] = int(i); c2 += 1

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True, outgoing=False))
async def start(event):
    print(event)

@client.on(events.NewMessage(pattern='/start', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def start(event):
    markup = event.client.build_reply_markup([[Button.text('دسته بندی بر اساس خواننده 💜')], [Button.text('کانال دیسلاو 🖤'), Button.text('فول آرشیو دیسلاو 💯')], [Button.text('استیکر دیسلاوی ❤️‍🩹'), Button.text('ریمیکس دیسلاوی ❤️‍🔥')], [Button.text('دونیت کانال دیسلاو 💰'), Button.text('دونیت سازنده ربات 💰')], [Button.text('ارسال پیشنهاد به ادمین ✉️')]])
    keyboard = [[Button.url('عضویت در کانال دیسلاو', b'https://t.me/Chanell_Disslove')]]
    members = []
    async for u in client.iter_participants('Chanell_Disslove', aggressive=True): members.append(u.id)
    if event.raw_text == '/start':
        if event.peer_id.user_id in members:
            await event.reply('سلام دوست عزیز. به بات دیسلاو خوش اومدی. توی این بات میتونید آهنگ های دیسلاو رو دانلود و گوش کنید.', buttons=markup)
            cur.execute('INSERT INTO starts VALUES (%s);', (event.peer_id.user_id,))
            con.commit()
        else: await event.reply('برای استفاده از ربات باید در کانال دیسلاو عضو باشید', buttons=keyboard)
    elif event.raw_text[7:15] == 'download':
        starts = []
        cur.execute('SELECT * FROM starts;')
        rows = cur.fetchall()
        for s in rows: starts.append(int(s[0]))
        if event.peer_id.user_id in starts:
            text = event.raw_text
            fileid = event.raw_text[16:]
            cur.execute('SELECT * FROM musics WHERE id=%s;', (fileid,))
            rows = cur.fetchall()
            for i in rows:
                if i[0] == fileid: msgid = i[1]
            msg = await client.get_messages(-1001673499580, ids=int(msgid))
            await client.send_message(event.peer_id.user_id, msg)
        else:
            if event.peer_id.user_id in members:
                await event.reply('سلام دوست عزیز. به بات دیسلاو خوش اومدی. توی این بات میتونید آهنگ های دیسلاو رو دانلود و گوش کنید.', buttons=markup)
                cur.execute('INSERT INTO starts VALUES (%s);', (event.peer_id.user_id,))
                con.commit()
            else: await event.reply('برای استفاده از ربات باید در کانال دیسلاو عضو باشید', buttons=keyboard)

@client.on(events.NewMessage(pattern='دسته بندی بر اساس خواننده 💜', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def category(event):
    markup = event.client.build_reply_markup([[Button.text('مهراب 🛑'), Button.text('معراج 🛑')], [Button.text('علی بابا 🛑'), Button.text('میلاد راستاد 🛑')],[Button.text('ارشاد 🛑'), Button.text('بهزاد پکس 🛑')],[Button.text('فرشاد دارک لاو 🛑'), Button.text('فرشاد پیکسل 🛑')],[Button.text('ایمان نولاو 🛑'), Button.text('راهب 🛑')],[Button.text('رادین 🛑'), Button.text('پویا یواستار 🛑')], [Button.text('برگشت ⬅️')]])
    await event.reply('ورود به دسته بندی ها', buttons=markup)

@client.on(events.NewMessage(pattern='برگشت ⬅️', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def back(event):
    markup = event.client.build_reply_markup([[Button.text('دسته بندی بر اساس خواننده 💜')], [Button.text('کانال دیسلاو 🖤'), Button.text('فول آرشیو دیسلاو 💯')], [Button.text('استیکر دیسلاوی ❤️‍🩹'), Button.text('ریمیکس دیسلاوی ❤️‍🔥')], [Button.text('دونیت کانال دیسلاو 💰'), Button.text('دونیت سازنده ربات 💰')], [Button.text('ارسال پیشنهاد به ادمین ✉️')]])
    await event.reply('منو بازیابی شد', buttons=markup)

@client.on(events.NewMessage(pattern='مهراب 🛑', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def mehrab(event):
    cur.execute('SELECT * FROM musics WHERE artist=%s;', ('Mehrab',))
    rows = cur.fetchall()
    msg = ''
    c = 1
    for i in rows:
        msg += f'{c}. {i[2]} - {i[3]}: [download](https://telegram.me/ChanellDissloveBot?start=download-{i[0]})'
        c += 1
    await event.reply(msg, parse_mode='md', link_preview=False)

@client.on(events.NewMessage(pattern='علی بابا 🛑', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def alibaba(event):
    cur.execute('SELECT * FROM musics WHERE artist=%s;', ('AliBaba',))
    rows = cur.fetchall()
    msg = ''
    c = 1
    for i in rows:
        msg += f'{c}. {i[2]} - {i[3]}: [download](https://telegram.me/ChanellDissloveBot?start=download-{i[0]})'
        c += 1
    await event.reply(msg, parse_mode='md', link_preview=False)

@client.on(events.NewMessage(pattern='میلاد راستاد 🛑', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def miladrastad(event):
    cur.execute('SELECT * FROM musics WHERE artist=%s;', ('MiladRastad',))
    rows = cur.fetchall()
    msg = ''
    c = 1
    for i in rows:
        msg += f'{c}. {i[2]} - {i[3]}: [download](https://telegram.me/ChanellDissloveBot?start=download-{i[0]})'
        c += 1
    await event.reply(msg, parse_mode='md', link_preview=False)

@client.on(events.NewMessage(pattern='ارشاد 🛑', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def ershad(event):
    cur.execute('SELECT * FROM musics WHERE artist=%s;', ('Ershad',))
    rows = cur.fetchall()
    msg = ''
    c = 1
    for i in rows:
        msg += f'{c}. {i[2]} - {i[3]}: [download](https://telegram.me/ChanellDissloveBot?start=download-{i[0]})'
        c += 1
    await event.reply(msg, parse_mode='md', link_preview=False)

@client.on(events.NewMessage(pattern='بهزاد پکس 🛑', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def behzadpax(event):
    cur.execute('SELECT * FROM musics WHERE artist=%s;', ('BehzadPax',))
    rows = cur.fetchall()
    msg = ''
    c = 1
    for i in rows:
        msg += f'{c}. {i[2]} - {i[3]}: [download](https://telegram.me/ChanellDissloveBot?start=download-{i[0]})'
        c += 1
    await event.reply(msg, parse_mode='md', link_preview=False)

@client.on(events.NewMessage(pattern='فرشاد دارک لاو 🛑', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def farshaddarklove(event):
    cur.execute('SELECT * FROM musics WHERE artist=%s;', ('FarshadDarkLove',))
    rows = cur.fetchall()
    msg = ''
    c = 1
    for i in rows:
        msg += f'{c}. {i[2]} - {i[3]}: [download](https://telegram.me/ChanellDissloveBot?start=download-{i[0]})'
        c += 1
    await event.reply(msg, parse_mode='md', link_preview=False)

@client.on(events.NewMessage(pattern='فرشاد پیکسل 🛑', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def farshadpixel(event):
    cur.execute('SELECT * FROM musics WHERE artist=%s;', ('FarshadPixel',))
    rows = cur.fetchall()
    msg = ''
    c = 1
    for i in rows:
        msg += f'{c}. {i[2]} - {i[3]}: [download](https://telegram.me/ChanellDissloveBot?start=download-{i[0]})'
        c += 1
    await event.reply(msg, parse_mode='md', link_preview=False)

@client.on(events.NewMessage(pattern='معراج 🛑', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def meraj(event):
    cur.execute('SELECT * FROM musics WHERE artist=%s;', ('meraj',))
    rows = cur.fetchall()
    msg = ''
    c = 1
    for i in rows:
        msg += f'{c}. {i[2]} - {i[3]}: [download](https://telegram.me/ChanellDissloveBot?start=download-{i[0]})'
        c += 1
    await event.reply(msg, parse_mode='md', link_preview=False)

@client.on(events.NewMessage(pattern='رادین 🛑', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def radin(event):
    cur.execute('SELECT * FROM musics WHERE artist=%s;', ('radin',))
    rows = cur.fetchall()
    msg = ''
    c = 1
    for i in rows:
        msg += f'{c}. {i[2]} - {i[3]}: [download](https://telegram.me/ChanellDissloveBot?start=download-{i[0]})'
        c += 1
    await event.reply(msg, parse_mode='md', link_preview=False)

@client.on(events.NewMessage(pattern='پویا یواستار 🛑', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def pouyaustar(event):
    cur.execute('SELECT * FROM musics WHERE artist=%s;', ('PouyaUStart',))
    rows = cur.fetchall()
    msg = ''
    c = 1
    for i in rows:
        msg += f'{c}. {i[2]} - {i[3]}: [download](https://telegram.me/ChanellDissloveBot?start=download-{i[0]})'
        c += 1
    await event.reply(msg, parse_mode='md', link_preview=False)

@client.on(events.NewMessage(pattern='ایمان نولاو 🛑', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def imannolove(event):
    cur.execute('SELECT * FROM musics WHERE artist=%s;', ('ImanNoLove',))
    rows = cur.fetchall()
    msg = ''
    c = 1
    for i in rows:
        msg += f'{c}. {i[2]} - {i[3]}: [download](https://telegram.me/ChanellDissloveBot?start=download-{i[0]})'
        c += 1
    await event.reply(msg, parse_mode='md', link_preview=False)

@client.on(events.NewMessage(pattern='ارسال پیشنهاد به ادمین ✉️', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def contact(event):
    async with client.conversation(event.peer_id.user_id) as conv:
        await conv.send_message('متن پیشنهاد خود را ارسال کنید (ارسال فایل یا تصویر مجاز نیست). برای توقف عملیات دستور "/cancel" را ارسال کنید')
        res = await conv.get_response().raw_text
        for c in owners: await client.send_message(c, res)

@client.on(events.NewMessage(pattern='دونیت کانال دیسلاو 💰', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def donatechannel(event):
    keyboard = [[Button.url('حمایت مالی', b'https://google.com')]]
    await event.reply('برای دونیت یا همون حمایت مالی از کانال دیسلاو میتونید از لینک زیر استفاده کنید', buttons=keyboard)

@client.on(events.NewMessage(pattern='دونیت سازنده ربات 💰', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def donateme(event):
    keyboard = [[Button.url('حمایت مالی', b'https://google.com')]]
    await event.reply('برای دونیت یا همون حمایت مالی از سازنده ربات میتونید از لینک زیر استفاده کنید', buttons=keyboard)

@client.on(events.NewMessage(pattern='استیکر دیسلاوی ❤️‍🩹', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def sticker(event):
    messages = [102, 103, 104, 105, 106]
    msg = await client.get_messages(-1001673499580, ids=messages)
    for i in msg: await client.send_message(event.peer_id.user_id, i)
    await event.reply('استیکر های کانال دیسلاو 👆')

@client.on(events.NewMessage(pattern='ریمیکس دیسلاوی ❤️‍🔥', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def remix(event):
    messages = [107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128]
    msg = await client.get_messages(-1001673499580, ids=messages)
    for i in msg: await client.send_message(event.peer_id.user_id, i)
    await event.reply('ریمیکس های کانال دیسلاو 👆 برای ریمیکس های بیشتر در کانال عضو شوید')

@client.on(events.NewMessage(pattern='فول آرشیو دیسلاو 💯', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def fullarchive(event):
    await event.reply('''[🔺فول آرشیو تمامی ترک های بهزاد پکس](https://t.me/full_Archive_Diss/253)\n[🔻فول آرشیو تمامی ترک های علی بابا](https://t.me/full_Archive_Diss/622)\n[🔺فول آرشیو تمامی ترک های میلاد راستاد](https://t.me/full_Archive_Diss/421)\n[🔻فول آرشیو تمامی ترک های ارشاد](https://t.me/full_Archive_Diss/721)\n[🔺فول آرشیو تمامی ترک های پویا یواستار](https://t.me/full_Archive_Diss/502)\n[🔺فول آرشیو تمامی ترک های فرشاد دارک لاو](https://t.me/full_Archive_Diss/192)\n[🔻فول آرشیو تمامی ترک های فرشاد پیکسل](https://t.me/full_Archive_Diss/79)\n[🔻فول آرشیو تمامی ترک های معراج](https://t.me/full_Archive_Diss/94)\n[🔺فول آرشیو تمامی ترک های ایمان نولاو](https://t.me/full_Archive_Diss/39)\n[🔺فول آرشیو تمامی ترک های راهب ](https://t.me/full_Archive_Diss/829)\n[🔻فول آرشیو تمامی ترک های مهراب](https://t.me/full_Archive_Diss/900)\n[🔺فول آرشیو تمامی ترک های رادین](https://t.me/full_Archive_Diss/1160)\n\n💯 فول آلبوم هر خواننده‌ایو میخواید بزنید روش\n💢 این لیست بروزرسانی میشه ...\n\n🥀›› 『 @Radio_Dislove1 』 ♡''', parse_mode='md', link_preview=False)

@client.on(events.NewMessage(pattern='کانال دیسلاو 🖤', incoming=True, outgoing=False, func=lambda e: e.is_private))
async def channel(event):
    keyboard = [[Button.url('عضویت در کانال دیسلاو', b'https://t.me/Chanell_Disslove')]]
    await event.reply('با کلیک روی دکمه زیر وارد کانال دیسلاو میشید (جوین فراموش نشه)', buttons=keyboard)

@client.on(events.NewMessage(pattern='/addmusic', from_users=admins+owners, incoming=True, outgoing=False, func=lambda e: e.is_private and e.message.media))
async def addmusic(event):
    text = event.raw_text
    artist = event.raw_text[10:]
    tmpid = uuid.uuid4().hex
    repmsg = await event.message.get_reply_message()
    msg = await client.send_message(-1001673499580, repmsg)
    cur.execute('INSERT INTO musics VALUES (%s, %s, %s, %s);', (tmpid, msg.id, artist, repmsg.media.title))
    con.commit()
    await event.reply(f'آهنگ آپلود شد ✅ از لینک زیر برای دانلود استفاده کنید: \n https://telegram.me/ChanellDissloveBot?start=download-{tmpid}\nآیدی آهنگ: {tmpid}', link_preview=False)

@client.on(events.NewMessage(pattern='/delmusic', from_users=admins+owners, incoming=True, outgoing=False, func=lambda e: e.is_private))
async def delmusic(event):
    text = event.raw_text
    musicid = event.raw_text[10:]
    cur.execute('DELETE FROM musics WHERE id=%s;', (musicid,))
    con.commit()
    await event.reply('آهنگ با موفقیت حذف شد ✅')

@client.on(events.NewMessage(pattern='/addadmin', from_users=owners, incoming=True, outgoing=False, func=lambda e: e.is_private))
async def addadmin(event):
    text = event.raw_text
    user = text[10:]
    if user in admins: await event.reply(f'کاربر [{user}](tg://user?id={user}) قبلا به لیست ادمین ها اضافه شده است ✅')
    else:
        admins.append(int(user))
        adminfile = open('admins.txt', 'w')
        for i in admins: adminfile.write(str(i) + '\n')
        await event.reply(f'کاربر [{user}](tg://user?id={user}) به لیست ادمین ها اضافه شد ✅')

@client.on(events.NewMessage(pattern='/deladmin', from_users=owners, incoming=True, outgoing=False, func=lambda e: e.is_private))
async def deladmin(event):
    text = event.raw_text
    user = text[10:]
    del admins[admins.index(int(user))]
    adminfile = open('admins.txt', 'w')
    for i in admins: adminfile.write(str(i) + '\n')
    await event.reply(f'کاربر [{user}](tg://user?id={user}) از لیست ادمین ها حذف شد ❌')

client.start(bot_token=bot_token)
print('Client Started')
client.run_until_disconnected()
