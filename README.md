# Converting edits.xml

So you have spent a day or more editing data in the wonderful [MAPS.ME](https://maps.me/en/download/)
application, but don't see your changes on the map? Most likely there were some errors uploading.
Try opening and closing the app, and then waiting for a minute. If that doesn't help, click a
searching icon (usually a magnifier) and type `?edits` with no spaces or quotes. You will see
a list of your edits. Scroll it down to see if there are any non-uploaded edits. If there are,
you may need this script.

Use a file manager to locate `/MapsWithMe/edits.xml` file. Share it to your email or messaging
app, so you can access the file at your computer. Then run this script:

    ./edits_to_josm.py /path/to/edits.xml josm_edits.xml

Then open the result (`josm_edits.xml`) in JOSM as a new layer. DO NOT UPLOAD THE FILE!
Use it to find non-uploaded objects and to compare tags with the objects currently in
OpenStreetMap.

## Author and License

Written by Ilya Zverev, published under a MIT license.
