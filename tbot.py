from PIL import Image
from moviepy import VideoFileClip
from colorama import Fore, init
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

from telethon import TelegramClient, functions, types, errors, utils
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from telethon.tl.functions.channels import JoinChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import Channel, Chat, User, DialogFilter, InputMessagesFilterPhotos, DocumentAttributeVideo, InputMessagesFilterVideo, InputMessagesFilterDocument
import sys, asyncio, pandas as pd, re, random as r, sqlite3, numpy as np, os, imagehash, warnings, requests

warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv(dotenv_path=os.getenv('DOTENV_FILE_PATH'))
init(autoreset=True)

APP_ID = os.getenv('app_id')
APP_TOKEN = os.getenv('app_token')
CHATS_GROUPS = os.getenv('chats_groups')
FORWARD_LOG = os.getenv('forward_log')
PASSWORD = os.getenv('password')
RECIPIENTS = os.getenv('recipients')
RECIPIENTS_FALSE = os.getenv('recipients_false')
SEARCH_CHANNELS = os.getenv('search_channels')
SESSIONS = os.getenv('sessions')
TG = os.getenv('tg')
TG_DATA = os.getenv('tg_data')
MAX_CHANNEL = int(os.getenv('max_channel'))
SECRET_CHANNEL = int(os.getenv('secret_channel'))
TG_DEADS_DATA = os.getenv('tg_deads_data')
con = sqlite3.connect(TG_DATA)
cur = con.cursor()

if len(sys.argv) < 3:
    lst_functions = ['get dialogs id', 'leave chats and channels', 'send to bot user', 'change bio',  'forward post','get activation code', 'join chat', 'fresh channels','view posts', 'edit 2FA', 'create folder', 'join_channel', 'find image', 'find video', 'channel info', 'comment on post', 'statistic on posts', 'sophia', 'collect raw data', 'votet', 'change name & upload photo', 'delete messages from channel', 'check username', 'get recipients', 'find document', 'edit messages', 'get history of dialog']

    print(Fore.RED + 'Enter number of function and number of bot!')
    [print(Fore.LIGHTYELLOW_EX + str(id), Fore.LIGHTGREEN_EX + '==>', Fore.LIGHTBLUE_EX +i) for id, i in enumerate(lst_functions) if i]
    sys.exit(1)

if len(sys.argv) == 4:
    date_min = sys.argv[3]
    channel_username = sys.argv[3]

n = int(sys.argv[2])-2
entry = int(sys.argv[1])
df = pd.DataFrame()
df1 = pd.read_excel(TG, sheet_name='credentials')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

client = TelegramClient(f"{SESSIONS}/{re.sub(r'[.].+','', str(df1['phone'][n]))}", APP_ID, APP_TOKEN)

