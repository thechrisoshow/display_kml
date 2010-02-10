require 'uri'
require 'net/http'

while true do
  url = "http://display-kml.appspot.com/purge"
  r = Net::HTTP.get_response(URI.parse(url).host, URI.parse(url).path)
  puts r
end