from pa.fin.routes.asset import asset


@asset.route('asset/list')
def list():
    return "Asset List Page"
