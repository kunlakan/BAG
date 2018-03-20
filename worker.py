import discord
import asyncio

IMG_TYPE = [".gif", ".jpeg", ".jpg", ".png", ".tiff"]
CLIENT = discord.Client()

@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name + " (" + str(CLIENT.user.id) + ")")
    print('------')

#PONx3 Emotes (should crate set/get emotes function in the future)
@CLIENT.event
async def on_message(message):
    if(message.author != CLIENT.user):        
        if message.content == "Hello":
            await message.channel.send("PON!")

        #PONx3 GIF ---------------------------------------------------------------------------------
        if "_ponx3" in message.content:
            await message.channel.send("https://media.giphy.com/media/5yBoVAfQXjthm/200w_d.gif")
        # ------------------------------------------------------------------------------------------

        # GALLERY ----------------------------------------------------------------------------------
        #Post all image attachments and embeds to #gallery channel
        # ------------------------------------------------------------------------------------------
        GALLERY_CHANNEL = CLIENT.get_channel(418087684016308234)

        if len(message.attachments) > 0:
            for current_attachment in message.attachments:
                atURL = current_attachment.url.lower()
                for imgType in IMG_TYPE :
                    if imgType in atURL:
                        em = discord.Embed()
                        em.set_image(url=current_attachment.url);
                        await GALLERY_CHANNEL.send(embed=em)
                        break;

        if len(message.embeds) > 0:
            for current_embed in message.embeds:
                emURL = current_embed.url.lower()
                for imgType in IMG_TYPE :
                    if imgType in emURL:
                        em = discord.Embed()
                        em.set_image(url=current_embed.url);
                        await GALLERY_CHANNEL.send(embed=em)
                        break;
        # ------------------------------------------------------------------------------------------

        
CLIENT.run(os.environ.get('TOKEN'))
