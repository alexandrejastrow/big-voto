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
	db_host := envs.GoDotEnvVariable("DB_HOST")
	db_port := envs.GoDotEnvVariable("DB_PORT")
	db_user := envs.GoDotEnvVariable("DB_USER")
	db_pass := envs.GoDotEnvVariable("DB_PASS")
	db_name := envs.GoDotEnvVariable("DB_NAME")

	db, err := sql.Open("postgres", "host="+db_host+" port="+db_port+" user="+db_user+" password="+db_pass+" dbname="+db_name+" sslmode=disable")

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

		time.Sleep(30 * time.Second)

		data = time.Now().Format("2006-01-02 15:04:05")
		query_deactivate = "UPDATE polls SET is_active = 'false' WHERE start_date >'" + data + "' OR end_date <= '" + data + "';"
		err = find(db, query_deactivate)

		if err != nil {
			log.Printf(" [x] %s", err)
		}
		log.Printf(" [x] %s", query_deactivate)

		time.Sleep(30 * time.Second)
	}

}
