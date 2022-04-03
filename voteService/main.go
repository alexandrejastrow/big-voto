package main

import (
	"database/sql"

	"github.com/alexandrejastrow/big-voto/voteService/envs"
	"github.com/alexandrejastrow/big-voto/voteService/myerrors"
	"github.com/alexandrejastrow/big-voto/voteService/pollservice"
	"github.com/alexandrejastrow/big-voto/voteService/rabbitmq"
	"github.com/joho/godotenv"
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
func main() {
	godotenv.Load()

	db, err := conn()

	myerrors.FailOnError(err, "Failed to connect to Postgres")

	defer db.Close()

	conn_rabbitMQ, err := rabbitmq.Connection()

	myerrors.FailOnError(err, "Failed to connect to RabbitMQ")

	defer conn_rabbitMQ.Close()

	go rabbitmq.Recive(conn_rabbitMQ, db)
	go pollservice.Task()
	forever := make(chan bool)

	<-forever

}
