from flask import Blueprint, render_template, request
from app.database import Database

queries_bp = Blueprint("query", __name__)


@queries_bp.route("/list_tables")
def list_tables():
    """List all tables in the database."""

    # >>>> TODO 1: Write a query to list all the tables in the database. <<<<

    query = """SHOW Tables; """

    with Database() as db:
        tables = db.execute(query)
    return render_template("list_tables.html", tables=tables)


@queries_bp.route("/search_movie", methods=["POST"])
def search_movie():
    """Search for movies by name."""
    movie_name = request.form["movie_name"]

    # >>>> TODO 2: Search Motion Picture by Motion picture name. <<<<
    #              List the movie `name`, `rating`, `production` and `budget`.

    query =  """ SELECT name, rating, production, budget 
    FROM MotionPicture 
    WHERE name= %s; """
    
    with Database() as db:
        movies = db.execute(query, movie_name)
    return render_template("search_results.html", movies=movies)


@queries_bp.route("/search_liked_movies", methods=["POST"])
def search_liked_movies():
    """Search for movies liked by a specific user."""
    user_email = request.form["user_email"]

    # >>>> TODO 3: Find the movies that have been liked by a specific user’s email. <<<<
    #              List the movie `name`, `rating`, `production` and `budget`.

    query = """ SELECT m.name, m.rating, m.production, m.budget
    FROM MotionPicture m JOIN likes l ON m.id = l.mpid
    WHERE l.uemail = %s; """

    with Database() as db:
        movies = db.execute(query, user_email)
    return render_template("search_results.html", movies=movies)


@queries_bp.route("/search_by_country", methods=["POST"])
def search_by_country():
    """Search for movies by country using the Location table."""
    country = request.form["country"]

    # >>>> TODO 4: Search motion pictures by their shooting location country. <<<<
    #              List only the motion picture names without any duplicates.

    query = """SELECT DISTINCT m.name
     FROM MotionPicture m JOIN Location l on m.id = l.mpid
      WHERE l.country = %s; """

    with Database() as db:
        movies = db.execute(query, (country,))
    return render_template("search_results_by_country.html", movies=movies)


@queries_bp.route("/search_directors_by_zip", methods=["POST"])
def search_directors_by_zip():
    """Search for directors and the series they directed by zip code."""
    zip_code = request.form["zip_code"]

    # >>>> TODO 5: List all directors who have directed TV series shot in a specific zip code. <<<<
    #              List the director name and TV series name only without duplicates.

    query = """ 
SELECT DISTINCT P.name, m.name AS 'TV Series'
FROM People P 
	JOIN Role R ON P.id = R.pid 
	JOIN Series S ON S.mpid = R.mpid
	JOIN MotionPicture M ON M.id = S.mpid
	
WHERE R.role_name = 'Director' AND M.id IN (SELECT mpid
		FROM Location
		WHERE zip = %s);"""

    with Database() as db:
        results = db.execute(query, (zip_code))
    return render_template("search_directors_results.html", results=results)


@queries_bp.route("/search_awards", methods=["POST"])
def search_awards():
    """Search for award records where the award count is greater than `k`."""
    k = int(request.form["k"])

    # >>>> TODO 6: Find the people who have received more than “k” awards for a single motion picture in the same year. <<<<
    #              List the person `name`, `motion picture name`, `award year` and `award count`.

    query = """ SELECT P.name, Mp.name, A.award_year AS 'award year', COUNT(P.id) AS 'award count'
FROM People P JOIN Award A ON A.pid = P.id
JOIN MotionPicture Mp ON Mp.id = A.mpid

GROUP BY P.name, Mp.name, A.award_year
HAVING COUNT(P.id) > %s; """

    with Database() as db:
        results = db.execute(query, k)
    return render_template("search_awards_results.html", results=results)


