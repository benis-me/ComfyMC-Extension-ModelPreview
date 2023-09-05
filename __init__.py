import os
import server
import folder_paths
from aiohttp import web


@server.PromptServer.instance.routes.get("/view_model/{type}")
async def view_model(request):
    type_name = request.match_info.get("type", None)
    if type_name is None:
        return web.Response(status=404)
    if not "filename" in request.rel_url.query:
        return web.Response(status=404)

    filename = request.rel_url.query["filename"]
    model_path = folder_paths.get_full_path(type_name, filename)
    if model_path is None:
        return web.Response(status=404)

    model_path = os.path.splitext(model_path)[0]
    for ext in ['png', 'jpg', 'webp', 'gif']:
        for appendix in ['', '_preview.', 'preview', 'previews.']:
            img_path = model_path + '.' + appendix + ext
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    return web.Response(body=f.read(), content_type=f'image/{ext}')
    return web.Response(status=404)

NODE_CLASS_MAPPINGS = {}
__all__ = ['NODE_CLASS_MAPPINGS']