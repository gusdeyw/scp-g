package main

import (
	"github.com/gofiber/fiber/v2"
)

// Config handlers
func getAllConfig(c *fiber.Ctx) error {
	var configs []Config
	if err := db.Find(&configs).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}
	return c.JSON(configs)
}

func getConfig(c *fiber.Ctx) error {
	varConf := c.Params("var_conf")
	var config Config
	if err := db.Where("var_conf = ?", varConf).First(&config).Error; err != nil {
		return c.Status(404).JSON(fiber.Map{"error": "Config not found"})
	}
	return c.JSON(config)
}

func updateConfig(c *fiber.Ctx) error {
	varConf := c.Params("var_conf")

	type UpdateConfigRequest struct {
		ValueConf string `json:"value_conf"`
	}

	var req UpdateConfigRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{"error": "Invalid request body"})
	}

	var config Config
	if err := db.Where("var_conf = ?", varConf).First(&config).Error; err != nil {
		return c.Status(404).JSON(fiber.Map{"error": "Config not found"})
	}

	config.ValueConf = req.ValueConf
	if err := db.Save(&config).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(config)
}

// Model handlers
func getAllModels(c *fiber.Ctx) error {
	var models []Model
	if err := db.Find(&models).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}
	return c.JSON(models)
}

func createModel(c *fiber.Ctx) error {
	type CreateModelRequest struct {
		TableCode string `json:"table_code"`
		TableName string `json:"table_name"`
	}

	var req CreateModelRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{"error": "Invalid request body"})
	}

	model := Model{
		TableCode: req.TableCode,
		TableName: req.TableName,
	}

	if err := db.Create(&model).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(201).JSON(model)
}

func getModel(c *fiber.Ctx) error {
	tableCode := c.Params("table_code")
	var model Model
	if err := db.Where("table_code = ?", tableCode).First(&model).Error; err != nil {
		return c.Status(404).JSON(fiber.Map{"error": "Model not found"})
	}
	return c.JSON(model)
}

func updateModel(c *fiber.Ctx) error {
	tableCode := c.Params("table_code")

	type UpdateModelRequest struct {
		TableName string `json:"table_name"`
	}

	var req UpdateModelRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{"error": "Invalid request body"})
	}

	var model Model
	if err := db.Where("table_code = ?", tableCode).First(&model).Error; err != nil {
		return c.Status(404).JSON(fiber.Map{"error": "Model not found"})
	}

	model.TableName = req.TableName
	if err := db.Save(&model).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(model)
}

func deleteModel(c *fiber.Ctx) error {
	tableCode := c.Params("table_code")
	var model Model
	if err := db.Where("table_code = ?", tableCode).First(&model).Error; err != nil {
		return c.Status(404).JSON(fiber.Map{"error": "Model not found"})
	}

	if err := db.Delete(&model).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Model deleted successfully"})
}

// Model Detail handlers
func getAllModelDetails(c *fiber.Ctx) error {
	var modelDetails []ModelDetail
	if err := db.Find(&modelDetails).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}
	return c.JSON(modelDetails)
}

func createModelDetail(c *fiber.Ctx) error {
	type CreateModelDetailRequest struct {
		ModelCode       string `json:"model_code"`
		ModelDetailCode string `json:"model_detail_code"`
		ModelDetailName string `json:"model_detail_name"`
		ModelDetailType string `json:"model_detail_type"`
	}

	var req CreateModelDetailRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{"error": "Invalid request body"})
	}

	// Validate type
	if req.ModelDetailType != "varchar" && req.ModelDetailType != "int" && req.ModelDetailType != "id" {
		return c.Status(400).JSON(fiber.Map{"error": "Invalid model_detail_type. Must be 'varchar', 'int', or 'id'"})
	}

	modelDetail := ModelDetail{
		ModelCode:       req.ModelCode,
		ModelDetailCode: req.ModelDetailCode,
		ModelDetailName: req.ModelDetailName,
		ModelDetailType: req.ModelDetailType,
	}

	if err := db.Create(&modelDetail).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}

	return c.Status(201).JSON(modelDetail)
}

