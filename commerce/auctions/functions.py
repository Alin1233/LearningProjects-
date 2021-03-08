from .models import *


def price(listings):
    #querry the db for all the bids made for a listing and append the highest bid to a list
    current_price = []
    for listing in listings:
        bids=Bids.objects.filter(listing__title=listing.title).order_by('-bid')
        current_price.append(bids[0])
    return(current_price)
