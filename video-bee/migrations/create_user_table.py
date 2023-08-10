def up():
	return """
		create table if not exists public.user(
			id serial NOT NULL PRIMARY KEY,
			name text NOT NULL,
			password text NOT NULL,
			mail text NOT NULL,
			image text NOT NULL,
			registration_date date,
			active smallint
		)
	"""


def down():
	return """
		drop table if exists public.user
	"""
