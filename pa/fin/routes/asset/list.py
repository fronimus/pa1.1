from pa.fin.routes.asset import asset


@asset.route('asset/list')
def asset_list():
    return "Asset List Page"
