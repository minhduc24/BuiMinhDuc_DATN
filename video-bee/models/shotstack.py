import shotstack_sdk as shotstack
from shotstack_sdk.api import edit_api
from shotstack_sdk.model.video_asset import VideoAsset
from shotstack_sdk.model.image_asset import ImageAsset
from shotstack_sdk.model.clip import Clip
from shotstack_sdk.model.track import Track
from shotstack_sdk.model.timeline import Timeline
from shotstack_sdk.model.output import Output
from shotstack_sdk.model.edit import Edit
from shotstack_sdk.model.offset import Offset
from config import SHOTSTACK_API_KEY
from models.projects import *
from schemas.projects import UpdateColumnRequest
from sqlalchemy.orm import Session
import requests
import boto3
from config import S3_RESULT_BUCKET, S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY
import os

s3 = boto3.resource('s3',
        aws_access_key_id=S3_ACCESS_KEY_ID,
        aws_secret_access_key= S3_SECRET_ACCESS_KEY)

bucket = s3.Bucket(S3_RESULT_BUCKET)

host = 'https://api.shotstack.io/stage'
configuration = shotstack.Configuration(host = host)

configuration.api_key['DeveloperKey'] = SHOTSTACK_API_KEY

def download_file(edit_infor: dict, db: Session):
    with shotstack.ApiClient(configuration) as api_client:
        api_instance = edit_api.EditApi(api_client)

        video_asset = VideoAsset(
            src=edit_infor['videos']['s3_url'],
            trim=float(edit_infor['videos']['start_time'])
        )

        video_clip = Clip(
            asset=video_asset,
            start=0.0,
            length=float(edit_infor['videos']['end_time']-edit_infor['videos']['start_time'])
        )

        track = Track(clips=[video_clip])
        vid_img = None
        if edit_infor['images']:
            edit_infor['images']['start'] = edit_infor['images']['start'] or 0.0
            edit_infor['images']['end'] = edit_infor['images']['end'] or 0.0
            image_asset = ImageAsset(
                src=edit_infor['images']['src']
            )
            image_clip = Clip(
                asset=image_asset,
                start=float(edit_infor['images']['start']),
                length=float(edit_infor['images']['end'] - edit_infor['images']['start']),
                offset=Offset(
                    x=float(edit_infor['images']['vertical']),
                    y=float(edit_infor['images']['horizontal'])
                ),
                scale=edit_infor['images']['scale'],
                position='topLeft'
            )
            vid_img = Track(clips=[image_clip,video_clip])
        if vid_img:
            track = vid_img

        timeline = Timeline(
            background="#000000",
            tracks=[track]
        )

        output = Output(
            format='mp4',
            resolution='sd'
        )

        edit = Edit(
            timeline=timeline,
            output=output
        )

        try:
            api_response = api_instance.post_render(edit)
            # return  {"status": api_response['response']['id']}
            id = api_response['response']['id']
        except Exception as e:
            print(f"Unable to resolve API call: {e}")

        try:
            api_response = api_instance.get_render(id, data=False, merged=True)
            status = api_response['response']['status']
            while status != 'done':
                api_response = api_instance.get_render(id, data=False, merged=True)
                status = api_response['response']['status']
                if status == 'done':
                    print(f"{api_response['response']['url']}")
            r = requests.get(api_response['response']['url'], allow_redirects=True, stream=True)
            chunk_size = 1024*1024
            with open(f"shotstack-video/{edit_infor['videos']['video_name']}", 'wb') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
            if os.path.isfile(f"shotstack-video/{edit_infor['videos']['video_name']}"):
                s3_result = bucket.put_object(Key=f"{edit_infor['videos']['video_name']}", Body=open(f"shotstack-video/{edit_infor['videos']['video_name']}", 'rb'))
                os.remove(f"shotstack-video/{edit_infor['videos']['video_name']}")
            projectUpdate = UpdateColumnRequest
            projectUpdate.s3_url = f"https://resultvideo.s3.ap-southeast-1.amazonaws.com/{s3_result.key}"
            projectUpdate.metadata = "{}"
            projectUpdate.user_id = edit_infor['videos']['user_id']
            projectUpdate.pid = edit_infor['videos']['pId']
            projectUpdate.pname = edit_infor['videos']['pName']
            save_projectt(db, projectUpdate)
            return {"s3_url": f"https://resultvideo.s3.ap-southeast-1.amazonaws.com/{s3_result.key}"}
        except Exception as e:
            print(f"Unable to resolve API call: {e}")
            return {"stautus": "false roi huhu"}