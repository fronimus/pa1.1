from flask import render_template

from pa import db
from pa.fin.models import Record, Asset
from pa.fin.routes.asset import asset


class YieldsHistory:
    def __init__(self):
        self.yields_history_items = []

    def append(self, item):
        self.yields_history_items.append(item)


class YieldsHistoryItem:
    def __init__(self, start_date=None, end_date=None, yields=None):
        self.start_date = start_date
        self.end_date = end_date
        self.yields = yields


@asset.route('asset/analyse/all')
def analyse():
    assets_prices = {}
    for asset in db.session.query(Asset):
        query = db.session.query(Record).filter(Record.asset_id == asset.id).order_by(Record.date.asc()).all()
        assets_prices.update({asset.name: []})

        if len(query) >= 2:
            asset_price = {'amount': query[0].amount, 'date': query[0].date.isoformat()}
            assets_prices[asset.name].append(asset_price)

            asset.yields_history = YieldsHistory()
            pairs = zip(query[:-1], query[1:])

            for record, next_record in pairs:
                if not (record.is_replenish or next_record.is_replenish):
                    if asset_price['date'] != next_record.date.isoformat():
                        asset_price = {'amount': asset_price['amount'] + next_record.amount,
                                       'date': next_record.date.isoformat()}
                        assets_prices[asset.name].append(asset_price)
                    else:
                        asset_price['amount'] += next_record.amount

                    asset.yields_history.append(YieldsHistoryItem(start_date=record.date, end_date=record.date,
                                                                  yields=next_record.amount / asset_price['amount']))
                else:
                    if asset_price['date'] != next_record.date.isoformat():
                        asset_price = {'amount': asset_price['amount'] + next_record.amount,
                                       'date': next_record.date.isoformat()}
                        assets_prices[asset.name].append(asset_price)
                    else:
                        asset_price['amount'] += next_record.amount
        elif len(query) == 1:
            assets_prices[asset.name].append({'amount': query[0].amount, 'date': query[0].date.isoformat()})
    return render_template('asset.jinja2', assets_prices=assets_prices)
