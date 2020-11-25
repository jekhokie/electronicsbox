#!/usr/bin/env python
#
# Creates an image for display on a 7.5in Waveshare e-Paper display, such as the one seen here:
#   https://www.waveshare.com/product/7.5inch-hd-e-paper-b.htm
#
# TODO:
#   - DRY up the code, and organize into functions/better organization
#   - Better error handling in case of failed calls/etc.

import feedparser
import io
import os
import requests
import textwrap
import yaml
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
from pyowm import OWM
from yahoo_fin import stock_info
from xml.dom.minidom import parseString

# load configs
with open('config/settings.yml', 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)

# configurable parameters - update in config/settings.yml
font_file = config['font_file']
font_file_bold = config['font_file_bold']
font_file_italic = config['font_file_italic']
ticker_symbol = config['ticker_symbol']
rss_link = config['rss_link']
owm_api_key = config['owm_api_key']
owm_city_latitude = config['owm_city_latitude']
owm_city_longitude = config['owm_city_longitude']
sonos_host = config['sonos_host']

# image output configurations
output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')
image_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')

# constants
BLACK = 'rgb(0,0,0)'
WHITE = 'rgb(255,255,255)'
PAPER_W = 800   # e-paper width pixels
PAPER_H = 400   # e-paper height pixels
BOX_W = 5       # width of box outlines

# coordinates for start and center points of columns and rows
QUARTER_COL = PAPER_W/4/2
CENTER_COL_1 = QUARTER_COL
CENTER_COL_2 = PAPER_W/2 - QUARTER_COL
CENTER_COL_3 = PAPER_W/2 + QUARTER_COL
CENTER_COL_4 = PAPER_W - QUARTER_COL

START_COL_1 = 0
START_COL_2 = PAPER_W/4
START_COL_3 = PAPER_W/2
START_COL_4 = PAPER_W - PAPER_W/4

QUARTER_ROW = PAPER_H/4/2
CENTER_ROW_1 = QUARTER_ROW
CENTER_ROW_2 = PAPER_H/2 - QUARTER_ROW
CENTER_ROW_3 = PAPER_H/2 + QUARTER_ROW
CENTER_ROW_4 = PAPER_H - QUARTER_ROW

START_ROW_1 = 0
START_ROW_2 = PAPER_H/4
START_ROW_3 = PAPER_H/2
START_ROW_4 = PAPER_H - PAPER_H/4

#### API INITIALIZATION ####
owm = OWM(owm_api_key)
owm_manager = owm.weather_manager()
weather_data = None

#### DRAWING CANVAS ####
# create new drawing surface for image
img = Image.new("RGB", (PAPER_W, PAPER_H), (WHITE))
canvas = ImageDraw.Draw(img)

#### DIVIDERS ####
# draw dividers for data fields
canvas.rectangle((0, 0, PAPER_W, PAPER_H), outline=BLACK, width=BOX_W)
canvas.line([(PAPER_W/2 - BOX_W/2, 0), (PAPER_W/2 - BOX_W/2, PAPER_H)], fill=BLACK, width=BOX_W)
canvas.line([(PAPER_W - PAPER_W/4 - BOX_W/2, 0), (PAPER_W - PAPER_W/4 - BOX_W/2, 120)], fill=BLACK, width=BOX_W)
canvas.line([(PAPER_W/2 - BOX_W/2, 120), (PAPER_W, 120)], fill=BLACK, width=BOX_W)
canvas.line([(0, PAPER_H/2), (PAPER_W/2 - BOX_W/2, PAPER_H/2)], fill=BLACK, width=BOX_W)

#### UPDATE TIME ####
# last updated fonts
updated_font_heading = ImageFont.truetype(font_file_bold, 20)
updated_font = ImageFont.truetype(font_file, 15)

# capture current date/time
update_datetime = datetime.now()
update_time = update_datetime.strftime('%m/%d/%y @ %I:%M:%S %p')

# last updated information
canvas.rectangle((PAPER_W/2 - BOX_W/2, PAPER_H-50, PAPER_W, PAPER_H), fill=BLACK)
canvas.text((PAPER_W/2 + 10, PAPER_H-40), 'Last Updated:', font=updated_font_heading, fill=WHITE)
canvas.text((PAPER_W/2 + 180, PAPER_H-36), update_time, font=updated_font, fill=WHITE)

