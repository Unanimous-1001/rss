import json
import xml.etree.ElementTree as ET
import datetime
import pytz

def format_rss_date(dt):
    """Formats a datetime object for RSS pubDate with GMT+5 offset."""
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0500")

def get_gmt5_date():
    """Gets the current time in GMT+5."""
    utc_now = datetime.datetime.utcnow()
    gmt5_tz = pytz.timezone('Asia/Karachi') # Maldives is also GMT+5
    gmt5_now = utc_now.replace(tzinfo=pytz.utc).astimezone(gmt5_tz)
    return gmt5_now

def generate_rss_from_json(json_file_path, rss_file_path):
    """Generates an RSS feed XML file from a JSON file."""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file_path}")
        return

    root = ET.Element('rss', version='2.0', xmlns_media="http://search.yahoo.com/mrss/")
    channel = ET.SubElement(root, 'channel')
    ET.SubElement(channel, 'title').text = 'Manhwa Updates'
    ET.SubElement(channel, 'link').text = 'https://unanimous-1001.github.io/rss/'  # Replace with your website URL
    ET.SubElement(channel, 'description').text = 'Latest Manhwa Updates and Information'
    ET.SubElement(channel, 'language').text = 'en-us'
    ET.SubElement(channel, 'pubDate').text = format_rss_date(get_gmt5_date())
    ET.SubElement(channel, 'atom:link', rel="self", href="https://unanimous-1001.github.io/rss/rss1.xml", xmlns="http://www.w3.org/2005/Atom")

    for manhwa in data:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = manhwa['title']
        ET.SubElement(item, 'link').text = manhwa['link']
        description = f"""
            <img src="{manhwa['cover_image_url']}" alt="{manhwa['title']} Cover" width="200"><br/>
            <strong>Name:</strong> {manhwa['title']}<br/>
            <strong>Rank:</strong> {manhwa['rank']}<br/>
            <strong>Genres:</strong> {manhwa['genres']}<br/>
            <strong>Synopsis:</strong> {manhwa['synopsis']}
        """
        ET.SubElement(item, 'description').text = f"<![CDATA[{description}]]>"
        ET.SubElement(item, 'pubDate').text = manhwa['pubDate'] #use the date from the json file.
        ET.SubElement(item, 'guid').text = manhwa['guid']
        ET.SubElement(item, 'media:thumbnail', url=manhwa['cover_image_url'])

    tree = ET.ElementTree(root)
    tree.write(rss_file_path, encoding='utf-8', xml_declaration=True)
    print(f"RSS feed generated successfully: {rss_file_path}")

if __name__ == "__main__":
    json_file_path = "manhwa_data.json"  # Replace with your JSON file path
    rss_file_path = "rss1.xml"  # Replace with your desired RSS file path
    generate_rss_from_json(json_file_path, rss_file_path)
