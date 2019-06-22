

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
            'div', {"class": "details"}).text.strip()
        self.info["Description"] = self.ad.find(
            'div', {"class": "description"})
        self.info["Date"] = self.ad.find(
            'span', {"class": "date-posted"}).text.strip()
        self.info["Location"] = self.ad.find('div', {"class": "location"})
        self.info["Price"] = self.ad.find('div', {"class": "price"})

    def __parse_info(self):
        keys_to_pop = []

        # Parse ad information
        for key, value in self.info.items():
            if not value:
                keys_to_pop.append(key)

            else:
                if key == "Url":
                    self.info[key] = 'http://www.kijiji.ca' + value

                elif key == "Description":
                    self.info[key] = value.text.strip()\
                        .replace(self.info["Details"], '')

                elif key == "Location":
                    self.info[key] = value.text.strip()\
                        .replace(self.info["Date"], '')

                elif key not in ["Image", "Details", "Date"]:
                    self.info[key] = value.text.strip()

        for key in keys_to_pop:
            self.info.pop(key)
