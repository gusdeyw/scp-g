package main

import (
	"log"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

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
	ID               uint   `json:"id" gorm:"primaryKey"`
	ModelCode        string `json:"model_code"`
	ModelDetailCode  string `json:"model_detail_code" gorm:"unique"`
	ModelDetailName  string `json:"model_detail_name"`
	ModelDetailType  string `json:"model_detail_type"`
}

var db *gorm.DB

func initDatabase() {
	var err error
	db, err = gorm.Open(sqlite.Open("production.db"), &gorm.Config{})
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}

	// Auto migrate the schema
	db.AutoMigrate(&Config{}, &Model{}, &ModelDetail{})

	// Seed initial config data
	seedConfig()
}

func seedConfig() {
	var count int64
	db.Model(&Config{}).Count(&count)
	if count == 0 {
		configs := []Config{
			{VarConf: "LANG", ValueConf: "Go"},
			{VarConf: "FRAMEWORK", ValueConf: "Fiber"},
			{VarConf: "DATABASE", ValueConf: "SQLite"},
		}
		db.Create(&configs)
	}
}

func main() {
	initDatabase()

	app := fiber.New(fiber.Config{
		ErrorHandler: func(c *fiber.Ctx, err error) error {
			return c.Status(500).JSON(fiber.Map{
				"error": err.Error(),
			})
		},
	})

	// CORS middleware
	app.Use(cors.New())

	// Routes
	app.Get("/", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{
			"message": "Welcome to Production API (Go Fiber)",
		})
	})

	// Config routes
	config := app.Group("/api/config")
	config.Get("/", getAllConfig)
	config.Get("/:var_conf", getConfig)
	config.Put("/:var_conf", updateConfig)

	// Model routes
	model := app.Group("/api/model")
	model.Get("/", getAllModels)
	model.Post("/", createModel)
	model.Get("/:table_code", getModel)
	model.Put("/:table_code", updateModel)
	model.Delete("/:table_code", deleteModel)

	// Model detail routes
	modelDetail := app.Group("/api/model_detail")
	modelDetail.Get("/", getAllModelDetails)
	modelDetail.Post("/", createModelDetail)
	modelDetail.Get("/:model_detail_code", getModelDetail)
	modelDetail.Put("/:model_detail_code", updateModelDetail)
	modelDetail.Delete("/:model_detail_code", deleteModelDetail)

	// Generate routes
	app.Get("/api/generate_go", generateGo)

	log.Fatal(app.Listen(":5000"))
}