@queries_bp.route("/find_youngest_oldest_actors", methods=["GET"])
def find_youngest_oldest_actors():
    """
    Find the youngest and oldest actors based on the difference 
    between the award year and their date of birth.
    """

    # >>>> TODO 7: Find the youngest and oldest actors to win at least one award. <<<<
    #              List the actor names and their age (at the time they received the award). 
    #              The age should be computed from the person’s date of birth to the award winning year only. 
    #              In case of a tie, list all of them.

    query = """ 
(SELECT p.name, MAX(a.award_year - YEAR(p.dob)) as age 
    FROM People p JOIN role R ON (p.id = R.pid AND role_name = 'Actor')
JOIN Award a ON r.pid = a.pid)

UNION

(SELECT p.name, MIN(a.award_year - YEAR(p.dob)) as age 
    FROM People p JOIN role R ON (p.id = R.pid AND role_name = 'Actor')
JOIN Award a ON r.pid = a.pid) """

    with Database() as db:
        actors = db.execute(query)
    
    # Filter out actors with null ages (if any)
    actors = [actor for actor in actors if actor[1] is not None]
    if actors:
        min_age = min(actors, key=lambda x: x[1])[1]
        max_age = max(actors, key=lambda x: x[1])[1]
        youngest_actors = [actor for actor in actors if actor[1] == min_age]
        oldest_actors = [actor for actor in actors if actor[1] == max_age]
        return render_template(
            "actors_by_age.html",
            youngest_actors=youngest_actors,
            oldest_actors=oldest_actors,
        )
    else:
        return render_template(
            "actors_by_age.html", youngest_actors=[], oldest_actors=[]
        )


@queries_bp.route("/search_producers", methods=["POST"])
def search_producers():
    """
    Search for American producers based on a minimum box office collection and maximum budget.
    """
    box_office_min = float(request.form["box_office_min"])
    budget_max = float(request.form["budget_max"])

    # >>>> TODO 8: Find the American [USA] Producers who had a box office collection of more than or equal to “X” with a budget less than or equal to “Y”. <<<< 
    #              List the producer `name`, `movie name`, `box office collection` and `budget`.

    query = """SELECT p.name, mp.name, boxoffice_collection, budget
    FROM People p JOIN Role r on (p.id = r.pid and role_name = 'Producer')
    JOIN MotionPicture mp on r.mpid = mp.id
    JOIN Movie m on mp.id = m.mpid
    WHERE p.nationality = 'USA' AND boxoffice_collection >= %s AND budget <= %s;

"""

    with Database() as db:
        results = db.execute(query, (box_office_min, budget_max))
    return render_template("search_producers_results.html", results=results)


@queries_bp.route("/search_multiple_roles", methods=["POST"])
def search_multiple_roles():
    """
    Search for people who have multiple roles in movies with a rating above a given threshold.
    """
    rating_threshold = float(request.form["rating_threshold"])

    # >>>> TODO 9: List the people who have played multiple roles in a motion picture where the rating is more than “X”. <<<<
    #              List the person’s `name`, `motion picture name` and `count of number of roles` for that particular motion picture.

    query = """SELECT p.name, mp.name, COUNT(r.pid) 
    FROM People p JOIN Role r on p.id = r.pid
    JOIN MotionPicture mp on r.mpid = mp.id
    WHERE mp.rating > %s
    GROUP BY p.name, mp.name
    HAVING COUNT(r.pid) > 1; """

    with Database() as db:
        results = db.execute(query, (rating_threshold,))
    return render_template("search_multiple_roles_results.html", results=results)


@queries_bp.route("/top_thriller_movies_boston", methods=["GET"])
def top_thriller_movies_boston():
    """Display the top 2 thriller movies in Boston based on rating."""

    # >>>> TODO 10: Find the top 2 rates thriller movies (genre is thriller) that were shot exclusively in Boston. <<<<
    #               This means that the movie cannot have any other shooting location. 
    #               List the `movie names` and their `ratings`.

    query = """ SELECT mp.name, mp.rating 
   FROM MotionPicture mp JOIN Movie m on mp.id = m.mpid
    JOIN Location l on m.mpid = l.mpid
    JOIN Genre G ON m.mpid = g.mpid AND g.genre_name = 'Thriller'
    GROUP BY mp.id
    HAVING MAX(l.city)='Boston' and COUNT(DISTINCT l.city)=1 
    Order BY mp.rating DESC
    LIMIT 2;
     """

    with Database() as db:
        results = db.execute(query)
    return render_template("top_thriller_movies_boston.html", results=results)