#### STOCK ####
# stock fonts
stock_font_ticker = ImageFont.truetype(font_file_bold, 40)
stock_font = ImageFont.truetype(font_file_bold, 20)
stock_font_diff = ImageFont.truetype(font_file_bold, 18)

# get yahoo ticket symbol
quote = stock_info.get_quote_table(ticker_symbol)
price = round(quote['Quote Price'], 2)
prev_close = round(quote['Previous Close'], 2)
delta = round(price - prev_close, 2)
symbol = '+' if delta >= 0 else '-'   # display up/down arrow based on movement

# format outputs for display
price_str = "${:.2f}".format(price)
diff_str = "({} ${:.2f})".format(str(symbol), abs(delta))

# calculate size of display values
ticker_center_x = PAPER_W - (PAPER_W / 4 / 2)
ticker_size = stock_font_ticker.getsize(ticker_symbol)
price_size = stock_font.getsize(price_str)
diff_size = stock_font_diff.getsize(diff_str)

# display values
canvas.text((CENTER_COL_4 - stock_font_ticker.getsize(ticker_symbol)[0]/2, 5), ticker_symbol, font=stock_font_ticker, fill=BLACK)
canvas.text((CENTER_COL_4 - stock_font.getsize(price_str)[0]/2, 55), price_str, font=stock_font, fill=BLACK)
canvas.text((CENTER_COL_4 - stock_font_diff.getsize(diff_str)[0]/2, 80), diff_str, font=stock_font_diff, fill=BLACK)

#### DATE ####
# date fonts
date_day = ImageFont.truetype(font_file_bold, 18)
date_display = ImageFont.truetype(font_file, 16)

# display values
cur_day = update_datetime.strftime('%A')
cur_date = update_datetime.strftime('%d %B %Y')
canvas.text((CENTER_COL_3 - date_day.getsize(cur_day)[0]/2, 25), cur_day, font=date_day, fill=BLACK)
canvas.text((CENTER_COL_3 - date_display.getsize(cur_date)[0]/2, 65), cur_date, font=date_display, fill=BLACK)

#### RSS ####
# rss fonts
rss_source = ImageFont.truetype(font_file_italic, 14)
rss_title = ImageFont.truetype(font_file_bold, 16)
rss_summary = ImageFont.truetype(font_file, 12)

# get latest RSS feed article
d = feedparser.parse(rss_link)
latest_article = d.entries[0]

# format the source
source_text = "[{}]".format(d.feed.title)
source_text_size = rss_source.getsize(source_text)

# wrap the article summary to fit in the box
title_width_chars = 40
summary_width_chars = 62
title_divider_width = 50

title_wrapper = textwrap.TextWrapper(width=title_width_chars, max_lines=2)
summary_wrapper = textwrap.TextWrapper(width=summary_width_chars, max_lines=5)

title_lines = title_wrapper.wrap(latest_article.title)
summary_lines = summary_wrapper.fill(latest_article.summary)

# display RSS details
title_line_height = rss_title.getsize(title_lines[0])
title_height = (2*title_line_height[1]) if len(title_lines) == 2 else title_line_height[1]

canvas.text((PAPER_W/4 - source_text_size[0]/2, 10), source_text, font=rss_source, fill=BLACK)
canvas.text((BOX_W + 5, 35), "\n".join(title_lines), font=rss_title, fill=BLACK)
canvas.line([(PAPER_W/4 - title_divider_width/2, title_height + 45), (PAPER_W/4 + title_divider_width/2, title_height + 45)], fill=BLACK, width=1)
canvas.text((BOX_W + 5, title_height + 55), summary_lines, font=rss_summary, fill=BLACK)

#### WEATHER ####
# weather fonts
weather_major_heading = ImageFont.truetype(font_file_bold, 18)
weather_heading = ImageFont.truetype(font_file_bold, 16)
weather_status = ImageFont.truetype(font_file_italic, 16)
weather_sub_heading = ImageFont.truetype(font_file_bold, 14)
weather_value = ImageFont.truetype(font_file, 14)

