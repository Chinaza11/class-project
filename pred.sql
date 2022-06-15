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
  		longitude INteger not NULL,
  		dominus INTEGER NOT NULL,
  		paladin INTEGER NOT NULL,
  		pic_60 INTEGER NOT NULL,
  		resistant_variety INTEGER NOT NULL,
  		telone INTEGER NOT NULL,
  		untreated_check INTEGER NOT NULL
);