@queries_bp.route("/search_movies_by_likes", methods=["POST"])
def search_movies_by_likes():
    """
    Search for movies that have received more than a specified number of likes,
    where the liking users are below a certain age.
    """
    min_likes = int(request.form["min_likes"])
    max_age = int(request.form["max_age"])

    # >>>> TODO 11: Find all the movies with more than “X” likes by users of age less than “Y”. <<<<
    #               List the movie names and the number of likes by those age-group users.

    query = """ SELECT mp.name, COUNT(l.uemail) as likes
    FROM MotionPicture mp JOIN Likes l on mp.id = l.mpid
    JOIN Users u on l.uemail = u.email
    WHERE u.age < %s
    GROUP BY mp.name
    HAVING COUNT(l.uemail) > %s; """

    with Database() as db:
        results = db.execute(query, (max_age, min_likes))
    return render_template("search_movies_by_likes_results.html", results=results)


@queries_bp.route("/actors_marvel_warner", methods=["GET"])
def actors_marvel_warner():
    """
    List actors who have appeared in movies produced by both Marvel and Warner Bros.
    """

    # >>>> TODO 12: Find the actors who have played a role in both “Marvel” and “Warner Bros” productions. <<<<
    #               List the `actor names` and the corresponding `motion picture names`.

    query = """SELECT p.name as 'actor names', mp.name as 'motion picture names', mp.production
FROM people p JOIN role r ON (r.pid = p.id AND role_name = 'Actor') 
JOIN motionpicture mp ON (r.mpid = mp.id)

WHERE p.id IN (
SELECT p.id
FROM people p JOIN role r ON (r.pid = p.id)
JOIN motionpicture mp ON (r.mpid = mp.id AND production = 'Marvel')
WHERE p.id IN (
SELECT p.id
FROM people p JOIN role r ON (r.pid = p.id)
JOIN motionpicture mp ON (r.mpid = mp.id AND production = 'Warner Bros'))
)

 """

    with Database() as db:
        results = db.execute(query)
    return render_template("actors_marvel_warner.html", results=results)


@queries_bp.route("/movies_higher_than_comedy_avg", methods=["GET"])
def movies_higher_than_comedy_avg():
    """
    Display movies whose rating is higher than the average rating of comedy movies.
    """

    # >>>> TODO 13: Find the motion pictures that have a higher rating than the average rating of all comedy (genre) motion pictures. <<<<
    #               Show the names and ratings in descending order of ratings.

    query = """
    Select name, rating 
FROM MotionPicture mp
    WHERE rating > 
    (SELECT AVG(rating) 
	FROM MotionPicture mp JOIN genre g ON (mp.id = g.mpid AND genre_name='comedy')) 
    ORDER BY rating DESC 
    """

    with Database() as db:
        results = db.execute(query)
    return render_template("movies_higher_than_comedy_avg.html", results=results)


@queries_bp.route("/top_5_movies_people_roles", methods=["GET"])
def top_5_movies_people_roles():
    """
    Display the top 5 movies that involve the most people and roles.
    """

    # >>>> TODO 14: Find the top 5 movies with the highest number of people playing a role in that movie. <<<<
    #               Show the `movie name`, `people count` and `role count` for the movies.

    query = """ SELECT m.name as 'movie name', COUNT(DISTINCT r.pid) as 'people count', COUNT(r.role_name) as 'role count'
    FROM MotionPicture m JOIN Role r on m.id = r.mpid
    GROUP BY m.name
    ORDER BY COUNT(DISTINCT r.pid) DESC 
    LIMIT 5"""

    with Database() as db:
        results = db.execute(query)
    return render_template("top_5_movies_people_roles.html", results=results)


@queries_bp.route("/actors_with_common_birthday", methods=["GET"])
def actors_with_common_birthday():
    """
    Find pairs of actors who share the same birthday.
    """

    # >>>> TODO 15: Find actors who share the same birthday. <<<<
    #               List the actor names (actor 1, actor 2) and their common birthday.

    query = """SELECT p.name, p2.name, p.dob as 'birthday'
    FROM People p JOIN People p2 ON p.dob = p2.dob AND p.id < p2.id
    JOIN ROLE r1 ON r1.pid=p.id 
    WHERE p.name!=p2.name; """

    with Database() as db:
        results = db.execute(query)
    return render_template("actors_with_common_birthday.html", results=results)