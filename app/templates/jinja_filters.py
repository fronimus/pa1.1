from app import app


@app.template_filter()
def bin2str(binary_string):
    return binary_string.decode('utf-8')


@app.template_filter()
def debug_obj(obj):
    try:
        return vars(obj)
    except Exception:
        return obj