async def main():
    tl_errors = (TypeError, ValueError, AttributeError, errors.rpcerrorlist.PeerFloodError, errors.rpcerrorlist.UsernameInvalidError, errors.rpcerrorlist.BotInvalidError, errors.rpcbaseerrors.ForbiddenError, errors.rpcerrorlist.InputUserDeactivatedError, errors.rpcerrorlist.InputUserDeactivatedError, errors.rpcerrorlist.ChannelPrivateError, errors.rpcerrorlist.InviteRequestSentError, errors.rpcbaseerrors.BadRequestError)

    old_channels, files, lst, links, views, dates, topics = [], [], [], [], [], [], []

    t = r.uniform(10, 30)
    message = df1['text'][n]

    try: media_id = df1['media_id'][n].split('$')
    except AttributeError: media_id = []
    try: 
        next_id, last_id = int(df1['next_id'][n])-1, int(df1['last_id'][n])-1
    except (AttributeError, ValueError): next_id, last_id = -1, -1
    me = await client.get_me() 
    print (f'Phone >>> {me.phone}\n{me.first_name} {me.last_name}\t{me.id}\t{me.username}\nHave {len(media_id)} attachments!')

    if entry == 26: #get dialog info and get data about participants
        column_names = ['id', 'message', 'date'] 
        raw_dict = {i:[] for i in column_names}
        async for message in client.iter_messages(SECRET_CHANNEL):
            try:
                if message.from_id.user_id:
                    print(message.id)
                    raw_dict['id'].append(message.from_id.user_id)
                    raw_dict['message'].append(message.message)
                    raw_dict['date'].append(str(message.date))
            except AttributeError: pass
        pd.DataFrame(raw_dict).to_excel('data.xlsx', index=False)
        input('> ')
        df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
        ids = list({i for i in df['id']})
        ids.sort()
        new_dict = {i:[] for i in ['id', 'username', 'full name', 'phone', 'message', 'date']}
        for i in ids:
            user = await client(GetFullUserRequest(i))
            first_name = user.users[0].first_name if user.users[0].first_name else ""
            last_name = user.users[0].last_name if user.users[0].last_name else ""
            full_name = f"{first_name} {last_name}".strip()
            username = user.users[0].username if user.users[0].username else "-"
            phone = user.users[0].phone if user.users[0].phone else "-"
            for id, j in enumerate(df['id']):
                if i == j:
                    new_dict['id'].append(i)
                    new_dict['username'].append(username)
                    new_dict['full name'].append(full_name)
                    new_dict['phone'].append(phone)
                    new_dict['message'].append(str(df['message'][id]))
                    new_dict['date'].append(str(df['date'][id]))
            print(i)
        pd.DataFrame(new_dict).to_excel('new_data.xlsx', index=False)

    elif entry == 25: #edit messages, use bot 2
        async for message in client.iter_messages(MAX_CHANNEL, search='video: '):
            message_lst = message.text.split('\n')
            for id, line in enumerate(message_lst):
                if 'video: ' in line:
                    message_lst.pop(id)
            await client.edit_message(MAX_CHANNEL, message.id, '\n'.join(message_lst))


    elif entry == 23: #I don't know))
        #data = [i for i in cur.execute('select id, link, title, members, type, city, sub_region, region, description, bot, user, suggest, keyword, note, priority from channels where suggest != 1')]
        data = [i[0] for i in cur.execute('select link from channels ')]
        df2 = pd.read_excel(TG, sheet_name='channels')

        #letters = [chr(i) for i in range(ord('a'), ord('o'))]
        #for id, i in enumerate(letters):
        for id, i in enumerate(df2['link']):
            if str(i) != 'nan' and i not in data and i not in lst:
                lst.append(i)
            
        df['link'] = lst 
        df.to_excel('tg_data.xlsx')

    elif entry == 22: #clean false bots
        with open('false') as f:
            for i in f.read().split('\n'):
                if i:
                    links = [k for k in cur.execute(f"select link, city, sub_region, region, keyword, note, priority from channels where link = '{i}'")]
                    #links = set(links)
                    for j in links:
                        print(j[0]+'\t'+j[4]+'\t'+j[5]+'\t'+str(j[6]))
                    #cur.execute(f"delete from false_bots where username='{i}'")
