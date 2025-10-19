from flask import Blueprint, jsonify, send_file
import sqlite3
import os
import tempfile
import zipfile
from io import BytesIO

generate_bp = Blueprint('generate', __name__)

DATABASE = os.path.join(os.path.dirname(__file__), 'production.db')

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@generate_bp.route('/api/generate_go', methods=['GET'])
def generate_go_project():
    # Check config for LANG=Go
    db = get_db()
    config = db.execute("SELECT value_conf FROM config WHERE var_conf = 'LANG'").fetchone()
    db.close()
    if not config or config['value_conf'] != 'Go':
        return jsonify({'error': 'Config not set for Go generation'}), 400

    # Fetch models and details
    db = get_db()
    models = db.execute('SELECT * FROM model').fetchall()
    model_details = db.execute('SELECT * FROM model_detail').fetchall()
    db.close()

    # Group details by model_code
    details_by_model = {}
    for detail in model_details:
        model_code = detail['model_code']
        if model_code not in details_by_model:
            details_by_model[model_code] = []
        details_by_model[model_code].append(detail)

    # Create temp directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate go.mod
        go_mod = f"""module scp-g-generated

go 1.21

require github.com/gofiber/fiber/v2 v2.52.5
"""
        with open(os.path.join(temp_dir, 'go.mod'), 'w') as f:
            f.write(go_mod)

        # Generate main.go
        routes = []
        for model in models:
            table_code = model['table_code']
            capitalized = table_code.capitalize()
            routes.append(f"""\t// {table_code} routes
\tapi.Get("/{table_code}", handlers.Get{capitalized})
\tapi.Get("/{table_code}/:id", handlers.Get{capitalized}ByID)
\tapi.Post("/{table_code}", handlers.Create{capitalized})
\tapi.Put("/{table_code}/:id", handlers.Update{capitalized})
\tapi.Delete("/{table_code}/:id", handlers.Delete{capitalized})""")

        main_go = f"""package main

import (
\t"log"

\t"scp-g-generated/handlers"

\t"github.com/gofiber/fiber/v2"
\t"github.com/gofiber/fiber/v2/middleware/cors"
\t"github.com/gofiber/fiber/v2/middleware/logger"
)

func main() {{
\t// Create Fiber app
\tapp := fiber.New(fiber.Config{{
\t\tErrorHandler: func(c *fiber.Ctx, err error) error {{
\t\t\tcode := fiber.StatusInternalServerError
\t\t\tif e, ok := err.(*fiber.Error); ok {{
\t\t\t\tcode = e.Code
\t\t\t}}
\t\t\treturn c.Status(code).JSON(fiber.Map{{
\t\t\t\t"error": err.Error(),
\t\t\t}})
\t\t}},
\t}})

\t// Middleware
\tapp.Use(logger.New())
\tapp.Use(cors.New())

\t// Routes
\tapi := app.Group("/api")

{"".join(routes)}

\t// Health check
\tapp.Get("/", func(c *fiber.Ctx) error {{
\t\treturn c.JSON(fiber.Map{{
\t\t\t"message": "Generated Go API with Fiber",
\t\t\t"status":  "running",
\t\t}})
\t}})

\tlog.Fatal(app.Listen(":3000"))
}}
"""
        with open(os.path.join(temp_dir, 'main.go'), 'w') as f:
            f.write(main_go)

        # Create directories
        models_dir = os.path.join(temp_dir, 'models')
        handlers_dir = os.path.join(temp_dir, 'handlers')
        os.makedirs(models_dir)
        os.makedirs(handlers_dir)

        # Generate models
        for model in models:
            table_code = model['table_code']
            table_name = model['table_name']
            details = details_by_model.get(table_code, [])
            fields = []
            for detail in details:
                field_name = detail['model_detail_name']
                field_type = detail['model_detail_type']
                if field_type == 'id':
                    go_type = 'int'
                elif field_type == 'int':
                    go_type = 'int'
                elif field_type == 'varchar':
                    go_type = 'string'
                else:
                    go_type = 'string'
                fields.append(f'\t{field_name} {go_type} `json:"{field_name}"`')

            model_go = f"""package models

type {table_code} struct {{
{"\n".join(fields)}
}}
"""
            with open(os.path.join(models_dir, f'{table_code.lower()}.go'), 'w') as f:
                f.write(model_go)

        # Generate handlers
        for model in models:
            table_code = model['table_code']
            table_name = model['table_name']
            details = details_by_model.get(table_code, [])
            id_field = next((d['model_detail_name'] for d in details if d['model_detail_type'] == 'id'), 'ID')

            capitalized = table_code.capitalize()
            handler_go = f"""package handlers

import (
\t"strconv"

\t"scp-g-generated/models"

\t"github.com/gofiber/fiber/v2"
)

// Mock data storage (in memory)
var {table_code.lower()} = []models.{table_code}{{}} // Mock storage

// Get{capitalized} returns all {table_name}
func Get{capitalized}(c *fiber.Ctx) error {{
\treturn c.JSON({table_code.lower()})
}}

// Get{capitalized}ByID returns a {table_name} by ID
func Get{capitalized}ByID(c *fiber.Ctx) error {{
\tid, err := strconv.Atoi(c.Params("id"))
\tif err != nil {{
\t\treturn c.Status(400).JSON(fiber.Map{{"error": "Invalid ID"}})
\t}}
\tfor _, item := range {table_code.lower()} {{
\t\tif item.{id_field} == id {{
\t\t\treturn c.JSON(item)
\t\t}}
\t}}
\treturn c.Status(404).JSON(fiber.Map{{"error": "{table_name} not found"}})
}}

// Create{capitalized} creates a new {table_name}
func Create{capitalized}(c *fiber.Ctx) error {{
\tvar item models.{table_code}
\tif err := c.BodyParser(&item); err != nil {{
\t\treturn c.Status(400).JSON(fiber.Map{{"error": "Invalid input"}})
\t}}
\t// Mock ID assignment
\titem.{id_field} = len({table_code.lower()}) + 1
\t{table_code.lower()} = append({table_code.lower()}, item)
\treturn c.Status(201).JSON(item)
}}

// Update{capitalized} updates a {table_name} by ID
func Update{capitalized}(c *fiber.Ctx) error {{
\tid, err := strconv.Atoi(c.Params("id"))
\tif err != nil {{
\t\treturn c.Status(400).JSON(fiber.Map{{"error": "Invalid ID"}})
\t}}
\tvar updatedItem models.{table_code}
\tif err := c.BodyParser(&updatedItem); err != nil {{
\t\treturn c.Status(400).JSON(fiber.Map{{"error": "Invalid input"}})
\t}}
\tfor i, item := range {table_code.lower()} {{
\t\tif item.{id_field} == id {{
\t\t\t{table_code.lower()}[i] = updatedItem
\t\t\t{table_code.lower()}[i].{id_field} = id
\t\t\treturn c.JSON({table_code.lower()}[i])
\t\t}}
\t}}
\treturn c.Status(404).JSON(fiber.Map{{"error": "{table_name} not found"}})
}}

// Delete{capitalized} deletes a {table_name} by ID
func Delete{capitalized}(c *fiber.Ctx) error {{
\tid, err := strconv.Atoi(c.Params("id"))
\tif err != nil {{
\t\treturn c.Status(400).JSON(fiber.Map{{"error": "Invalid ID"}})
\t}}
\tfor i, item := range {table_code.lower()} {{
\t\tif item.{id_field} == id {{
\t\t\t{table_code.lower()} = append({table_code.lower()}[:i], {table_code.lower()}[i+1:]...)
\t\t\treturn c.JSON(fiber.Map{{"message": "{table_name} deleted"}})
\t\t}}
\t}}
\treturn c.Status(404).JSON(fiber.Map{{"error": "{table_name} not found"}})
}}
"""
            with open(os.path.join(handlers_dir, f'{table_code.lower()}.go'), 'w') as f:
                f.write(handler_go)

        # Create zip
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zip_file.write(file_path, arcname)

        zip_buffer.seek(0)
        return send_file(zip_buffer, as_attachment=True, download_name='generated_go_project.zip', mimetype='application/zip')