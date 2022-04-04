package pollservice

import (
	"database/sql"
	"log"
	"os"
	"time"

	"github.com/alexandrejastrow/big-voto/voteService/envs"
	"github.com/alexandrejastrow/big-voto/voteService/myerrors"

	_ "github.com/lib/pq"
)

func conn() (*sql.DB, error) {

	pg_host := envs.GoDotEnvVariable("DB_HOST")
	pg_port := envs.GoDotEnvVariable("DB_PORT")
	pg_user := envs.GoDotEnvVariable("DB_USER")
	pg_pass := envs.GoDotEnvVariable("DB_PASS")
	pg_name := envs.GoDotEnvVariable("DB_NAME")

	db, err := sql.Open("postgres", "host="+pg_host+" port="+pg_port+" user="+pg_user+" password="+pg_pass+" dbname="+pg_name+" sslmode=disable")

	return db, err
}

func find(db *sql.DB, query string) error {
	_, err := db.Query(query)
	return err
}

func Task() {
	db, err := conn()
	os.Setenv("TZ", "America/Sao_Paulo")
	myerrors.FailOnError(err, "Failed to connect to Postgres")
	defer db.Close()
	data := time.Now().Format("2006-01-02 15:04:05")
	query_active := ""
	query_deactivate := ""

	for {

		data = time.Now().Format("2006-01-02 15:04:05")
		query_active = "UPDATE polls SET is_active = 'true' WHERE start_date <='" + data + "' AND end_date >= '" + data + "';"
		err := find(db, query_active)
		if err != nil {
			log.Printf(" [x] %s", err)
		}
		log.Printf(" [x] %s", query_active)

		time.Sleep(60 * time.Second)

		data = time.Now().Format("2006-01-02 15:04:05")
		query_deactivate = "UPDATE polls SET is_active = 'false' WHERE start_date >'" + data + "' OR end_date <= '" + data + "';"
		err = find(db, query_deactivate)

		if err != nil {
			log.Printf(" [x] %s", err)
		}
		log.Printf(" [x] %s", query_deactivate)

		time.Sleep(60 * time.Second)
	}

}
