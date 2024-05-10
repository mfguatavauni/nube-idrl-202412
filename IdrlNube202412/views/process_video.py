from flask import current_app
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, ImageClip
from moviepy.video.fx.resize import resize
# from models.models import Task, db
import time
import os
from google.cloud import storage
import io
import tempfile
from google.cloud import pubsub_v1

# from app.celery_config import celery

# @celery.task(bind=True)
def process_video_task(filename, task_id):
    client = storage.Client()
    bucket_name = 'idrl-bucket'
    bucket = client.bucket(bucket_name)

    # uploads_dir = os.getenv('UPLOAD_FOLDER', '/')
    # path_to_video = os.path.join(uploads_dir, filename)
    path_to_logo = os.path.join('/home/smilenaguevara/nube-idrl-202412/IdrlNube202412/uploads', 'idrl_logo.png')
    milliseconds = int(round(time.time() * 1000))
    file_processed_name = f"{str(milliseconds)}_{filename}"
    output_path = os.path.join("/home/smilenaguevara/nube-idrl-202412/IdrlNube202412/uploads/processed", file_processed_name)
    
    blob = bucket.blob(filename)
    with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
        blob.download_to_filename(temp_video_file.name)
        temp_video_path = temp_video_file.name
    

    try:
        clip = VideoFileClip(temp_video_path)

        if clip.duration > 20:
            print(clip.duration)
            clip = clip.subclip(0, 20)

        clip_resized = resize(clip, width=clip.w, height=int(clip.w * 9 / 16))
        center_x = clip_resized.w / 2
        center_y = clip_resized.h / 2
        logo_clip = ImageClip(path_to_logo, duration=0.5)

        logo_clip_start = ImageClip(path_to_logo, duration=0.5)
        logo_clip_start = logo_clip_start.set_position(('center', 'center')).set_start(0)

        logo_clip_end = ImageClip(path_to_logo, duration=0.5)
        logo_clip_end = logo_clip_end.set_position(('center', 'center')).set_start(clip_resized.duration - 0.5)


        final_clip = CompositeVideoClip([clip_resized, logo_clip_start, logo_clip_end])

    
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        processed_blob = bucket.blob(f"processed/{file_processed_name}")
        processed_blob.upload_from_filename(output_path)
        
    except Exception as e:
        print(f"Error processing video {filename}: {str(e)}")

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/soluciones-cloud-2024120/subscriptions/your-subscription-name'

def callback(message):
    print(f'Received message: {message}')
    data = json.loads(message.data.decode('utf-8'))
    filename = data['filename']
    task_id = data['task_id']

    try:
        process_video_task(filename, task_id)
        message.ack()
    except Exception as e:
        print(f'Error processing video {filename}: {str(e)}')
        message.nack()

def main():
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f'Listening for messages on {subscription_path}')
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

if __name__ == '__main__':
    main()