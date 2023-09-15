#!/bin/bash
echo "Hello"
# set -e
set -u





function create_user_and_extension()  {
	local database=$1
	echo "  Creating user root"
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER"  -d $database <<-EOSQL
		DROP user IF EXISTS root;
		CREATE user root;
		DROP user IF EXISTS rls_role;
		CREATE user rls_role;
		DROP user IF EXISTS rdsadmin;
		CREATE user rdsadmin;
		drop extension if exists pg_trgm;
		create extension pg_trgm with schema public;

EOSQL
}


function create_user_and_database() {
	local database=$1
	echo "  Creating user and database '$database'"
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER"  <<-EOSQL
	    CREATE USER $database;
	    CREATE DATABASE $database;

	    GRANT ALL PRIVILEGES ON DATABASE $database TO $database;
EOSQL
}


if [ -n "$POSTGRES_DATABASES" ]; then
	echo "database creation requested: $POSTGRES_DATABASES"
		create_user_and_database $POSTGRES_DATABASES
	echo "Multiple databases created"
fi



#version1





#version2 
	# echo  "Creating csv files for partial tables"
	# PGPASSWORD="Zxczxc789+"	psql   -h stratint-prod.cepdytvppwr9.us-east-1.rds.amazonaws.com -p 5432 -U postgres  -d stratint -c "\\COPY (select * FROM public.profiles WHERE updated_at > '2023-02-01')    TO  '/workspace/prd_dump_30_01_2023_profiles.csv' WITH (DELIMITER ',', FORMAT CSV)"
	# PGPASSWORD="Zxczxc789+"	psql   -h stratint-prod.cepdytvppwr9.us-east-1.rds.amazonaws.com -p 5432 -U postgres  -d stratint -c "\\COPY (select * FROM public.twt_timeline_data_post_date_partitioned WHERE updated_at > '2021-12-01') TO  '/workspace/prd_dump_30_01_2023_tweet.csv' WITH (DELIMITER ',', FORMAT CSV)"
	# PGPASSWORD="Zxczxc789+"	psql   -h stratint-prod.cepdytvppwr9.us-east-1.rds.amazonaws.com -p 5432 -U postgres  -d stratint -c "\\COPY (select * FROM public.retweeted_by_profiles WHERE updated_at > '2023-03-01') TO  '/workspace/prd_dump_30_01_2023_retweet.csv' WITH (DELIMITER ',', FORMAT CSV)"
	
	# PGPASSWORD="Zxczxc789+"	psql   -h stratint-prod.cepdytvppwr9.us-east-1.rds.amazonaws.com -p 5432 -U postgres  -d stratint -c "\\COPY (SELECT id, full_name, twitter_username, current_followers_count  FROM profiles where updated_at > '2023-03-01') TO  '~/Documents/sources/api_test/prd_dump_30_01_2023_companies.csv' WITH (DELIMITER ',', FORMAT CSV)"

	#COPY (select * FROM public.retweeted_by_profiles WHERE updated_at > '2022-11-01') TO  '/workspace/prd_dump_30_01_2023_retweet.csv' WITH (DELIMITER ',', FORMAT CSV) "
	# <<-EOSQL
	# 	COPY (select * FROM public.profiles WHERE updated_at > '2023-02-01') TO  '~/postgres-demo/db/prd_dump_30_01_2023_profiles.csv' WITH (DELIMITER ',', FORMAT CSV)  ;

	# EOSQL

 		# COPY (select * FROM public.twt_timeline_data_post_date_partitioned WHERE updated_at > '2022-11-01') TO  '/workspace/prd_dump_30_01_2023_tweet.csv' WITH (DELIMITER ',', FORMAT CSV)  ;
 		# COPY (select * FROM public.retweeted_by_profiles WHERE updated_at > '2022-11-01') TO  '/workspace/prd_dump_30_01_2023_retweet.csv' WITH (DELIMITER ',', FORMAT CSV)  ;




