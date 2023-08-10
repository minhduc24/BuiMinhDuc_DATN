def up():
	return """
		create table if not exists public.project(
			id serial NOT NULL PRIMARY KEY,
            project_name text,
			user_id integer,
			project_information json,
			s3_url text,
			created_at timestamp,
			modified_at timestamp,
			active smallint
		)
	"""


def down():
	return """
		drop table if exists public.project
	"""
