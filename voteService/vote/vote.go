package vote

import (
	"database/sql"
	"encoding/json"
	"fmt"

	_ "github.com/lib/pq"
)

type Vote struct {
	AlternativeID string `json:"alternative_id"`
	PollId        string `json:"poll_id"`
}

func (v Vote) Save(db *sql.DB) error {

	//UPDATE     alternatives
	//SET        votes = votes + 1
	//WHERE id = '9925a45e-a448-4fd5-be21-bc0ea2699cda' AND
	//(SELECT is_active FROM polls WHERE id = '47fe5302-ce84-4b46-ab0f-220b1196407f')

	query := "UPDATE alternatives SET votes = votes + 1 WHERE id = '" + v.AlternativeID + "';"

	_, err := db.Exec(query)

	fmt.Println(query)
	return err

}

func CreateVote(s string) *Vote {
	v := Vote{}
	json.Unmarshal([]byte(s), &v)
	return &v
}
