#!/bin/bash
echo "Hello"
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

  psql -d $POSTGRES_DATABASES -U postgres -p 5432 <<-EOSQL
  create table rsa_prime_numbers(number_p varchar, number_q varchar );

insert into rsa_prime_numbers values('103779377958267757190065635917732205083108381531763768320394295990403358880201379268354743339748693362016696418560752211143311894169598804931043022540741643253357599492528171227518120563194307392704178077430959266009165265272518763028449773333152554495033465603845314763380770107279138993340283005534599736921', '128830454699289447730318248512405923191217353155485349580442596627670358048732468679888404855618692989010920714213985738742970349426163441786401299351760343181376498242217941204678437884063895559215959351154146991700122864723151025839401044262759216905235699167238928281174707378885310087059157680633098958109');
insert into rsa_prime_numbers values('103974713197962935425624555617147382360815223190476226312432525377699565414362852001524718636451407673050068755456552947068611494214847786590593582511907016004103101281148036054483577904737497725765649290159063384789049071670048033857749307073915907888160805903272106950761484906455367975632580980229717439557', '126569951123467880193314651957096194900488504634800319902065367376639438604331692863536093570181660145556824415457731675017944507660593624032517001615651119733076919599006827711055723801980734146605401399598025960066938589323479895496373258091136498140277342774686227798343038343065265540788693172474158688349');
insert into rsa_prime_numbers values('104982338053587254117562288138776235487680481371547957124019020062375245989233436198031104849766136650870278945671452654905691990840688950023224581456710928479624628585167555917193686308864055878856139599054683710290743287290430258367314550013144039410374472381512170662509817507104975199530003754111471253729', '119609534824779657993847257181060542817729401142116814480572267433170001192255515422468181590916421955179795028594895943511452203455825857692324041939400179929204222047226344382198692138871588069824827409495399376154225186192882227496221824075160217819250381101249595563086873962158444033918845078623227858977');

EOSQL

done;




if [[ $? -ne 0 ]] ; then
    exit 0
fi









