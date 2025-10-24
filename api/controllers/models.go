package controllers

// Database models
type Config struct {
	ID        uint   `json:"id" gorm:"primaryKey"`
	VarConf   string `json:"var_conf" gorm:"unique"`
	ValueConf string `json:"value_conf"`
}

type Model struct {
	ID        uint   `json:"id" gorm:"primaryKey"`
	TableCode string `json:"table_code" gorm:"unique"`
	TableName string `json:"table_name"`
}

type ModelDetail struct {
	ID              uint   `json:"id" gorm:"primaryKey"`
	ModelCode       string `json:"model_code"`
	ModelDetailCode string `json:"model_detail_code" gorm:"unique"`
	ModelDetailName string `json:"model_detail_name"`
	ModelDetailType string `json:"model_detail_type"`
}