# get weather statistics
weather_data = owm_manager.one_call(lat=owm_city_latitude, lon=owm_city_longitude, exclude='minutely,hourly,alerts')

# display weather heading
canvas.text((START_COL_4 - weather_major_heading.getsize('Weather')[0]/2, 130), 'Weather', font=weather_major_heading, fill=BLACK)

# display current weather
cur_weather = weather_data.current
cur_temp = cur_weather.temperature('fahrenheit')
cur_wind = cur_weather.wind('miles_hour')
cur_status_display = cur_weather.detailed_status
cur_temp_display = "{:.0f} {}".format(cur_temp['temp'], '\u00b0')
cur_feels_display = "{:.0f} {}".format(cur_temp['feels_like'], '\u00b0')
cur_humidity_display = "{:.0f} %".format(cur_weather.humidity)
cur_wind_display = "{:.0f} mph".format(cur_wind['speed'])

canvas.text((CENTER_COL_3 - weather_heading.getsize('Current')[0]/2, 165), 'Current', font=weather_heading, fill=BLACK, width=1)
canvas.line([(CENTER_COL_3 - 85, 190), (CENTER_COL_3 + 85, 190)], fill=BLACK)
canvas.text((CENTER_COL_3 - weather_status.getsize(cur_status_display)[0]/2, 200), cur_status_display, font=weather_status, fill=BLACK)
canvas.text((START_COL_3 + 15, 230), 'Temp:', font=weather_sub_heading, fill=BLACK)
canvas.text((START_COL_3 + 120, 230), cur_temp_display, font=weather_value, fill=BLACK)
canvas.text((START_COL_3 + 15, 250), 'Feels Like:', font=weather_sub_heading, fill=BLACK)
canvas.text((START_COL_3 + 120, 250), cur_feels_display, font=weather_value, fill=BLACK)
canvas.text((START_COL_3 + 15, 270), 'Humidity:', font=weather_sub_heading, fill=BLACK)
canvas.text((START_COL_3 + 120, 270), cur_humidity_display, font=weather_value, fill=BLACK)
canvas.text((START_COL_3 + 15, 290), 'Wind:', font=weather_sub_heading, fill=BLACK)
canvas.text((START_COL_3 + 120, 290), cur_wind_display, font=weather_value, fill=BLACK)

# divider between current vs. today forecasted
canvas.line([(START_COL_4, 170), (START_COL_4, 320)], fill=BLACK, width=2)

# display today's forecasted weather
today_weather = weather_data.forecast_daily[0]
today_wind = today_weather.wind('miles_hour')
today_temp = today_weather.temperature('fahrenheit')
today_status_display = today_weather.detailed_status
today_temp_low_display = "{:.0f} {}".format(today_temp['min'], '\u00b0')
today_temp_high_display = "{:.0f} {}".format(today_temp['max'], '\u00b0')
today_humidity_display = "{:.0f} %".format(today_weather.humidity)
today_wind_display = "{:.0f} mph".format(today_wind['speed'])

canvas.text((CENTER_COL_4 - weather_heading.getsize('Today (Forecast)')[0]/2, 165), 'Today (Forecast)', font=weather_heading, fill=BLACK, width=1)
canvas.line([(CENTER_COL_4 - 85, 190), (CENTER_COL_4 + 85, 190)], fill=BLACK)
canvas.text((CENTER_COL_4 - weather_status.getsize(today_status_display)[0]/2, 200), today_status_display, font=weather_status, fill=BLACK)
canvas.text((START_COL_4 + 15, 230), 'Temp High:', font=weather_sub_heading, fill=BLACK)
canvas.text((START_COL_4 + 120, 230), today_temp_high_display, font=weather_value, fill=BLACK)
canvas.text((START_COL_4 + 15, 250), 'Temp Low:', font=weather_sub_heading, fill=BLACK)
canvas.text((START_COL_4 + 120, 250), today_temp_low_display, font=weather_value, fill=BLACK)
canvas.text((START_COL_4 + 15, 270), 'Humidity:', font=weather_sub_heading, fill=BLACK)
canvas.text((START_COL_4 + 120, 270), today_humidity_display, font=weather_value, fill=BLACK)
canvas.text((START_COL_4 + 15, 290), 'Wind:', font=weather_sub_heading, fill=BLACK)
canvas.text((START_COL_4 + 120, 290), today_wind_display, font=weather_value, fill=BLACK)

