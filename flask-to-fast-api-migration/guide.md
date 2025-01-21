# Guide: Migrating from Flask to FastAPI with Codegen

This guide walks you through the steps to migrate your codebase from Flask to FastAPI using Codegen. Follow along to modernize your static file handling, template syntax, and routes while ensuring compatibility with FastAPI. Each step includes a direct link to the appropriate codemod for easy implementation.

---

## 🎉 Overview of Changes

The migration focuses on these key updates:

1. **Static File Handling**  
   Migrate static file handling to FastAPI's approach.  
   [Run the Static File Handling Codemod](https://www.codegen.sh/search/6752?skillType=codemod)

2. **Template Syntax Refactoring**  
   Refactor Jinja2 template syntax for better compatibility and readability.  
   [Run the Template Syntax Codemod](https://www.codegen.sh/search/6750?skillType=codemod)

3. **Migration Feedback Enhancement**  
   Enhance feedback during the migration process for better tracking and debugging.  
   [Run the Migration Feedback Codemod](https://www.codegen.sh/search/6698?skillType=codemod)

4. **Route Migration**  
   Migrate Flask routes to FastAPI's routing system.  
   [Run the Route Migration Codemod](https://www.codegen.sh/search/6699?skillType=codemod)

---

## How to Migrate

### Step 1: Migrate Static File Handling

FastAPI uses a different approach for serving static files. Use the static file handling codemod to:

- Update your static file serving logic to align with FastAPI's methods.

👉 [Run the Static File Handling Codemod](https://www.codegen.sh/search/6752?skillType=codemod)

---

### Step 2: Refactor Template Syntax

Refactor your Jinja2 template syntax to ensure compatibility with FastAPI. This includes:

- Updating template rendering logic.
- Ensuring all template syntax is compatible with FastAPI.

👉 [Run the Template Syntax Codemod](https://www.codegen.sh/search/6750?skillType=codemod)

---

### Step 3: Enhance Migration Feedback

Improve the feedback you receive during the migration process. This helps in tracking progress and debugging issues.

👉 [Run the Migration Feedback Codemod](https://www.codegen.sh/search/6698?skillType=codemod)

---

### Step 4: Migrate Flask Routes

FastAPI has a different routing system compared to Flask. Use the route migration codemod to:

- Convert Flask routes to FastAPI routes.
- Ensure all route handlers are updated to FastAPI's syntax.

👉 [Run the Route Migration Codemod](https://www.codegen.sh/search/6699?skillType=codemod)

---

## Need Help?

If you encounter issues or have specific edge cases not addressed by the codemods, reach out to the Codegen support team or visit the [Codegen Documentation](https://www.codegen.sh/docs) for detailed guidance.

Start your FastAPI migration today and enjoy the benefits of a cleaner, modern codebase!
