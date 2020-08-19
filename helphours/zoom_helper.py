import validators
from helphours.models.zoom_link import ZoomLink


class LinkParseError(Exception):
    def __init__(self, message):
        super().__init__(message)


def parse_links(raw_text):
    lines = [line.strip() for line in raw_text.splitlines()]
    zoom_links = []
    index = 0
    temp_description = ""
    for line in lines:
        if line:
            if index % 2 == 0:
                if len(line) > 256:
                    raise LinkParseError('Description too long: must be under 512 characters')
                temp_description = line
            else:
                url = line
                if not validators.url(url):
                    raise LinkParseError(f'Invalid url: {url}')
                new_link = ZoomLink(url=url, description=temp_description)
                zoom_links.append(new_link)
                temp_description = ''
            index += 1
    if index % 2 != 0:
        raise LinkParseError('Invalid input. There should be 1 description for every url')
    return zoom_links
