from flask import current_app
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, ImageClip
from moviepy.video.fx.resize import resize
from models.models import Task, db
import time
import os

from app.celery_config import celery

@celery.task(bind=True)
def process_video_task(self, filename, task_id):
    uploads_dir = os.getenv('UPLOAD_FOLDER', 'remote_folder')
    path_to_video = os.path.join(uploads_dir, filename)
    path_to_logo = os.path.join('/app/uploads', 'idrl_logo.png')
    milliseconds = int(round(time.time() * 1000))
    file_processed_name = f"{str(milliseconds)}_{filename}"
    output_path = os.path.join(uploads_dir, "processed", file_processed_name)

    try:
        clip = VideoFileClip(path_to_video)

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
        # with current_app.app_context():
        #     task = Task.query.get(task_id)
        #     if task:
        #         task.status = 'PROCESSED'
        #         task.path = file_processed_name
        #         db.session.commit()
    except Exception as e:
        print(f"Error processing video {filename}: {str(e)}")
        if task_id:
            task = Task.query.get(task_id)
            if task:
                task.status = 'ERROR'
                db.session.commit()