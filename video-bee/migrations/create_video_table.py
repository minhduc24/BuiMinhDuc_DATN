def up():
	return """
		create table if not exists public.video(
			id serial NOT NULL PRIMARY KEY,
            project_id integer, 
            video_name text,
			video_type text,
			s3_url text,
            created_at timestamp,
			active smallint
		)
	"""


def down():
	return """
		drop table if exists public.video
	"""