#### SONOS ####
# sonos fonts
sonos_major_heading = ImageFont.truetype(font_file_bold, 20)
sonos_now_playing = ImageFont.truetype(font_file_italic, 16)
sonos_sub_heading = ImageFont.truetype(font_file_bold, 14)
sonos_value = ImageFont.truetype(font_file, 14)

# get sonos currently playing information
sonos_artist = ""
sonos_track = ""
sonos_elapsed = ""
sonos_soap_url = "http://{}:1400/MediaRenderer/AVTransport/Control".format(sonos_host)
sonos_soap_headers = {'SOAPAction': 'urn:schemas-upnp-org:service:AVTransport:1#GetPositionInfo', 'Content-Type': 'text/xml; charset=UTF-8'}
sonos_soap_envelope = """<?xml version="1.0"?>
                         <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                           <s:Body>
                             <u:GetPositionInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
                               <InstanceID>0</InstanceID>
                               <Channel>Master</Channel>
                             </u:GetPositionInfo>
                           </s:Body>
                         </s:Envelope>
"""

try:
    sonos_response = requests.post(sonos_soap_url, data=sonos_soap_envelope, headers=sonos_soap_headers)
    sonos_response_xml = parseString(sonos_response.content)

    track = sonos_response_xml.getElementsByTagName('Track')[0]
    track_id = track.firstChild.nodeValue

    # check if anything is playing and, if so, get information
    if str(track_id) != '0':
        # elapsed time
        sonos_elapsed = sonos_response_xml.getElementsByTagName('RelTime')[0].firstChild.nodeValue

        # artist and track
        track_metadata_str = sonos_response_xml.getElementsByTagName('TrackMetaData')[0].firstChild.nodeValue
        track_metadata = parseString(track_metadata_str)
        sonos_track = track_metadata.getElementsByTagName('dc:title')[0].firstChild.nodeValue
        sonos_artist = track_metadata.getElementsByTagName('dc:creator')[0].firstChild.nodeValue
except:
    print('Failed to get information from Sonos device')

# wrap text to make it fit
sonos_value_width_chars = 40
sonos_value_wrapper = textwrap.TextWrapper(width=sonos_value_width_chars, max_lines=2)

sonos_artist_display = sonos_value_wrapper.wrap(sonos_artist)
sonos_track_display = sonos_value_wrapper.wrap(sonos_track)

# display the results
canvas.text((START_COL_2 - sonos_major_heading.getsize('SONOS')[0]/2, START_ROW_3 + 5), 'SONOS', font=sonos_major_heading, fill=BLACK)
canvas.line([(START_COL_2 - 45, START_ROW_3 + 35), (START_COL_2 + 45, START_ROW_3 + 35)], fill=BLACK, width=1)
canvas.text((START_COL_2 - sonos_now_playing.getsize('Now Playing')[0]/2, START_ROW_3 + 45), 'Now Playing', font=sonos_now_playing, fill=BLACK)
canvas.text((START_COL_1 + 15, START_ROW_3 + 80), 'Artist:', font=sonos_sub_heading, fill=BLACK)
canvas.text((START_COL_1 + 90, START_ROW_3 + 80), "\n".join(sonos_artist_display), font=sonos_value, fill=BLACK)
canvas.text((START_COL_1 + 15, START_ROW_3 + 120), 'Track:', font=sonos_sub_heading, fill=BLACK)
canvas.text((START_COL_1 + 90, START_ROW_3 + 120), "\n".join(sonos_track_display), font=sonos_value, fill=BLACK)
canvas.text((START_COL_1 + 15, START_ROW_3 + 160), 'Elapsed:', font=sonos_sub_heading, fill=BLACK)
canvas.text((START_COL_1 + 90, START_ROW_3 + 160), sonos_elapsed, font=sonos_sub_heading, fill=BLACK)

#### WRITE IMAGE ####
# write canvas to file and close
output_file = os.path.join(output_dir, 'output_image.png')
img.save(output_file)
img.close()
