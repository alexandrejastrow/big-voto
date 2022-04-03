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

	rabbitUser := envs.GoDotEnvVariable("RABBITMQ_USER")
	rabbitPass := envs.GoDotEnvVariable("RABBITMQ_PASSWORD")
	rabbitHost := envs.GoDotEnvVariable("RABBITMQ_HOST")
	rabbitPort := envs.GoDotEnvVariable("RABBITMQ_PORT")

	conn, err := amqp.Dial(fmt.Sprintf("amqp://%s:%s@%s:%s/", rabbitUser, rabbitPass, rabbitHost, rabbitPort))

	return conn, err
}
