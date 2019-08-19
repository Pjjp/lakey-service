
from django.conf.urls import url

from . import commands


urlpatterns = [

    url(
        r'chunk/render_exploration_map',
        commands.DownloadRequestRenderCommands.as_view(),
        name='chunk.render_exploration_map'
    )
]