#                    try:
#                        result = await client(functions.account.CheckUsernameRequest(username=i))
#                        print(i, '==>', result)
#                    except errors.rpcerrorlist.UsernameInvalidError:
#                        print(i, '==>', 'free')
#                    except errors.rpcerrorlist.FloodWaitError as e:
#                        if re.search(r'A wait of \d+ seconds', str(e)):
#                            wait_time = re.search(r' \d+ ', str(e)).group(0)
#                            print(e, j)
#                            await asyncio.sleep(int(str(wait_time).strip()))
#                            try:
#                                result = await client(functions.account.CheckUsernameRequest(username=i))
#                                print(i, '==>', result)
#                            except errors.rpcerrorlist.UsernameInvalidError:
#                                print(i, '==>', 'free')

    elif entry == 21: 
        print('Under development!')
    
    elif entry == 20:
        photo_path = str(df1['media_id'][n])
        first_name = str(df1['name'][n]).split(' ')[0]
        last_name = str(df1['name'][n]).split(' ')[1]
        await client(UpdateProfileRequest(first_name=first_name, last_name=last_name))
        await asyncio.sleep(r.uniform(5, 10))
        file = await client.upload_file(photo_path)
        await client(UploadProfilePhotoRequest(file=file))
        username = str(df1['username'][n]).strip()
        print(username)
        if username in ['nan', 'None']:
            new_username = input('Username >>> ').strip()
            await client(UpdateUsernameRequest(new_username))


    elif entry == 19:
        message = await client.get_messages(channel_username, ids=message_poll)
        await message.click(0)

    elif entry == 18:
        con1 = sqlite3.connect(TG_DEADS_DATA)
        cur1 = con1.cursor()        
        channels = [i[1][13:] for i in cur1.execute("select id, link from tg_ref")]

        for channel in channels:
            try:last_id = max([int(i[0].split('/')[-1]) for i in cur1.execute("select link from raw_data where link like ?", [f"%{channel}%"])])
            except ValueError: last_id=0
            async for message in client.iter_messages(channel, limit=10000, reverse=True, offset_id=last_id):   
                if message.message:
                    raw = str(message.message)
                    date = str(message.date).split(' ')[0]
                    link = f'https://t.me/{channel}/'+str(message.id)
                    try:
                        cur1.execute("insert into raw_data (raw, date, link) values (?,?,?)", [raw, date, link])
                        print(channel, '>>>', message.id)
                    except sqlite3.IntegrityError: pass
        con1.commit()
        cur1.close()
        con1.close()

    elif entry == 17:
        channels = [i[1][13:] for i in cur.execute("select id, link from channels where note='monthly_report'")]
        for i in channels:
            async for message in client.iter_messages(i):
                date = str(message.date).split(' ')[0]
                date = int(''.join(date.split('-')))

                if date >= int(date_min):
                    links.append(f'https://t.me/{i}/{str(message.id)}')
                    views.append(message.views)
                    dates.append(str(message.date))
                    topics.append(i)

                else: break
        df['link'] = links
        df['views'] = views
        df['date'] = dates
        df['channel'] = topics
        df.to_excel('TG_views_statistic.xlsx')

    elif entry == 16:
        df2 = pd.read_excel(TG, sheet_name='published_posts')
        my_base = [i[0] for i in cur.execute('select link from published_posts')]

        for id, i in enumerate(df2['link']):
            if str(i) != 'nan':
                link = i.lower().strip()
                i00 = link.split('https://t.me/')
                i1 = i00[1]
                i0 = i1.split('/')
                i1 = i0[0]
                i2 = int(i0[1])
                try:
                    post = await client.get_messages(entity=i1, ids=i2)

                    try: channel_id = int(post.chat.id)
                    except: channel_id = 0

                    try: 
                        members = await client(GetFullChannelRequest(post.chat.id))
                        members = members.full_chat.participants_count
                    except: members = 0 

                    try: views = int(post.views)
                    except: views = 0

                    try: repost = int(post.forwards)
                    except: repost = 0

                    try: date = int(str(post.date).split(' ')[0].replace('-',''))
                    except: date = 0

                    try: reaction = sum([i.count for i in post.reactions.results if i.count])
                    except AttributeError: reaction = 0

                    try: comment = post.replies.replies 
                    except: comment = 0

                    await asyncio.sleep(3)

                    if link not in my_base:
                        try:
                            cur.execute("insert into published_posts  (id,members, link, views, likes, comments, reposts, task, date) values (?,?,?,?,?,?,?,?,?)", (channel_id, int(members), link, views, reaction, comment, repost, str(df2['task'][id]), date)), print(id+2, 'new')
                        except sqlite3.IntegrityError: 
                            cur.execute("update published_posts set views = ?, likes = ? , members = ?, comments = ?, reposts = ? where link=?", (views, reaction, int(members), comment, repost, link)), print(id+2, 'updated')
                    elif link in my_base and post.views != 0:
                        cur.execute("update published_posts set views = ?, likes = ? , members = ?, comments = ?, reposts = ? where link=?", (views, reaction, int(members), comment, repost, link)), print(id+2, 'updated')
                    elif link in my_base and post.views == 0:
                        print(id+2, 'removed >>> ', link)
                except (AttributeError, NameError, ValueError, errors.rpcerrorlist.ChannelPrivateError, errors.rpcerrorlist.UsernameInvalidError) as e: print(id+2, e, link) 

    elif entry == 15:
        posts_for_commenting = sys.argv[3].split(r"://t.me/")
        for i in posts_for_commenting[1:]:
            post_to_comment = i.split('/')
            channel = post_to_comment[0]
            post = int(post_to_comment[1])

            async def comment_on_post():
                comment = await client.send_message(channel, message=message, comment_to=post)

                async for cmt in client.iter_messages(channel, reply_to=post):
                    if int(cmt.from_id.user_id) == int(me.id):
                        print('https://t.me/' + i + '?comment='+str(cmt.id))

            try: await comment_on_post()
            except errors.rpcerrorlist.ChatGuestSendForbiddenError:
                full_channel = await client(GetFullChannelRequest(channel))
                discussion_group_id = full_channel.full_chat.linked_chat_id

                try:
                    await client(JoinChannelRequest(discussion_group_id))
                    await asyncio.sleep(30,100)
                    await comment_on_post()
                except errors.rpcerrorlist.InviteRequestSentError: pass

    elif entry == 14:
        l1, l2, l3, l4, l5, l6, l7 = [], [], [], [], [], [], []
        next_id, last_id = int(df1['next_id'][n])-2, int(df1['last_id'][n])-2
        df2 = pd.read_excel(TG, sheet_name='channels')

        async def get_channel_info(username):
            chat = await client(functions.channels.GetFullChannelRequest(channel=username))
            l1.append(int(chat.full_chat.id))
            l2.append(str('https://t.me/'+username))
            l3.append(str(chat.chats[0].title))
            l4.append(int(chat.full_chat.participants_count))

            if chat.chats[0].broadcast: l5.append('CHANNEL')
            elif not chat.chats[0].broadcast: l5.append('SUPERGROUP')

            l6.append(str(chat.full_chat.about))
            l7.append(str(df2['keyword'][id]))
            print(id+2)

        for id, i in enumerate(df2['link']):
            if last_id >= id >= next_id:
                if str(i) == 'nan': continue

                i = str(i).lower().strip()[13:]

                try: await get_channel_info(i)
                except tl_errors as e:

                    if re.search(r'^A wait of \d+ seconds', str(e)):
                        wait_time = re.search(r' \d+ ', str(e)).group(0)
                        print(e)
                        await asyncio.sleep(int(str(wait_time).strip()))
                        
                        try: await get_channel_info(i)
                        except tl_errors as e: print(e)

                    else : print(e)

        df['id'] = l1
        df['link'] = l2
        df['title'] = l3
        df['members'] = l4
        df['type'] = l5
        df['description'] = l6
        df['keyword'] = l7
        df.to_excel(f'{next_id+2}-{last_id+2}_tg_channels.xlsx')
    
    elif entry == 24:
        df0 = open(SEARCH_CHANNELS, 'r').read().split('\n')
        df0 = [i for i in df0 if i]
        document_name = media_id[0].split('/')[-1]
        #document =  await client.send_file('me', media_id[0])
        #print(document.file.size)
        document_size = 0
        for id, j in enumerate(df0):
            if last_id >= id >= next_id:
                try:
                    async for doc in  client.iter_messages(j[13:], filter=InputMessagesFilterDocument):
                        post_date = int(str(doc.date).split(' ')[0].replace('-',''))
                        if post_date < int(date_min) : break
                        if doc.file and doc.file.ext == '.pdf':
                            if doc.file.name.lower().strip() == document_name.lower().strip():
                                print(Fore.LIGHTBLUE_EX + j + '/'+str(doc.id))
                            if  int(doc.file.size) == document_size:
                                print(Fore.LIGHTMAGENTA_EX + j +'/'+str(doc.id))
                except tl_errors as e: print(e)

    elif entry == 13:
        df0 = open(SEARCH_CHANNELS, 'r').read().split('\n')
        df0 = [i for i in df0 if i]
        video_name = media_id[0].split('/')[-1]
        clip = VideoFileClip(media_id[0])
        video_duration = int(clip.duration)
        video_size = os.path.getsize(media_id[0])
        clip.close()
        for id, j in enumerate(df0):
            if last_id >= id >= next_id:
                try:
                    async for video in  client.iter_messages(j[13:], filter=InputMessagesFilterVideo):
                        post_date = int(str(video.date).split(' ')[0].replace('-',''))
                        if post_date < int(date_min) : break
                        seek_video = int(video.media.document.attributes[0].duration)
                        seek_text = str(video.text).lower()
                        seek_size = video.media.document.size
                        if  len(video.media.document.attributes) > 1 and video_name.lower() == str(video.media.document.attributes[1].file_name).lower():
                            print(Fore.LIGHTBLUE_EX + j + '/'+str(video.id))
                            break
                        if seek_video == video_duration:
                            print(Fore.LIGHTYELLOW_EX + j + '/' + str(video.id))
                        if video_size == seek_size:
                            print(Fore.LIGHTMAGENTA_EX + j +'/'+str(video.id))
                except tl_errors as e: 
                    if 'DocumentAttributeHasStickers' in str(e):
                        print(Fore.LIGHTRED_EX + j + '/'+str(video.id))
                    else: print(e) 

    elif entry == 12:
        df0 = open(SEARCH_CHANNELS, 'r').read().split('\n')
        df0 = [i for i in df0 if i]
        for id, j in enumerate(df0):
            if last_id >= id >= next_id:
                try:
                    async for photo in  client.iter_messages(j[13:], filter=InputMessagesFilterPhotos):
                        post_date = int(str(photo.date).split(' ')[0].replace('-',''))
                        if post_date < int(date_min) : break
                        media = await photo.download_media()
                        imageB_pil = Image.open(media)
                        imageA_pil = Image.open(media_id[0])
                        hashA = imagehash.average_hash(imageA_pil)
                        hashB = imagehash.average_hash(imageB_pil)
                        os.remove(media)
                        cutoff = 5
                        if hashA - hashB < cutoff:
                            print(id+1, 'https://t.me/'+j[13:]+'/'+str(photo.id))
                            break
                except tl_errors as e: print(e)     

    elif entry == 11:
        channel_username = sys.argv[3].split(r'https://t.me/')[-1]
        channels = [channel_username]
        for i in channels:
            await client(JoinChannelRequest(i))
            await asyncio.sleep(r.uniform(10, 20))

    elif entry == 10:
        links = input('Enter links on chatlists >>> ').split(' ')
        for i in links:
            i = i.split('/')
            result = await client(functions.chatlists.CheckChatlistInviteRequest(slug=i[4]))
            peers = result.peers
            await client(functions.chatlists.JoinChatlistInviteRequest(slug=i[4],peers=peers
    ))      
            await asyncio.sleep(3)

    elif entry == 9: #change cloud password
        result = await client.edit_2fa(current_password=str(df1['note'][n]), new_password=PASSWORD)
        print(result)

    elif entry == 8: #increase views on last 10 posts of selected channels
        channels_for_support = [i[1][13:] for i in cur.execute("select id, link from channels where note = 'support'")]

        for channel in channels_for_support:
            ms_ids = []
            async for i in client.iter_messages(channel, 10): ms_ids.append(i.id)
            await client(functions.messages.GetMessagesViewsRequest(peer=channel, id=ms_ids, increment=True))
            await asyncio.sleep(10)

    elif entry == 0: #get chats and groups for forwarding
        df0 = open(CHATS_GROUPS, 'w')
        df11 = open(FORWARD_LOG, 'a')
        df2 = open(FORWARD_LOG, 'r').read().split('\n')
        df2 = [int(i.split('\t')[0]) for i in df2 if i]
        our_channels = [int(j) for j in df4['id']]
        dialogs = await client.get_dialogs()
        entry1 = int(input('0 >>> forward\n1 >>> link\n2 >>> text\n3 >>> media\n>>> '))
        if entry1 == 1:
            bann = 'embed_links'
        elif entry1 == 2:
            bann = 'send_messages'
        elif entry1 == 3:
            bann = 'send_media'
        for id, i in enumerate(dialogs):
            if i.entity.id not in our_channels and not isinstance(i.entity, User) and int(i.entity.id) not in df2:
                try:
                    if entry1 != 0 and not i.entity.broadcast  and not i.entity.slowmode_enabled and not getattr(i.entity.default_banned_rights, bann):
                        try:
                            if i.entity.username: lst.append(str(i.entity.id)+'\t'+'https://t.me/'+str(i.entity.username))
                            else: lst.append (str(i.entity.id)+'\t'+'https://t.me/c/'+str(i.entity.id))
                        except AttributeError as e: print(e)#lst.append(str(i.entity.id)+'\t'+'error')         
                    elif entry1 == 0 and not i.entity.broadcast  and not i.entity.slowmode_enabled:
                        try:
                            if i.entity.username: lst.append(str(i.entity.id)+'\t'+'https://t.me/'+str(i.entity.username))
                            else: lst.append (str(i.entity.id)+'\t'+'https://t.me/c/'+str(i.entity.id))
                        except AttributeError as e: print(e) #lst.append(str(i.entity.id)+'\t'+'error')
                except AttributeError as e: print(e)
        lst.sort()
        df0.write('\n'.join(lst)+'\n'), df0.close()
        df11.write('\n'.join(lst)+'\n'), df11.close()

    elif entry == 1: #leave channels/chats/users except ours
        our_channels = [j[0] for j in cur.execute("select id from channels where keyword='наш'")]
        dialogs = await client.get_dialogs()
        for id, i in enumerate(dialogs):
            if i.entity.id not in our_channels:
                await client.delete_dialog(dialogs[id])
                print(id)

    elif entry == 2: #send to bot/user
        with open(RECIPIENTS, 'r') as f:
            df0 = [str(i) for i in f.read().split('\n') if i]
        
        for id, i in enumerate(media_id):
            if '.mp4' in i:
                clip = VideoFileClip(i)
                duration = int(clip.duration)
                width = int(clip.w)
                height = int(clip.h)
                clip.close()
                video_attributes = DocumentAttributeVideo(duration=duration, w=width, h=height)
                files = await client.send_file('me', i, attributes=[video_attributes], supports_streaming=True, caption=message)
            else: 
                file = await client.upload_file(i)
                files.append(i)

        async def sender():
            if len(media_id) == 0: await client.send_message(peer_id, message, link_preview=True)
            elif len(media_id) == 1 and '.mp4' in  media_id[0]: await client.send_file(peer_id, files.media, caption=message)
            elif len(media_id) >= 1: await client.send_file(peer_id, files, caption=message)
            print(id)
            await asyncio.sleep(r.uniform(1, 60))

        async def send_to_bot_user():
            if j.lower().strip()[-3:] == 'bot':
                result = await client(functions.messages.StartBotRequest(bot=peer_id, peer=me.id, start_param='start'))
                await asyncio.sleep(r.uniform(7, 12))
                last_message = (await client.get_messages(peer_id, 1))[0]
                if last_message.message == 'Выберите ваш язык:':
                    await last_message.click(text='Русский')
                    await asyncio.sleep(r.uniform(3, 4))
            await sender()

        def add_error_record(record):
            print(record)
            lst.append(record)
       
        for id, j in enumerate(df0):
            if last_id >= id >= next_id:
                j = str(j).strip()
                try:
                    peer = await client.get_input_entity(j)
                    peer_id, access_hash = peer.user_id, peer.access_hash
                except tl_errors as e:
                    add_error_record(j + '\t' + str(e))
                    continue 
                try: await send_to_bot_user() 
                except tl_errors as e:
                    try:
                        if '(caused by StartBotRequest)' in str(e): await sender()

                        else: add_error_record(j + '\t' + str(e))

                    except errors.rpcerrorlist.PeerFloodError as e: print(e)
                    except tl_errors as e: add_error_record(j + '\t' + str(e))

                except errors.FloodWaitError as e:
                    print('Flood wait for ', e.seconds)
                    if e.seconds > 7200: 
                        print('Flooded')
                        break
                    await asyncio.sleep(e.seconds)
                    try: await send_to_bot_user()
                    except tl_errors as e: 
                        try:
                            if '(caused by StartBotRequest)' in str(e): await sender()
                            else: add_error_record(j + '\t' + str(e))
                        except tl_errors as e: add_error_record(j + '\t' + str(e))

        lst = list(set(lst))
        if len(lst) > 0:
            with open(RECIPIENTS_FALSE, 'a') as f: f.write('\n'.join(lst)+'\n')
    
    elif entry == 4: #forward post/send to chat
        if len(sys.argv) < 4:
            print(Fore.LIGHTYELLOW_EX + "0 ==> forward\n1 ==> link/text\n2 ==> media")
            exit()
        entry1 = int(sys.argv[3])

        with open(CHATS_GROUPS, 'r') as f:
            df0 = [int(i.split('\t')[0])  for i in f.read().split('\n') if i]
        with open(CHATS_GROUPS, 'r') as f:
            df00 = [str(i.split('\t')[-1])  for i in f.read().split('\n') if i]
        dialogs = await client.get_dialogs()
        my_dialogs = [int(i.entity.id) for i in dialogs]

        if entry1 == 0:
            message = message.split('https://t.me/')
            message = message[1].split('/')
            message_id = int(message[1])
            from_chat = str(message[0])
            await client(JoinChannelRequest(from_chat))

        if entry1 == 2:
            message=str(message)
            tg_medias = []
            for id, i in enumerate(media_id):
                tg_media = await client.upload_file(i)
                tg_medias.append(i)

        for id, j in enumerate(df0):
            if last_id >= id >= next_id:
                try:
                    if j not in my_dialogs:
                        await client(JoinChannelRequest(df00[id][13:]))
                        await asyncio.sleep(r.uniform(30, 100))
                    if entry1 == 0:
                        repost = await client.forward_messages(j[13:], message_id, from_chat)
                        print(j+'/'+str(repost.id))
                        lst.append(j+'/'+str(repost.id))
                    elif entry1 == 1:
                        repost = await client.send_message(j, message)
                        print(df00[id] + '/' + str(repost.id))
                    elif entry1 == 2:
                        repost = await client.send_file(j[13:], tg_medias, supports_streaming=True,caption=message)
                        print(j+'/'+str(repost[0].id))
                    await asyncio.sleep(r.uniform(30, 100))

                except tl_errors as e:
                    print(Fore.LIGHTRED_EX + df00[id] + ' ==> ' + str(e))
                    if re.search(r'A wait of \d+ seconds', str(e)):
                        wait_time = re.search(r' \d+ ', str(e)).group(0)
                        print(e, j)
                        await asyncio.sleep(int(str(wait_time).strip()))
                        try:
                            if entry1 == 0:
                                repost = await client.forward_messages(j[13:], message_id, from_chat)
                                print(j+'/'+str(repost.id))
                                lst.append(j+'/'+str(repost.id))
                            elif entry1 == 1:
                                repost = await client.send_message(j[13:], message)
                                print(j+'/'+str(repost.id))
                            elif entry1 == 2:
                                repost = await client.send_file(j[13:], tg_medias, supports_streaming=True,caption=message)
                                print(j+'/'+str(repost[0].id))
                            await asyncio.sleep(r.uniform(30, 100))
                        except tl_errors as e: lst.append(str(e) +'\t'+ str(df00[id]))

                    else: 
                        try:lst.append(str(e) +'\t'+str(df00[id]))
                        except IndexError: lst.append(str(e))
        file = open(f'tg_forwarder_links', 'a')
        file.write('\n'.join(lst)+'\n'), file.close()

    elif entry == 3:
        print('Under development!')
        #await client.send_message('me', message)
        #await client(UpdateProfileRequest(about="test"))

    elif entry == 5: #Get activation code
        async for message in client.iter_messages(777000, 1): 
            print(re.search(r'\d+', message.text).group(0))
    
    elif entry == 6: #Join chat
        df0 = open(CHATS_GROUPS, 'r').read().split('\n')
        df0 = [str(i) for i in df0 if i]
        my_groups = []
        dialogs = await client.get_dialogs()

        for id, i in enumerate(dialogs):
            try: my_groups.append(i.entity.id)
            except AttributeError: pass

        for id, j in enumerate(df0):
            if last_id >= id >= next_id:
                try:
                    discuusion_group = await client(GetFullChannelRequest(j))
                    await asyncio.sleep(r.uniform(5, 10))
                    for i in discuusion_group.chats:
                        if not i.broadcast and i.id not in my_groups:
                            await client(JoinChannelRequest(i.id))
                            await asyncio.sleep(r.uniform(500, 700))
                    print(id+1, j) 

                except tl_errors as e:
                    if re.search(r'^A wait of \d+ seconds', str(e)):
                        wait_time = re.search(r' \d+ ', str(e)).group(0)
                        print(e, j)
                        await asyncio.sleep(int(str(wait_time).strip()))
                        try:
                            discuusion_group = await client(GetFullChannelRequest(j))
                            await asyncio.sleep(r.uniform(5, 10))
                            for i in discuusion_group.chats:
                                await client(JoinChannelRequest(i.id))
                                await asyncio.sleep(r.uniform(500, 700))
                            print(id+1, j) 
                        except tl_errors as e: print(j, e), lst.append(j+'\t'+str(e))
                    else: lst.append(j+'\t'+str(e))
        file = open(f'tg_errors', 'a')
        file.write('\n'.join(lst)+'\n'), file.close()

    elif entry == 7: #check if channel is active
        now = datetime.now().astimezone()
#         links = [i[0] for i in cur.execute("select link from channels where type='CHANNEL' and status='check' and suggest = 1")]
#         print(*links, sep='\n')
#         exit()
        df2 = pd.read_excel(TG, sheet_name='channels')
        next_id, last_id = int(df1['next_id'][n])-2, int(df1['last_id'][n])-2
        for id, i in enumerate(df2['link']):
            if last_id >= id >= next_id:
                if str(i) == 'nan': continue
                print(id)
                try:
                    last_message = await client.get_messages(i[13:], limit=1)

                    if last_message:
                        if now - last_message[0].date.astimezone() <= timedelta(days=7):
                            lst.append(i + '\tactive')
                        else:  lst.append(i + '\tdead')

                    else: lst.append(i + '\terror')
                except tl_errors as e:
                    lst.append(i + f'\t{e}')
        with open('tg_status', 'a') as f: f.write('\n'.join(lst)+'\n')

with client: client.loop.run_until_complete(main())

con.commit()
cur.close()
con.close()
