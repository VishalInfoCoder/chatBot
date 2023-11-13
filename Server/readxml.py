import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('godget.xml')

# Get the root element
root = tree.getroot()

namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

# Extract URLs
urls = [url.text for url in root.findall('.//ns:loc', namespaces=namespace)]
set_url=set(urls)
print(len(set_url)) 
# Print the URLs

  