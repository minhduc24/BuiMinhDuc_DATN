import shotstack_sdk as shotstack
import os

import pexelsapi.pexels
from shotstack_sdk.model.image_asset import ImageAsset
from shotstack_sdk.api               import edit_api
from shotstack_sdk.model.clip        import Clip
from shotstack_sdk.model.track       import Track
from shotstack_sdk.model.timeline    import Timeline
from shotstack_sdk.model.output      import Output
from shotstack_sdk.model.edit        import Edit
from shotstack_sdk.model.title_asset import TitleAsset
from shotstack_sdk.model.video_asset import VideoAsset
from shotstack_sdk.model.soundtrack  import Soundtrack
from shotstack_sdk.model.transition  import Transition
from config import SHOTSTACK_API_KEY,SHOTSTACK_HOST,SHOTSTACK_ASSETS_URL,PEXELS_API_KEY

api = pexelsapi.pexels.Pexels(PEXELS_API_KEY)
configuration = shotstack.Configuration(host= SHOTSTACK_HOST)
configuration.api_key['DeveloperKey'] = SHOTSTACK_API_KEY


def submit(data):
    min_clips = 4.0
    max_clips = 8.0
    clip_length = 2.0
    video_start = 4.0

    if data['soundtrack'] == 'Disco':
        data['soundtrack'] = 'https://videoaws.s3.ap-southeast-1.amazonaws.com/Disco.mp3'
    if data['soundtrack'] == 'Freeflow':
        data['soundtrack'] = 'https://videoaws.s3.ap-southeast-1.amazonaws.com/freeflow.mp3'
    if data['soundtrack'] == 'Melodic':
        data['soundtrack'] = 'https://videoaws.s3.ap-southeast-1.amazonaws.com/Melodic.mp3'

    search_videos = api.search_videos(
        query=data.get("search"),
        orientation='', size='', color='', locale='', page=1,
        per_page=max_clips
    )

    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)
        video_clips = []

        title_asset = TitleAsset(
            text=data.get('title'),
            style="minimal",
            size="small"
        )

        title_transition = Transition(
            _in="fade",
            out="fade"
        )

        title_clip = Clip(
            asset=title_asset,
            length=video_start,
            start=0.0,
            transition=title_transition,
            effect="zoomIn"
        )

        for index, video in enumerate(search_videos.get('videos')):
            if index >= max_clips:
                break

            hd_file = None
            videos = video.get('video_files')

            for entry in videos:
                if entry.get('height') == 720 or entry.get('width') == 1920:
                    hd_file = entry

            if hd_file is None:
                hd_file = videos[0]

            video_asset = VideoAsset(
                src=hd_file.get('link'),
                trim=1.0
            )

            video_clip = Clip(
                asset=video_asset,
                start=video_start + (index * clip_length),
                length=clip_length
            )

            video_clips.append(video_clip)

            title_transition = Transition(
                _in="fade",
                out="fade"
            )
        print(555, data['soundtrack'])
        soundtrack = Soundtrack(
            src=data['soundtrack'],
            effect="fadeOut"
        )
        timeline = Timeline(
            background="#000000",
            soundtrack=soundtrack,
            tracks=[Track(clips=[title_clip]), Track(clips=video_clips)]
        )

        output = Output(
            format="mp4",
            resolution="sd"
        )

        edit = Edit(
            timeline=timeline,
            output=output
        )

        return api_instance.post_render(edit)['response']


def status(render_id):
    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)

        return api_instance.get_render(render_id, data=True, merged=True)['response']