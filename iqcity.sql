create table tsubindex (id serial primary key , name varchar(200), image varchar(500), description text
    , weight_default float
    , created timestamp default now(), creator_id bigint constraint fk_subindex_creator references auth_user
    , modified timestamp default now(), modifier_id bigint constraint fk_subindex_modifier references auth_user
    , deleted timestamp, deleter_id bigint constraint fk_subindex_deleter references auth_user);

create table tindicatortype (id int primary key , name varchar(200), image varchar(500), description text
    , weight_default float
    , created timestamp default now(), creator_id bigint constraint fk_indtype_creator references auth_user
    , modified timestamp default now(), modifier_id bigint constraint fk_indtype_modifier references auth_user
    , deleted timestamp, deleter_id bigint constraint fk_indtype_deleter references auth_user);

insert into tindicatortype (id, name) values (1,'Цифровизация'),(2,'Бытовая'),(3,'Социальная');

create table tindicatorgroup (id serial primary key , name varchar(200), image varchar(500), description text
    , weight_default float
    , created timestamp default now(), creator_id bigint constraint fk_indicatorgroup_creator references auth_user
    , modified timestamp default now(), modifier_id bigint constraint fk_indicatorgroup_modifier references auth_user
    , deleted timestamp, deleter_id bigint constraint fk_indicatorgroup_deleter references auth_user);

create table tindicator (id serial primary key, name varchar(200) not null , image varchar(500), description text
    , weight_default float
    , subindex_id bigint constraint fk_indicator_subindex references tsubindex not null
    , indicatorgroup_id bigint constraint fk_indicator_group references tindicatorgroup not null
    , indicatortype_id bigint constraint fk_indicator_indtype references tindicatortype not null default 1
    , created timestamp default now(), creator_id bigint constraint fk_indicator_creator references auth_user
    , modified timestamp default now(), modifier_id bigint constraint fk_indicator_modifier references auth_user
    , deleted timestamp, deleter_id bigint constraint fk_indicator_deleter references auth_user);

update tindicator set weight_default=1::float4/(select count(1) from tindicator where deleted is null) where deleted is null;

create table tregion (id serial primary key , name varchar(200), image varchar(500), description text
    , created timestamp default now(), creator_id bigint constraint fk_region_creator references auth_user
    , modified timestamp default now(), modifier_id bigint constraint fk_region_modifier references auth_user
    , deleted timestamp, deleter_id bigint constraint fk_region_deleter references auth_user);

create table tcity (id serial primary key , name varchar(200), image varchar(500), description text, parent_id bigint
    , population int, area float, vvp float
    , region_id bigint constraint fk_city_region references tregion not null
    , created timestamp default now(), creator_id bigint constraint fk_city_creator references auth_user
    , modified timestamp default now(), modifier_id bigint constraint fk_city_modifier references auth_user
    , deleted timestamp, deleter_id bigint constraint fk_city_deleter references auth_user);

create table trawdata (id serial primary key, name varchar(200)
    , weight_default float, param text, value text
    , city_id bigint constraint fk_rawdata_city references tcity not null
    , indicator_id bigint constraint fk_rawdata_indicator references tindicator not null
    , created timestamp default now(), creator_id bigint constraint fk_city_creator references auth_user
    , modified timestamp default now(), modifier_id bigint constraint fk_city_modifier references auth_user
    , deleted timestamp, deleter_id bigint constraint fk_city_deleter references auth_user);

create table tindicatordata (id serial primary key, value float
    , city_id bigint constraint fk_inddata_city references tcity not null
    , indicator_id bigint constraint fk_inddata_indicator references tindicator not null
    , created timestamp default now(), creator_id bigint constraint fk_city_creator references auth_user
    , modified timestamp default now(), modifier_id bigint constraint fk_city_modifier references auth_user
    , deleted timestamp, deleter_id bigint constraint fk_city_deleter references auth_user);


create table tiqindex_history (id serial primary key, iq_index float
    , city_id bigint constraint fk_inddata_city references tcity not null
    , created timestamp default now(), creator_id bigint constraint fk_city_creator references auth_user
    , modified timestamp default now(), modifier_id bigint constraint fk_city_modifier references auth_user
    , deleted timestamp, deleter_id bigint constraint fk_city_deleter references auth_user);

create or replace view vr_iq_index as
select
    c.region_id
    ,d.city_id
    ,c.population
    ,c.area
    ,c.vvp
    ,sum(case when i.indicatortype_id=1 then coalesce(i.weight_default,1)*d.val end) digital
    ,sum(case when i.indicatortype_id=2 then coalesce(i.weight_default,1)*d.val end) social
    ,sum(case when i.indicatortype_id=3 then coalesce(i.weight_default,1)*d.val end) utility
    ,sum(coalesce(i.weight_default,1)*d.val) iq_index
    from tcity c, (select city_id, indicator_id, value as val from tindicatordata where deleted is null
        union all select city_id, indicator_id, sum(sign(length(ltrim(trim(value),'0')))) from trawdata where deleted is null
        group by city_id, indicator_id) d
       , tindicator i where d.city_id=c.id and d.indicator_id=i.id and i.deleted is null
    group by region_id, city_id, population, area,vvp;

select * from vr_iq_index;

drop function if exists fset_2gis(pitem json) ;

create or replace function fset_2gis(pdata json) returns json language plpgsql as $$
declare vCityID bigint := 3;
begin
    insert into trawdata (name, param, value, city_id, indicator_id)
    select 'Велопрокат', name||address_name, id, vCityID
         , (select id from tindicator where name='Количество точек велопроката')
    from json_to_recordset(pdata) as x (id int, name text, address_name text);
    insert into tiqindex_history(iq_index, city_id)
    select iq_index, city_id from vr_iq_index where city_id=vCityID;
    return '{"status": "ok"}';
end
$$;

drop function if exists fset_bim(phouses json) ;


create or replace function fset_bim(pdata json) returns json language plpgsql as $$
declare vCityID bigint := 3;
begin
    insert into trawdata (name, param, value, city_id, indicator_id)
    select 'BIM дом',address ,bim, vCityID
         , (select id from tindicator where name='Количество домов с BIM')
    from json_to_recordset(pdata) as x (address text, bim text);
    insert into tiqindex_history(iq_index, city_id)
    select iq_index, city_id from vr_iq_index where city_id=vCityID;
    return '{"status": "ok"}';
end
$$;
