

class KijijiAd():

    def __init__(self, ad):
        self.title = ad.find('a', {"class": "title"}).text.strip()
        self.id = ad['data-listing-id']
        self.ad = ad
        self.info = {}

        self.__locate_info()
        self.__parse_info()

    def __locate_info(self):
        # Locate ad information
        self.info["Title"] = self.ad.find('a', {"class": "title"})
        self.info["Image"] = str(self.ad.find('img'))
        self.info["Url"] = self.ad.get("data-vip-url")
        self.info["Details"] = self.ad.find(
            'div', {"class": "details"})
        self.info["Description"] = self.ad.find(
            'div', {"class": "description"})
        self.info["Date"] = self.ad.find(
            'span', {"class": "date-posted"})
        self.info["Location"] = self.ad.find('div', {"class": "location"})
        self.info["Price"] = self.ad.find('div', {"class": "price"})
        self.info["DataSource"] = str(self.ad.find('img').get('data-src'))

    def __parse_info(self):
        # Parse Details and Date information
        self.info["Details"] = self.info["Details"].text.strip() \
            if self.info["Details"] is not None else ""
        self.info["Date"] = self.info["Date"].text.strip() \
            if self.info["Date"] is not None else ""

        # Parse remaining ad information
        for key, value in self.info.items():
            if value:
                if key == "Url":
                    self.info[key] = 'http://www.kijiji.ca' + value

                elif key == "Description":
                    self.info[key] = value.text.strip() \
                        .replace(self.info["Details"], '')

                elif key == "Location":
                    self.info[key] = value.text.strip() \
                        .replace(self.info["Date"], '')
                    
                elif key == "Image":
                    self.info[key] = '<img src =\"' + (self.info["DataSource"]) + '\"/>'

                elif key not in ["DataSource", "Details", "Date"]:
                    self.info[key] = value.text.strip()
