# ![TMDB_Scraper](https://github.com/youtipie18/TMDB-Scrapper/assets/130830075/d11bb2c8-f2b9-4fc7-b208-9014c3d73780)

TMDB Scraper is a Scrapy project that includes multiple spiders to retrieve all movies and TV series, updating every 24h.

## Installation

### Using GitHub:
Download code from repository or use:
```bash
git clone https://github.com/youtipie18/TMDB-Scrapper.git
```

Don't forget to install requirements:
```bash
pip install -r requirements.txt
```

### Using Docker
Download image from DockerHub:
```bash
docker pull youtipie/tmdb-scraper
```

## Usage

To run this project, you need to set up the database where you want to store the scraped items. You will also need a [TMDB API key](https://developer.themoviedb.org/docs/getting-started).

> **Note**
> You can use different databases such as Mysql, Postgres or Sqlite.

### Run using local machine

- First you need to set 2 environment variables: TMDB API key and database uri. Example:

```code
API_KEY=some.api.key.1kadashfh712h37h1asda-o120-93#2198ajs8d
DATABASE_URI=sqlite:///results.db
```

> **Note** 
> You can also use an .env file to set the env variables. Just put it in the root directory:
>  ```bash
> ├── spiders
> ├── ...
> ├── scrapy.cfg
> └── .env
> ```

- Finally you can start spiders using following command:
```bash
scrapy crawl <spider_name>
```

### Run using docker

After installing this project with `docker pull`, you can start the container with the following command:
```bash
docker run -d -e API_KEY=<your_api_key> -e DATABASE_URI=<your_db_uri> --name spider youtipie/tmdb-scraper:latest
```
That's it! Once started, it will run all the necessary spiders and create a cron task to update movies and TV series at midnight.

## List of spiders

### 1. Category Spider
**Description**: Run this spider first! This spider will extract all genres.
```bash
scrapy crawl category
```

### 2. Movie Spider
**Description**: Run this spider to collect all movie data. This is the initial data collection, so the process can take a long time.
```bash
scrapy crawl movie
```

### 3. Series Spider
**Description**: Run this spider to collect all series data. This is the initial data collection, so the process can take a long time.
```bash
scrapy crawl series
```

### 4. Update Movies Spider
**Description**: Run this spider to update all movies that have been added or changed on TMDB. You can schedule this spider using cron or other tools.
```bash
scrapy crawl update_movies
```

### 5. Update Series Spider
**Description**: Run this spider first! This spider will extract all genres.
```bash
scrapy crawl update_series
```

## Scheduling Updates

To keep your data up-to-date, you can schedule the `update_movies` and `update_series` spiders using cron jobs or other scheduling tools. Here is an example of a cron job to run the update spiders daily at midnight:

```bash
0 0 * * * root /app/daily_spiders.sh
```

## License

[MIT](./LICENSE)
