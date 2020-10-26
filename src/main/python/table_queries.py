
create_table = """

create table if not exists covid_us (

final_date date primary key,
cases bigint,
deaths bigint,
recovered bigint
);

"""

table_if_exists = """

select to_regclass('covid_us')

"""


select_table = """

select * from covid_us limit 1;

"""

drop_table ="""
drop table covid_us
"""
truncate_table = """
truncate table covid_us
"""

select_max_date = """
select max(final_date) as max_date from covid_us

"""

select_null = """
select * from covid_us where recovered IS NULL;

"""

insert_into = """

insert into covid_us (
    final_date,
    cases ,
    deaths ,
    recovered ) values (%s,%s,%s,%s) 

"""
