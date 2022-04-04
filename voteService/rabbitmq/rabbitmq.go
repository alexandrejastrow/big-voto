package rabbitmq

import (
	"database/sql"
	"fmt"
	"log"

	"github.com/alexandrejastrow/big-voto/voteService/envs"
	"github.com/alexandrejastrow/big-voto/voteService/myerrors"
	"github.com/alexandrejastrow/big-voto/voteService/vote"
	"github.com/streadway/amqp"
)

func Recive(conn *amqp.Connection, db *sql.DB) {

	ch, err := conn.Channel()
	myerrors.FailOnError(err, "Failed to open a channel")

	defer ch.Close()

	q, err := ch.QueueDeclare(
		"votes", // name
		false,   // durable
		false,   // delete when unused
		false,   // exclusive
		false,   // no-wait
		nil,     // arguments
	)
	myerrors.FailOnError(err, "Failed to declare a queue")

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	myerrors.FailOnError(err, "Failed to register a consumer")

	forever := make(chan bool)
	log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
	go func() {
		for d := range msgs {
			log.Printf(" [x] Received %s", d.Body)
			v := vote.CreateVote(string(d.Body))
			v.Save(db)
		}
	}()
	<-forever
}

func Connection() (*amqp.Connection, error) {

	rabbitmq_host := envs.GoDotEnvVariable("RABBITMQ_HOST")
	rabbitmq_port := envs.GoDotEnvVariable("RABBITMQ_PORT")
	rabbitmq_user := envs.GoDotEnvVariable("RABBITMQ_USER")
	rabbitmq_pass := envs.GoDotEnvVariable("RABBITMQ_PASS")

	url := "amqp://" + rabbitmq_user + ":" + rabbitmq_pass + "@" + rabbitmq_host + ":" + rabbitmq_port

	fmt.Println(url)
	conn, err := amqp.Dial("amqp://guest:guest@rabbitmq:5672")

	return conn, err
}
