"""
Scripts to load the database
"""
#--------------------------------------------------------------------
# Venue
#--------------------------------------------------------------------
vdata1 = {
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
}
vdata2 = {
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"
}
vdata3 = {
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
}
venues = [vdata1, vdata2, vdata3]

#-------------------------------------------------
#Artist
#-------------------------------------------------
adata1 = {
    "id": 1,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
}
adata2 = {
    "id": 2,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
}
adata3 = {
    "id": 3,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
}
artists = [adata1, adata2, adata3]

#-------------------------------------------------
#Show
#-------------------------------------------------
sdata1 = {
    "id": 1,
    "artist_id": 1,
    "venue_id": 1,
    "start_time": "2019-05-21T21:30:00.000Z"
}

sdata2 = {
    "id": 2,
    "artist_id": 2,
    "venue_id": 3,
    "start_time": "2019-06-15T23:00:00.000Z"
}

sdata3 = {
    "id": 3,
    "artist_id": 3,
    "venue_id": 3,
    "start_time": "2035-04-01T20:00:00.000Z"
}

sdata4 = {
    "id": 4,
    "artist_id": 3,
    "venue_id": 3,
    "start_time": "2035-04-08T20:00:00.000Z"
}

sdata5 = {
    "id": 5,
    "artist_id": 3,
    "venue_id": 3,
    "start_time": "2035-04-15T20:00:00.000Z"
}

shows = [sdata1, sdata2, sdata3, sdata4]

#TODO -> Rewrite using orm level
import psycopg2, psycopg2.extras



def load_table(table_name = 'test_table', data_list=[{"A": 1, "B": "2"}, {"A": 10, "B": "20"}]):
    fields = ','.join(field for field in data_list[0].keys())
    values_list = []
    for d in data_list:
        vals = tuple(v for v in d.values())
        values_list.append(vals)
    
    sql_binding = "INSERT INTO \"%s\" (%s) VALUES " %(table_name, fields)
    print(sql_binding)
    conn = psycopg2.connect(dbname="fyyur", user="hamed.zoghi")
    cur = conn.cursor()
    for row in values_list:
        print(row)
        cur.execute(sql_binding + "%s", str(row))

    # psycopg2.extras.execute_values(
    #     cur, sql_binding + "%s" + ";",  values_list, template=None, page_size=100, fetch=True)

    cur.close()
    # print(fields)
    # print(len(values_list[0]))
    # print(sql_binding)
    # print(values_list)

    return
