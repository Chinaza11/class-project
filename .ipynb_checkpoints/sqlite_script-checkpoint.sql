PRAGMA foreign_keys=ON;
DROP table if EXISTS treatments;
create table treatments(
		treatments_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    	treatments_name TEXT not NULL,
		year INteger not NULL,
  		replicate INteger not NULL,
  		root_knot_nematode_planting INteger not NULL,
  		root_knot_nematode_midseason INteger not NULL,
  		root_knot_nematode_end_of_season INteger not NULL,
		weed INteger not NULL,
  		vigor_rating INteger not NULL,
  		gall_rating INteger not NULL,
  		fruit_yield INteger not NULL,
		southern_blight INteger not NULL,
  		latitude INteger not NULL,
  		longitude INteger not NULL
);

insert into treatments (treatments_name,year,replicate,root_knot_nematode_planting,root_knot_nematode_midseason,root_knot_nematode_end_of_season,weed,vigor_rating,gall_rating,fruit_yield,southern_blight,latitude,longitude) values ('Untreated check',2019,1,7,1,320,9,4,3,51,8,31.502951,-83.545263);
