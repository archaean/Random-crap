select * from wonitem.wonitems;

select * from wonitem.druid_spell;

create table druid_items as
select Item, won.Spell item_Spell, dru.Spell druid_Spell from wonitem.wonitems won
join wonitem.druid_spell dru on LOWER(dru.Spell) = LOWER(won.Spell);

create table druid_item_counter as
select Item, count(distinct item_Spell) count_Spell from druid_items group by Item;

select * from druid_item_counter;

create table won_item_counter as
select Item, count(distinct Spell) count_Spell from wonitem.wonitems group by Item;

select * from won_item_counter;

create table full_set as
select dru.Item from won_item_counter won
join druid_item_counter dru on won.Item = dru.item and won.count_Spell = dru.count_Spell
order by dru.Item;

create table not_full_set as
select dru.Item from won_item_counter won
join druid_item_counter dru on won.Item = dru.item and won.count_Spell != dru.count_Spell
order by dru.Item;

select * from druid_items
join not_full_set on druid_items.Item = not_full_set.Item;

select * from wonitems
join not_full_set on wonitems.Item = not_full_set.Item;