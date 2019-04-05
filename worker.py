from __future__ import print_function

import os
import discord
import asyncio
import datetime
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools
import jwt
from google.oauth2 import service_account

IMG_TYPE = [".gif", ".jpeg", ".jpg", ".png", ".tiff"]
CLIENT = discord.Client()

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_INFO = os.environ.get('GoogleServiceAccount')
credentials = service_account.Credentials.from_service_account_info(
	SERVICE_ACCOUNT_INFO, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)


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
            await CLIENT.send_message(message.channel, "PON!")

        #PONx3 GIF ---------------------------------------------------------------------------------
        if "_ponx3" in message.content:
            await CLIENT.send_message(message.channel, "https://media.giphy.com/media/5yBoVAfQXjthm/200w_d.gif")
        # ------------------------------------------------------------------------------------------
		
		#Schedule For the Week ---------------------------------------------------------------------
        if "_schedule" in message.content:
            now = datetime.datetime.utcnow()
            now = now.isoformat() + 'Z'
            nextWeek = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'
            events_result = service.events().list(calendarId=os.environ.get('CalendarId'),
                                                  singleEvents=True, orderBy='startTime', timeMin=now,
                                                  timeMax=nextWeek).execute()

            events = events_result.get('items', [])
            eventsMessages = []

            if not events:
                print('No upcoming events found.')
            for event in events:
                summary = event['summary']
                location = event.get('location')
                description = event.get('description')
                start = event['start'].get('dateTime', event['start'].get('time'))

                if start is not None:
                    # Trim the UTC offset because python 3.6 is dumb and doesn't know how to handle the colon in the offset. It's fixed in 3.7
                    startTime = datetime.datetime.strptime(str(start)[:-6], "%Y-%m-%dT%H:%M:%S")
                    endTime = datetime.datetime.strptime(str(event['end'].get('dateTime', event['end'].get('time')))[:-6],
                                                         "%Y-%m-%dT%H:%M:%S")
                    eventsMessages.extend(BuildEventMessage(summary, startTime.strftime("%m/%d/%Y"),
                                                          startTime.strftime("%I:%M %p"), endTime.strftime("%I:%M %p"),
                                                          location, description))

                else:
                    date = datetime.datetime.strptime(str(event['start'].get('dateTime', event['start'].get('date'))),
                                                      "%Y-%m-%d")
                    eventsMessages.extend(BuildEventMessage(summary, date.strftime("%m/%d/%Y"), None, None, location, description))

            await CLIENT.send_message(message.channel, ''.join(eventStrings))
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
                        await CLIENT.send_message(GALLERY_CHANNEL, embed=em)
                        break;

        if len(message.embeds) > 0:
            for current_embed in message.embeds:
                emURL = current_embed.url.lower()
                for imgType in IMG_TYPE :
                    if imgType in emURL:
                        em = discord.Embed()
                        em.set_image(url=current_embed.url);
                        await CLIENT.send_message(GALLERY_CHANNEL, embed=em)
                        break;
        # ------------------------------------------------------------------------------------------


def BuildEventMessage(summary, date, start, end, location, description):
    eventStrings = []
    eventStrings.append(":calendar:" + summary + "\n" + "When: " + date + " ")
    if start is not None and end is not None:
        eventStrings.append(start + "-" + end + "\n")
    if location is not None:
        eventStrings.append("Where: " + location + "\n")
    if description is not None:
        description = description.replace("<br>", "\n").replace("<b>", "**").replace("</b>", "**")
        eventStrings.append("Details: " + description + "\n")
    return eventStrings

CLIENT.run(os.environ.get('TOKEN', True))