#PGPASSWORD="Zxczxc789+"   /usr/bin/pg_dump -Fc --host stratint-prod.cepdytvppwr9.us-east-1.rds.amazonaws.com --port 5432 --dbname stratint --username postgres --verbose --file /workspace/prd_dump_30_01_2023.dump   -T  profiles -T  twt_timeline_data_post_date_partitioned  -T retweeted_by_profiles 






#version1
  psql -d $POSTGRES_DATABASES -U postgres -p 5432 <<-EOSQL
  create table rsa_prime_numbers(number_p varchar, number_q varchar );

insert into rsa_prime_numbers values('103779377958267757190065635917732205083108381531763768320394295990403358880201379268354743339748693362016696418560752211143311894169598804931043022540741643253357599492528171227518120563194307392704178077430959266009165265272518763028449773333152554495033465603845314763380770107279138993340283005534599736921', '128830454699289447730318248512405923191217353155485349580442596627670358048732468679888404855618692989010920714213985738742970349426163441786401299351760343181376498242217941204678437884063895559215959351154146991700122864723151025839401044262759216905235699167238928281174707378885310087059157680633098958109');
insert into rsa_prime_numbers values('103974713197962935425624555617147382360815223190476226312432525377699565414362852001524718636451407673050068755456552947068611494214847786590593582511907016004103101281148036054483577904737497725765649290159063384789049071670048033857749307073915907888160805903272106950761484906455367975632580980229717439557', '126569951123467880193314651957096194900488504634800319902065367376639438604331692863536093570181660145556824415457731675017944507660593624032517001615651119733076919599006827711055723801980734146605401399598025960066938589323479895496373258091136498140277342774686227798343038343065265540788693172474158688349');
insert into rsa_prime_numbers values('104982338053587254117562288138776235487680481371547957124019020062375245989233436198031104849766136650870278945671452654905691990840688950023224581456710928479624628585167555917193686308864055878856139599054683710290743287290430258367314550013144039410374472381512170662509817507104975199530003754111471253729', '119609534824779657993847257181060542817729401142116814480572267433170001192255515422468181590916421955179795028594895943511452203455825857692324041939400179929204222047226344382198692138871588069824827409495399376154225186192882227496221824075160217819250381101249595563086873962158444033918845078623227858977');

EOSQL


#version2
# 	psql -d $dump -U postgres -p 5432 <<-EOSQL
# CREATE TABLE public.profiles (
# 	id int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY,
# 	first_name varchar(64) NULL,
# 	last_name varchar(64) NULL,
# 	full_name varchar(128) NULL,
# 	topic varchar(64) NULL,
# 	twitter_username varchar(64) NULL,
# 	social_networks_urls jsonb NULL,
# 	current_followers_count int4 NULL,
# 	bio varchar(32767) NULL,
# 	image_url varchar(2048) NULL,
# 	"location" varchar(255) NULL,
# 	created_at timestamp NULL DEFAULT now(),
# 	hidden bool NULL DEFAULT false,
# 	following_count int4 NULL,
# 	tweet_count int4 NULL,
# 	listed_count int4 NULL,
# 	url varchar NULL,
# 	twitter_id varchar NULL,
# 	our_profile bool NULL,
# 	updated_at timestamp NULL DEFAULT now(),
# 	influencer_group_id int4 NULL,
# 	full_name_edited bool NULL DEFAULT false,
# 	social_network varchar NULL,
# 	is_active bool NULL DEFAULT true,
# 	CONSTRAINT profiles_pkey PRIMARY KEY (id),
# 	CONSTRAINT fk_profile_influencer_group_id FOREIGN KEY (influencer_group_id) REFERENCES public.influencer_groups(id)
# );
# CREATE INDEX idx_our_profile ON public.profiles USING btree (our_profile) WHERE (our_profile IS TRUE);
# CREATE INDEX profile_twitter_id_indx ON public.profiles USING btree (twitter_id);
# CREATE INDEX profiles_influencer_group_id ON public.profiles USING btree (influencer_group_id);
# CREATE INDEX profiles_twitter_username_indx ON public.profiles USING btree (lower((twitter_username)::text));

# COPY profiles FROM '/workspace/prd_dump_30_01_2023_profiles.csv' CSV;