func getModelDetail(c *fiber.Ctx) error {
	modelDetailCode := c.Params("model_detail_code")
	var modelDetail ModelDetail
	if err := db.Where("model_detail_code = ?", modelDetailCode).First(&modelDetail).Error; err != nil {
		return c.Status(404).JSON(fiber.Map{"error": "Model detail not found"})
	}
	return c.JSON(modelDetail)
}

func updateModelDetail(c *fiber.Ctx) error {
	modelDetailCode := c.Params("model_detail_code")

	type UpdateModelDetailRequest struct {
		ModelCode       string `json:"model_code"`
		ModelDetailName string `json:"model_detail_name"`
		ModelDetailType string `json:"model_detail_type"`
	}

	var req UpdateModelDetailRequest
	if err := c.BodyParser(&req); err != nil {
		return c.Status(400).JSON(fiber.Map{"error": "Invalid request body"})
	}

	// Validate type
	if req.ModelDetailType != "varchar" && req.ModelDetailType != "int" && req.ModelDetailType != "id" {
		return c.Status(400).JSON(fiber.Map{"error": "Invalid model_detail_type. Must be 'varchar', 'int', or 'id'"})
	}

	var modelDetail ModelDetail
	if err := db.Where("model_detail_code = ?", modelDetailCode).First(&modelDetail).Error; err != nil {
		return c.Status(404).JSON(fiber.Map{"error": "Model detail not found"})
	}

	modelDetail.ModelCode = req.ModelCode
	modelDetail.ModelDetailName = req.ModelDetailName
	modelDetail.ModelDetailType = req.ModelDetailType

	if err := db.Save(&modelDetail).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(modelDetail)
}

func deleteModelDetail(c *fiber.Ctx) error {
	modelDetailCode := c.Params("model_detail_code")
	var modelDetail ModelDetail
	if err := db.Where("model_detail_code = ?", modelDetailCode).First(&modelDetail).Error; err != nil {
		return c.Status(404).JSON(fiber.Map{"error": "Model detail not found"})
	}

	if err := db.Delete(&modelDetail).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}

	return c.JSON(fiber.Map{"message": "Model detail deleted successfully"})
}

// Generate handler
func generateGo(c *fiber.Ctx) error {
	// Get all models and their details
	var models []Model
	if err := db.Find(&models).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}

	var modelDetails []ModelDetail
	if err := db.Find(&modelDetails).Error; err != nil {
		return c.Status(500).JSON(fiber.Map{"error": err.Error()})
	}

	// Get config
	var langConfig Config
	db.Where("var_conf = ?", "LANG").First(&langConfig)

	if langConfig.ValueConf != "Go" {
		return c.Status(400).JSON(fiber.Map{"error": "LANG config must be set to 'Go'"})
	}

	// Generate Go code (simplified version - you can expand this)
	generatedCode := generateGoCode(models, modelDetails)

	c.Set("Content-Type", "application/zip")
	c.Set("Content-Disposition", "attachment; filename=\"generated_go_project.zip\"")

	return c.SendString(generatedCode)
}

func generateGoCode(models []Model, modelDetails []ModelDetail) string {
	// This is a simplified code generation
	// In a real implementation, you'd create actual Go files and zip them
	code := "package main\n\n"
	code += "import (\n"
	code += "\t\"github.com/gofiber/fiber/v2\"\n"
	code += "\t\"gorm.io/gorm\"\n"
	code += ")\n\n"

	for _, model := range models {
		code += "type " + model.TableName + " struct {\n"
		code += "\tID uint `json:\"id\" gorm:\"primaryKey\"`\n"

		// Find details for this model
		for _, detail := range modelDetails {
			if detail.ModelCode == model.TableCode {
				fieldType := "string"
				if detail.ModelDetailType == "int" {
					fieldType = "int"
				} else if detail.ModelDetailType == "id" {
					fieldType = "uint"
				}
				code += "\t" + detail.ModelDetailName + " " + fieldType + " `json:\"" + detail.ModelDetailName + "\"`\n"
			}
		}
		code += "}\n\n"
	}

	code += "func main() {\n"
	code += "\tapp := fiber.New()\n\n"
	code += "\t// Routes would go here\n\n"
	code += "\tapp.Listen(\":3000\")\n"
	code += "}\n"

	return code
}