# CREATE TABLE public.twt_timeline_data_post_date_partitioned (
# 	id int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY,
# 	author_id varchar NOT NULL,
# 	"source" varchar NULL,
# 	possibly_sensitive varchar NULL,
# 	reference_type varchar NULL,
# 	reference_post_id varchar NULL,
# 	post_id varchar NULL,
# 	conversation_id varchar NULL,
# 	in_reply_to_user_id varchar NULL,
# 	retweet_count int8 NULL,
# 	reply_count int8 NULL,
# 	like_count int8 NULL,
# 	quote_count int8 NULL,
# 	tweet_text varchar NULL,
# 	post_date timestamp NOT NULL,
# 	load_id int4 NULL,
# 	update_id int4 NULL,
# 	created_at timestamp NULL DEFAULT now(),
# 	updated_at timestamp NULL DEFAULT now(),
# 	CONSTRAINT twt_timeline_data_partitioned_post_date_pkey PRIMARY KEY (id, post_date),
# 	CONSTRAINT fk_load_id_partitoned_post_date_id FOREIGN KEY (load_id) REFERENCES public.load_dates(id),
# 	CONSTRAINT fk_update_id_partitioned_post_date_id FOREIGN KEY (load_id) REFERENCES public.load_dates(id)
# )
# PARTITION BY RANGE (post_date);
# CREATE INDEX twt_timeline_data_post_date_partitioned_author_id_indx ON ONLY public.twt_timeline_data_post_date_partitioned USING btree (author_id);
# CREATE INDEX twt_timeline_data_post_date_partitioned_gin_trgm_indx ON ONLY public.twt_timeline_data_post_date_partitioned USING gin (tweet_text gin_trgm_ops);
# CREATE INDEX twt_timeline_data_post_date_partitioned_post_id_indx ON ONLY public.twt_timeline_data_post_date_partitioned USING btree (post_id);
# CREATE INDEX twt_timeline_data_post_date_partitioned_ref_type ON ONLY public.twt_timeline_data_post_date_partitioned USING btree (reference_type) WHERE ((reference_type IS NULL) OR ((reference_type)::text = ANY (ARRAY[('quoted'::character varying)::text, ('replied_to'::character varying)::text])));

# COPY twt_timeline_data_post_date_partitioned FROM '/workspace/prd_dump_30_01_2023_tweet.csv' CSV;


# CREATE TABLE public.retweeted_by_profiles (
# 	id int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY,
# 	tweet_text varchar NULL,
# 	author_id varchar NULL,
# 	retweeted_post_id varchar NULL,
# 	conversation_id varchar NULL,
# 	retweet_count int8 NULL,
# 	reply_count int8 NULL,
# 	like_count int8 NULL,
# 	quote_count int8 NULL,
# 	twt_created_at varchar NULL,
# 	load_id int4 NULL,
# 	update_id int4 NULL,
# 	created_at timestamp NULL DEFAULT now(),
# 	updated_at timestamp NULL DEFAULT now(),
# 	CONSTRAINT retweeted_by_profiles_pkey PRIMARY KEY (id),
# 	CONSTRAINT fk_retweet_load_id FOREIGN KEY (load_id) REFERENCES public.load_dates(id),
# 	CONSTRAINT fk_retweet_update_id FOREIGN KEY (load_id) REFERENCES public.load_dates(id)
# )
# WITH (
# 	autovacuum_enabled=false
# );
# CREATE INDEX retweeted_by_profiles_author_id_indx ON public.retweeted_by_profiles USING btree (author_id);
# CREATE INDEX retweeted_by_profilesgin_trgm_indx ON public.retweeted_by_profiles USING gin (tweet_text gin_trgm_ops);
# CREATE INDEX retweeted_profiles_retweeted_post_id_indx ON public.retweeted_by_profiles USING btree (retweeted_post_id);

# COPY retweeted_by_profiles FROM '/workspace/prd_dump_30_01_2023_retweet.csv' CSV;


# EOSQL


done;




if [[ $? -ne 0 ]] ; then
    exit 0
fi









